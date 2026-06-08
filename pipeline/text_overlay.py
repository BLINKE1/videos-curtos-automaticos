"""Renderização de texto sobre o vídeo (legendas, gancho e call-to-action).

Helpers compartilhados entre o editor de b-roll e o slideshow de fotos.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip
from config import VIDEO_WIDTH, VIDEO_HEIGHT

# Compatibilidade Pillow 10+ x moviepy 1.0.3: o resize do moviepy ainda usa
# Image.ANTIALIAS, removido no Pillow 10. Reaponta para LANCZOS (equivalente).
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.LANCZOS

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:\\Windows\\Fonts\\arialbd.ttf",
]

# Paleta da marca (mesma do nail-sosuka): roxo primário
ACCENT = (168, 85, 212)


def load_font(size: int):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def wrap_text(text: str, font, draw, max_width: int) -> list:
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


def _anchor_y(position: str, total_h: int) -> int:
    if position == "top":
        return 260
    if position == "center":
        return (VIDEO_HEIGHT - total_h) // 2
    # bottom (padrão de legenda)
    return VIDEO_HEIGHT - 360 - total_h


def render_banner(text: str, font, position: str = "top", pill: bool = True) -> np.ndarray:
    """Desenha um bloco de texto centralizado com fundo (pílula) em destaque."""
    img = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    line_h = font.size + 16
    lines = wrap_text(text.upper(), font, draw, VIDEO_WIDTH - 200)
    total_h = len(lines) * line_h
    y = _anchor_y(position, total_h)

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        x = (VIDEO_WIDTH - lw) // 2
        pad_x, pad_y = 32, 14

        if pill:
            draw.rounded_rectangle(
                [x - pad_x, y - pad_y, x + lw + pad_x, y + line_h - pad_y],
                radius=28,
                fill=(*ACCENT, 235),
            )
        # contorno preto para legibilidade quando não há pílula
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((x + dx, y + dy), line, font=font, fill=(60, 20, 80, 255))
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
        y += line_h

    return np.array(img)


def make_text_clip(
    text: str,
    start: float,
    end: float,
    position: str = "top",
    fontsize: int = 64,
    fade: float = 0.4,
    pill: bool = True,
) -> ImageClip:
    """Cria um clip de texto (gancho/CTA) posicionado e com fade in/out."""
    font = load_font(fontsize)
    frame = render_banner(text, font, position=position, pill=pill)

    rgb = frame[:, :, :3]
    alpha = frame[:, :, 3].astype(float) / 255.0

    clip = ImageClip(rgb).set_start(start).set_end(end)
    mask = ImageClip(alpha, ismask=True).set_start(start).set_end(end)
    clip = clip.set_mask(mask)

    if fade and end - start > 2 * fade:
        clip = clip.crossfadein(fade).crossfadeout(fade)

    return clip
