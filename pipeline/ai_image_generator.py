"""Geração de imagens por IA (text-to-image) para o modo "unha impossível".

Backend padrão: Pollinations (gratuito, sem chave de API). É plugável via a
variável de ambiente IMAGE_PROVIDER para, no futuro, trocar por um serviço pago
de maior qualidade ou de vídeo (Replicate, Runway, etc.).
"""

import os
import time
import urllib.parse
import requests
from config import VIDEO_WIDTH, VIDEO_HEIGHT, IMAGE_PROVIDER, IMAGE_MODEL

POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}"

# Reforça enquadramento de unha em close e realismo, independente do prompt.
STYLE_SUFFIX = (
    "professional nail art photography, extreme close-up of manicured fingernails, "
    "hyperrealistic, dramatic cinematic lighting, ultra detailed, vertical 9:16"
)


def generate_images(
    prompts: list,
    output_dir: str,
    width: int = VIDEO_WIDTH,
    height: int = VIDEO_HEIGHT,
    provider: str = None,
    model: str = None,
) -> list:
    """Gera uma imagem por prompt e retorna os caminhos salvos."""
    provider = (provider or IMAGE_PROVIDER).lower()

    if provider == "pollinations":
        return _pollinations(prompts, output_dir, width, height, model or IMAGE_MODEL)

    raise NotImplementedError(
        f"Provider de imagem '{provider}' não implementado. "
        "Use IMAGE_PROVIDER=pollinations (grátis, sem chave) ou plugue um "
        "backend pago aqui (ex.: Replicate/Runway)."
    )


def _pollinations(prompts: list, output_dir: str, width: int, height: int, model: str) -> list:
    paths = []
    for i, prompt in enumerate(prompts, 1):
        full = f"{prompt}, {STYLE_SUFFIX}"
        url = POLLINATIONS_URL.format(prompt=urllib.parse.quote(full))
        params = {
            "width": width,
            "height": height,
            "nologo": "true",
            "seed": i * 7,
            "model": model,
        }
        dest = os.path.join(output_dir, f"ai_{i:02d}.jpg")
        if _download(url, params, dest):
            paths.append(dest)
            print(f"      imagem {i}/{len(prompts)} gerada")

    if not paths:
        raise RuntimeError(
            "Nenhuma imagem de IA pôde ser gerada. Verifique a conexão com a internet."
        )
    return paths


def _download(url: str, params: dict, dest: str, retries: int = 3) -> bool:
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=120)
            r.raise_for_status()
            content_type = r.headers.get("content-type", "")
            if "image" not in content_type:
                raise ValueError(f"resposta não é imagem ({content_type}): {r.text[:80]}")
            with open(dest, "wb") as f:
                f.write(r.content)
            return True
        except Exception as e:
            last = attempt == retries - 1
            suffix = "" if last else f"; aguardando {2 ** attempt}s"
            print(f"      tentativa {attempt + 1}/{retries} falhou ({e}){suffix}")
            if not last:
                time.sleep(2 ** attempt)
    return False
