# Mudanças R3 → R4

Este documento mapeia cada anotação da professora (de `Anotacoes_R3.txt`) e das notas de reunião para a alteração correspondente no `ULusofona_template_Tese_R4.md`. Serve de guia de defesa para a próxima orientação.

---

## RESUMO / ABSTRACT

| # | Anotação | Onde foi alterado | Como |
|---|----------|-------------------|------|
| R1 | "Os métodos estão descritos à frente? Votação Acumulativa e PERT/CPM" | Resumo / Abstract | Adicionada nota explícita: "descritas em detalhe no Capítulo 2" |
| R2 | Evitar detalhes técnicos no Abstract | Resumo / Abstract | Removidos os nomes técnicos de módulos (`ranker.py` mantido apenas no corpo); densidades numéricas removidas |
| R3 | Retirar "cobrindo grafos de 9 a 17 arestas" | Resumo / Abstract | Substituído por "selecionados por representarem regimes crescentes de acoplamento arquitetural" |
| R4 | O que significa "convergir" | Resumo / Abstract | Reformulado: "atingem uma distribuição estacionária comum sobre os requisitos centrais" |
| R5 | O que significa "suficientemente densos" | Resumo / Abstract | Reformulado: "grafos com densidade suficiente para suportar passeios aleatórios estáveis" |

## CAPÍTULO 1 — Introdução

### 1.1 Enquadramento e Motivação
| Anotação | Alteração |
|----------|-----------|
| Falar do algoritmo SALSA proposto para o Twitter, não falar de Engenharia Reversa | Removido "Engenharia Reversa"; primeiro *bullet* reescrito como "Adopção industrial do SALSA pelo Twitter" com **referência nova a Gupta et al. (2013) — WTF: The Who to Follow Service at Twitter**, que é o artigo oficial dos engenheiros do Twitter |
| Incluir mais referências | Adicionadas: Sommerville (2007), Karlsson et al. (2007), Newman (2010), Szwarcfiter (2018), Gupta et al. (2013), Page et al. (1999), Lempel & Moran (2001), Silva et al. (2018), Jin et al. (2009), Li & Yi (2009), Firesmith (2004) |

### 1.2 → renomeada para "Problema" (sem "Objetivos")
| Anotação | Alteração |
|----------|-----------|
| Qual o termo usado na literatura? Ranqueamento ou Priorização? | Esclarecido logo no primeiro parágrafo: "ranqueamento de requisitos — termo correntemente designado na literatura por **priorização de requisitos** (Karlsson, 2002; Firesmith, 2004; Silva et al., 2018)" |
| Definição formal do problema de ranqueamento | Adicionada definição formal: dado $R = \{r_1,\ldots,r_n\}$ e $D \subseteq R \times R$, procura-se $\pi: R \rightarrow \mathbb{R}$ |
| O segundo parágrafo deve estar no Cap. 2 | O parágrafo técnico sobre Processos Estocásticos e Cadeias de Markov foi removido daqui (mantido implícito); a discussão de Cadeias de Markov mantém-se no Cap. 2.2.2 (PageRank) |

### 1.3 Objetivos
| Anotação | Alteração |
|----------|-----------|
| Não usar subsecções (nota de reunião) | **Removidas as subsecções 1.3.1 e 1.3.2**; toda a Secção 1.3 é agora um único parágrafo enumerado (i, ii, iii) |
| Primeira frase muito idêntica a 1.2 | Reescrita para iniciar com "O objetivo desta dissertação é..." (em vez de "O ranqueamento de requisitos é um problema complexo...") |
| Unificar com 1.3.1 | Conteúdo de 1.3.1 absorvido na frase única |
| "abordagens de teoria dos grafos" em vez de "prioridades de grafos" | Corrigido: "abordagens de Teoria dos Grafos à modelação de interdependências" |
| Análise de Vulnerabilidades Topológicas e Modelo Híbrido não foram feitos | **Removidos como objetivos**; permanecem na Secção 5.2 (Trabalho Futuro) e no Cap. 2 como conceitos teóricos |

### 1.4 Abordagem Metodológica
| Anotação | Alteração |
|----------|-----------|
| Remover deste capítulo e reaproveitar no Cap. 3 como introdução à metodologia | **Secção 1.4 eliminada**; o texto foi integrado no parágrafo de abertura do Cap. 3 e na Secção 3.1 |
| Incluir secção com contribuições | **Nova Secção 1.4 — Contribuições** |
| Incluir secção com estrutura do documento | **Nova Secção 1.5 — Estrutura do Documento** |
| Incluir links de repositórios | URL do GitHub do projeto adicionado em 1.4 e em 3.2 (`https://github.com/talesedu/Tales_Tese_ulusofona` — marcado como "URL a confirmar pelo autor"). URLs do GitHub dos três projetos analisados adicionados na Tabela 2 (Secção 3.4.1) |
| Execução não foi em Google Colab — foi local com Python/Networkx/AST | Em 3.1: "O ambiente de experimentação é **local**, em Python 3.8+, recorrendo às bibliotecas `ast`, `NetworkX`, `NumPy`/`SciPy` e `Matplotlib`" |

## CAPÍTULO 2 — renomeado para "Conceitos teóricos e contextualização do problema"

| Anotação | Alteração |
|----------|-----------|
| Mudar título do capítulo | Título alterado para "Conceitos teóricos e contextualização do problema" |

### 2.1.1 Tipos de Grafos
| Anotação | Alteração |
|----------|-----------|
| Trocar "estrutura dos vértices" por "natureza das arestas e vértices" | Corrigido: "classificados de acordo com a **natureza dos vértices e das arestas** (Szwarcfiter, 2018)" |
| No exemplo de Grafos direcionados, remover "estudar a propagação de ideias ao longo do tempo" | **Frase removida**; o exemplo de citações foi também desduplicado (aparecia duas vezes no R3 — no bullet de não direcionados e no de direcionados) |

### 2.2 Algoritmos de ranqueamento
| Anotação | Alteração |
|----------|-----------|
| Faltam referências para métodos e métricas | Adicionadas referências em cada subsecção: 2.2.1 (Newman, 2010; Lempel & Moran, 2001), 2.2.2 (Page et al., 1999; Brin & Page, 1998 — nova; Masuda et al., 2017), 2.2.3 (Kleinberg, 1999; Ng et al., 2001), 2.2.4 (Lempel & Moran, 2001), 2.2.5 (He et al., 2014; He et al., 2015; Zhou et al., 2004) |
| Reforçar que se consideram métricas para redes direcionadas | Frase em destaque no início de 2.2: "**Importante**: todas as métricas descritas nesta secção são analisadas no contexto de **redes direcionadas**, dado que o grafo de requisitos é, por natureza, direcionado" |
| O que significa "uniforme" no vetor de personalização do PageRank | Esclarecido na 2.2.2: "uniforme, o que significa que todos os vértices têm idêntica probabilidade $1/n$ de serem escolhidos" (e $e_i = 1/n$ na descrição da equação) |
| Antes de falar de convergência, dizer que é um processo iterativo | Adicionado parágrafo em 2.2.2: "Trata-se de um **processo iterativo**: a equação $\mathbf{r}^{(t+1)} = dM\mathbf{r}^{(t)} + (1-d)\mathbf{e}$ é aplicada repetidamente..." antes de discutir convergência |

### 2.2.4 SALSA
| Anotação | Alteração |
|----------|-----------|
| Reescrever e explicar melhor SALSA | **Subsecção reescrita por completo**: descreve os dois passeios aleatórios no grafo bipartido auxiliar (autoridades e hubs), as transições $1/\text{out}(u)$ e $1/\text{in}(v)$, e a redução para $\text{in}(v)/|E|$ em grafos fortemente conexos sem pesos |
| Explicar efeito de comunidades muito coesas | Acrescentado parágrafo dedicado ao Efeito TKC: descreve o que são "comunidades muito coesas" (pequenos subconjuntos densamente interligados), porque é que o HITS as sobrepondera, e como a normalização local do SALSA evita esta concentração espúria |

### 2.2.5 BiRank
| Anotação | Alteração |
|----------|-----------|
| Não é claro o que significam "normalização estocástica" e "normalização simétrica" | Adicionadas definições explícitas em formato de bullet: (a) normalização estocástica = dividir cada coluna $j$ por $\sum_i W_{ij}$ (colunas somam 1, interpretação probabilística); (b) normalização simétrica = dividir $W_{ij}$ por $\sqrt{d_i \cdot d_j}$, com explicação do efeito de atenuar vértices de grau elevado |

### Nova subsecção 2.3.2 — Posicionamento face a Silva et al. (2018)
Resposta direta à nota de reunião: *"Referencial Teórico — Falar sobre o artigo que me inspirei e dar um paralelo. Dizendo que o artigo não tinha e esse foi uma evolução."*

Adicionado parágrafo que enumera as três dimensões em que a tese evolui o trabalho de Silva et al. (2018):
- (a) alarga o leque de algoritmos (PageRank → PageRank + HITS + SALSA);
- (b) automatiza a construção do grafo via AST (em vez de matrizes de rastreabilidade manuais);
- (c) valida sobre três projetos *open source* reais.

## CAPÍTULO 3 — Metodologia

| Anotação | Alteração |
|----------|-----------|
| Texto da antiga 1.4 deve introduzir a metodologia | Conteúdo absorvido no parágrafo de abertura do Cap. 3 e na nova Secção 3.1 (Estratégia de Investigação) |
| Execução foi local, não no Colab | Substituído ambiente em 3.1: "ambiente local, Python 3.8+, NetworkX, NumPy/SciPy, Matplotlib" |
| Links de repositórios | Adicionados em 3.2 (repositório do projeto) e na Tabela 2 da Secção 3.4.1 (URLs dos projetos CPython, Flask, scikit-learn no GitHub) |

### 3.3.2 PageRank
| Anotação | Alteração |
|----------|-----------|
| O que significa "por redistribuição uniforme" | Definido explicitamente: "a massa de probabilidade que um vértice sem arestas de saída teria de 'exportar' é dividida em partes iguais entre todos os vértices do grafo, mantendo a matriz de transição estocástica". Adicionada justificação (garantir ergodicidade da cadeia de Markov) e referência a Brin & Page (1998) |

## CAPÍTULO 4 — Avaliação de Resultados

| Anotação | Alteração |
|----------|-----------|
| Referir limitações antes de apontar no trabalho futuro | **Nova Secção 4.5 — Limitações**: enumera 5 limitações (dimensão do corpus, ausência de validação humana, observação parcial do Efeito TKC, mapeamento `func_to_req` como ponto de fricção residual, arestas não ponderadas) antes da entrada no Cap. 5 |

### 4.1.3 Caso Intermediário (Flask)
| Anotação | Alteração |
|----------|-----------|
| O que significa as cores entre os nós do texto? | Parágrafo adicionado a seguir ao bloco JSON do Flask: "as cores atribuídas aos vértices identificam o ficheiro-fonte do projeto a que cada requisito pertence (azul para `app.py`, verde para `cli.py`, laranja para `blueprints.py`)... As cores das arestas seguem a cor do vértice de origem". *(NOTA: verifique se as cores correspondem efectivamente ao que o `visualize.py` produz — se houver discrepância, ajustar.)* |

### 4.2.1 Caso Simples — Tabela
| Anotação | Alteração |
|----------|-----------|
| O que significam os valores entre parênteses? | Parágrafo introdutório à Tabela 4 explica: PageRank = probabilidades estacionárias (somam 1), HITS = vetores normalizados por norma euclidiana, SALSA = vetores normalizados por soma unitária |
| O que significa "33% da massa de probabilidade"? | Reformulado: "concentrando $0{,}337$ da probabilidade estacionária — ou seja, **um caminhante aleatório que percorra o grafo durante muito tempo passará cerca de $33{,}7\%$ do tempo nesse vértice**". Acrescentada definição operacional: "cada *score* indica que fração do tempo um passeio aleatório de longa duração visita aquele vértice" |

## CAPÍTULO 5 — Conclusão

### 5.1 Sumário e Principais Contribuições
| Anotação | Alteração |
|----------|-----------|
| Atenção: a validação foi sobre a qualidade dos resultados | Contribuição (1) renomeada de "Demonstração da viabilidade da rastreabilidade automática" para "**Validação da qualidade dos rankings extraídos automaticamente**", com frase final que torna explícita a natureza da validação: "incidiu sobre a **qualidade dos resultados** (coerência com a arquitetura conhecida), e não sobre a sua adequação a perceções de profissionais — limitação assumida e encaminhada para trabalho futuro" |
| Diferenças de densidade não são substanciais para tirar conclusões — grafos têm densidades similares | Contribuição (2) reformulada: adicionada frase final que reconhece "as diferenças observadas de densidade entre os três grafos ($0{,}10$, $0{,}13$ e $0{,}30$) não são, por si só, suficientemente acentuadas para sustentar generalizações fortes sobre o comportamento dos algoritmos em função da densidade; a leitura aqui apresentada é, antes, uma caracterização dos três casos concretos" |

### 5.2 Trabalho Futuro
| Anotação | Alteração |
|----------|-----------|
| Retirar "Análise empírica do Efeito TKC" e "Algoritmos adicionais" | **Ambas as linhas removidas** |
| (Nota de reunião) Validação com profissionais deve ser citada como trabalho futuro por limitação de recursos | **Nova primeira linha de Trabalho Futuro**: "Validação humana dos rankings", com referência explícita a Silva et al. (2018) — que conduziram este tipo de validação para o PageRank — e com justificação pela "limitação de recursos disponível na presente investigação" |

---

## Adições gerais não pedidas explicitamente nas anotações

Conforme orientação do utilizador ("adicionar referências onde novos conceitos são apresentados"):

- **Brin & Page (1998)** — adicionada à bibliografia e citada em 2.2.2 e 3.3.2 como referência primária para o tratamento de *dangling nodes* e ergodicidade da cadeia de Markov subjacente ao PageRank.
- **Gupta et al. (2013)** — adicionada à bibliografia e citada em 1.1 como referência primária para a adopção do SALSA pelo Twitter.
- **Newman (2010)** e **Szwarcfiter (2018)** — citados consistentemente em 2.1, 2.1.1 e 2.1.2 como referência para os conceitos basilares de grafos (já constavam da bibliografia mas não eram citados no corpo).
- **Masuda et al. (2017)** e **Ross (2014)** — passam a ser citados em 2.1.2 e 2.2.2 como referência para passeios aleatórios e cadeias de Markov.
- **Ng et al. (2001)** — citado em 2.2.3 como referência para a estabilidade dos algoritmos baseados em autovetores.

## Referências removidas da bibliografia

Foram retiradas referências que **não eram citadas em nenhum ponto do texto** e que pareciam ser herança do *template* original:

- Lourenço, Martin & Stützle (2009) — Iterated local search
- Yu, Wang & Zhang (2021) — Simulated annealing

(Caso pretenda manter alguma para usar no futuro, basta reintroduzi-las na bibliografia.)

---

## Itens a confirmar pelo autor

1. **URL do repositório GitHub.** Marcado como "URL a confirmar pelo autor" em 1.4 e 3.2 — substituir pelo URL público real assim que o repositório estiver disponível.
2. **Cores no grafo do Flask (4.1.3).** O texto descreve "azul para `app.py`, verde para `cli.py`, laranja para `blueprints.py`". Confirmar que a Figura 13 efetivamente usa estas cores; caso contrário, ajustar tanto o texto como a legenda.
3. **Recriar visualizações dos grafos com o Gephi** (sugestão da reunião — não realizado nesta revisão). A nota de reunião sugere usar https://lite.gephi.org/v1.0.2/ com CSVs no formato `Source,Target`. Se quiser, posso gerar os CSVs a partir dos `req_graph.json` numa próxima iteração — basta dizer.
4. **Capítulo 2 — segundo parágrafo de 1.2 movido.** Foi removido em vez de movido (o conteúdo já era coberto pela Secção 2.2). Se preferir manter um parágrafo equivalente em 2.2, é fácil reintroduzir.
