"""Monta um vídeo vertical (9:16) a partir de fotos/clipes reais.

Pensado para canais de unha (ex.: Nail Sosuka): a manicure tira fotos e
vídeos curtos do trabalho real e o pipeline transforma em um Short/TikTok
com efeito Ken Burns (zoom suave), transições, música e textos.
"""

import os
import glob
import numpy as np
from PIL import Image
from moviepy.editor import (
    ImageClip,
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from moviepy.audio.fx.audio_loop import audio_loop
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, SECONDS_PER_IMAGE
from pipeline.text_overlay import make_text_clip

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
VIDEO_EXTS = (".mp4", ".mov", ".m4v", ".webm")

CROSSFADE = 0.5          # duração da transição entre mídias (s)
KEN_BURNS_ZOOM = 0.10    # zoom total aplicado em cada foto
MAX_CLIP_SECONDS = 6.0   # corta clipes de vídeo longos


def collect_media(folder: str) -> list:
    """Lista fotos e clipes da pasta, em ordem alfabética (ex.: 01.jpg, 02.jpg)."""
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Pasta de mídia não encontrada: {folder}")

    paths = sorted(
        p
        for p in glob.glob(os.path.join(folder, "*"))
        if p.lower().endswith(IMAGE_EXTS + VIDEO_EXTS)
    )
    if not paths:
        raise RuntimeError(
            f"Nenhuma foto ou vídeo em '{folder}'. "
            f"Formatos aceitos: {', '.join(IMAGE_EXTS + VIDEO_EXTS)}"
        )
    return paths


def build_slideshow(
    media_paths: list,
    output_path: str,
    music_path: str = None,
    narration_path: str = None,
    word_boundaries: list = None,
    hook: str = None,
    cta: str = None,
    seconds_per_image: float = SECONDS_PER_IMAGE,
    zoom: float = KEN_BURNS_ZOOM,
    logo_path: str = None,
    brand: str = None,
    handle: str = None,
) -> str:
    narration = AudioFileClip(narration_path) if narration_path else None

    # Com narração, o ritmo das fotos acompanha a duração da fala.
    if narration:
        seconds_per_image = max(narration.duration / max(len(media_paths), 1), 1.5)

    clips = _build_media_clips(media_paths, seconds_per_image, zoom)
    base = concatenate_videoclips(clips, method="compose", padding=-CROSSFADE)
    duration = base.duration

    brand = (brand or "").lower() or None
    has_outro = brand in ("outro", "both")

    layers = [base]
    if hook:
        layers.append(make_text_clip(hook, 0.3, min(3.5, duration), position="top"))
    # o CTA simples só aparece quando NÃO há vinheta de fechamento (que já traz o CTA)
    if cta and not has_outro:
        layers.append(
            make_text_clip(cta, max(0.0, duration - 3.0), duration, position="bottom")
        )
    if word_boundaries:
        from pipeline.video_editor import _build_subtitles

        layers.extend(_build_subtitles(word_boundaries, duration))

    if brand:
        from pipeline.brand import brand_overlays

        layers.extend(
            brand_overlays(
                logo_path,
                duration,
                intro=brand in ("intro", "both"),
                outro=has_outro,
                cta=cta,
                handle=handle,
            )
        )

    video = CompositeVideoClip(layers, size=(VIDEO_WIDTH, VIDEO_HEIGHT))
    video = video.set_audio(_build_audio(narration, music_path, duration))

    video.write_videofile(
        output_path,
        fps=VIDEO_FPS,
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )

    video.close()
    if narration:
        narration.close()
    return output_path


def _build_media_clips(paths: list, seconds_per_image: float, zoom: float) -> list:
    clips = []
    for i, path in enumerate(paths):
        try:
            if path.lower().endswith(VIDEO_EXTS):
                clip = _video_clip(path)
            else:
                clip = _photo_clip(path, seconds_per_image, zoom)
        except Exception as e:
            print(f"      Aviso: não foi possível usar {path}: {e}")
            continue

        if i > 0:
            clip = clip.crossfadein(CROSSFADE)
        clips.append(clip)

    if not clips:
        raise RuntimeError("Nenhuma mídia válida para montar o vídeo.")
    return clips


def _photo_clip(path: str, duration: float, zoom: float = KEN_BURNS_ZOOM):
    """Foto enquadrada em 9:16 com efeito Ken Burns (zoom suave)."""
    frame = _cover_image(path)
    clip = ImageClip(frame).set_duration(duration)
    zoomed = clip.resize(lambda t: 1 + zoom * t / duration).set_position("center")
    return CompositeVideoClip(
        [zoomed], size=(VIDEO_WIDTH, VIDEO_HEIGHT)
    ).set_duration(duration)


def _video_clip(path: str):
    clip = VideoFileClip(path).without_audio()
    clip = _crop_to_vertical(clip)
    if clip.duration > MAX_CLIP_SECONDS:
        clip = clip.subclip(0, MAX_CLIP_SECONDS)
    return clip


def _cover_image(path: str) -> np.ndarray:
    """Carrega a foto e recorta para preencher 1080x1920 (cover, sem distorcer)."""
    img = Image.open(path).convert("RGB")
    target_ratio = VIDEO_WIDTH / VIDEO_HEIGHT
    ratio = img.width / img.height

    if ratio > target_ratio:
        new_w = int(img.height * target_ratio)
        x1 = (img.width - new_w) // 2
        img = img.crop((x1, 0, x1 + new_w, img.height))
    elif ratio < target_ratio:
        new_h = int(img.width / target_ratio)
        y1 = (img.height - new_h) // 2
        img = img.crop((0, y1, img.width, y1 + new_h))

    img = img.resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.LANCZOS)
    return np.array(img)


def _crop_to_vertical(clip):
    target_ratio = VIDEO_WIDTH / VIDEO_HEIGHT
    clip_ratio = clip.w / clip.h

    if clip_ratio > target_ratio:
        new_w = int(clip.h * target_ratio)
        x1 = (clip.w - new_w) // 2
        clip = clip.crop(x1=x1, x2=x1 + new_w)
    elif clip_ratio < target_ratio:
        new_h = int(clip.w / target_ratio)
        y1 = (clip.h - new_h) // 2
        clip = clip.crop(y1=y1, y2=y1 + new_h)

    return clip.resize((VIDEO_WIDTH, VIDEO_HEIGHT))


def _build_audio(narration, music_path: str, duration: float):
    tracks = []

    if narration:
        tracks.append(narration.subclip(0, min(narration.duration, duration)))

    if music_path and os.path.exists(music_path):
        music = AudioFileClip(music_path)
        if music.duration < duration:
            music = audio_loop(music, duration=duration)
        music = music.subclip(0, duration)
        # música baixa por baixo da narração; alta quando é só música
        music = music.volumex(0.15 if narration else 0.85)
        tracks.append(music)

    if not tracks:
        return None
    if len(tracks) == 1:
        return tracks[0]
    return CompositeAudioClip(tracks)
