import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    CompositeVideoClip,
    CompositeAudioClip,
    concatenate_videoclips,
    concatenate_audioclips,
)
from moviepy.video.fx import FadeIn, FadeOut
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS

FONT_PATHS = [
    "C:\\Windows\\Fonts\\arialbd.ttf",
    "C:\\Windows\\Fonts\\arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]

MUSIC_PATHS = [
    "assets/music.mp3",
    "assets/music.wav",
    "assets/background.mp3",
]

TRANSITION_DURATION = 0.4
MUSIC_VOLUME = 0.10


def assemble_video(
    broll_paths: list, audio_path: str, word_boundaries: list, output_path: str
) -> str:
    narration = AudioFileClip(audio_path)
    duration = narration.duration

    broll = _build_broll(broll_paths, duration)

    final_audio = _mix_audio(narration, duration)
    broll = broll.with_audio(final_audio)

    subtitle_clips = _build_subtitles(word_boundaries, duration)
    final = CompositeVideoClip([broll] + subtitle_clips)

    final.write_videofile(
        output_path,
        fps=VIDEO_FPS,
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )

    narration.close()
    broll.close()
    return output_path


def _mix_audio(narration: AudioFileClip, duration: float):
    for path in MUSIC_PATHS:
        if os.path.exists(path):
            try:
                music = AudioFileClip(path).with_volume_scaled(MUSIC_VOLUME)
                music = _loop_audio(music, duration)
                print(f"      Música de fundo: {path}")
                return CompositeAudioClip([narration, music])
            except Exception as e:
                print(f"      Aviso música: {e}")
    return narration


def _loop_audio(clip: AudioFileClip, duration: float) -> AudioFileClip:
    if clip.duration >= duration:
        return clip.subclipped(0, duration)
    n = math.ceil(duration / clip.duration)
    looped = concatenate_audioclips([clip] * n)
    return looped.subclipped(0, duration)


def _build_broll(paths: list, duration: float):
    clips = []
    total = 0.0
    extended_paths = paths * 10

    for path in extended_paths:
        if total >= duration:
            break
        try:
            clip = VideoFileClip(path)
            clip = _crop_to_vertical(clip)
            clip = clip.with_effects([FadeIn(TRANSITION_DURATION), FadeOut(TRANSITION_DURATION)])
            clips.append(clip)
            total += clip.duration
        except Exception as e:
            print(f"      Aviso: não foi possível carregar {path}: {e}")

    if not clips:
        raise RuntimeError("Nenhum clipe de b-roll disponível para montar o vídeo.")

    video = concatenate_videoclips(clips, method="compose")
    return video.subclipped(0, min(duration, video.duration))


def _crop_to_vertical(clip):
    target_ratio = VIDEO_WIDTH / VIDEO_HEIGHT
    clip_ratio = clip.w / clip.h

    if clip_ratio > target_ratio:
        new_w = int(clip.h * target_ratio)
        x1 = (clip.w - new_w) // 2
        clip = clip.cropped(x1=x1, x2=x1 + new_w)
    elif clip_ratio < target_ratio:
        new_h = int(clip.w / target_ratio)
        y1 = (clip.h - new_h) // 2
        clip = clip.cropped(y1=y1, y2=y1 + new_h)

    return clip.resized((VIDEO_WIDTH, VIDEO_HEIGHT))


def _build_subtitles(word_boundaries: list, video_duration: float, words_per_cue: int = 3) -> list:
    if not word_boundaries:
        return []

    font = _load_font(52)
    clips = []
    i = 0

    while i < len(word_boundaries):
        chunk = word_boundaries[i : i + words_per_cue]
        start = chunk[0][0] / 1e7
        end = min((chunk[-1][0] + chunk[-1][1]) / 1e7, video_duration)
        if end <= start:
            i += words_per_cue
            continue
        text = " ".join(w[2] for w in chunk)

        frame = _render_subtitle(text, font)
        rgb = frame[:, :, :3]
        alpha = frame[:, :, 3].astype(float) / 255.0

        clip = ImageClip(rgb).with_start(start).with_end(end)
        mask = ImageClip(alpha, is_mask=True).with_start(start).with_end(end)
        clip = clip.with_mask(mask)
        clips.append(clip)
        i += words_per_cue

    return clips


def _render_subtitle(text: str, font) -> np.ndarray:
    img = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    lines = _wrap_text(text, font, draw, VIDEO_WIDTH - 100)
    line_h = 64
    total_h = len(lines) * line_h
    y = VIDEO_HEIGHT - 260 - total_h

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        x = (VIDEO_WIDTH - lw) // 2
        pad = 16

        draw.rounded_rectangle(
            [x - pad, y - pad, x + lw + pad, y + lh + pad],
            radius=8,
            fill=(0, 0, 0, 180),
        )
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((x + dx, y + dy), line, font=font, fill=(0, 0, 0, 255))
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
        y += line_h

    return np.array(img)


def _wrap_text(text: str, font, draw, max_width: int) -> list:
    words = text.split()
    lines, current = [], []

    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]

    if current:
        lines.append(" ".join(current))

    return lines or [text]


def _load_font(size: int):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()
