# Mudanças R5 → R6

Esta revisão (R6) executa as anotações registadas pelo autor em
`template/Anotacoes_R5.txt`, após avaliação do documento R5 em LaTeX. As mudanças
abrangem **conteúdo teórico novo** (Capítulo 2), **alterações no código da aplicação**
(ReqGraph/ranker) com **re-geração de figuras**, **correção de formatação LaTeX** e
**documentação**.

Documento (mantém-se em) LaTeX: `transformed_doc_R6_latex/`. Compilação descrita no
`transformed_doc_R6_latex/README.md`.

> **Nota de ambiente.** O `.venv` versionado é um ambiente Windows e não corre em Linux.
> Para re-executar a aplicação foi criado um venv Linux limpo
> (`networkx 3.6`, `matplotlib 3.10`, `numpy 2.4`, `scipy 1.17`). A geração dos grafos é
> **determinística**: os `req_graph.json`/`ranking_results.json` mantêm-se semanticamente
> idênticos aos do R5 (só mudaram as imagens). Logo, **nenhum número das tabelas do
> Capítulo 4 foi alterado**.

---

## Sumário das mudanças

| # (Anotação) | Tema | Tipo | Estado |
|--------------|------|------|--------|
| 1 | Spearman e Kendall no Cap. 2 | Texto | ✅ |
| 2 | Grafo denso e esparso no Cap. 2 | Texto | ✅ |
| 3 | AST Python no Cap. 2 | Texto | ✅ |
| 4 | Setas nos grafos direcionados de exemplo | Figuras | ✅ |
| 5 | Novo layout (não-circular) do Call Graph | Código + Figuras | ✅ |
| 6 | Justificação dos nomes de ficheiro no PDF | Formatação LaTeX | ✅ |
| 7 | `ranking_results` com fundo branco (papel) | Código + Figuras | ✅ |
| 8 | Este ficheiro R6 | Documentação | ✅ |
| 9 | Resposta à dúvida sobre validação do grafo | Texto | ✅ |

---

## Detalhe por anotação

### 1 — Spearman e Kendall (critérios de avaliação) no Capítulo 2
**Onde:** `chapters/02_fundamentos.tex` — nova subsecção *Comparação de rankings:
correlação de Spearman e Kendall* (`\label{sec:rank-correlation}`), no fim da §2.2.
**Como:** introduz, no plano conceptual, *rank correlation* como critério formal de
avaliação dos resultados: Spearman ρ (relação monotónica, forma fechada) e Kendall τ_b
(pares concordantes/discordantes com correção de *ties*). A formalização operacional
permanece em §3.4 (referência cruzada, sem duplicação). Já existiam nas abreviaturas e no
glossário; passa a haver explicação no corpo do texto.

### 2 — Grafo denso e esparso no Capítulo 2
**Onde:** `chapters/02_fundamentos.tex` — nova subsecção *Densidade: grafos esparsos e
densos* (`\label{sec:densidade}`), a seguir aos *Tipos de Grafos* (§2.1).
**Como:** define densidade `D = |E|/(n(n-1))` para digrafos (e `n(n-1)/2` para não
direcionados), distingue esparso vs. denso e liga aos valores reais reportados no Cap. 4
(0,125 / 0,262 / 0,304), reforçando a leitura de densidade como *proxy* de acoplamento e a
sua volatilidade em grafos pequenos.

### 3 — AST Python no Capítulo 2
**Onde:** `chapters/02_fundamentos.tex` — nova secção *Análise estática e Árvores de
Sintaxe Abstrata (AST)* (`\label{sec:ast}`), com subsecções *O que é uma AST*
(`sec:ast-conceito`) e *Da AST ao Grafo de Requisitos: validação por fase*
(`sec:ast-validacao`).
**Como:** explica análise estática vs. dinâmica, o módulo `ast` da *stdlib*, os nós
relevantes (`FunctionDef`, `Call`), um exemplo mínimo e o **determinismo** da extração.
Esta secção fundamenta o fluxo principal do processo descrito no Cap. 3.

### 4 — Setas nos grafos direcionados de exemplo
**Onde:** `transformed_doc_R6_latex/figures/image4.png`, `image8.png`, `image9.png`,
`image10.png`; gerador novo em `transformed_doc_R6_latex/scripts/gen_example_figures.py`.
**Como:** as setas passam a ser **escuras, grossas e terminam na borda do nó**
(`node_size` em `draw_networkx_edges`), visíveis mesmo reduzidas no PDF. Corrigiu-se ainda
uma **incoerência**: os grafos de PageRank (image8) e HITS (image9) usavam um grafo
diferente do descrito no texto; passam todos a usar o grafo canónico
A→B, A→C, B→C, C→A (graus de saída A:2, B:1, C:1), com o par recíproco A↔C desenhado em
arcos separados.

### 5 — Novo layout (não-circular) do Call Graph
**Onde:** `reqgraph/visualize.py` — nova função `_hierarchical_layout()` e ajustes em
`visualize_call_graph()`.
**Como:** substitui o `spring_layout` (aspeto circular/disperso) por um **layout
hierárquico top-down em camadas**, robusto a ciclos (via condensação de componentes
fortemente conexas + `multipartite_layout`). Figura, tamanho de nó e setas dimensionados
dinamicamente conforme a densidade; rótulos só quando o grafo é pequeno o suficiente.
Figuras regeneradas: `figures/call_graph_{simples_stdlib,medio_flask,complexo_sklearn}.png`.

### 6 — Justificação dos nomes de ficheiro no PDF
**Onde:** `transformed_doc_R6_latex/style/lusofona.sty` — redefinição de `\code` e `\req`.
**Como:** os comandos eram `\texttt{#1}` puro, que não permite quebra de linha em `_`, `/`
ou `.`, fazendo caminhos longos (ex.: `sklearn/linear_model/_logistic.py`) estourarem a
margem e impedirem a justificação. Passam a inserir `\allowbreak` após esses separadores:
o `\_` é tornado quebrável em todo o texto e, dentro de `\code`, o `/` e o `.` ficam
quebráveis via re-tokenização com `\scantokens` (solução robusta que funciona também em
legendas e títulos de secção). Mantém-se a compatibilidade com a escrita habitual `\_`, e
usa-se `\texorpdfstring` para *bookmarks* PDF limpos.

### 7 — `ranking_results` com fundo branco (papel)
**Onde:** `ranker.py` — dicionário `COLORS` (paleta) usado por `generate_ranking_chart()`
e `generate_comparison_chart()`.
**Como:** o tema escuro (*slate*) foi **substituído** por uma paleta clara (fundo branco,
texto escuro, grelha clara, cores de barra escurecidas para impressão). Figuras
regeneradas: `figures/ranking_results_*.png` e `figures/ranking_comparativo.png`.

### 8 — Este ficheiro R6
**Onde:** `template/Mudancas_R6.md` (este documento).
**Como:** registo direto de todas as atualizações desta iteração, no formato do
`Mudancas_R5.md`.

### 9 — Resposta à dúvida (por email) sobre validação do grafo
**Pergunta:** *como se valida que o grafo obtido está correto, garantindo que o output de
cada fase do pipeline está correto e que o grafo final representa as dependências?*
**Onde:** `chapters/02_fundamentos.tex` §*Da AST ao Grafo de Requisitos: validação por
fase* (`sec:ast-validacao`) + reforço em `chapters/04_resultados.tex` §4.5 (Validade
Interna).
**Como (argumento):** a validade é **construída fase a fase**, não aferida só no fim:
(i) a **AST** é correta por garantia da *toolchain* do Python; (ii) o **Call Graph** e o
**Grafo de Requisitos** são artefactos **inspecionáveis** (`call_graph.png`,
`req_graph.json`/`.dot`, `req_graph.png`); (iii) a semântica das arestas decorre
**objetivamente** da estrutura do código — como o conceito de requisito aqui **não** é o
de Sommerville mas uma agregação de responsabilidades cujas interdependências saem da
análise estática, a dependência `r_a → r_b` existe *por construção* sempre que uma função
de `r_a` invoca uma de `r_b`. Assim, a correção do grafo reduz-se à correção de dois passos
verificáveis: a deteção de chamadas pela AST (determinística) e o mapeamento
`func_to_req` — o único passo com subjetividade residual, isolado, com protocolo explícito
(§3.5.2) e registado como ameaça à validade (§4.5/§4.6).

---

## Artefactos de código alterados (raiz do repositório)

| Ficheiro | Mudança |
|----------|---------|
| `reqgraph/visualize.py` | Layout hierárquico do Call Graph (item 5). |
| `ranker.py` | Paleta de impressão (fundo branco) para os rankings (item 7). |
| `transformed_doc_R6_latex/scripts/gen_example_figures.py` | **Novo** — gera as figuras de exemplo direcionadas com setas (item 4). |
| `transformed_doc_R6_latex/style/lusofona.sty` | `\code`/`\req` com quebra de linha (item 6). |
| `transformed_doc_R6_latex/chapters/02_fundamentos.tex` | Densidade, Spearman/Kendall, AST + validação (itens 1, 2, 3, 9). |
| `transformed_doc_R6_latex/chapters/04_resultados.tex` | Reforço da validação por fase em §4.5 (item 9). |
| `transformed_doc_R6_latex/figures/*.png` | Figuras regeneradas (itens 4, 5, 7). |

## Como reproduzir as figuras

```bash
# venv Linux com as dependências científicas
python3 -m venv .venv-linux
./.venv-linux/bin/python -m pip install networkx matplotlib numpy scipy

# call/req graphs + rankings (itens 5 e 7)
for c in simples_stdlib medio_flask complexo_sklearn; do
  ./.venv-linux/bin/python -m reqgraph testes/$c --mapping testes/$c/mapeamento.py
done
./.venv-linux/bin/python ranker.py --all

# figuras de exemplo direcionadas (item 4)
./.venv-linux/bin/python template/transformed_doc_R6_latex/scripts/gen_example_figures.py

# (copiar os PNGs de testes/<caso>/ para transformed_doc_R6_latex/figures/ com os
#  nomes call_graph_<caso>.png, req_graph_<caso>.png, ranking_results_<caso>.png)
```

## Itens a confirmar/completar pelo autor (mantidos do R5)

1. Repositório GitHub público no momento da defesa.
2. *Inter-rater* do `func_to_req` (Cohen's κ) — recomendado, não bloqueante.
3. Análise de sensibilidade ao fator de amortecimento `d ∈ {0,5; 0,7; 0,85; 0,95}`.
