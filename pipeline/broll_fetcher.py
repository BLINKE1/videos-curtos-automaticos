import os
import requests
from config import PEXELS_API_KEY

PEXELS_API = "https://api.pexels.com/videos/search"


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
