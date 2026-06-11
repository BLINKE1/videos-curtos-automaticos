# 🎬 Prompts de vídeo IA — Nail Sosuka (RASCUNHO pra refinar)

Coletânea de prompts pra gerar vídeo de unha por IA (Seedance / Kling / Veo).
Prompts em **inglês** (os modelos entendem melhor); notas em PT-BR.

> ⚠️ **Mão e dedos são o mais difícil pra IA de vídeo.** Boas práticas:
> 1. Use **imagem → vídeo** (controla muito melhor que text-to-video puro).
> 2. Peça **movimento sutil** (batida impaciente = pouco movimento → menos deformação).
> 3. Gere **3–4 takes** e escolha o melhor.
> 4. Mantenha clipes **curtos (5s)** — saem mais limpos.
> 5. Sempre **9:16 vertical**.

---

## 🌟 Plano-herói (REFINADO): mão na mesa, unhas de lava, dedos batendo

> **O que mudou na refatoração:** ancora a anatomia da mão ("anatomically perfect", "five visible fingers"), sequência explícita de batidas (anelar → médio → indicador, um por segundo) pra IA não confundir os dedos, lava só **no bico da unha** (não na pele), lente 85mm pra look de cinema, e batidas alinhadas com a duração do clipe de 5s.

### Passo 1 — Imagem base (grátis: Pollinations / `--ai-nails`)
```
Anatomically perfect close-up of an elegant female right hand resting flat
on a dark walnut table, five visible fingers in a natural relaxed pose, soft
realistic skin texture with subtle fine lines. The fingertips end in long
almond nails made of glowing molten lava — black cracked obsidian crust
with bright orange-red molten seams and tiny embers floating up from the
nail tips only. Warm key light from upper right, deep ambient shadows,
shot on 85mm macro lens, shallow depth of field, photorealistic skin,
cinematic moody lighting, vertical 9:16, ultra detailed, sharp focus on nails.
```

### Passo 2 — Prompt de movimento (image-to-video)
```
The ring finger taps the table once, then the middle finger, then the index
finger — one tap per second, subtle and slow. Thumb and pinky stay relaxed
and still throughout. The molten lava seams in the nails pulse with bright
orange glow on each tap, tiny embers drift slowly upward from the nail tips
only. Camera slowly pushes in along the hand toward the fingertips, hovering
low above the table. Shallow depth of field, photorealistic, cinematic.
```

### Variação text-to-video (sem imagem)
```
Cinematic slow-motion close-up of an elegant female right hand resting flat
on a dark walnut table, five visible fingers in a natural relaxed pose,
photorealistic skin. The fingertips end in long almond nails made of glowing
molten lava: black cracked obsidian crust with bright orange-red molten
seams, tiny embers drifting upward from the nail tips only. The ring finger
taps once, then the middle, then the index — one tap per second, subtle
motion; thumb and pinky stay still. Lava seams pulse with each tap. Camera
slowly pushes in toward the fingertips. Shallow depth of field, warm key
light, deep shadows, 85mm macro lens, vertical 9:16.
```

### Veo 3 — áudio nativo (cola no fim do prompt)
```
... The fingernails tap on the wooden table producing a crisp, hollow
tapping sound — three taps over three seconds, faint crackling lava sizzle
between taps, quiet ambient room tone.
```

### Beat structure (clipe 5s)
- **0.0–1.0s** — mão repousada, seams da lava brilham e pulsam
- **1.0–2.0s** — toque do **anelar**
- **2.0–3.0s** — toque do **médio**
- **3.0–4.0s** — toque do **indicador**
- **4.0–5.0s** — push-in fecha nas unhas; brasas sobem; glow no pico

### Configurações
- Proporção **9:16** · Duração **5s** · Qualidade **alta / Pro**
- Câmera: leve **push-in** (10–15% ao longo dos 5s)
- Modo: **image-to-video** sempre que possível

### Negative prompt (reforçado)
```
deformed hands, extra fingers, missing fingers, fused fingers, double thumb,
claw fingers, wax fingers, uneven nail lengths, distorted fingers, mutated
hand, warped nails, blurry, low quality, flicker, jitter, lava spreading
onto skin, burning skin, smoke covering hand
```

---

## 💫 Plano 2 (NOVO): turntable no vazio — mão girando, void escuro

> **Por que é à prova de IA:** a mão fica quase parada (só o pulso gira **ou** a câmera orbita), fundo preto puro = zero erro de cenário, e a rotação revela os 5 dedos um a um = "wow moment" natural no meio do clipe. Ideal para o material **galáxia** ou **ouro líquido** (texturas que brilham com a mudança de ângulo).

### Passo 1 — Imagem base
```
Anatomically perfect elegant female right hand floating in a pure black void,
five visible fingers spread slightly apart in a graceful relaxed pose, palm
facing down. The fingertips end in long almond nails containing a living
swirling galaxy — deep purple and blue nebula clouds, bright pinprick white
stars, faint inner glow as if each nail were a window into deep space. Soft
realistic skin, smooth rim light from the right outlining the fingers, deep
black background, photorealistic, vertical 9:16, ultra detailed, shot on
85mm macro lens, sharp focus on nails.
```

### Passo 2A — Movimento "wrist turn" (image-to-video, mais seguro)
```
The hand rotates slowly and gracefully on its wrist — a smooth controlled
turn from palm-down to palm-side, ninety degrees over five seconds. The
fingers stay still and elegantly spread; only the wrist rotates. As the
nails turn, the galaxies inside them shimmer and stars twinkle softly. The
camera is locked. Shallow depth of field, soft rim light from the right,
deep black background, photorealistic, cinematic.
```

### Passo 2B — Movimento "camera orbit" (alternativa)
```
The hand stays completely still, fingers gracefully spread, palm facing down.
The camera slowly orbits around the hand on a smooth ninety-degree arc from
the side to the front, revealing the nails from changing angles over five
seconds. The galaxies inside the nails shimmer and stars twinkle softly as
the angle changes. Locked focus on the fingertips, deep black background,
soft rim light, cinematic, photorealistic.
```

### Veo 3 — áudio nativo
```
... Quiet ethereal cosmic ambience, faint shimmer of distant stars, no
mechanical sound, deep silence with a soft cinematic pad.
```

### Beat structure (clipe 5s)
- **0.0–1.0s** — mão estática, brilho/twinkle das estrelas estabelece
- **1.0–4.0s** — rotação contínua e suave (pulso **ou** câmera)
- **4.0–5.0s** — settle no melhor ângulo, twinkle no pico, leve push-in

### Configurações
- Proporção **9:16** · Duração **5s** · Qualidade **alta / Pro**
- Modo **2A** (wrist turn) tende a ser mais consistente; **2B** (camera orbit) tem cinematografia melhor mas pode quebrar a mão. Gere os dois e escolha.

### Negative prompt
```
deformed hands, extra fingers, missing fingers, fused fingers, double thumb,
claw fingers, broken wrist, rubber hand, hand drifting, uneven nail lengths,
distorted fingers, mutated hand, warped nails, blurry, low quality, flicker,
jitter, visible background, environment, props, table, floor
```

---

## 🎨 Variações de material da unha
Vale **para os dois planos** acima — troca só a descrição da unha (a frase que começa com `long almond nails ...`):

| Tema | Substitua por |
|---|---|
| Cristal/gelo | `long almond nails made of translucent ice crystal, frosty glow, light refractions` |
| Galáxia | `long almond nails containing a swirling galaxy, glowing stars and purple-blue nebula` |
| Ouro líquido | `long almond nails made of flowing liquid gold, metallic reflections, glossy` |
| Neon | `long almond nails glowing neon cyan and magenta, light trails, dark scene` |
| Fogo | `long almond nails wrapped in dancing flames, sparks, ember glow` |
| Água | `long almond nails made of flowing translucent water, ripples, droplets` |

---

## 🛠️ Notas por ferramenta

### Seedance (ByteDance) — acesso manual atual
- Topo em movimento e aderência ao prompt; **sem áudio nativo** (adicionar o som da
  batida depois — efeito "nail tap" royalty-free).
- Melhor no **image-to-video**: suba a imagem do Passo 1 e cole o prompt de movimento.
- Estrutura que ele curte: **[sujeito + aparência] + [ação/movimento] + [câmera] + [luz/estilo]**.

### Kling
- Image-to-video, modo **Profissional**, 5s, push-in leve.
- Usa o mesmo negative prompt acima.

### Veo 3 (Google) — quando quiser SOM junto
- Gera **áudio nativo** → dá pra pedir o som das unhas batendo:
```
... The fingernails tap on the wooden table producing a crisp tapping sound,
ambient quiet room tone ...
```

---

## 💡 Ideias de cenas (além da mão batendo) — pra refinar depois
- Mão girando lentamente mostrando as unhas impossíveis brilhando (turntable).
- Gota/efeito do material "formando" a unha do zero (lava escorrendo e solidificando).
- Mão saindo da água/fumaça e revelando as unhas.
- Close deslizando dedo por dedo (cada unha um material diferente).
- Unha "acendendo" no escuro (neon/galáxia) e iluminando o rosto.
- Dedos estalando e soltando faíscas/raios.

---

## 🔗 Relacionados
- `IDEIAS_UNHAS_IA.md` — 10 temas virais (modo imagem `--ai-nails`).
- Vinheta da marca: rode com `--brand both --handle @nailsosuka` pra colar logo + CTA.
