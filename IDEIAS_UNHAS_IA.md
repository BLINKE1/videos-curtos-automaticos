# 💅🔥 10 ideias virais de "unha impossível" (modo IA)

Conteúdo de **fantasia** pra atrair visualização e intercalar com os vídeos das
unhas reais. Copie o comando, rode, e poste no TikTok/Shorts.

> ⚠️ Ao postar, marque a opção **"conteúdo gerado por IA"**. A estratégia é:
> a IA atrai o público, o **trabalho real** da manicure converte em cliente.

Como rodar (precisa de `GROQ_API_KEY` no `.env`; as imagens são grátis via Pollinations):

```bash
python main.py "TEMA AQUI" --ai-nails 5 --music ./musica.mp3
```

`--ai-nails 5` = 5 cenas. Use `--upload --privacy public` pra já subir no YouTube Shorts.

---

## As 10 ideias

| # | Tema (comando) | Por que viraliza |
|---|---|---|
| 1 | `"unhas de lava vulcânica brilhando"` | Cor quente + brilho hipnotiza nos primeiros 3s |
| 2 | `"unhas de raio elétrico azul neon"` | Movimento de energia chama atenção no feed |
| 3 | `"unhas de galáxia com estrelas e nebulosa"` | Estético e "salvável" — gera compartilhamento |
| 4 | `"unhas de aquário com peixinhos nadando"` | Fofura + efeito impossível = comentários |
| 5 | `"unhas de fogo com chamas reais"` | Drama visual forte, ótimo pra hook |
| 6 | `"unhas de cristal de gelo congelado"` | Brilho gelado satisfatório, paleta clean |
| 7 | `"unhas de ouro líquido derretido"` | Luxo + textura metálica = sensação "rico" |
| 8 | `"unhas com borboletas 3D saindo delas"` | Efeito "saindo da tela" prende o olhar |
| 9 | `"unhas de aurora boreal brilhando no escuro"` | Cores raras, muito "wow" e salvável |
| 10 | `"unhas de diamante com cristais brilhantes"` | Brilho + tema desejo = alto engajamento |

### Bônus
| # | Tema (comando) | Por que viraliza |
|---|---|---|
| 11 | `"unhas de água em movimento tipo cachoeira"` | Movimento fluido é satisfatório |
| 12 | `"unhas neon cyberpunk brilhando no escuro"` | Estética trend, público jovem |

---

## Dicas de postagem

- **Gancho nos 3 primeiros segundos**: a IA já coloca um texto de impacto na tela.
- **Áudio em alta**: use um som que esteja bombando no TikTok (a música entra com `--music`).
- **Intercale**: 1 vídeo de IA (atrai) → 1 vídeo do trabalho real (converte).
- **Constância** importa mais que perfeição: poste com frequência.
- Na legenda, sempre inclua um convite pra agendar com a sua irmã (link/Whats).

## Quer mais qualidade?

As imagens grátis (Pollinations) já ficam boas. Pra **movimento de verdade**
(lava escorrendo, raios animados) dá pra plugar um serviço de vídeo pago
(Kling/Runway) em `pipeline/ai_image_generator.py` — o backend já é plugável.
