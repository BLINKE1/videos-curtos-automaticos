import json
import re
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL


def generate_script(topic: str) -> dict:
    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""Crie um roteiro para um vídeo curto de 58 segundos sobre: {topic}

Regras:
- Narração com 140-155 palavras (para durar ~58s em velocidade natural)
- Em português brasileiro
- Primeira frase: impacto imediato para prender atenção nos primeiros 3 segundos
- Frases curtas e dinâmicas
- Final com call-to-action (curtir, seguir ou comentar)

Responda SOMENTE com JSON neste formato:
{{
    "title": "título do vídeo (máximo 100 caracteres)",
    "description": "descrição para YouTube/TikTok (máximo 500 caracteres com hashtags relevantes)",
    "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
    "keywords": ["palavra visual 1", "palavra visual 2", "palavra visual 3"],
    "narration": "texto completo da narração"
}}"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Resposta inválida do Groq: {raw}")
