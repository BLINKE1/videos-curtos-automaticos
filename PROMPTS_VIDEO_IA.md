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

## 🌟 Plano-herói: mão na mesa, unhas impossíveis, dedos batendo impacientes

### Passo 1 — Imagem base (grátis: Pollinations / `--ai-nails`)
```
Extreme close-up of an elegant female hand resting on a dark wooden table,
long almond nails made of glowing molten lava, cracked obsidian texture with
bright orange-red glow and tiny embers, realistic skin, cinematic moody
lighting, shallow depth of field, vertical 9:16, photorealistic, ultra detailed
```

### Passo 2 — Prompt de movimento (image-to-video)
```
The fingers tap impatiently on the wooden table, one finger after another,
subtle and realistic finger motion, the molten lava nails glow and flicker,
small embers drift upward, slow motion, camera slowly glides along the hand
and pushes in, shallow depth of field, cinematic, photorealistic
```

### Variação text-to-video (sem imagem)
```
Cinematic slow-motion extreme close-up of an elegant hand resting on a dark
wooden table, long almond nails made of glowing molten lava with bright
orange-red glow and embers. The fingers tap impatiently on the table one after
another with subtle realistic motion. The camera slowly glides along the hand
and pushes in. Shallow depth of field, moody lighting, photorealistic, vertical 9:16.
```

### Configurações
- Proporção **9:16** · Duração **5s** (ou 10s) · Qualidade **alta / Pro**
- Câmera: leve **push-in** (aproximar)

### Negative prompt
```
deformed hands, extra fingers, missing fingers, distorted fingers, mutated hand,
warped nails, blurry, low quality, flicker, jitter
```

---

## 🎨 Variações de material da unha
Mesma estrutura, troca só a descrição da unha:

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
