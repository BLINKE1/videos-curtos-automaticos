import os
import argparse
import shutil
from datetime import datetime

from config import OUTPUT_DIR, TEMP_DIR
from pipeline.script_generator import (
    generate_script,
    generate_nail_caption,
    generate_fantasy_nail_prompts,
)
from pipeline.tts_generator import generate_audio
from pipeline.broll_fetcher import fetch_broll_videos
from pipeline.video_editor import assemble_video
from pipeline.photo_slideshow import collect_media, build_slideshow
from pipeline.ai_image_generator import generate_images
from pipeline.youtube_uploader import upload_video
from utils.helpers import ensure_dirs, clean_filename

# Preset dramático para o modo "unha impossível": cortes mais rápidos e zoom forte
FANTASY_SECONDS_PER_IMAGE = 2.5
FANTASY_ZOOM = 0.18


def create_short(topic: str, upload: bool = False, privacy: str = "private") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(TEMP_DIR, timestamp)
    broll_dir = os.path.join(run_dir, "broll")

    ensure_dirs(run_dir, broll_dir, OUTPUT_DIR)

    try:
        print(f"\n=== Gerando vídeo: {topic} ===\n")

        print("[1/5] Gerando roteiro...")
        script = generate_script(topic)
        print(f"      Título: {script['title']}")

        print("[2/5] Gerando áudio e legendas...")
        audio_path = os.path.join(run_dir, "audio.mp3")
        word_boundaries, audio_path = generate_audio(script["narration"], audio_path)
        print(f"      {len(word_boundaries)} palavras capturadas para legendas")

        print("[3/5] Buscando b-roll...")
        broll_paths = fetch_broll_videos(script["keywords"], broll_dir)
        print(f"      {len(broll_paths)} clipes baixados")

        print("[4/5] Montando vídeo...")
        output_filename = f"{timestamp}_{clean_filename(topic)}.mp4"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        assemble_video(broll_paths, audio_path, word_boundaries, output_path)
        print(f"      Salvo em: {output_path}")

        _maybe_upload(upload, output_path, script, privacy, step="[5/5]")

        print("\n=== Concluído! ===")
        return output_path

    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


def create_nail_slideshow(
    theme: str,
    photos_dir: str,
    music: str = None,
    narrate: bool = False,
    upload: bool = False,
    privacy: str = "private",
    logo: str = None,
    brand: str = None,
    handle: str = None,
) -> str:
    """Monta um Short/TikTok a partir de fotos reais do trabalho de unhas."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(TEMP_DIR, timestamp)
    ensure_dirs(run_dir, OUTPUT_DIR)

    try:
        print(f"\n=== Slideshow de unhas: {theme} ===\n")

        print("[1/4] Coletando fotos...")
        media_paths = collect_media(photos_dir)
        print(f"      {len(media_paths)} mídias encontradas em {photos_dir}")

        print("[2/4] Gerando textos com IA...")
        caption = generate_nail_caption(theme, with_narration=narrate)
        print(f"      Gancho: {caption['hook']} | Título: {caption['title']}")

        narration_path, word_boundaries = None, None
        if narrate and caption.get("narration"):
            print("      Gerando narração (TTS)...")
            narration_path = os.path.join(run_dir, "narration.mp3")
            word_boundaries, narration_path = generate_audio(
                caption["narration"], narration_path
            )

        print("[3/4] Montando vídeo...")
        output_filename = f"{timestamp}_{clean_filename(theme)}.mp4"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        build_slideshow(
            media_paths,
            output_path,
            music_path=music,
            narration_path=narration_path,
            word_boundaries=word_boundaries,
            hook=caption.get("hook"),
            cta=caption.get("cta"),
            logo_path=logo,
            brand=brand,
            handle=handle,
        )
        print(f"      Salvo em: {output_path}")

        _maybe_upload(upload, output_path, caption, privacy, step="[4/4]")

        print("\n=== Concluído! Pronto pro TikTok e YouTube Shorts ===")
        return output_path

    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


def create_fantasy_nail_video(
    theme: str,
    count: int = 5,
    music: str = None,
    upload: bool = False,
    privacy: str = "private",
    logo: str = None,
    brand: str = None,
    handle: str = None,
) -> str:
    """Gera um vídeo de "unha impossível" com imagens criadas por IA.

    Conteúdo de fantasia (lava, raios, galáxia...) para servir de isca de atenção
    e ser intercalado com os vídeos das unhas reais.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(TEMP_DIR, timestamp)
    img_dir = os.path.join(run_dir, "ai_images")
    ensure_dirs(run_dir, img_dir, OUTPUT_DIR)

    try:
        print(f"\n=== Unha impossível (IA): {theme} ===\n")

        print("[1/4] Gerando ideias e prompts com IA...")
        content = generate_fantasy_nail_prompts(theme, count=count)
        prompts = content["image_prompts"]
        print(f"      {len(prompts)} cenas | Título: {content['title']}")

        print("[2/4] Gerando imagens por IA...")
        image_paths = generate_images(prompts, img_dir)
        print(f"      {len(image_paths)} imagens prontas")

        print("[3/4] Montando vídeo (preset dramático)...")
        output_filename = f"{timestamp}_ia_{clean_filename(theme)}.mp4"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        build_slideshow(
            image_paths,
            output_path,
            music_path=music,
            hook=content.get("hook"),
            cta=content.get("cta"),
            seconds_per_image=FANTASY_SECONDS_PER_IMAGE,
            zoom=FANTASY_ZOOM,
            logo_path=logo,
            brand=brand,
            handle=handle,
        )
        print(f"      Salvo em: {output_path}")

        _maybe_upload(upload, output_path, content, privacy, step="[4/4]")

        print("\n=== Concluído! Lembre de marcar como 'conteúdo gerado por IA' ao postar ===")
        return output_path

    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


def _maybe_upload(upload: bool, output_path: str, meta: dict, privacy: str, step: str):
    if upload:
        print(f"{step} Fazendo upload para o YouTube...")
        video_id = upload_video(
            output_path,
            meta["title"],
            meta["description"],
            meta["tags"],
            privacy=privacy,
        )
        print(f"      https://youtube.com/watch?v={video_id}")
    else:
        print(f"{step} Upload pulado (use --upload para ativar)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de vídeos curtos automáticos")
    parser.add_argument("topic", help="Tema do vídeo (ou tema do slideshow de unhas)")
    parser.add_argument(
        "--photos",
        metavar="DIR",
        help="Pasta com fotos/clipes reais — ativa o modo slideshow de unhas",
    )
    parser.add_argument(
        "--ai-nails",
        type=int,
        metavar="N",
        help="Modo 'unha impossível': gera N imagens por IA (lava, raios, etc.)",
    )
    parser.add_argument(
        "--music", metavar="FILE", help="Trilha de fundo (mp3) para o slideshow"
    )
    parser.add_argument(
        "--narrate",
        action="store_true",
        help="Adiciona narração (TTS) por cima das fotos no modo slideshow",
    )
    parser.add_argument(
        "--brand",
        choices=["intro", "outro", "both"],
        help="Vinheta com o logo animado + CTA (abre, fecha ou ambos)",
    )
    parser.add_argument(
        "--logo",
        metavar="FILE",
        help="Caminho do logo PNG (padrão: assets/logo.png da Nail Sosuka)",
    )
    parser.add_argument(
        "--handle",
        metavar="@perfil",
        help="@ do perfil mostrado na vinheta (ex.: @nailsosuka)",
    )
    parser.add_argument("--upload", action="store_true", help="Fazer upload para YouTube")
    parser.add_argument(
        "--privacy",
        choices=["private", "unlisted", "public"],
        default="private",
        help="Visibilidade no YouTube (padrão: private)",
    )
    args = parser.parse_args()

    if args.ai_nails:
        create_fantasy_nail_video(
            args.topic,
            count=args.ai_nails,
            music=args.music,
            upload=args.upload,
            privacy=args.privacy,
            logo=args.logo,
            brand=args.brand,
            handle=args.handle,
        )
    elif args.photos:
        create_nail_slideshow(
            args.topic,
            args.photos,
            music=args.music,
            narrate=args.narrate,
            upload=args.upload,
            privacy=args.privacy,
            logo=args.logo,
            brand=args.brand,
            handle=args.handle,
        )
    else:
        create_short(args.topic, upload=args.upload, privacy=args.privacy)
