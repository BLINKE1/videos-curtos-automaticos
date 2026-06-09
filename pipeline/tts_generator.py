import asyncio
import edge_tts
from moviepy import AudioFileClip
from config import TTS_VOICE


async def _generate(text: str, voice: str, audio_path: str):
    communicate = edge_tts.Communicate(text, voice)
    word_boundaries = []

    with open(audio_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                word_boundaries.append(
                    (chunk["offset"], chunk["duration"], chunk["text"])
                )

    return word_boundaries


def _fallback_boundaries(text: str, audio_path: str) -> list:
    """Gera word boundaries distribuídos uniformemente pela duração do áudio."""
    try:
        clip = AudioFileClip(audio_path)
        duration = clip.duration
        clip.close()
    except Exception:
        return []

    words = text.split()
    if not words:
        return []

    duration_per_word = duration / len(words)
    boundaries = []
    for i, word in enumerate(words):
        offset = int(i * duration_per_word * 1e7)
        dur = int(duration_per_word * 1e7)
        boundaries.append((offset, dur, word))
    return boundaries


def generate_audio(text: str, audio_path: str, voice: str = TTS_VOICE):
    word_boundaries = asyncio.run(_generate(text, voice, audio_path))

    if not word_boundaries:
        print("      WordBoundary não retornou dados — usando fallback de timing.")
        word_boundaries = _fallback_boundaries(text, audio_path)

    return word_boundaries, audio_path
