import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
TTS_VOICE = os.getenv("TTS_VOICE", "pt-BR-FranciscaNeural")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30
TARGET_DURATION = 58

# Modo slideshow (fotos reais): tempo de cada foto na tela quando não há narração
SECONDS_PER_IMAGE = float(os.getenv("SECONDS_PER_IMAGE", "3.0"))

OUTPUT_DIR = "output"
TEMP_DIR = "temp"
