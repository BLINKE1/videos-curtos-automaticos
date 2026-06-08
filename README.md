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

## Modo slideshow de fotos reais (canais de unha 💅)

Em vez de usar b-roll de banco, este modo monta o vídeo a partir das **fotos e
clipes reais** do trabalho da manicure — o que mais engaja em canal de unha
(ex.: Nail Sosuka). Cada foto ganha efeito Ken Burns (zoom suave), transições
com crossfade, gancho e call-to-action na tela, e trilha de fundo.

1. Coloque as fotos/clipes numa pasta, nomeadas em ordem (ex.: `01.jpg`,
   `02.jpg`, `03.mp4`...). Formatos: JPG, PNG, WEBP, MP4, MOV.
2. (Opcional) Tenha um `.mp3` de música royalty-free.

```bash
# Slideshow só com fotos + textos gerados por IA
python main.py "francesinha rosa com glitter" --photos ./fotos_unhas

# Com música de fundo
python main.py "nail art floral" --photos ./fotos_unhas --music ./musica.mp3

# Com narração (locução por cima das fotos) + legendas
python main.py "cuidados com a cutícula" --photos ./fotos_unhas --narrate

# Gerar e já subir pro YouTube Shorts
python main.py "unhas de gel passo a passo" --photos ./fotos_unhas --music ./musica.mp3 --upload --privacy public
```

O MP4 gerado (9:16) também serve para **postar no TikTok** manualmente pelo
celular. A IA (Groq) cria o gancho, a chamada pra ação, o título, a descrição e
as hashtags automaticamente.

> Dica: o tempo de cada foto na tela é controlado por `SECONDS_PER_IMAGE` no
> `.env` (padrão 3s). Com `--narrate`, o ritmo acompanha a duração da narração.

## Formato de saída

- Resolução: **1080×1920** (9:16, vertical — Shorts/Reels)
- Duração: **~58 segundos**
- Formato: MP4 H.264, AAC
- Legendas automáticas sincronizadas com a narração
