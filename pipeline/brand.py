"""Vinheta de marca: logo animado (entra e sai) + call-to-action.

Pode abrir e/ou fechar o vídeo. O logo entra com um leve "pop" (escala + fade),
fica um instante e sai. No fechamento, aparece junto com um CTA e o @ do perfil.
"""

import os
import numpy as np
from PIL import Image
from moviepy import ImageClip, ColorClip
from moviepy.video.fx import CrossFadeIn, CrossFadeOut, Resize
from config import VIDEO_WIDTH, VIDEO_HEIGHT
from pipeline.text_overlay import make_text_clip

# logo padrão (copiado do repositório da Nail Sosuka)
DEFAULT_LOGO = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")

INTRO_DURATION = 2.4
OUTRO_DURATION = 3.2
POP_TIME = 0.45          # tempo do "pop" de entrada (s)
LOGO_WIDTH_FRAC = 0.60   # largura do logo em relação à largura do vídeo


def brand_overlays(
    logo_path: str = None,
    total_duration: float = 0.0,
    intro: bool = True,
    outro: bool = True,
    cta: str = None,
    handle: str = None,
) -> list:
    """Retorna a lista de clips de overlay da marca para compor sobre o vídeo."""
    logo_path = logo_path or DEFAULT_LOGO
    if not os.path.exists(logo_path):
        print(f"      Aviso: logo não encontrado em {logo_path}; vinheta ignorada.")
        return []

    rgb, alpha = _load_logo(logo_path)
    layers = []

    if intro:
        layers.append(
            _animated_logo(rgb, alpha, start=0.2, duration=INTRO_DURATION)
        )
        if handle:
            layers.append(
                make_text_clip(handle, 0.7, INTRO_DURATION, position="bottom",
                               fontsize=52, pill=False)
            )

    if outro and total_duration > OUTRO_DURATION:
        start = total_duration - OUTRO_DURATION
        # escurece o fundo para o cartão de encerramento ficar legível
        dark = (
            ColorClip((VIDEO_WIDTH, VIDEO_HEIGHT), color=(15, 5, 25))
            .with_opacity(0.55)
            .with_start(start)
            .with_end(total_duration)
            .with_effects([CrossFadeIn(0.4)])
        )
        layers.append(dark)
        layers.append(
            _animated_logo(rgb, alpha, start=start, duration=OUTRO_DURATION,
                           center_y=VIDEO_HEIGHT * 0.36)
        )
        if cta:
            layers.append(
                make_text_clip(cta, start + 0.4, total_duration, position="bottom",
                               fontsize=72)
            )
        if handle:
            layers.append(
                make_text_clip(handle, start + 0.6, total_duration, position="center",
                               fontsize=56, pill=False)
            )

    return layers


def _animated_logo(rgb, alpha, start: float, duration: float, center_y: float = None):
    clip = ImageClip(rgb).with_duration(duration)
    mask = ImageClip(alpha, is_mask=True).with_duration(duration)
    clip = clip.with_mask(mask)

    # "pop": escala de 0.7 -> 1.0 nos primeiros POP_TIME segundos
    def scale(t):
        k = min(t / POP_TIME, 1.0)
        return 0.7 + 0.3 * k

    clip = clip.with_effects([Resize(scale)])

    if center_y is None:
        clip = clip.with_position("center")
    else:
        # centraliza no eixo X, posição fixa no Y (topo do logo)
        clip = clip.with_position(lambda t: ("center", center_y - _logo_h(rgb) / 2))

    fade = min(0.4, duration / 3)
    return clip.with_effects([CrossFadeIn(fade), CrossFadeOut(fade)]).with_start(start)


def _logo_h(rgb) -> int:
    return rgb.shape[0]


def _load_logo(path: str):
    """Carrega o logo, recorta as bordas transparentes e redimensiona."""
    img = Image.open(path).convert("RGBA")

    bbox = img.getbbox()  # caixa do conteúdo não-transparente
    if bbox:
        img = img.crop(bbox)

    target_w = int(VIDEO_WIDTH * LOGO_WIDTH_FRAC)
    ratio = target_w / img.width
    img = img.resize((target_w, int(img.height * ratio)), Image.LANCZOS)

    arr = np.array(img)
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3].astype(float) / 255.0
    return rgb, alpha
