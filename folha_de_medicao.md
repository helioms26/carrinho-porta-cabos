# Folha de medição — carrinho porta-cabos VAHLE WS1F85-50-90-K

Cada linha corresponde a uma variável do arquivo `carrinho_WS1F85_v1.scad`.
Meça, anote na coluna **Medido** e substitua o número no `.scad`. Só isso.

**Como medir com régua sem errar feio:** apoie a peça sobre a régua (não a régua sobre a peça),
leia sempre pela mesma borda, e meça cada cota 2x. Para diâmetros de furo, use uma broca ou o
próprio parafuso como calibre — é mais confiável que régua.

---

## 1. Roldana — JÁ MEDIDO ✅

| Variável | Cota | Valor | Status |
|---|---|---|---|
| `roda_De` | Ø externo (aba) | 35,0 | ✅ você mediu |
| `roda_Dg` | Ø no fundo da garganta | 20,0 | ✅ você mediu |
| `roda_larg` | largura total | 16,0 | ✅ você mediu |
| `roda_furo` | **Ø do furo central / eixo** | 8,5 (chute) | ⬜ **MEDIR** |

> `roda_furo`: use o próprio parafuso do eixo. Se for M8, deixe 8,4–8,6.

---

## 2. Corpo amarelo — O QUE FALTA

| # | Variável | O que medir | Estimativa atual | Medido |
|---|---|---|---|---|
| 1 | `corpo_L` | comprimento total da peça, ponta a ponta | **90,0** (catálogo) | ⬜ confirmar |
| 2 | `eixo_ent` | **centro a centro dos dois furos de eixo** | 60,0 | ⬜ |
| 3 | `corpo_topo` | do centro do furo do eixo até a **borda de cima** | 22,0 | ⬜ |
| 4 | `corpo_base` | do centro do furo do eixo até a **borda de baixo** do corpo | 23,0 | ⬜ |
| 5 | `parede` | espessura da parede de fundo (a face lisa externa) | 4,0 | ⬜ |
| 6 | — | **espessura total da meia-casca** (a peça inteira, de face a face) | 12,5 calculado | ⬜ |

> A cota 6 é a mais importante de todas: ela valida `parede` + profundidade do bolso.
> Se a sua meia-casca medir, por exemplo, 14 mm, ajuste `parede` para 14 − 8,5 = 5,5.

---

## 3. Haste (a parte que quebrou)

| # | Variável | O que medir | Estimativa atual | Medido |
|---|---|---|---|---|
| 7 | `haste_larg` | largura da haste (no sentido do comprimento do corpo) | 22,0 | ⬜ |
| 8 | `haste_comp` | comprimento da haste, da base do corpo até a ponta | 45,0 | ⬜ |
| 9 | `furo_y` | da base do corpo até o **centro do furo da sela** | 28,0 | ⬜ |
| 10 | `furo_sela` | Ø do furo do parafuso da sela azul | 8,5 | ⬜ |
| 11 | `porca_chave` | **chave** da porca sextavada (face a face, não ponta a ponta) | 13,0 | ⬜ |
| 12 | `porca_prof` | profundidade do rebaixo onde a porca encaixa | 6,5 | ⬜ |

> `porca_chave`: M8 = 13 mm, M6 = 10 mm. Se a porca sair, meça ela direto.

---

## 4. Cabo de aço

| # | Variável | O que medir | Estimativa atual | Medido |
|---|---|---|---|---|
| 13 | `cabo_D` | Ø do cabo de aço do sistema | 10,0 | ⬜ |

---

## 5. Conferência final antes de imprimir

Rode estas 3 contas com os seus números. Se alguma der negativa ou apertada, tem cota errada:

1. `corpo_topo` deve ser **maior** que `(roda_De + 1,5) / 2` = 18,25
   → senão o bolso da roldana arromba a borda de cima.
2. `eixo_ent / 2 + (roda_De + 1,5) / 2` deve ser **menor** que `corpo_L / 2` = 45
   → senão a roldana passa da ponta da peça. (com 60 e 35: 30 + 18,25 = 48,25 ❌ **já estoura**)
3. `2 × (roda_larg/2 + 0,5) + 2 × parede` = espessura do carrinho montado.

> ⚠️ A conta 2 **já não fecha** com as estimativas atuais (`eixo_ent = 60`).
> Ou o entre-eixos é menor (~46–50 mm), ou o corpo é mais longo que 90 mm, ou a roldana
> passa da ponta de propósito. Essa é a primeira cota que eu preciso que você meça.

---

## Impressão (sugestão inicial)

| Item | Recomendação | Por quê |
|---|---|---|
| Material | **PETG** ou **ABS/ASA**; se puder, **PA (nylon) ou PETG-CF** | PLA quebra por fluência sob carga contínua e não aguenta sol/calor |
| Orientação | face externa lisa **na mesa**, peça deitada | camadas ficam perpendiculares ao esforço da haste |
| Paredes | 5 perímetros | resistência vem da parede, não do preenchimento |
| Preenchimento | 50–60 % giroide | |
| Camada | 0,20 mm | |
| Suporte | não precisa nesta orientação | |

---

## ⚠️ Aviso de segurança

Esse carrinho sustenta cabo suspenso em operação. Peça impressa em FDM tem
**resistência anisotrópica** — quebra na direção das camadas com uma fração da carga do
original injetado. Trate a peça impressa como **solução provisória**, teste sem carga
primeiro, e não use em trecho onde a queda do cabo atinja pessoas ou equipamento.
Não consigo estimar a carga admissível da peça impressa a partir de fotos — isso exigiria
ensaio ou simulação com o material real.
