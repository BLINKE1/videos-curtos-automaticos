"""Chroma key compositor: troca unhas verdes (e fundo branco opcional) por texturas.

Fluxo previsto:
1) Você grava uma mão com esmalte verde-chroma em fundo branco/neutro (9:16).
2) Este módulo isola, por frame (HSV no OpenCV), a região das unhas (verde) e
   opcionalmente do fundo (branco), e compõe três camadas:
       - fundo  : vídeo de textura (galáxia, fumaça, neon, ...) — onde era branco
       - mão    : pixels originais (pele real preservada)
       - unha   : vídeo de textura (lava, raio, ouro, ...) — onde era verde
3) Saída: MP4 9:16 com a mão real e as unhas/fundo trocados por texturas vivas.

Defaults dos thresholds HSV são conservadores (verde-chroma vivo, fundo claro).
Calibrar pra cada esmalte/iluminação ajustando NAIL_HSV / BG_HSV.
"""

import math
import os
import numpy as np
import cv2
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    VideoClip,
    concatenate_videoclips,
)
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS

# HSV no OpenCV: H em [0,179], S em [0,255], V em [0,255].
# Verde-chroma vivo (esmalte/fita chroma). Ajustar conforme a cor real.
NAIL_HSV_LOW = (35, 80, 60)
NAIL_HSV_HIGH = (90, 255, 255)

# Branco/claro (papel cartão, parede). Baixa saturação + alto brilho.
BG_HSV_LOW = (0, 0, 200)
BG_HSV_HIGH = (180, 40, 255)

FEATHER_PX = 3           # borda suave (pixels) — evita recorte "stickerizado"
MORPH_KERNEL = 3         # tamanho do kernel pra abrir/fechar a máscara
DESPILL = True           # remove tom esverdeado da pele perto da borda da unha


def chroma_composite(
    source_video: str,
    nail_texture_video: str,
    output_path: str,
    background_video: str = None,
    music_path: str = None,
    nail_hsv: tuple = (NAIL_HSV_LOW, NAIL_HSV_HIGH),
    bg_hsv: tuple = (BG_HSV_LOW, BG_HSV_HIGH),
    feather_px: int = FEATHER_PX,
    despill: bool = DESPILL,
    keep_source_audio: bool = False,
) -> str:
    """Compõe um vídeo trocando o verde (unhas) e o branco (fundo) por texturas.

    source_video: gravação real (mão com esmalte verde em fundo claro).
    nail_texture_video: vídeo curto que preencherá as unhas (lava, raio, ...).
    background_video: vídeo que substituirá o fundo (opcional). Sem ele, o fundo
        original é preservado.
    music_path: trilha sonora opcional (substitui o áudio).
    keep_source_audio: se True e sem music_path, mantém o áudio do source.
    """
    src = VideoFileClip(source_video)
    src = _crop_to_vertical(src)
    duration = src.duration

    nail_tex = _prepare_texture(nail_texture_video, duration)
    bg_tex = _prepare_texture(background_video, duration) if background_video else None

    nail_lower = np.array(nail_hsv[0], dtype=np.uint8)
    nail_upper = np.array(nail_hsv[1], dtype=np.uint8)
    bg_lower = np.array(bg_hsv[0], dtype=np.uint8)
    bg_upper = np.array(bg_hsv[1], dtype=np.uint8)
    kernel = np.ones((MORPH_KERNEL, MORPH_KERNEL), np.uint8)

    def make_frame(t):
        frame = src.get_frame(t)
        nail_t = nail_tex.get_frame(t)
        bg_t = bg_tex.get_frame(t) if bg_tex is not None else None
        return _composite_frame(
            frame, nail_t, bg_t,
            nail_lower, nail_upper,
            bg_lower, bg_upper,
            kernel, feather_px, despill,
        )

    out = VideoClip(make_frame, duration=duration)

    audio_clip = _resolve_audio(src, music_path, duration, keep_source_audio)
    if audio_clip is not None:
        out = out.with_audio(audio_clip)

    out.write_videofile(
        output_path,
        fps=VIDEO_FPS,
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )

    out.close()
    src.close()
    nail_tex.close()
    if bg_tex is not None:
        bg_tex.close()
    if audio_clip is not None:
        audio_clip.close()
    return output_path


def _composite_frame(
    frame, nail_tex, bg_tex,
    nail_lower, nail_upper,
    bg_lower, bg_upper,
    kernel, feather_px, despill,
):
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    nail_mask = cv2.inRange(hsv, nail_lower, nail_upper)
    nail_mask = cv2.morphologyEx(nail_mask, cv2.MORPH_OPEN, kernel)
    nail_mask = cv2.morphologyEx(nail_mask, cv2.MORPH_CLOSE, kernel)

    if bg_tex is not None:
        bg_mask = cv2.inRange(hsv, bg_lower, bg_upper)
        bg_mask = cv2.morphologyEx(bg_mask, cv2.MORPH_OPEN, kernel)
        bg_mask = cv2.bitwise_and(bg_mask, cv2.bitwise_not(nail_mask))
    else:
        bg_mask = None

    if feather_px > 0:
        nail_alpha = cv2.GaussianBlur(nail_mask, (0, 0), feather_px) / 255.0
        bg_alpha = (
            cv2.GaussianBlur(bg_mask, (0, 0), feather_px) / 255.0
            if bg_mask is not None
            else None
        )
    else:
        nail_alpha = nail_mask / 255.0
        bg_alpha = bg_mask / 255.0 if bg_mask is not None else None

    if despill:
        edge = ((nail_alpha > 0.05) & (nail_alpha < 0.95)).astype(np.float32)
        frame = _despill_green(frame, edge)

    out = frame.astype(np.float32)

    if bg_alpha is not None:
        m = bg_alpha[..., None]
        out = out * (1.0 - m) + bg_tex.astype(np.float32) * m

    m = nail_alpha[..., None]
    out = out * (1.0 - m) + nail_tex.astype(np.float32) * m

    return np.clip(out, 0, 255).astype(np.uint8)


def _despill_green(frame, edge_mask):
    """Reduz o canal verde nas bordas (luz verde refletindo na pele)."""
    f = frame.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    cap = (r + b) / 2.0
    new_g = np.minimum(g, cap)
    g = g * (1.0 - edge_mask) + new_g * edge_mask
    f[..., 1] = g
    return f.astype(np.uint8)


def _prepare_texture(path: str, duration: float):
    clip = VideoFileClip(path).without_audio()
    clip = _crop_to_vertical(clip)
    return _loop_to_duration(clip, duration)


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


def _loop_to_duration(clip, duration: float):
    if clip.duration >= duration:
        return clip.subclipped(0, duration)
    n = math.ceil(duration / clip.duration)
    return concatenate_videoclips([clip] * n).subclipped(0, duration)


def _resolve_audio(src, music_path, duration, keep_source_audio):
    if music_path and os.path.exists(music_path):
        music = AudioFileClip(music_path)
        if music.duration >= duration:
            return music.subclipped(0, duration)
        return music
    if keep_source_audio and src.audio is not None:
        return src.audio.subclipped(0, min(src.audio.duration, duration))
    return None
