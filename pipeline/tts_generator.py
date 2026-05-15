import asyncio
import edge_tts
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


def generate_audio(text: str, audio_path: str, voice: str = TTS_VOICE):
    """Returns (word_boundaries, audio_path).
    word_boundaries: list of (offset_100ns, duration_100ns, word)
    """
    word_boundaries = asyncio.run(_generate(text, voice, audio_path))
    return word_boundaries, audio_path
