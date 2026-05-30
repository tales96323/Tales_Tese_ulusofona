# Mudanças R4 → R5

Esta revisão (R5) converte o documento para LaTeX e aplica as melhorias identificadas pela skill `academic-paper-reviewer` (painel de 5 perspetivas — EIC + Metodologia + Domínio + Perspetiva + Devil's Advocate).

Documento R5 em LaTeX: `transformed_doc_R5_latex/`. Compilação descrita no `transformed_doc_R5_latex/README.md`.

---

## Sumário das melhorias

A revisão R5 endereça três fragilidades metodológicas centrais que o painel identificou de forma consensual:

1. **Ausência de RQs explícitas + métricas formais de comparação** (consenso EIC, Metodologia, Perspetiva).
2. **Construct validity do `func_to_req` não defendida** (consenso Domínio, DA).
3. **Reinterpretação retórica de resultados nulos como sucesso** — flagged como CRITICAL pelo Devil's Advocate.

Foram também detetadas e corrigidas **incoerências nos números reportados no R4** (ver secção [Correções de dados](#correcoes-de-dados) abaixo).

---

## P1 — Críticas (incorporadas no R5)

| # | Anotação | Onde foi alterado em R5 | Como |
|---|----------|--------------------------|------|
| P1.1 | **Adicionar Research Questions explícitas** | `chapters/01_introducao.tex` §1.3 (Objetivos e *Research Questions*) | Adicionadas RQ1 (concordância entre algoritmos), RQ2 (efeito da densidade), RQ3 (coerência arquitetural). Cada RQ tem critério verificável. |
| P1.2 | **Métricas formais de comparação de rankings** | `chapters/04_resultados.tex` §4.3 (nova secção "Correlações Spearman e Kendall"); script `compute_rank_correlations.py` (raiz) | Calculadas correlações de Spearman ρ e Kendall τ_b entre todos os 6 pares de algoritmos em cada um dos 3 projetos (18 medições). Tabela 4.4 mostra os valores, com pares "convergentes fortes" destacados. Resultados rejeitam a hipótese de R4 de "convergência no caso mais denso". |
| P1.3 | **Threats to Validity formal (Wohlin)** | `chapters/04_resultados.tex` §4.5 | Substituída a antiga Secção 4.5 "Limitações" por uma categorização formal segundo Wohlin (Construct/Internal/External/Conclusion). 12 ameaças categorizadas, cada uma com justificação e referência cruzada para trabalho futuro. |
| P1.4 | **Reformular discussão SALSA como resultado nulo** | `chapters/02_fundamentos.tex` §2.2.4; `chapters/04_resultados.tex` §4.6 | Inserida `notebox` "Caveat metodológico" no Cap. 2 a aviso que o Efeito TKC não foi observado. No Cap. 4 §4.6 ponto 3, "Efeito TKC mitigado" foi substituído por "resultado nulo — SALSA não distinguiu o que os outros distinguiram; a propriedade teórica não pôde ser empiricamente testada neste corpus". |
| P1.5 | **URL GitHub público** | `chapters/01_introducao.tex` §1.4; `chapters/03_metodologia.tex` §3.2 | URL `https://github.com/tales96323/Tales_Tese_ulusofona` consolidado nas duas referências (sem mais "URL a confirmar"). |
| P1.6 | **Critério a priori de "convergência"** | `chapters/03_metodologia.tex` §3.5 | Definido antes da análise: ρ ≥ 0.7 *e* τ_b ≥ 0.55, OR top-1 idêntico em ≥ 2 algoritmos. Salvaguarda contra *p-hacking*. |

---

## P2 — Reforços fortes (incorporados no R5)

| # | Anotação | Onde foi alterado em R5 | Como |
|---|----------|--------------------------|------|
| P2.1 | **Protocolo formal de mapeamento `func_to_req`** | `chapters/03_metodologia.tex` §3.4.2 (nova) | 5 passos formais (levantamento de domínios → granularidade → atribuição → revisão de cobertura → validação de coerência) com guidelines concretas (5–30 funções por requisito). Limitação de ausência de inter-rater explicitada em `notebox`. |
| P2.2 | **Clarificação ontológica de "requisito"** | `chapters/01_introducao.tex` §1.2 (`notebox`) | Inserida nota: "requisito" aqui = "agregação de responsabilidades implementadas no código-fonte, *proxy* de *domain feature*". Distingue da definição clássica de Sommerville. |
| P2.3 | Análise de sensibilidade ao `d` | `chapters/04_resultados.tex` §4.5 (Internal Validity) + `chapters/05_conclusao.tex` §5.2 | Registada como ameaça à validade e como trabalho futuro com domínio {0.5, 0.7, 0.85, 0.95}. |
| P2.4 | **Literatura recente (2019–2025)** | `chapters/02_fundamentos.tex` §2.3; `references.bib` | Acrescentadas Berander & Andrews (2005), Achimugu et al. (2014), Bukhsh et al. (2020), Saaty (1980), Karlsson & Ryan (1997), Wohlin et al. (2012), Spearman (1904), Kendall (1938), Goodman & Kruskal (1954), Riaz et al. (2014), Rasiman et al. (2022). |
| P2.5 | Implicações práticas | `chapters/04_resultados.tex` §4.6 (parágrafo "Implicações práticas") | Workflow concreto para engenheiro de requisitos: gerar grafo → ranker → considerar top-5 do PR + HITS-auth + HITS-hub → "candidato a requisito crítico" = aparece no top-5 de ≥ 2 algoritmos. |
| P2.6 | Justificar escolha PR/HITS/SALSA face a alternativas | `chapters/02_fundamentos.tex` §2.2 (parágrafo "Escolha de PageRank, HITS e SALSA face a alternativas") | Justificação em 3 razões; menciona Katz, betweenness, k-core como alternativas para trabalho futuro. |
| P2.7 | Tabela 7 (Estado dos objetivos) reformulada | `chapters/05_conclusao.tex` Tabela 5.1 | Inclui agora estado real ("Concluído"/"Não realizado") + RQs + 3 itens não realizados encaminhados para trabalho futuro. |
| P2.8 | Visualizações Gephi | `transformed_doc_R5_latex/README.md` | Registado como tarefa pendente — instruções dadas para gerar CSVs `Source,Target` a partir dos `req_graph.json`. |
| P2.9 | Esclarecer divergência nº requisitos mapeados vs. no grafo | `chapters/04_resultados.tex` §4.1.1 | Coluna nova na Tabela 4.3 "Requisitos isolados (singletons)" + parágrafo dedicado: stdlib 1, Flask **6**, sklearn 1. |

---

## P3 — Polimento (durante conversão LaTeX)

| # | Item | Resultado |
|---|------|-----------|
| P3.1 | Paralelismo PT↔EN no Abstract | Reescrito do zero em paralelo (`front/abstract_pt.tex` ↔ `front/abstract_en.tex`). |
| P3.2 | Tabela de abreviaturas completada | `front/abbreviations.tex` — adicionados AHP, NDCG, RP, RQ, ρ, τ_b, in(v)/out(v), além das siglas R4. |
| P3.3 | Lista de Figuras + Lista de Tabelas | Auto-geradas por LaTeX (`\listoffigures`, `\listoftables` em `main.tex`). |
| P3.4 | Apêndice com `mapeamento.py` completo | `back/apendices.tex` Apêndice C — referencia os três ficheiros `mapeamento.py` no repositório público. |
| P3.5 | Glossário expandido | `back/glossario.tex` — acrescentados: Cadeia de Markov, Distribuição estacionária, Ergodicidade, Feature module, Kendall τ_b, Rank correlation, Spearman ρ, Threats to validity. |
| P3.6 | Citações APA 7 consistentes | `biblatex` com `style=apa` + biber; todas as citações no corpo usam `\citet{...}` ou `\parencite{...}`. |

---

## Correções de dados

Durante o trabalho de revisão foram detetadas **discrepâncias entre os números reportados no R4 e os valores reais nos artefactos**:

| Métrica | Projeto | R4 reportou | Valor real | Fonte |
|---------|---------|-------------|------------|-------|
| Vértices no Grafo de Requisitos | Flask | "13 requisitos" implícito na Tabela 3 | **7** | `testes/medio_flask/req_graph.json` |
| Vértices no Grafo de Requisitos | scikit-learn | "9 requisitos" | **8** | `testes/complexo_sklearn/req_graph.json` |
| Densidade | stdlib | 0.10 | **0.125** | calculada como \|E\|/(n(n-1)) |
| Densidade | Flask | 0.13 | **0.262** | idem |
| Densidade | sklearn | 0.30 | **0.304** | idem |
| Requisitos isolados | Flask | não reportado | **6** (REQ_BLUEPRINTS, REQ_CLI_DISCOVERY, REQ_CLI_TYPES, REQ_STATIC_FILES, REQ_TEMPLATING, REQ_TESTING) | calculado por diff |

A divergência mais relevante é **Flask: 6 dos 13 requisitos mapeados são singletons**. Esta omissão no R4 era metodologicamente significativa porque mascara o impacto da estratégia de seleção parcial de ficheiros (a *templating engine* do Flask reside em `jinja2`, não em `app.py`/`cli.py`/`blueprints.py`). O R5 reporta isto explicitamente na Tabela 4.3 e discute-o como ameaça à validade externa em §4.5.

Os valores corretos foram extraídos por `compute_rank_correlations.py` (raiz) e cruzados manualmente com os JSONs em `testes/<projeto>/`.

---

## Estrutura do R5 (resumo)

```
template/transformed_doc_R5_latex/
├── main.tex                  # entry point
├── references.bib            # APA via biblatex+biber
├── style/lusofona.sty        # margens, fontes, cores institucionais
├── front/                    # capa, agradecimentos, resumos, abreviaturas
├── chapters/                 # 5 capítulos (1 Introdução → 5 Conclusão)
├── back/                     # glossário + 3 apêndices
├── figures/                  # (vazio — copiar imagens do R4 para aqui)
└── README.md                 # instruções de compilação
```

Compilar com `latexmk -xelatex main.tex` ou as 4 invocações manuais
documentadas no `README.md`.

---

## Itens a confirmar/completar pelo autor (antes da defesa)

1. **Repositório GitHub público.** O URL `https://github.com/tales96323/Tales_Tese_ulusofona` é assumido no corpo da tese — confirmar que o repositório é público no momento da defesa.

2. **Cores no grafo do Flask (Figura 4.2).** A descrição "azul `app.py` / verde `cli.py` / laranja `blueprints.py`" foi mantida do R4. Verificar que a figura efetivamente usa essas cores.

3. **Recriar visualizações no Gephi (R3, ainda em aberto).** Sugerido pela orientadora; ficheiros CSV `Source,Target` podem ser gerados a partir de `testes/<projeto>/req_graph.json`. Substituir as figuras `req_graph.png` por versões Gephi.

4. **Copiar imagens para `figures/`.** As referências `\includegraphics` apontam para `example-image-*` (placeholders); substituir pelos PNGs reais do R3 (`template/transformed_doc_R3/media/media/imageN.png`) ou pelos PNGs novos do Gephi.

5. **Inter-rater do `func_to_req` (recomendado, não bloqueante).** Pedir a um colega que reproduza o mapeamento de um dos três projetos e calcular Cohen's κ — adicionaria solidez empírica significativa antes da defesa.

6. **Análise de sensibilidade ao `d`.** Pequeno *script* adicional que executa `nx.pagerank` para `d ∈ {0.5, 0.7, 0.85, 0.95}` e produz um gráfico de estabilidade de rank. Quase grátis em tempo (≤ 1 dia).
