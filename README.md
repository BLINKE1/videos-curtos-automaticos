# Videos Curtos Automáticos

Pipeline automatizado para geração e upload de vídeos curtos (58s, 9:16) no YouTube usando inteligência artificial — **100% gratuito**.

## Stack

| Etapa | Ferramenta | Custo |
|---|---|---|
| Roteiro | Groq API (Llama 3) | Gratuito |
| Voz (TTS) | Edge TTS | Gratuito, sem conta |
| B-roll | Pexels API | Gratuito |
| Edição | MoviePy + Pillow | Open source |
| Upload | YouTube Data API v3 | Gratuito (OAuth) |

## Pré-requisitos

- Python 3.9+
- Contas gratuitas: [Groq](https://console.groq.com) e [Pexels](https://www.pexels.com/api)
- Conta Google (opcional, para upload no YouTube)

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

```bash
cp .env.example .env
# Edite o .env com suas chaves de API
```

### Groq (roteiro)
1. Crie conta em https://console.groq.com
2. Crie uma API key em **API Keys**
3. Adicione no `.env`: `GROQ_API_KEY=gsk_...`

### Pexels (b-roll)
1. Crie conta em https://www.pexels.com/api
2. Copie sua API key
3. Adicione no `.env`: `PEXELS_API_KEY=...`

### YouTube (upload — opcional)
1. Acesse https://console.cloud.google.com
2. Crie um projeto e ative a **YouTube Data API v3**
3. Crie credenciais **OAuth 2.0** (tipo: Desktop app)
4. Baixe o JSON e salve como `client_secrets.json` na raiz do projeto

## Uso

```bash
# Gerar vídeo sem upload
python main.py "curiosidades sobre o espaço"

# Gerar e fazer upload (privado por padrão)
python main.py "curiosidades sobre o espaço" --upload

# Gerar e publicar diretamente
python main.py "curiosidades sobre o espaço" --upload --privacy public
```

O vídeo final é salvo na pasta `output/`.

## Formato de saída

- Resolução: **1080×1920** (9:16, vertical — Shorts/Reels)
- Duração: **~58 segundos**
- Formato: MP4 H.264, AAC
- Legendas automáticas sincronizadas com a narração
