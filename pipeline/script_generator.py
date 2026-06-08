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

    return _parse_json(response.choices[0].message.content)


def generate_nail_caption(theme: str, with_narration: bool = False) -> dict:
    """Copy para um vídeo de unhas montado a partir de fotos reais.

    Retorna gancho (texto na tela no início), CTA, título, descrição, tags e,
    opcionalmente, uma narração curta para locução por cima das fotos.
    """
    client = Groq(api_key=GROQ_API_KEY)

    narration_rule = (
        '- "narration": locução curta de 35-45 palavras, em PT-BR, calorosa, '
        "como uma manicure falando do trabalho dela e terminando com convite "
        "para agendar/seguir."
        if with_narration
        else '- "narration": ""  (deixe vazio)'
    )

    prompt = f"""Você cria conteúdo para o TikTok/YouTube Shorts de um estúdio de unhas.
Tema do vídeo (fotos reais do trabalho da manicure): {theme}

Gere textos curtos, em português brasileiro, com energia e linguagem de redes sociais.

Regras:
- "hook": frase curta de impacto (máx. 6 palavras) que aparece NA TELA nos primeiros segundos.
- "cta": chamada para ação curta (máx. 5 palavras), ex.: "Agende já! 💅".
- "title": título do vídeo (máx. 80 caracteres) com 1-2 emojis.
- "description": descrição com hashtags fortes de nicho de unhas (máx. 400 caracteres).
- "tags": 6 tags relevantes (unhas, nail art, manicure, etc.).
{narration_rule}

Responda SOMENTE com JSON neste formato:
{{
    "hook": "...",
    "cta": "...",
    "title": "...",
    "description": "...",
    "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"],
    "narration": "..."
}}"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        response_format={"type": "json_object"},
    )

    return _parse_json(response.choices[0].message.content)


def _parse_json(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Resposta inválida do Groq: {raw}")
