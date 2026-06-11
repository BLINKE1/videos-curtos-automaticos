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

## Modo "unha impossível" (imagens geradas por IA 🔥)

Conteúdo de **fantasia** — unhas impossíveis (lava, raios, galáxia, cristal...) —
para servir de **isca de atenção** e ser intercalado com os vídeos das unhas
reais. As imagens são geradas por IA (text-to-image) a partir de prompts que a
própria IA (Groq) cria, e montadas com um preset dramático (cortes rápidos +
zoom forte).

```bash
# Gera 5 cenas de unha impossível sobre o tema
python main.py "unhas de lava vulcânica" --ai-nails 5 --music ./epic.mp3

# Gera e sobe pro YouTube Shorts
python main.py "unhas de raio elétrico" --ai-nails 6 --upload --privacy public
```

O backend de imagem é **gratuito e sem chave** ([Pollinations](https://pollinations.ai),
`IMAGE_PROVIDER=pollinations`) e plugável — dá pra trocar por um serviço pago de
maior qualidade (ou de vídeo) no futuro, em `pipeline/ai_image_generator.py`.

> ⚠️ **Transparência:** é conteúdo gerado por IA. A descrição já inclui a hashtag
> `#IA`, e ao postar no TikTok/YouTube **marque a opção "conteúdo gerado por IA"**.
> Use só pra entreter/atrair — os agendamentos vêm dos vídeos do trabalho real.

## Modo chroma key (mão real + texturas trocadas) 🎬

Você grava **uma vez** uma mão de verdade com **esmalte verde-chroma** sobre
**fundo branco claro** (papel cartão, parede). O pipeline isola por frame as
unhas e o fundo e troca cada um por uma textura de vídeo real do Pexels
(lava borbulhando, galáxia girando, raio elétrico, ouro líquido, ...).

Resultado: mão e movimento humanos reais + unhas/fundo "impossíveis". Uma
gravação vira N vídeos com texturas diferentes.

```bash
# Unhas de lava (fundo original preservado)
python main.py "unhas de lava" --chroma ./minha_gravacao.mp4 --nail-texture lava

# Unhas de raio + fundo de galáxia
python main.py "unhas elétricas" --chroma ./take01.mp4 \
   --nail-texture electric --bg-texture galaxy --music ./epic.mp3

# Vinheta + upload direto
python main.py "ouro líquido" --chroma ./take02.mp4 \
   --nail-texture gold --bg-texture smoke \
   --brand both --handle @nailsosuka --upload --privacy public
```

**Texturas pré-mapeadas (`--nail-texture` / `--bg-texture`):**
`lava`, `fire`, `electric`, `galaxy`, `gold`, `water`, `smoke`, `neon`, `crystal`.
Também aceita caminho local de MP4 se você já tem o clipe.

**Como gravar bem:**
- Esmalte verde-chroma vivo (ou fita adesiva verde colada nas unhas)
- Fundo branco fosco, **iluminação difusa e frontal** (sem sombra forte)
- 9:16, 60fps se possível (reduz motion blur na borda da unha)
- Mantenha ~30cm entre a mão e o fundo (reduz "green spill" na pele)

**Calibração:** thresholds HSV vivem em `pipeline/chroma_compositor.py`
(`NAIL_HSV_LOW/HIGH`, `BG_HSV_LOW/HIGH`). Ajuste se o key falhar com o seu
esmalte específico.

## Vinheta de marca (logo animado + CTA) ✨

Adiciona o **logo da Nail Sosuka entrando e saindo** com um "pop" (escala + fade)
e uma chamada pra ação. Funciona com os modos `--photos` e `--ai-nails`.

```bash
# Abre e fecha com a vinheta da marca
python main.py "unhas de lava" --ai-nails 5 --brand both --handle @nailsosuka

# Só no fechamento (logo + CTA + @perfil sobre fundo escurecido)
python main.py "francesinha rosa" --photos ./fotos --brand outro --handle @nailsosuka

# Só na abertura
python main.py "nail art floral" --photos ./fotos --brand intro --handle @nailsosuka
```

- `--brand intro|outro|both` — onde a vinheta aparece.
- `--logo FILE` — logo PNG (padrão: `assets/logo.png`, já incluso).
- `--handle @perfil` — o @ mostrado na vinheta.

No **fechamento**, a vinheta escurece o fundo e mostra logo + CTA + @perfil; o CTA
simples de rodapé é suprimido automaticamente pra não duplicar.

## Formato de saída

- Resolução: **1080×1920** (9:16, vertical — Shorts/Reels)
- Duração: **~58 segundos**
- Formato: MP4 H.264, AAC
- Legendas automáticas sincronizadas com a narração
