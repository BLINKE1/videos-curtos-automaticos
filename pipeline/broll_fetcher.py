import os
import requests
from config import PEXELS_API_KEY

PEXELS_API = "https://api.pexels.com/videos/search"

# Texturas pré-mapeadas para o modo --chroma (unhas e fundo).
TEXTURE_KEYWORDS = {
    "lava": ["lava texture closeup", "molten lava macro", "magma flow"],
    "fire": ["fire closeup", "flame macro", "ember slow motion"],
    "electric": ["electricity arc", "plasma energy", "lightning bolt"],
    "galaxy": ["nebula loop", "galaxy stars", "space nebula"],
    "gold": ["liquid gold", "molten gold texture", "gold paint"],
    "water": ["water ripple closeup", "ink in water", "liquid macro"],
    "smoke": ["dark smoke", "black smoke macro", "ink smoke"],
    "neon": ["neon lights dark", "purple neon", "cyberpunk lights"],
    "crystal": ["crystal texture", "ice macro", "diamond sparkle"],
}


def fetch_broll_videos(keywords: list, output_dir: str, per_keyword: int = 3) -> list:
    headers = {"Authorization": PEXELS_API_KEY}
    downloaded = []

    for keyword in keywords:
        videos = _search(keyword, headers, per_keyword, orientation="portrait")
        if not videos:
            videos = _search(keyword, headers, per_keyword, orientation=None)

        for video in videos:
            best = _pick_best_file(video["video_files"])
            if not best:
                continue
            dest = os.path.join(output_dir, f"{video['id']}.mp4")
            if _download(best["link"], dest):
                downloaded.append(dest)

    return downloaded


def fetch_texture_video(theme: str, output_dir: str) -> str:
    """Baixa 1 clipe vertical do Pexels pra usar como textura no chroma key.

    `theme` pode ser uma chave de TEXTURE_KEYWORDS (ex.: "lava", "galaxy") ou
    uma string livre — nesse caso é usada como termo de busca direto.
    Retorna o caminho do MP4 baixado, ou levanta RuntimeError se nada veio.
    """
    headers = {"Authorization": PEXELS_API_KEY}
    queries = TEXTURE_KEYWORDS.get(theme.lower(), [theme])

    for query in queries:
        videos = _search(query, headers, per_page=3, orientation="portrait")
        if not videos:
            videos = _search(query, headers, per_page=3, orientation=None)
        for video in videos:
            best = _pick_best_file(video["video_files"])
            if not best:
                continue
            dest = os.path.join(output_dir, f"tex_{theme}_{video['id']}.mp4")
            if _download(best["link"], dest):
                return dest

    raise RuntimeError(
        f"Nenhuma textura encontrada no Pexels para '{theme}'. "
        f"Tente outra chave: {', '.join(sorted(TEXTURE_KEYWORDS))}"
    )


def _search(keyword: str, headers: dict, per_page: int, orientation) -> list:
    params = {"query": keyword, "per_page": per_page, "size": "medium"}
    if orientation:
        params["orientation"] = orientation
    try:
        resp = requests.get(PEXELS_API, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json().get("videos", [])
    except Exception as e:
        print(f"      Erro ao buscar '{keyword}': {e}")
        return []


def _pick_best_file(files: list):
    portrait = [f for f in files if f.get("height", 0) > f.get("width", 0)]
    candidates = portrait if portrait else files
    candidates = sorted(candidates, key=lambda x: x.get("height", 0), reverse=True)
    return candidates[0] if candidates else None


def _download(url: str, dest: str) -> bool:
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"      Erro ao baixar clipe: {e}")
        return False
