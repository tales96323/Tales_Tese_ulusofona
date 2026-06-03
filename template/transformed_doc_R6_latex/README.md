# Tese de Mestrado — R6 (versão LaTeX)

Versão LaTeX da dissertação **"Uma perspectiva de engenharia sobre a evolução de algoritmos de ranqueamento baseada em grafos"**, R6.

## Estrutura

```
transformed_doc_R6_latex/
├── main.tex                          # Documento principal (entry point)
├── references.bib                    # Bibliografia BibTeX
├── style/
│   └── lusofona.sty                  # Estilo Lusófona (margens, fontes, cores)
├── front/
│   ├── cover.tex                     # Capa
│   ├── acknowledgements.tex
│   ├── abstract_pt.tex               # Resumo
│   ├── abstract_en.tex               # Abstract
│   └── abbreviations.tex
├── chapters/
│   ├── 01_introducao.tex
│   ├── 02_fundamentos.tex
│   ├── 03_metodologia.tex
│   ├── 04_resultados.tex
│   └── 05_conclusao.tex
├── back/
│   ├── glossario.tex
│   └── apendices.tex
├── figures/                          # (vazio — figuras devem ser copiadas para aqui)
└── README.md
```

## Compilação

### Recomendado: XeLaTeX (suporte Unicode nativo, fontes do sistema)

```bash
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex
```

### Alternativa: pdfLaTeX

```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

### Em uma linha com `latexmk` (mais robusto)

```bash
latexmk -xelatex main.tex
# para limpar:
latexmk -C
```

## Dependências (TeX Live / MiKTeX)

| Pacote | Função |
|--------|--------|
| `geometry` | margens A4 |
| `babel` | idiomas (português + inglês) |
| `csquotes` | aspas tipográficas |
| `microtype` | refinamentos tipográficos |
| `fontspec` (XeLaTeX) | fontes do sistema |
| `setspace` | entrelinha 1.5 |
| `titlesec` | títulos de capítulo/secção |
| `fancyhdr` | cabeçalho/rodapé |
| `enumitem` | listas |
| `booktabs`, `tabularx`, `longtable`, `multirow`, `makecell` | tabelas |
| `xcolor` (table, dvipsnames) | cores |
| `graphicx` | imagens |
| `caption`, `subcaption` | legendas |
| `hyperref` (hidelinks) | hiperligações |
| `cleveref` | referências cruzadas |
| `amsmath`, `amssymb`, `amsthm`, `mathtools`, `bm` | matemática |
| `listings` | código JSON / Python |
| `biblatex` (style=apa) + biber | bibliografia APA |
| `tcolorbox` | caixas de nota |
| `tikz`, `background` | marca de revisão |

Instalação (Arch Linux):
```bash
sudo pacman -S texlive-most texlive-bibtexextra texlive-fontsextra biber
```

Instalação (Ubuntu/Debian):
```bash
sudo apt-get install texlive-full biber
```

## Figuras

Os ficheiros `.tex` referenciam figuras pelos nomes do R4 (e.g.
`image11.png`, `image12.png`...). As substituições estão marcadas
como `example-image-*` para permitir a compilação imediata; basta
copiar os PNGs do R4 (de
`template/transformed_doc_R3/media/media/` ou
`testes/<projeto>/req_graph.png`, etc.) para a pasta `figures/` e
substituir os nomes nos `\includegraphics`.

Sugestão da orientadora (R3) ainda em aberto: **recriar visualizações
no Gephi** (https://lite.gephi.org/v1.0.2/) para melhor leitura
visual dos grafos. Os CSVs `Source,Target` podem ser exportados a
partir dos `req_graph.json` em `testes/<projeto>/`.

## Notas de revisão R6

Ver `Mudancas_R6.md` (na pasta-mãe) para o mapeamento completo das
alterações desta revisão (R5 → R6): Spearman/Kendall, densidade e AST
no Cap. 2, validação do grafo por fase, setas nos grafos de exemplo,
novo layout do Call Graph, ranking em fundo branco e justificação dos
nomes de ficheiro. Para o histórico anterior (R4 → R5), ver
`Mudancas_R5.md`. Em resumo, o R5 trouxe:

- **P1 — Críticas:** RQs explícitas (Cap. 1.3), Spearman/Kendall
  (Cap. 4.3 novo), Threats to Validity formal (Cap. 4.5), SALSA
  reformulado como resultado nulo (Cap. 2.2.4, 4.4), critério de
  convergência *a priori* (Cap. 3.5), URL GitHub fixado.
- **P2 — Reforços:** Protocolo `func_to_req` (Cap. 3.4.2), nota
  ontológica (Cap. 1.2), literatura RE 2019–2025 (Cap. 2.3), Tabela
  de estado de objetivos (Cap. 5.1), número correto de vértices
  isolados.

## Cálculo de Spearman / Kendall

O *script* `compute_rank_correlations.py` (raiz do repositório) é
executado uma única vez para produzir `rank_correlations.json`. Os
valores que aparecem na Tabela 4.4 (`correlacoes`) são extraídos
deste ficheiro.

```bash
cd "../../.."   # voltar à raiz do repositório
python3 compute_rank_correlations.py
```

Saída esperada (excerto):
```
=== simples_stdlib (n=9, |E|=9, density=0.125) ===
PageRank vs SALSA-auth   ρ=0.8393  τ=0.7500  Top1=no
HITS-hub vs SALSA-hub    ρ=0.7589  τ=0.7016  Top1=no
...
```

## Licença

Conteúdo do autor; consulte o repositório principal para a licença
do código.
