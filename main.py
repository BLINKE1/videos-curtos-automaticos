import os
import argparse
import shutil
from datetime import datetime

from config import OUTPUT_DIR, TEMP_DIR
from pipeline.script_generator import generate_script
from pipeline.tts_generator import generate_audio
from pipeline.broll_fetcher import fetch_broll_videos
from pipeline.video_editor import assemble_video
from pipeline.youtube_uploader import upload_video
from utils.helpers import ensure_dirs, clean_filename


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

        if upload:
            print("[5/5] Fazendo upload para o YouTube...")
            video_id = upload_video(
                output_path,
                script["title"],
                script["description"],
                script["tags"],
                privacy=privacy,
            )
            print(f"      https://youtube.com/watch?v={video_id}")
        else:
            print("[5/5] Upload pulado (use --upload para ativar)")

        print("\n=== Concluído! ===")
        return output_path

    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de vídeos curtos automáticos")
    parser.add_argument("topic", help="Tema do vídeo")
    parser.add_argument("--upload", action="store_true", help="Fazer upload para YouTube")
    parser.add_argument(
        "--privacy",
        choices=["private", "unlisted", "public"],
        default="private",
        help="Visibilidade no YouTube (padrão: private)",
    )
    args = parser.parse_args()

    create_short(args.topic, upload=args.upload, privacy=args.privacy)
