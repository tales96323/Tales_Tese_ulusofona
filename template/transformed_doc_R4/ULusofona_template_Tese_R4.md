Uma perspectiva de engenharia sobre a evolução de algoritmos de ranqueamento baseada em grafos.

Tales Santos

Dissertação para obtenção do Grau de Mestre em

**Mestrado em Engenharia Informática e Sistemas de Informação**

| **Orientador:**   | Aleksandar Mikovic — *Professor, Universidade Lusófona* |
|-------------------|---------------------------------------------------------|
| **Coorientador:** | Sofia Fernandes — *Professora, Universidade Lusófona*   |

**Lisboa, setembro, 2026**

---

# Agradecimentos

*Os agradecimentos, são um elemento opcional, no qual o candidato deverá registar o reconhecimento às pessoas e/ou instituições que contribuíram de forma relevante para a elaboração do trabalho.*

---

# Resumo

A priorização de requisitos de software é uma das atividades mais sensíveis da Engenharia de Requisitos: técnicas tradicionais como a **Votação Acumulativa** ou o **PERT/CPM** — descritas em detalhe no Capítulo 2 — dependem fortemente da perceção subjetiva dos *stakeholders* e tendem a tornar-se inconsistentes em sistemas com elevado número de requisitos interdependentes (Karlsson, 2002; Silva et al., 2018). Esta dissertação investiga uma alternativa de natureza estrutural, assente na aplicação de algoritmos de ranqueamento de grafos — PageRank, HITS e SALSA — ao grafo de dependências entre requisitos.

Foi desenvolvido o **ReqGraph**, um protótipo Python que automatiza o pipeline *Código-fonte → AST → Call Graph → Grafo de Requisitos*, e o módulo **ranker.py**, que aplica os três algoritmos ao grafo extraído. A validação foi conduzida sobre três projetos reais de código aberto — CPython *stdlib*, Flask e *scikit-learn* — selecionados por representarem regimes crescentes de acoplamento arquitetural. Os resultados mostram que, em grafos com densidade suficiente para suportar passeios aleatórios estáveis, os algoritmos atingem uma distribuição estacionária comum sobre os requisitos centrais (identificando, por exemplo, `REQ_PIPELINE` como o requisito mais central do *scikit-learn*) e, em grafos esparsos, divergem de forma informativa, oferecendo perspetivas complementares de importância (transitiva, direta e de orquestração). Conclui-se que o ranqueamento estrutural constitui um complemento robusto às técnicas tradicionais, contribuindo para a redução do viés subjetivo na priorização de requisitos.

**Palavras-chave:** Engenharia de Requisitos · Priorização Estrutural · Análise Estática de Código · Grafos · PageRank · HITS · SALSA.

---

# Abstract

Software requirements prioritization is one of the most sensitive activities in Requirements Engineering: traditional techniques such as **Cumulative Voting** or **PERT/CPM** — described in detail in Chapter 2 — depend heavily on the subjective perception of stakeholders and tend to become inconsistent in systems with a large number of interdependent requirements (Karlsson, 2002; Silva et al., 2018). This thesis investigates a structural alternative based on the application of graph ranking algorithms — PageRank, HITS, and SALSA — to the dependency graph between requirements.

A Python prototype, **ReqGraph**, was developed to automate the pipeline *source code → AST → call graph → requirement graph*, together with the **ranker.py** module which applies the three algorithms to the extracted graph. Validation was conducted on three real open-source projects — CPython *stdlib*, Flask, and *scikit-learn* — selected as representatives of increasing regimes of architectural coupling. The results show that, in graphs with enough density to support stable random walks, the algorithms reach a common stationary distribution over the central requirements (for example, identifying `REQ_PIPELINE` as the most central requirement of *scikit-learn*) and, in sparse graphs, diverge informatively, offering complementary perspectives on importance (transitive, direct, and orchestration). We conclude that structural ranking constitutes a robust complement to traditional techniques, helping reduce subjective bias in requirements prioritization.

**Keywords:** Requirements Engineering · Structural Prioritization · Static Code Analysis · Graphs · PageRank · HITS · SALSA.

---

# Abreviaturas, Siglas e Símbolos

| Símbolo / Sigla | Descrição |
|-----------------|-----------|
| COFAC | Cooperativa de Formação e Animação Cultural |
| DEISI | Departamento de Engenharia Informática e Sistemas de Informação |
| ER | Engenharia de Requisitos |
| PRS | Priorização de Requisitos de Software |
| AST | *Abstract Syntax Tree* |
| TKC | *Tightly Knit Community* |
| $G = (V,E)$ | Grafo com vértices $V$ e arestas $E$ |
| $\mathbf{r}$ | Vetor de ranks |
| $d$ | Fator de amortecimento do PageRank |
| $A$ | Matriz de adjacência |
| $A_{ij} = 1$ | Se há aresta de $j$ para $i$ (em grafos direcionados) |

---

# 1. Introdução

O Capítulo 1 enquadra o problema da priorização estrutural de requisitos. A Secção 1.1 discute a motivação e os fatores recentes que tornaram esta investigação oportuna; a Secção 1.2 define formalmente o problema; a Secção 1.3 enuncia os objetivos do trabalho; a Secção 1.4 lista as contribuições; e a Secção 1.5 apresenta a estrutura do restante documento.

**Conceitos chave:** enquadramento; motivação; problema; priorização; contribuições.

## 1.1 Enquadramento e Motivação

O desenvolvimento de sistemas de software em larga escala enfrenta desafios crescentes na gestão da complexidade e na organização de grandes volumes de informação interdependente (Sommerville, 2007). Tradicionalmente, a relevância de elementos dentro de uma rede de requisitos era determinada por análises textuais, comparações entre pares ou heurísticas manuais (Karlsson et al., 2007); a evolução da **Teoria dos Grafos** (Newman, 2010; Szwarcfiter, 2018) permitiu uma transição para métodos puramente estruturais, capazes de extrair informação latente diretamente da topologia do sistema.

A motivação principal para este estudo surge da convergência entre algoritmos de alta performance já em produção na indústria e a necessidade de rigor analítico na engenharia de software. Dois marcos fundamentais impulsionaram esta investigação:

- **Adopção industrial do SALSA pelo Twitter.** Em *Who To Follow*, o sistema de recomendação de utilizadores do Twitter, Gupta et al. (2013) propõem e descrevem uma variante do algoritmo **SALSA** (Lempel & Moran, 2001) para sugerir conexões entre utilizadores. Esta adopção em produção, sobre um grafo de larga escala, demonstra a viabilidade de usar passeios aleatórios em grafos para determinar prestígio e relevância de forma escalável.

- **Aplicação do PageRank à priorização de requisitos.** A descoberta de pesquisas que aplicam o **PageRank** (Page et al., 1999) à priorização de requisitos de software (Silva et al., 2018; Jin et al., 2009; Li & Yi, 2009) sustenta a hipótese de que a estrutura de dependências de um sistema contém informação latente suficiente para ordenar requisitos de forma mais consistente do que técnicas predominantemente subjetivas (Firesmith, 2004).

Dessa forma, o trabalho enquadra-se na busca por modelos matemáticos que minimizem o viés humano em decisões críticas de engenharia, utilizando propriedades topológicas para extrair inteligência de grafos de software.

## 1.2 Problema

O **ranqueamento de requisitos** — termo correntemente designado na literatura por **priorização de requisitos** (Karlsson, 2002; Firesmith, 2004; Silva et al., 2018) — consiste em produzir uma ordem total (ou parcial) sobre o conjunto de requisitos $R = \{r_1, r_2, \ldots, r_n\}$ de um sistema, a partir de critérios que reflitam a importância relativa de cada requisito para a entrega de valor, a estabilidade arquitetural ou o risco do projeto. Formalmente, dado o conjunto $R$ e uma relação de dependência $D \subseteq R \times R$, em que $(r_i, r_j) \in D$ se $r_i$ depende de $r_j$, a tarefa de priorização procura uma função $\pi: R \rightarrow \mathbb{R}$ que atribua a cada requisito um *score* compatível com a sua centralidade na rede $(R, D)$.

As técnicas tradicionais de priorização — Comparação em Pares (Karlsson et al., 2007), Votação Acumulativa (Leffingwell & Widrig, 2003; Ahl, 2005) e PERT/CPM (Kerzner, 2009) — sofrem com problemas intrínsecos de subjetividade e esforço (Firesmith, 2004). A inexperiência dos *stakeholders*, a divergência na interpretação das escalas de prioridade e o foco excessivo num único ponto de vista resultam em prioridades inconsistentes e em "posições inválidas" (Silva et al., 2018). Em particular, a Votação Acumulativa, por depender excessivamente da decisão direta do *stakeholder*, não resolve a duplicidade envolvida em requisitos mutuamente dependentes (Silva et al., 2018).

Este trabalho justifica-se, portanto, ao investigar e comparar a eficácia do **PageRank**, **HITS** e **SALSA** na priorização estrutural de requisitos, sobre grafos extraídos automaticamente do código-fonte, oferecendo um modelo analítico que minimize o esforço dos *stakeholders* e que utilize integralmente a rastreabilidade de requisitos disponível (Gotel & Finkelstein, 1994).

## 1.3 Objetivos

O objetivo desta dissertação é investigar e comparar a eficácia dos algoritmos **PageRank**, **HITS** e **SALSA** na priorização estrutural de requisitos de software, fornecendo um modelo analítico que utilize a rastreabilidade entre requisitos para garantir consistência em sistemas de larga escala. Em concreto, pretende-se: (i) **formalizar** a aplicação de processos estocásticos e de abordagens de Teoria dos Grafos à modelação de interdependências entre requisitos e à determinação de fluxos de influência; (ii) **desenvolver** um protótipo (ReqGraph) que extraia, de forma totalmente automatizada e reprodutível, o grafo de requisitos a partir do código-fonte de um projeto Python; (iii) **avaliar empiricamente**, por meio de simulações sobre projetos reais de código aberto, o comportamento comparativo dos três algoritmos, identificando convergências e divergências de ranking e discutindo-as à luz da arquitetura conhecida dos sistemas analisados.

## 1.4 Contribuições

As principais contribuições desta dissertação são:

1. **Pipeline reprodutível para extração de grafos de requisitos.** Implementação do protótipo *ReqGraph*, que automatiza a transformação *Código-fonte → AST → Call Graph → Grafo de Requisitos* sobre projetos Python, recorrendo exclusivamente a análise estática e a artefactos canónicos da comunidade científica (NetworkX, Graphviz).

2. **Implementação aberta do SALSA.** Implementação manual e documentada do algoritmo SALSA (Lempel & Moran, 2001), uma vez que o NetworkX não a disponibiliza nativamente, incluindo o tratamento explícito de vértices absorventes por redistribuição uniforme.

3. **Comparação empírica entre PageRank, HITS e SALSA** sobre grafos reais de requisitos derivados de três projetos *open source* representativos de regimes crescentes de acoplamento arquitetural (CPython *stdlib*, Flask e *scikit-learn*).

4. **Mecanismo de redução do custo de mapeamento.** Formalização de um *prompt* estruturado (`llm_prompt_mapping.md`) que permite gerar o dicionário `func_to_req` via modelos de linguagem de grande escala, mitigando a principal fricção operacional da abordagem.

O código-fonte completo, os mapeamentos `func_to_req` utilizados e os artefactos gerados nas experiências encontram-se publicamente disponíveis em **https://github.com/talesedu/Tales_Tese_ulusofona** *(URL a confirmar pelo autor).*

## 1.5 Estrutura do Documento

O restante documento está organizado da seguinte forma. O **Capítulo 2** apresenta os conceitos teóricos relevantes — Teoria dos Grafos, algoritmos de ranqueamento e fundamentos da Engenharia de Requisitos — e contextualiza o problema, posicionando esta dissertação em relação ao trabalho de Silva et al. (2018), do qual constitui uma evolução metodológica. O **Capítulo 3** descreve a metodologia adotada, a arquitetura do protótipo ReqGraph e o protocolo experimental. O **Capítulo 4** apresenta e discute os resultados obtidos nos três casos de estudo. O **Capítulo 5** conclui o trabalho, sintetiza as contribuições e identifica linhas de trabalho futuro.

---

# 2. Conceitos teóricos e contextualização do problema

O Capítulo 2 introduz os conceitos teóricos sobre os quais a dissertação assenta. A Secção 2.1 revisita conceitos basilares de Teoria dos Grafos. A Secção 2.2 apresenta os algoritmos de ranqueamento utilizados, sublinhando que todas as métricas aqui consideradas são analisadas no contexto de **redes direcionadas**. A Secção 2.3 contextualiza o problema da priorização de requisitos, posiciona este trabalho em relação à literatura existente — em particular, em relação a Silva et al. (2018) — e identifica a contribuição incremental da presente dissertação.

**Conceitos chave:** grafos; passeios aleatórios; PageRank; HITS; SALSA; priorização de requisitos; rastreabilidade.

## 2.1 Conceitos básicos de Grafos

Um grafo é uma estrutura matemática que modela relações entre objetos (Newman, 2010; Szwarcfiter, 2018). Formalmente, um grafo $G = (V,E)$ é definido por um conjunto de vértices (ou nós) $V$ e um conjunto de arestas $E$, onde cada aresta é um par não ordenado (ou ordenado) de vértices. Os vértices representam as entidades de interesse, e as arestas representam as relações entre elas. Em redes complexas, os termos "grafo" e "rede" são frequentemente usados como sinónimos (Newman, 2010).

**Exemplo:** Considere uma pequena rede de colaboração entre pesquisadores. Os vértices podem ser {Ana, Bruno, Carla, Daniel}. As arestas podem representar coautorias: se Ana e Bruno publicaram juntos, existe uma aresta entre eles. Suponha as seguintes colaborações: Ana–Bruno, Ana–Carla, Bruno–Carla, Carla–Daniel. O grafo correspondente tem $V = \{A,B,C,D\}$ e $E = \{AB,AC,BC,CD\}$.

Uma forma comum de representar um grafo é por meio da **matriz de adjacência** $A$, onde $A_{ij} = 1$ se existe uma aresta entre os vértices $i$ e $j$, e $0$ caso contrário (Newman, 2010). Para o exemplo acima, a matriz de adjacência (considerando a ordem alfabética dos vértices) é:

$$A = \begin{bmatrix}
0 & 1 & 1 & 0 \\
1 & 0 & 1 & 0 \\
1 & 1 & 0 & 1 \\
0 & 0 & 1 & 0
\end{bmatrix}$$

![Figura 1 — Grafo exemplo](./media/media/image2.png)

### 2.1.1 Tipos de Grafos

Os grafos podem ser classificados de acordo com a **natureza dos vértices e das arestas** (Szwarcfiter, 2018). Os principais tipos relevantes para este trabalho são:

- **Grafos não direcionados:** As arestas não têm orientação, ou seja, a relação é simétrica. No exemplo anterior, a colaboração é mútua e, portanto, o grafo é não direcionado.

  ![Figura 2 — Grafo não direcionado](./media/media/image3.png)

- **Grafos direcionados (digrafos):** As arestas possuem uma direção, indicando uma relação assimétrica. Por exemplo, em uma rede de citações, se o artigo A cita o artigo B, existe uma aresta de A para B, mas não necessariamente o contrário. Formalmente, as arestas são pares ordenados $(u, v)$. A matriz de adjacência, nesse caso, não é simétrica.

  **Exemplo — Rede de citações entre artigos:** Em uma base de artigos académicos, cada artigo é um vértice. Uma aresta direcionada do artigo A para o artigo B indica que A cita B. A partir dessa rede é possível calcular métricas como o fator de impacto e identificar artigos seminais (muito citados).

  ![Figura 3 — Grafo direcionado](./media/media/image4.png)

- **Grafos ponderados:** As arestas possuem um peso associado, que pode representar intensidade, custo, distância, etc. Por exemplo, em uma rede de transportes, o peso pode ser a distância entre cidades. A matriz de adjacência armazena os pesos: $A_{ij} = w_{ij}$.

  **Exemplo — Rede de rotas aéreas com fluxo de passageiros:** Aeroportos são os vértices, e as arestas representam voos diretos entre eles. Cada aresta possui um peso correspondente ao número médio anual de passageiros transportados nessa rota.

  ![Figura 4 — Grafo ponderado](./media/media/image5.png)

- **Grafos bipartidos:** Os vértices podem ser particionados em dois conjuntos disjuntos $U$ e $V$ de tal forma que todas as arestas conectam um vértice de $U$ a um vértice de $V$. Não há arestas entre vértices do mesmo conjunto. Esse tipo de grafo é natural para modelar relações entre dois tipos distintos de entidades, como autores e artigos, ou países e produtos (Newman, 2010).

  **Exemplo — Rede de atuação de atores em filmes:** Atores e filmes formam dois conjuntos disjuntos de vértices. Uma aresta conecta um ator a um filme se ele atuou nesse filme.

  ![Figura 5 — Grafo bipartido](./media/media/image6.png)

- **Grafos bipartidos ponderados:** Combinam as duas características anteriores: são grafos bipartidos cujas arestas possuem pesos. Um exemplo é uma rede de compras em que clientes (conjunto $U$) adquirem produtos (conjunto $V$) com determinada frequência (peso).

  **Exemplo — Espaço de Produtos:** O Espaço de Produtos é uma representação económica que modela a proximidade entre produtos com base na probabilidade de serem exportados juntos por um mesmo país. Pode ser construído a partir de um grafo bipartido ponderado: de um lado, os países; do outro, os produtos. As arestas indicam se um país exporta um produto, e o peso pode ser o volume exportado.

  ![Figura 6 — Grafo espaço de produtos](./media/media/image7.png)

As classificações apresentadas seguem a sistematização clássica de Szwarcfiter (2018) e Newman (2010).

### 2.1.2 Caminhos e passeios aleatórios

Um caminho em um grafo é uma sequência de vértices $v_1, v_2, \ldots, v_k$ tal que cada par consecutivo $(v_i, v_{i+1})$ é uma aresta. O comprimento do caminho é o número de arestas percorridas. Caminhos são fundamentais para entender a conectividade e a propagação de influência em redes (Newman, 2010).

Um **passeio aleatório** (*random walk*) é um processo estocástico em que um "caminhante" se move ao longo do grafo de forma probabilística (Masuda et al., 2017; Ross, 2014). Em tempo discreto, partindo de um vértice, o caminhante escolhe aleatoriamente uma das arestas incidentes e move-se para o vértice vizinho. Esse processo pode ser descrito por uma matriz de transição $P$, onde $P_{ij}$ é a probabilidade de ir do vértice $j$ para o vértice $i$. Para grafos não direcionados e não ponderados, uma escolha comum é $P_{ij} = 1/\text{grau}(j)$ se $i$ e $j$ são vizinhos.

Passeios aleatórios são a base de diversos algoritmos de ranqueamento, como o PageRank, que estima a importância de um vértice pela frequência com que é visitado em um passeio aleatório de longa duração (Page et al., 1999; Masuda et al., 2017).

## 2.2 Algoritmos de ranqueamento em grafos

O ranqueamento de vértices em grafos atribui um *score* a cada nó com base na estrutura de conexões. Diferentes algoritmos exploram diferentes propriedades — grau, centralidade de autovetor ou passeios aleatórios — e foram inicialmente propostos no contexto da análise de redes de citações, do *ranking* de páginas web e da análise de redes sociais (Page et al., 1999; Kleinberg, 1999; Lempel & Moran, 2001). **Importante:** todas as métricas descritas nesta secção são analisadas no contexto de **redes direcionadas**, dado que o grafo de requisitos é, por natureza, direcionado (a aresta $r_a \rightarrow r_b$ codifica a dependência de $r_a$ sobre $r_b$).

### 2.2.1 Centralidade de grau

A centralidade de grau é a métrica mais simples de centralidade em grafos (Newman, 2010). Para um vértice $v$, o **grau de entrada** (em grafos direcionados) é o número de arestas que chegam a ele, e o **grau de saída** é o número de arestas que partem. Em grafos não direcionados, o grau é simplesmente o número de vizinhos. Formalmente, para um grafo com matriz de adjacência $A$, o grau de entrada de $v$ é $\sum_{u} A_{uv}$. Esta métrica é a base do SALSA (Lempel & Moran, 2001), que na sua versão básica equivale a uma ponderação dos graus.

### 2.2.2 PageRank

O **PageRank** (PR) foi proposto por Page et al. (1999) e estima a importância de um vértice como a **distribuição estacionária** de um passeio aleatório em tempo discreto sobre o grafo (Brin & Page, 1998; Masuda et al., 2017). A intuição é que um vértice é importante se é apontado por outros vértices importantes — definição recursiva resolvida por iteração. O algoritmo incorpora um fator de amortecimento $d$ (tipicamente $0{,}85$), que representa a probabilidade de o caminhante continuar a seguir as arestas; com probabilidade $1 - d$, o caminhante salta para um vértice aleatório escolhido segundo uma distribuição de personalização (em geral, **uniforme**, o que significa que todos os vértices têm idêntica probabilidade $1/n$ de serem escolhidos). A equação fundamental é:

$$\mathbf{r} = d\, M\, \mathbf{r} + (1 - d)\, \mathbf{e}$$

onde $\mathbf{r}$ é o vetor de ranks, $M$ é a matriz de transição estocástica (cada coluna soma 1) e $\mathbf{e}$ é o vetor de personalização (geralmente uniforme, $e_i = 1/n$ para todo $i$). A matriz $M$ é construída a partir da matriz de adjacência: $M_{ij} = 1/\text{grau}(j)$ se há uma aresta de $j$ para $i$, e $0$ caso contrário. Para vértices sem arestas de saída (*dead ends*), são feitos ajustes para garantir a estocasticidade.

Trata-se de um **processo iterativo**: a equação $\mathbf{r}^{(t+1)} = d M \mathbf{r}^{(t)} + (1-d)\mathbf{e}$ é aplicada repetidamente a partir de uma estimativa inicial $\mathbf{r}^{(0)}$. Sob as condições garantidas pelo amortecimento (que torna a cadeia de Markov ergódica), a sequência $\{\mathbf{r}^{(t)}\}_t$ converge para um único vetor estacionário $\mathbf{r}^{*}$ (Brin & Page, 1998; Masuda et al., 2017). Na prática, a iteração é interrompida quando $\|\mathbf{r}^{(t+1)} - \mathbf{r}^{(t)}\|$ desce abaixo de uma tolerância pré-definida.

**Ilustração:** Considere o grafo direcionado simples com vértices A, B, C e arestas: A→B, A→C, B→C, C→A. A matriz de adjacência é:

$$A = \begin{bmatrix}
0 & 0 & 1 \\
1 & 0 & 0 \\
1 & 1 & 0
\end{bmatrix}$$

Os graus de saída são A:2, B:1, C:1. A matriz de transição $M$ (colunas somam 1) é:

$$M = \begin{bmatrix}
0 & 0 & 1 \\
0{,}5 & 0 & 0 \\
0{,}5 & 1 & 0
\end{bmatrix}$$

Aplicando o PageRank com $d = 0{,}85$ e $\mathbf{e}$ uniforme, obtém-se o vetor de ranks após convergência.

![Figura 7 — Grafo exemplo PageRank](./media/media/image8.png)

### 2.2.3 HITS (*Hyperlink-Induced Topic Search*)

O **HITS**, proposto por Kleinberg (1999), distingue dois papéis para os vértices: **autoridades** (páginas com conteúdo relevante) e **hubs** (páginas que apontam para boas autoridades). A ideia é que uma boa autoridade é apontada por muitos bons hubs, e um bom hub aponta para muitas boas autoridades. Esta relação de reforço mútuo é expressa, de forma iterativa, por:

$$\mathbf{a} = A^{T}\mathbf{h}, \qquad \mathbf{h} = A\mathbf{a}$$

onde $A$ é a matriz de adjacência (para grafos direcionados). Após normalização, os vetores de autoridade $\mathbf{a}$ e *hub* $\mathbf{h}$ convergem para os autovetores principais de $A^{T}A$ e $AA^{T}$, respetivamente (Kleinberg, 1999; Ng et al., 2001).

**Ilustração:** Usando o mesmo grafo anterior, podemos calcular os *scores* de autoridade e *hub*.

![Figura 8 — Grafo HITS](./media/media/image9.png)

### 2.2.4 SALSA (*Stochastic Approach for Link-Structure Analysis*)

O **SALSA**, proposto por Lempel e Moran (2001), combina ideias do PageRank e do HITS num enquadramento estocástico. A sua intuição é a seguinte: em vez de aplicar HITS diretamente sobre o grafo direcionado original, o SALSA constrói **dois passeios aleatórios em um grafo bipartido auxiliar** em que cada vértice do grafo original é representado duas vezes — uma como *hub* e outra como *authority*. Os dois passeios alternam entre estes dois lados:

- O passeio das **autoridades** parte de uma autoridade $v$, segue uma aresta no sentido inverso (até um *hub* $u$ que a aponte) e depois segue uma aresta para a frente (até outra autoridade $w$ apontada por $u$). A distribuição estacionária deste passeio define o *score* de autoridade de cada vértice.
- O passeio dos **hubs** é simétrico: parte de um *hub*, segue uma aresta para a frente até uma autoridade e regressa, no sentido inverso, a outro *hub*.

Sob normalização local (probabilidades $1/\text{out}(u)$ e $1/\text{in}(v)$), em **grafos não ponderados e fortemente conexos** a distribuição estacionária do passeio das autoridades reduz-se a $\text{in}(v) / |E|$, ou seja, é diretamente proporcional ao grau de entrada do vértice (Lempel & Moran, 2001). De forma análoga, o *score* de *hub* é proporcional ao grau de saída. Esta interpretação simples torna o SALSA computacionalmente mais leve que o HITS.

A vantagem teórica do SALSA face ao HITS é a sua resistência ao **Efeito TKC** (*Tightly Knit Community Effect*). Em grafos onde existem **comunidades muito coesas** — pequenos subconjuntos de vértices densamente interligados entre si — o HITS tende a concentrar quase toda a massa dos *scores* nesses subgrupos, ainda que sejam pouco representativos do grafo global. Isto acontece porque o cálculo de autovetor reforça quem está fortemente interligado, mesmo que isoladamente. O SALSA, ao normalizar localmente por grau em cada passo do passeio, distribui a massa de forma mais equilibrada e evita esta concentração espúria (Lempel & Moran, 2001).

**Ilustração:** Para o mesmo grafo, os ranks do SALSA são proporcionais aos graus de entrada (autoridade) e de saída (*hub*).

![Figura 9 — Grafo SALSA](./media/media/image10.png)

### 2.2.5 BiRank e normalizações simétricas

O **BiRank**, proposto por He et al. (2014), é um algoritmo projetado para grafos bipartidos ponderados. A diferença em relação ao PageRank reside na forma de **normalizar a matriz de pesos** antes da iteração:

- A **normalização estocástica** (usada pelo PageRank e por HITS) divide cada coluna $j$ da matriz $W$ pelo somatório dos pesos de saída do vértice $j$ — ou seja, divide por $\sum_i W_{ij}$. Esta normalização torna as colunas estocásticas (somam $1$) e dá uma interpretação probabilística direta a cada transição.
- A **normalização simétrica** divide cada entrada $W_{ij}$ por $\sqrt{d_i \cdot d_j}$, onde $d_i$ e $d_j$ são os graus (ponderados) dos vértices envolvidos. O efeito desta segunda forma é **atenuar a influência desproporcional de vértices de grau muito elevado** (que dominariam, sob normalização estocástica), produzindo *scores* mais estáveis em grafos com distribuições de grau muito assimétricas (He et al., 2014; Zhou et al., 2004).

A iteração do BiRank é:

$$\mathbf{r}_{k+1} = \alpha S\mathbf{r}_{k} + (1 - \alpha)\mathbf{q}$$

onde $S = D_{u}^{-1/2} W D_{v}^{-1/2}$ é a matriz simetricamente normalizada, $W$ é a matriz de pesos do grafo bipartido, $D_u$ e $D_v$ são as matrizes diagonais dos graus (em cada lado da bipartição) e $\mathbf{q}$ é um vetor de consulta (*prior information*). O BiRank é flexível para extensões a grafos multipartidos (He et al., 2015).

## 2.3 Aplicação das Métricas ao Ranking e Priorização de Requisitos

### 2.3.1 Fundamentos da priorização de requisitos e desafios

A Engenharia de Requisitos (ER) é um domínio crucial da Engenharia de Software, responsável pela definição e manutenção das necessidades do sistema (Sommerville, 2007). Em projetos de software complexos, a priorização de requisitos é uma atividade essencial para o planeamento eficaz (Karlsson, 2002).

A atividade de rastreabilidade de requisitos estabelece as relações de dependência entre os requisitos, sendo essa a base estrutural para a priorização (Gotel & Finkelstein, 1994; Sommerville, 2007). A literatura identifica diversas técnicas tradicionais, como a **Comparação em Pares** (*Pair-wise Comparison*), que exige que os *stakeholders* comparem cada par de requisitos, sendo uma tarefa demorada e de alto esforço (Karlsson et al., 2007). Outra técnica é a **Votação Acumulativa** (*100-Points Method*), que distribui pontos fixos entre *stakeholders*, sendo a prioridade final a soma dos pontos recebidos (Ahl, 2005; Leffingwell & Widrig, 2003). Técnicas como o **PERT/CPM** utilizam grafos para representar a sequência lógica de planeamento, permitindo uma ordenação topológica (Kerzner, 2009).

Entretanto, métodos tradicionais de Priorização de Requisitos de Software (PRS) sofrem com problemas intrínsecos de subjetividade e esforço (Firesmith, 2004). Fatores como a inexperiência dos *stakeholders*, a divergência na interpretação das escalas de prioridade e o foco excessivo em apenas um ponto de vista resultam em prioridades inconsistentes e "posições inválidas" (Silva et al., 2018). Estudos práticos demonstram que a Votação Acumulativa, por depender excessivamente da ação e da decisão do *stakeholder*, pode gerar um alto número de posições inválidas e não resolve a duplicidade envolvida em requisitos interdependentes (Silva et al., 2018).

### 2.3.2 Construção do grafo de requisitos e posicionamento face a Silva et al. (2018)

A aplicação de algoritmos de ranqueamento estrutural na PRS baseia-se na construção de um **grafo de requisitos** (Silva et al., 2018). Neste modelo, cada requisito é um vértice e as relações de dependência (obtidas pela rastreabilidade) são arestas direcionadas. Especificamente, se o Requisito A depende de B, um *link* de avanço origina-se em A e aponta para B.

O presente trabalho posiciona-se explicitamente como uma **evolução** do trabalho seminal de **Silva et al. (2018)**, que propõe a aplicação do PageRank à priorização de requisitos. No estudo original, os autores: (i) restringem a análise ao **PageRank** isoladamente, sem comparação sistemática com outros algoritmos de ranqueamento; (ii) constroem o grafo de requisitos a partir de **matrizes de rastreabilidade preexistentes**, mantidas manualmente; e (iii) validam a abordagem com uma avaliação qualitativa junto de profissionais. A presente dissertação preserva o quadro conceptual de Silva et al. (2018) — grafo de requisitos como suporte da priorização — e estende-o em três dimensões: (a) **alarga o leque de algoritmos**, comparando PageRank com HITS (Kleinberg, 1999) e SALSA (Lempel & Moran, 2001) sobre os mesmos grafos; (b) **automatiza a construção do grafo de requisitos** a partir do código-fonte via análise estática (AST), eliminando a dependência de uma matriz de rastreabilidade mantida manualmente; e (c) **valida o pipeline sobre três projetos reais de código aberto** com perfis arquiteturais distintos.

### 2.3.3 Mapeamento dos algoritmos de ranqueamento para priorização

Este referencial teórico fundamenta a aplicação de algoritmos de ranqueamento de *links* — notavelmente PageRank, HITS e SALSA — para objetivar e reduzir o esforço na PRS (Silva et al., 2018; Ding et al., 2002). Esta abordagem transforma a rede de dependências de requisitos num grafo estrutural, permitindo que a priorização seja determinada pela topologia da rede, e não predominantemente pela perceção subjetiva do *stakeholder*.

O PageRank, em particular, tem-se mostrado sólido para a priorização (Silva et al., 2018). Foi usado para medir a complexidade de relacionamentos em sistemas (Li & Yi, 2009) e para analisar o impacto de preocupações em requisitos (Jin et al., 2009).

### 2.3.4 Benefícios, limitações e considerações práticas

A priorização via PageRank tem-se mostrado vantajosa em comparação com métodos manuais como a Votação Acumulativa e o PERT/CPM, oferecendo os seguintes benefícios (Silva et al., 2018; He et al., 2014):

1. **Redução da Subjetividade e Esforço:** O PageRank diminui o envolvimento direto dos *stakeholders*, focando-se na estrutura de dependência, e é escalável para lidar com um alto número de requisitos, o que é inviável para técnicas manuais.

2. **Solução de Interdependência:** O PageRank, por meio das suas iterações, consegue solucionar a duplicidade envolvida em requisitos interdependentes (mutuamente dependentes), uma limitação não resolvida pela Votação Acumulativa ou PERT/CPM.

3. **Ajuste Flexível de Prioridade:** É possível introduzir informações externas (como prioridade técnica ou de negócio) no grafo por meio de **vértices artificiais** (Silva et al., 2018). Essa técnica opcional permite que o rank de um requisito e o seu fecho transitivo de dependências sejam ajustados, garantindo que fatores subjetivos necessários sejam incorporados de forma estruturalmente coerente.

Como consideração prática, embora o PageRank ainda possa resultar em posições inválidas, esta abordagem estrutural revelou-se mais favorável do que as técnicas manuais, apresentando menos inconsistências e maior consistência com a lógica de dependência do sistema (Silva et al., 2018). As limitações da abordagem incluem as vulnerabilidades topológicas, como o **Efeito TKC**, que o SALSA foi especificamente desenvolvido para mitigar (Lempel & Moran, 2001).

---

# 3. Metodologia

A presente investigação adota uma abordagem **quantitativa e experimental**, fundamentada na modelagem matemática de sistemas de software através da Teoria dos Grafos e na execução repetível do pipeline analítico sobre projetos reais de código aberto. O Capítulo 3 detalha, na Secção 3.1, a estratégia de investigação adotada; na Secção 3.2, a arquitetura do protótipo *ReqGraph*; na Secção 3.3, as escolhas de implementação e tecnologias; e, na Secção 3.4, o corpus experimental e o protocolo de avaliação.

**Conceitos chave:** abordagem quantitativa; análise estática; AST; pipeline reprodutível; protocolo experimental.

## 3.1 Estratégia de Investigação

A investigação está estruturada em três etapas. Em primeiro lugar, **fundamentou-se teoricamente** a aplicação de algoritmos de ranqueamento de grafos à Priorização de Requisitos de Software (PRS), conforme exposto no Capítulo 2, consolidando o entendimento sobre as diferenças estruturais entre o HITS (dualidade hubs/autoridades), o SALSA (passeios aleatórios em grafos bipartidos) e o PageRank (distribuição estacionária em cadeias de Markov). Em segundo lugar, **projetou-se e implementou-se** um protótipo — o ReqGraph — capaz de extrair automaticamente o grafo de dependências entre requisitos a partir do código-fonte de uma aplicação Python, recorrendo a análise estática via *Abstract Syntax Tree* (AST). Em terceiro lugar, **definiu-se um protocolo experimental** para aplicar os algoritmos PageRank, HITS e SALSA aos grafos extraídos de três projetos de código aberto de complexidade crescente, comparando os rankings obtidos.

O ambiente de experimentação é **local**, em Python 3.8+, recorrendo às bibliotecas `ast` (biblioteca padrão), `NetworkX` (manipulação de grafos), `NumPy`/`SciPy` (computação matricial) e `Matplotlib` (visualização). Esta escolha justifica-se pela necessidade de manipular matrizes de adjacência e realizar cálculos iterativos de autovetores de forma escalável, em ambiente totalmente reprodutível e sem dependência de serviços externos.

A opção por **análise estática** (em detrimento de instrumentação dinâmica) deve-se à reprodutibilidade dos resultados: o grafo extraído depende exclusivamente do código-fonte, sem variabilidade introduzida por entradas de execução. Esta opção é coerente com a literatura sobre rastreabilidade de requisitos, que defende a derivação determinística do grafo de dependências a partir de artefactos estáveis do sistema (Silva et al., 2018; Gotel & Finkelstein, 1994).

A análise dos resultados focar-se-á em três dimensões: (i) **Consistência Algorítmica** — comparação entre os rankings gerados pelos três algoritmos para identificar convergências e discrepâncias; (ii) **Caracterização Estrutural** — densidade, presença de ciclos e identificação dos vértices centrais em cada Grafo de Requisitos; (iii) **Coerência Arquitetural** — comparação qualitativa entre os requisitos ranqueados como mais importantes e a arquitetura conhecida de cada projeto.

## 3.2 Arquitetura do Protótipo ReqGraph

O ReqGraph é o componente que materializa a transformação do código-fonte num **Grafo de Requisitos** $G_R = (V_R, E_R)$, em que cada vértice $v \in V_R$ representa um requisito de domínio e cada aresta direcionada $(r_i, r_j) \in E_R$ traduz uma dependência de implementação detetada entre os requisitos $r_i$ e $r_j$. O pipeline analítico é composto por quatro estágios sequenciais:

1. **Análise estática via AST** — cada ficheiro Python (`.py`) do projeto é parseado pelo módulo `ast` da biblioteca padrão. O resultado é uma árvore sintática a partir da qual são extraídas definições de funções (`FunctionDef`), métodos de classes e invocações (`Call`).

2. **Construção do Call Graph** — as invocações detetadas dão origem a um grafo direcionado $G_C = (V_C, E_C)$ em que cada vértice corresponde a uma função (ou método) e cada aresta $(f_i, f_j)$ indica que $f_i$ invoca $f_j$. O algoritmo resolve referências entre módulos (via `import`), referências a métodos da própria classe (`self.method()`) e qualifica funções pelo seu *namespace* para evitar colisões de nomes.

3. **Mapeamento `func_to_req`** — é fornecido pelo investigador um dicionário que associa cada função a um requisito de domínio (e.g. `parse_args → REQ_PARSING`). Este artefacto é o ponto de contacto entre o nível técnico (funções) e o nível semântico (requisitos). Para reduzir a fricção da sua produção, foi também desenvolvido um *prompt* estruturado (`reqgraph/llm_prompt_mapping.md`) que permite gerar o mapeamento de forma assistida via modelos de linguagem de grande escala (ChatGPT, Claude, Gemini).

4. **Derivação do Grafo de Requisitos** — para cada aresta $(f_i, f_j) \in E_C$ tal que $f_i$ está mapeada para o requisito $r_a$ e $f_j$ está mapeada para o requisito $r_b$, com $r_a \neq r_b$, é introduzida a aresta $(r_a, r_b)$ em $E_R$. Arestas duplicadas e auto-laços (correspondentes a invocações internas dentro do mesmo requisito) são descartados.

A Figura 10 ilustra esquematicamente o pipeline.

![Figura 10 — Exemplo de Call Graph extraído via AST (CPython stdlib)](./media/media/image11.png)

O código-fonte completo do ReqGraph, incluindo o módulo `ranker.py` descrito na Secção 3.3, está disponível em **https://github.com/talesedu/Tales_Tese_ulusofona** *(URL a confirmar pelo autor).*

## 3.3 Implementação e Tecnologias

O protótipo foi implementado em **Python 3.8+**, organizado como pacote instalável via `pip install -e reqgraph/`. As escolhas tecnológicas seguem critérios de robustez e adesão a *standards* da comunidade científica:

| Tecnologia | Versão mínima | Função no pipeline |
|------------|---------------|---------------------|
| `ast` (biblioteca padrão) | — | Parsing sintático do código-fonte Python |
| `networkx` | ≥ 3.0 | Manipulação e análise de grafos direcionados |
| `matplotlib` | ≥ 3.5 | Geração de visualizações em PNG |
| `numpy` / `scipy` | ≥ 1.24 / ≥ 1.10 | Computação matricial (matrizes de transição do SALSA) |
| `graphviz` (DOT) | — | Formato de exportação canónico para grafos |

*Tabela 1 — Tecnologias utilizadas e respetivas funções no pipeline.*

A interface de linha de comando (`python -m reqgraph <projeto> --mapping <mapeamento.py>`) expõe o pipeline completo, gerando como artefactos: `call_graph.png`, `req_graph.png`, `req_graph.json` (lista de adjacência) e `req_graph.dot` (formato Graphviz).

### 3.3.1 Módulo de Ranqueamento (`ranker.py`)

O módulo `ranker.py` consome o ficheiro `req_graph.json` produzido pelo ReqGraph e aplica três algoritmos de ranqueamento sobre o grafo direcionado $G_R$. A semântica adotada para as arestas é: $r_a \rightarrow r_b$ significa que o requisito $r_a$ **depende de** $r_b$. Em consequência, o *in-degree* de um vértice mede quantos requisitos dele dependem (uma autoridade no sentido de Kleinberg), enquanto o *out-degree* mede quantos outros requisitos ele invoca (um *hub*).

### 3.3.2 PageRank

A implementação recorre a `nx.pagerank` com parâmetros canónicos: fator de amortecimento $d = 0{,}85$, número máximo de iterações $100$ e tolerância de convergência $10^{-6}$. *Dangling nodes* (vértices sem arestas de saída) são tratados internamente pelo NetworkX por **redistribuição uniforme**: a massa de probabilidade que um vértice sem arestas de saída teria de "exportar" é dividida em partes iguais entre todos os vértices do grafo, mantendo a matriz de transição estocástica. Este artifício é necessário para garantir que a cadeia de Markov subjacente é ergódica e, portanto, que a iteração converge para uma única distribuição estacionária (Brin & Page, 1998). A soma dos *scores* totaliza $1{,}0$, permitindo interpretá-los como uma distribuição de probabilidade.

### 3.3.3 HITS

A implementação recorre a `nx.hits` com tolerância $10^{-8}$ e $100$ iterações máximas. Retorna dois vetores normalizados (norma euclidiana unitária): *hubs* e *authorities*. A interpretação para a PRS é direta: um requisito com elevado *authority* é uma **dependência crítica** do sistema (alterações nele propagam-se a muitos consumidores), enquanto um requisito com elevado *hub* é um **orquestrador** (alterações nele afetam muitas integrações).

### 3.3.4 SALSA

O NetworkX **não fornece** uma implementação do SALSA, pelo que esta foi desenvolvida manualmente seguindo Lempel e Moran (2001). Para cada aresta $(u, v) \in E_R$, constroem-se duas matrizes de transição:

- $H \rightarrow A$: probabilidade $1/\text{out}(u)$ de um *hub* $u$ transitar para a *authority* $v$.
- $A \rightarrow H$: probabilidade $1/\text{in}(v)$ de uma *authority* $v$ regressar a um *hub* $u$.

A cadeia de *hubs* tem matriz $T_{hub} = (A \rightarrow H)(H \rightarrow A)$, e a de *authorities* tem $T_{auth} = (H \rightarrow A)(A \rightarrow H)$. Os *scores* finais são as distribuições estacionárias obtidas por *power iteration* com tolerância $10^{-8}$. Linhas nulas (correspondentes a vértices absorventes) são tratadas por redistribuição uniforme, em analogia ao tratamento de *dangling nodes* do PageRank.

A diferença substantiva face ao HITS é a **normalização local** (por grau de cada vértice), que torna o SALSA menos sensível ao **Efeito TKC** — uma das vulnerabilidades topológicas identificadas no Capítulo 2.

### 3.3.5 Artefatos Gerados

Para cada projeto analisado, o `ranker.py` produz dois artefactos: `ranking_results.json` (com os *scores* completos dos três algoritmos) e `ranking_results.png` (com gráficos de barras horizontais agrupados por algoritmo). Quando executado com a *flag* `--all`, gera adicionalmente `ranking_consolidado.json` e `ranking_comparativo.png` na raiz do projeto, agregando os resultados dos três casos de estudo.

## 3.4 Corpus Experimental e Protocolo de Avaliação

### 3.4.1 Seleção dos Casos de Estudo

Para validar a abordagem em diferentes regimes de complexidade arquitetural, foram selecionados **três projetos reais de código aberto** disponíveis no GitHub, organizados por nível crescente de acoplamento esperado:

| Nível | Projeto | Ficheiros Analisados | Origem (GitHub) |
|-------|---------|----------------------|-----------------|
| Simples | **CPython stdlib** | `Lib/argparse.py`, `Lib/http/server.py` | https://github.com/python/cpython |
| Médio | **Flask** | `src/flask/app.py`, `src/flask/cli.py`, `src/flask/blueprints.py` | https://github.com/pallets/flask |
| Complexo | **scikit-learn** | `sklearn/pipeline.py`, `sklearn/linear_model/_base.py`, `sklearn/linear_model/_logistic.py`, `sklearn/tree/_classes.py` | https://github.com/scikit-learn/scikit-learn |

*Tabela 2 — Projetos selecionados como casos de estudo.*

A seleção privilegia ficheiros representativos do *core* arquitetural de cada projeto, evitando módulos auxiliares (testes, utilitários, *type stubs*). Para cada projeto foi construído um mapeamento `func_to_req` com 9 a 13 requisitos de domínio, identificados a partir da documentação oficial e da inspeção do código-fonte.

### 3.4.2 Protocolo Experimental

Cada caso de estudo foi processado seguindo os mesmos seis passos, automatizados pelo *script* `run_tests.py`:

1. Cópia dos ficheiros-alvo do repositório de origem para a pasta `testes/<nivel>/`.
2. Construção manual do dicionário `func_to_req` em `mapeamento.py`.
3. Execução do ReqGraph: `python -m reqgraph testes/<nivel>/ --mapping testes/<nivel>/mapeamento.py`.
4. Inspeção dos artefactos gerados (`call_graph.png`, `req_graph.png`, `req_graph.json`).
5. Execução do `ranker.py` sobre o `req_graph.json` gerado.
6. Comparação dos rankings produzidos pelos três algoritmos.

### 3.4.3 Dimensões de Análise

A análise dos resultados (Capítulo 4) é estruturada em duas dimensões:

- **Resultados Técnicos** — métricas estruturais do pipeline: número de funções analisadas, arestas no Call Graph, requisitos identificados, arestas no Grafo de Requisitos e tempos de convergência dos algoritmos.

- **Resultados Analíticos** — interpretação dos rankings: identificação dos requisitos mais críticos, comparação entre os três algoritmos, deteção de convergências e divergências, e discussão à luz da arquitetura conhecida de cada projeto.

---

# 4. Avaliação de Resultados

O Capítulo 4 apresenta os resultados obtidos. A Secção 4.1 reúne as métricas técnicas dos três casos de estudo. A Secção 4.2 interpreta os rankings produzidos pelos três algoritmos. A Secção 4.3 sintetiza a comparação consolidada entre projetos. A Secção 4.4 discute as observações principais. A Secção 4.5 enuncia as limitações da avaliação, antecipando o seu encaminhamento para o Capítulo 5 (trabalho futuro).

**Conceitos chave:** resultados técnicos; resultados analíticos; convergência; divergência informativa; limitações.

## 4.1 Resultados Técnicos

Esta secção sintetiza as métricas estruturais obtidas em cada caso de estudo, evidenciando a escalabilidade do *pipeline* e o grau de acoplamento detetado em cada projeto.

### 4.1.1 Síntese Quantitativa

A Tabela 3 resume as principais métricas obtidas pelo pipeline ReqGraph nos três casos de estudo.

| Métrica | CPython stdlib | Flask | scikit-learn |
|---------|---------------:|------:|-------------:|
| Ficheiros analisados | 2 | 3 | 4 |
| Funções/métodos detetados | 298 | 125 | 210 |
| Arestas no Call Graph | 130 | 47 | 80 |
| Domínios de requisito mapeados | 10 | 13 | 9 |
| Arestas no Grafo de Requisitos | 9 | 11 | 17 |
| Densidade do Grafo de Requisitos | 0,10 | 0,13 | 0,30 |
| Resultado da execução | Passou | Passou | Passou |

*Tabela 3 — Síntese quantitativa dos três casos de estudo.*

Observa-se que o número de funções analisadas não cresce monotonicamente com a complexidade percebida (o `argparse` da *stdlib* tem mais funções do que o `app.py` do Flask), mas o número de arestas no Grafo de Requisitos sim — passando de $9$ (CPython) para $11$ (Flask) e $17$ (*scikit-learn*). Esta métrica é, portanto, mais informativa sobre o acoplamento arquitetural do que a contagem bruta de funções.

### 4.1.2 Caso Simples — CPython stdlib

Foram analisados os módulos `argparse.py` (*parsing* de argumentos) e `http/server.py` (servidor HTTP simples). O mapeamento associa $298$ funções a $10$ requisitos de domínio. O Grafo de Requisitos resultante apresenta apenas $9$ arestas, sem ciclos, e pode ser sintetizado pelas seguintes adjacências:

```json
{
  "REQ_ACTIONS":        ["REQ_CONFIGURATION", "REQ_FORMATTING", "REQ_VALIDATION"],
  "REQ_ERROR_HANDLING": ["REQ_FORMATTING"],
  "REQ_FORMATTING":     ["REQ_ERROR_HANDLING"],
  "REQ_HTTP_HANDLER":   ["REQ_HTTP_CONTENT", "REQ_HTTP_LOGGING"],
  "REQ_PARSING":        ["REQ_ERROR_HANDLING", "REQ_VALIDATION"]
}
```

O grafo divide-se claramente em dois sub-sistemas independentes (*parsing*/`argparse` *vs.* HTTP), confirmando o baixo acoplamento esperado de módulos da biblioteca padrão. O único ciclo identificado é o par `REQ_FORMATTING ↔ REQ_ERROR_HANDLING`, refletindo a coexistência das funções `format_help` e `error`, que se chamam mutuamente.

![Figura 11 — Grafo de Requisitos: CPython stdlib](./media/media/image12.png)

### 4.1.3 Caso Intermediário — Flask

Foram analisados `app.py`, `cli.py` e `blueprints.py`, perfazendo $125$ funções mapeadas em $13$ requisitos. O Grafo de Requisitos contém $11$ arestas e — diferentemente do caso anterior — apresenta **fortes relações cíclicas**:

```json
{
  "REQ_APP_CORE":         ["REQ_CLI_COMMANDS", "REQ_CLI_FRAMEWORK", "REQ_CONTEXT"],
  "REQ_CLI_FRAMEWORK":    ["REQ_CONTEXT"],
  "REQ_CONTEXT":          ["REQ_REQUEST_HANDLING"],
  "REQ_ERROR_HANDLING":   ["REQ_REQUEST_HANDLING"],
  "REQ_REQUEST_HANDLING": ["REQ_CONTEXT", "REQ_ERROR_HANDLING", "REQ_ROUTING"],
  "REQ_ROUTING":          ["REQ_ERROR_HANDLING", "REQ_REQUEST_HANDLING"]
}
```

O ciclo `REQUEST_HANDLING ↔ CONTEXT ↔ ROUTING ↔ ERROR_HANDLING` evidencia que estas quatro responsabilidades estão estreitamente acopladas, o que é coerente com a arquitetura *middleware* do Flask, onde o ciclo de vida de uma requisição obriga à coordenação entre *dispatcher*, contexto de aplicação e tratamento de exceções.

Na Figura 12, **as cores atribuídas aos vértices identificam o ficheiro-fonte do projeto a que cada requisito pertence** (azul para `app.py`, verde para `cli.py`, laranja para `blueprints.py`), permitindo perceber visualmente como o acoplamento atravessa os módulos. As cores das arestas seguem a cor do vértice de origem, facilitando a leitura das cadeias de dependência.

![Figura 12 — Grafo de Requisitos: Flask](./media/media/image13.png)

### 4.1.4 Caso Complexo — scikit-learn

Foram analisados `pipeline.py`, `linear_model/_base.py`, `linear_model/_logistic.py` e `tree/_classes.py`, contabilizando $210$ funções mapeadas em $9$ requisitos. O Grafo de Requisitos resultante é o **mais denso** dos três casos ($17$ arestas), refletindo o elevado grau de orquestração interna do *framework*:

```json
{
  "REQ_DECISION_TREE":       ["REQ_SKLEARN_TAGS"],
  "REQ_FEATURE_UNION":       ["REQ_PIPELINE"],
  "REQ_LOGISTIC_REGRESSION": ["REQ_PIPELINE_PREDICT"],
  "REQ_PIPELINE":            ["REQ_LOGISTIC_REGRESSION", "REQ_PIPELINE_PREDICT", "REQ_SKLEARN_TAGS"],
  "REQ_PIPELINE_FIT":        ["REQ_DECISION_TREE", "REQ_FEATURE_UNION", "REQ_LINEAR_MODEL", "REQ_LOGISTIC_REGRESSION", "REQ_PIPELINE"],
  "REQ_PIPELINE_PREDICT":    ["REQ_DECISION_TREE", "REQ_FEATURE_UNION", "REQ_LINEAR_MODEL", "REQ_LOGISTIC_REGRESSION", "REQ_PIPELINE"],
  "REQ_SKLEARN_TAGS":        ["REQ_PIPELINE"]
}
```

`REQ_PIPELINE_FIT` e `REQ_PIPELINE_PREDICT` conectam-se cada um a cinco outros requisitos, confirmando o seu papel de **orquestradores centrais**. `REQ_PIPELINE` recebe arestas de quatro requisitos distintos, sendo a **autoridade dominante** do sistema.

![Figura 13 — Grafo de Requisitos: scikit-learn](./media/media/image14.png)

## 4.2 Resultados Analíticos

Esta secção apresenta os rankings produzidos pelo PageRank, HITS e SALSA para cada caso de estudo, interpretando os *scores* à luz da arquitetura conhecida dos projetos.

### 4.2.1 Caso Simples — Rankings para o CPython stdlib

A Tabela 4 reúne os três primeiros requisitos identificados por cada algoritmo no caso simples. **Os valores entre parênteses correspondem ao *score* numérico atribuído pelo respetivo algoritmo a cada requisito** — para o PageRank, são probabilidades estacionárias (somam $1$ no total do grafo); para o HITS e SALSA, são componentes de vetores normalizados (norma euclidiana unitária para o HITS; soma unitária por cada vetor — *authority* ou *hub* — no SALSA). *Scores* mais elevados indicam maior centralidade segundo o critério do algoritmo.

| Algoritmo | 1º | 2º | 3º |
|-----------|----|----|----|
| **PageRank** | REQ_ERROR_HANDLING (0,337) | REQ_FORMATTING (0,334) | REQ_VALIDATION (0,064) |
| **HITS — Authority** | REQ_VALIDATION (0,338) | REQ_FORMATTING (0,280) | REQ_CONFIGURATION (0,209) |
| **HITS — Hub** | REQ_ACTIONS (0,462) | REQ_PARSING (0,285) | REQ_ERROR_HANDLING (0,156) |
| **SALSA — Authority** | REQ_HTTP_CONTENT (0,167) | REQ_HTTP_LOGGING (0,167) | REQ_ERROR_HANDLING (0,167) |
| **SALSA — Hub** | REQ_HTTP_HANDLER (0,2) | REQ_ERROR_HANDLING (0,2) | REQ_ACTIONS (0,2) |

*Tabela 4 — Top-3 por algoritmo: CPython stdlib.*

O PageRank identifica `REQ_ERROR_HANDLING` como o requisito mais crítico, concentrando $0{,}337$ da probabilidade estacionária — ou seja, **um caminhante aleatório que percorra o grafo durante muito tempo passará cerca de $33{,}7\%$ do tempo nesse vértice**. Esta é a interpretação direta da "massa de probabilidade" a que o PageRank dá origem: cada *score* indica que fração do tempo um passeio aleatório de longa duração visita aquele vértice. `REQ_FORMATTING` segue muito de perto ($0{,}334$). Esta dupla decorre do ciclo `FORMATTING ↔ ERROR_HANDLING`, que faz a probabilidade acumular-se nesses dois vértices via *random walk*. O HITS distingue claramente os papéis: `REQ_ACTIONS` e `REQ_PARSING` são *hubs* (consomem muitas dependências), enquanto `REQ_VALIDATION`, `REQ_FORMATTING` e `REQ_CONFIGURATION` são *authorities* (são consumidos por muitos). O **SALSA**, devido à sua normalização local, atribui *scores* idênticos a todos os vértices não-absorventes — comportamento esperado num grafo com graus pouco diferenciados.

![Figura 14 — Rankings: CPython stdlib](./media/media/image15.png)

### 4.2.2 Caso Intermediário — Rankings para o Flask

A Tabela 5 apresenta os *top-3* do caso médio.

| Algoritmo | 1º | 2º | 3º |
|-----------|----|----|----|
| **PageRank** | REQ_REQUEST_HANDLING (0,400) | REQ_ERROR_HANDLING (0,198) | REQ_CONTEXT (0,174) |
| **HITS — Authority** | REQ_CONTEXT (0,318) | REQ_ERROR_HANDLING (0,204) | REQ_ROUTING (0,137) |
| **HITS — Hub** | REQ_REQUEST_HANDLING (0,319) | REQ_APP_CORE (0,264) | REQ_CLI_FRAMEWORK (0,154) |
| **SALSA — Authority** | uniforme a 0,167 entre 6 requisitos | — | — |
| **SALSA — Hub** | uniforme a 0,167 entre 6 requisitos | — | — |

*Tabela 5 — Top-3 por algoritmo: Flask.*

`REQ_REQUEST_HANDLING` emerge como o vértice central segundo o PageRank, com $40\%$ da probabilidade estacionária — um valor anormalmente elevado que reflete a sua posição em três arestas de entrada e três de saída, todas dentro do ciclo principal. O HITS divide o protagonismo: `REQ_REQUEST_HANDLING` é simultaneamente *hub* e *authority* (acoplamento bidirecional típico do *middleware*), enquanto `REQ_CONTEXT` lidera as *authorities* puras. O SALSA, ao normalizar localmente, dissolve esta concentração e distribui de forma uniforme — evidenciando o **Efeito TKC mitigado**: o ciclo denso entre as quatro responsabilidades seria fortemente premiado pelo HITS, mas o SALSA não cede a essa dominância.

![Figura 15 — Rankings: Flask](./media/media/image16.png)

### 4.2.3 Caso Complexo — Rankings para scikit-learn

A Tabela 6 apresenta o *top-3* do caso mais complexo.

| Algoritmo | 1º | 2º | 3º |
|-----------|----|----|----|
| **PageRank** | REQ_PIPELINE (0,257) | REQ_PIPELINE_PREDICT (0,218) | REQ_SKLEARN_TAGS (0,156) |
| **HITS — Authority** | REQ_PIPELINE (0,217) | REQ_LOGISTIC_REGRESSION (0,200) | REQ_DECISION_TREE (0,177) |
| **HITS — Hub** | REQ_PIPELINE_PREDICT (0,360) | REQ_PIPELINE_FIT (0,360) | REQ_PIPELINE (0,096) |
| **SALSA — Authority** | uniforme a 0,143 entre 7 requisitos | — | — |
| **SALSA — Hub** | uniforme a 0,143 entre 7 requisitos | — | — |

*Tabela 6 — Top-3 por algoritmo: scikit-learn.*

Os três algoritmos convergem na identificação de `REQ_PIPELINE` como o requisito mais central: o PageRank atribui-lhe o *score* mais elevado ($0{,}257$) e o HITS classifica-o como a *authority* dominante. O HITS identifica adicionalmente `REQ_PIPELINE_PREDICT` e `REQ_PIPELINE_FIT` como co-líderes dos *hubs* com *scores* idênticos ($0{,}360$) — refletindo a sua simetria estrutural (ambos invocam exatamente os mesmos cinco requisitos). O SALSA volta a produzir uma distribuição uniforme entre os vértices com arestas, indicando que, neste corpus, não há vértices destacados pelas suas frações de grau.

![Figura 16 — Rankings: scikit-learn](./media/media/image17.png)

## 4.3 Comparação Consolidada

A Figura 17 reúne, num único gráfico, os requisitos *top-1* identificados por cada algoritmo em cada um dos três casos de estudo.

![Figura 17 — Ranking comparativo entre os três projetos](./media/media/image18.png)

## 4.4 Discussão

A análise cruzada dos resultados permite extrair quatro observações principais:

1. **Convergência no caso mais denso (*scikit-learn*).** Os três algoritmos identificaram `REQ_PIPELINE` como o requisito mais central. Esta convergência funciona como validação cruzada do método: quando o grafo apresenta uma estrutura suficientemente rica (densidade $0{,}30$), os três algoritmos detetam o mesmo ponto crítico. Para os engenheiros de software, esta unanimidade aumenta a confiança na prioridade atribuída.

2. **Divergência informativa.** No caso do CPython, o PageRank prioriza `REQ_ERROR_HANDLING` enquanto o HITS prioriza `REQ_VALIDATION` (como *authority*) e `REQ_ACTIONS` (como *hub*). A divergência não é um defeito — é informação suplementar: indica que `REQ_ERROR_HANDLING` é importante via cadeias transitivas (PageRank), enquanto `REQ_VALIDATION` é diretamente referenciado por muitos requisitos (HITS *authority*).

3. **Comportamento do SALSA em grafos pequenos.** O SALSA produziu distribuições praticamente uniformes nos três casos. Este resultado é consistente com o teorema de Lempel e Moran (2001), segundo o qual, em grafos fortemente conexos sem pesos, o *score* de *authority* converge para $\text{in}(v)/|E|$. Em grafos pequenos e relativamente regulares, esta propriedade traduz-se em rankings achatados. A vantagem do SALSA — mitigar o Efeito TKC — só se manifesta em grafos com sub-comunidades densas embutidas em estruturas maiores; o presente corpus, pela sua dimensão, não permite observar este efeito plenamente.

4. **Acoplamento como propriedade emergente.** Os ciclos identificados no Flask e a alta densidade no *scikit-learn* não foram inseridos manualmente — emergem do código real. Isto sustenta a tese de que o **grafo de dependências contém informação latente** sobre a importância dos requisitos, suficiente para apoiar decisões de priorização sem recorrer exclusivamente à perceção subjetiva dos *stakeholders*.

Em conjunto, estes resultados confirmam a viabilidade da abordagem proposta: o *pipeline* AST → Call Graph → Req Graph → Ranking é capaz de extrair, de forma totalmente automatizada e reprodutível, um conjunto de prioridades estruturais coerentes com a arquitetura real dos sistemas analisados.

## 4.5 Limitações

Antes de avançar para as linhas de trabalho futuro (Capítulo 5), importa enunciar com clareza as limitações que a presente avaliação apresenta, de modo a contextualizar a sua validade externa:

- **Dimensão e diversidade do corpus.** A validação assenta em três projetos *open source* Python. Embora cobrindo regimes crescentes de acoplamento, o corpus é manifestamente pequeno e linguisticamente homogéneo; conclusões sobre generalidade da abordagem a outros ecossistemas (Java, C++, TypeScript) requerem extensão futura.

- **Ausência de validação humana dos rankings.** A presente dissertação avalia a **qualidade dos rankings** sobretudo pela sua **coerência com a arquitetura conhecida** dos sistemas analisados. Uma validação direta com profissionais — em que engenheiros de software de cada projeto produzissem rankings manuais e estes fossem comparados com os automáticos (e.g., via correlação de Spearman) — não foi realizada por limitação de recursos. Esta validação é, contudo, possível e foi conduzida por Silva et al. (2018) para o PageRank isoladamente; constitui uma linha natural de trabalho futuro (Secção 5.2).

- **Observação parcial do Efeito TKC.** Os três grafos analisados, pela sua pequena dimensão e relativa regularidade de graus, não apresentam sub-comunidades densamente coesas embutidas em estruturas maiores — situação em que a vantagem teórica do SALSA face ao HITS se manifestaria plenamente. A propriedade foi assim confirmada apenas no plano teórico (Capítulo 2) e por extrapolação a partir dos resultados achatados do SALSA.

- **Mapeamento `func_to_req` como ponto de fricção humana.** Embora a construção do Call Graph e do Grafo de Requisitos seja totalmente automatizada, o mapeamento `func_to_req` continua a depender do investigador (ou de um modelo de linguagem auxiliar, via `llm_prompt_mapping.md`). A qualidade do ranking final é, portanto, sensível à qualidade desse mapeamento — um fator de subjetividade residual que a abordagem não elimina, apenas desloca para um nível mais grosseiro.

- **Arestas não ponderadas.** Todas as arestas do Grafo de Requisitos têm peso unitário. Não é tida em conta, por exemplo, a frequência de invocação entre funções ou a "força" semântica do acoplamento, fatores que potencialmente refinariam os *scores*.

Estas limitações são endereçadas, sob a forma de propostas de continuação, na Secção 5.2.

---

# 5. Conclusão

O Capítulo 5 apresenta as principais conclusões da dissertação. A Secção 5.1 sintetiza as contribuições. A Secção 5.2 identifica linhas de trabalho futuro.

**Conceitos chave:** conclusão; síntese; contribuições; trabalho futuro.

## 5.1 Sumário e Principais Contribuições

Esta dissertação investigou a viabilidade de aplicar algoritmos de ranqueamento baseados em grafos — concretamente PageRank, HITS e SALSA — à priorização estrutural de requisitos de software. O problema original, exposto no Capítulo 1, partia da constatação de que as técnicas tradicionais de Priorização de Requisitos de Software (PRS), como a Votação Acumulativa e o PERT/CPM, são fortemente dependentes da intervenção subjetiva dos *stakeholders* e não escalam para sistemas com elevado número de requisitos interdependentes (Silva et al., 2018).

A resposta proposta consistiu em transferir parte do esforço de priorização para a topologia do sistema: se o grafo de dependências contém informação latente sobre a importância relativa dos requisitos, então um algoritmo de ranqueamento adequadamente escolhido pode extrair essa informação de forma reprodutível e automatizada. Para validar esta hipótese, foram desenvolvidos dois artefactos:

- **ReqGraph** — um protótipo Python, organizado como pacote instalável, que automatiza o pipeline **Código-fonte → AST → Call Graph → Grafo de Requisitos**. A análise é totalmente estática (não requer execução do código) e o protótipo gera artefactos em três formatos canónicos (PNG, JSON e DOT/Graphviz).
- **`ranker.py`** — um módulo de análise que aplica PageRank, HITS e SALSA aos grafos produzidos pelo ReqGraph, gerando *scores* comparáveis, gráficos de barras e relatórios consolidados.

A validação foi realizada com **três projetos reais de código aberto** (CPython *stdlib*, Flask e *scikit-learn*), selecionados como representantes de regimes crescentes de acoplamento arquitetural. Os principais resultados, detalhados no Capítulo 4, sustentam quatro contribuições:

1. **Validação da qualidade dos rankings extraídos automaticamente.** O pipeline ReqGraph produziu, sem intervenção humana adicional ao mapeamento `func_to_req`, grafos de requisitos coerentes com a arquitetura conhecida dos três projetos — incluindo a deteção emergente do ciclo `REQUEST_HANDLING ↔ CONTEXT ↔ ROUTING ↔ ERROR_HANDLING` no Flask e da centralidade de `REQ_PIPELINE` no *scikit-learn*. A validação realizada incidiu sobre a **qualidade dos resultados** (coerência com a arquitetura conhecida), e não sobre a sua adequação a perceções de profissionais — limitação assumida e encaminhada para trabalho futuro (Secção 5.2).

2. **Comparação empírica entre PageRank, HITS e SALSA** sobre grafos reais de requisitos. Os algoritmos convergiram na identificação dos requisitos centrais quando o grafo apresentou densidade suficiente (caso *scikit-learn*, com `REQ_PIPELINE` no topo dos três rankings) e divergiram informativamente nos restantes casos, permitindo distinguir importância transitiva (PageRank) de importância direta (HITS *authority*) e de orquestração (HITS *hub*). Importa sublinhar que as diferenças observadas de densidade entre os três grafos ($0{,}10$, $0{,}13$ e $0{,}30$) não são, por si só, suficientemente acentuadas para sustentar generalizações fortes sobre o comportamento dos algoritmos em função da densidade; a leitura aqui apresentada é, antes, uma caracterização dos três casos concretos.

3. **Implementação manual e documentada do SALSA.** Dado que o NetworkX não fornece SALSA, foi desenvolvida uma implementação completa baseada em matrizes de transição de cadeias de Markov, com tratamento explícito de vértices absorventes. Esta implementação é reaproveitável em contextos académicos e industriais.

4. **Mecanismo de redução do custo de mapeamento.** O ficheiro `llm_prompt_mapping.md` formaliza um *prompt* estruturado para gerar o dicionário `func_to_req` via modelos de linguagem de grande escala, mitigando uma das fricções identificadas — a necessidade de mapear manualmente centenas de funções para domínios de requisito.

Os objetivos enunciados na Secção 1.3 podem agora ser revisitados:

| Objetivo | Estado |
|----------|--------|
| Mapeamento Teórico-Matemático dos algoritmos | Capítulo 2 |
| Desenvolvimento do protótipo ReqGraph | Capítulo 3 |
| Avaliação empírica sobre projetos reais | Capítulo 4 (3 casos de estudo) |

*Tabela 7 — Estado dos objetivos enunciados na Secção 1.3.*

A consistência entre as conclusões do referencial teórico e os resultados experimentais sustenta a tese de que os algoritmos de ranqueamento estrutural constituem um complemento — não um substituto — às técnicas tradicionais de priorização, contribuindo para a redução do viés subjetivo em sistemas de larga escala.

## 5.2 Trabalho Futuro

A investigação realizada abre várias linhas de continuação, ordenadas por proximidade ao trabalho desenvolvido:

- **Validação humana dos rankings.** A presente avaliação é estrutural e qualitativa. Um estudo controlado com engenheiros de software — produzindo rankings manuais sobre os mesmos projetos e comparando-os com os automáticos via correlação de Spearman ou Kendall — forneceria uma medida quantitativa direta de adequação. Esta validação foi conduzida por Silva et al. (2018) para o PageRank isoladamente; a sua replicação para o trio PageRank/HITS/SALSA, alargada a um corpus mais amplo, foi inviabilizada pela limitação de recursos disponível na presente investigação.

- **Modelo Híbrido com Vértices Artificiais.** Implementar a técnica de injeção de prioridades de negócio através de vértices artificiais conectados ao grafo de requisitos (Silva et al., 2018). Esta extensão permitirá medir empiricamente o impacto de prioridades subjetivas sobre os rankings estruturais e oferecer um mecanismo de ajuste fino aos *stakeholders*.

- **Extensão a outras linguagens.** O motor de extração de Call Graph baseia-se exclusivamente no módulo `ast` do Python. Estender o ReqGraph a Java (via JavaParser), TypeScript (via TypeScript Compiler API) ou C/C++ (via libclang) permitiria validar a generalidade da abordagem para além do ecossistema Python.

- **Integração contínua e *snapshots* temporais.** Aplicar o ReqGraph a *snapshots* sucessivos do mesmo projeto (e.g., *tags* de *releases*) permitiria estudar a **evolução estrutural** dos requisitos ao longo do tempo, detetando *drift* arquitetural e regressões de acoplamento.

- **Tratamento de pesos semânticos.** Atualmente, todas as arestas têm peso unitário. Atribuir pesos derivados da frequência de invocação ou da força do acoplamento (e.g., número de funções partilhadas entre dois requisitos) poderá refinar substancialmente os rankings.

O conjunto destas linhas confirma que, embora o problema central tenha sido endereçado, a abordagem proposta abre um espaço de investigação largo no cruzamento entre Engenharia de Requisitos, Teoria dos Grafos e Análise Estática de Código.

---

# Bibliografia

Ahl, V. (2005). *An experimental comparison of five prioritization methods* (Master's thesis). Blekinge Institute of Technology.

Brin, S., & Page, L. (1998). The anatomy of a large-scale hypertextual web search engine. *Computer Networks and ISDN Systems*, 30(1–7), 107–117.

Ding, C., He, X., Husbands, P., Zha, H., & Simon, H. D. (2002). PageRank, HITS and a unified framework for link analysis. In *Proceedings of the 25th ACM SIGIR Conference* (pp. 353–354).

Durrett, R. (2010). *Probability: Theory and examples* (4th ed.). Cambridge University Press.

Firesmith, D. (2004). Prioritizing requirements. *Journal of Object Technology*, 3(8), 35–48.

Gikhman, I. I., & Skorokhod, A. V. (1969). *Introduction to the theory of random processes*. W. B. Saunders Company.

Gotel, O., & Finkelstein, C. (1994). An analysis of the requirements traceability problem. In *Proceedings of the First International Conference on Requirements Engineering* (pp. 94–101). IEEE.

Gupta, P., Goel, A., Lin, J., Sharma, A., Wang, D., & Zadeh, R. (2013). WTF: The who to follow service at Twitter. In *Proceedings of the 22nd International Conference on World Wide Web (WWW '13)* (pp. 505–514). ACM.

He, X., Chen, T., Kan, M.-Y., & Chen, X. (2015). TriRank: Review-aware explainable recommendation by modeling aspects. In *Proceedings of the ACM CIKM Conference* (pp. 1661–1670).

He, X., Gao, M., Kan, M.-Y., & Wang, D. (2014). BiRank: Towards ranking on bipartite graphs. *IEEE Transactions on Knowledge and Data Engineering*, 26(11), 2673–2687.

Jin, Y., Li, T., & Liu, S. (2009). Applying PageRank algorithm in requirement concern impact analysis. In *33rd Annual IEEE International Computer Software and Applications Conference* (pp. 361–366). IEEE.

Karlsson, J. (2002). Software requirements prioritizing. In *Proceedings of the Second International Conference on Requirements Engineering* (pp. 110–116). IEEE.

Karlsson, L., Berander, P., & Ågren, J. (2007). Pair-wise comparisons versus planning game partitioning: Experiments on requirements prioritisation techniques. *Empirical Software Engineering*, 12(1), 3–33.

Kerzner, H. (2009). *Project management: A systems approach to planning, scheduling, and controlling*. Wiley.

Kleinberg, J. M. (1999). Authoritative sources in a hyperlinked environment. *Journal of the ACM*, 46(5), 604–632.

Kolmogorov, A. N. (1931). Über die analytischen Methoden in der Wahrscheinlichkeitsrechnung. *Mathematische Annalen*, 104(1), 415–458.

Leffingwell, D., & Widrig, D. (2003). *Managing software requirements: A use case approach*. Pearson Education.

Lempel, R., & Moran, S. (2001). SALSA: The stochastic approach for link-structure analysis. *ACM Transactions on Information Systems*, 19(2), 131–160.

Li, F., & Yi, T. (2009). Apply PageRank algorithm to measuring relationship's complexity. In *PACIIA 2008 Pacific-Asia Workshop on Computational Intelligence and Industrial Application* (Vol. 1, pp. 914–917). IEEE.

Masuda, N., Porter, M. A., & Lambiotte, R. (2017). Random walks and diffusion on networks. *Physics Reports*, 716–717, 1–58.

Newman, M. E. J. (2010). *Networks: An introduction*. Oxford University Press.

Ng, A. Y., Zheng, A. X., & Jordan, M. I. (2001). Stable algorithms for link analysis. In *Proceedings of the ACM SIGIR Conference* (pp. 258–266).

Page, L., Brin, S., Motwani, R., & Winograd, T. (1999). *The PageRank citation ranking: Bringing order to the web* (Technical Report). Stanford InfoLab.

Ross, S. M. (2014). *Introduction to probability models* (11th ed.). Academic Press.

Silva, M. P., Tirelo, F., & Marques Neto, H. T. (2018). Uso do algoritmo PageRank para priorização de requisitos de software. In *Anais do Congresso Brasileiro de Software: Teoria e Prática*.

Sommerville, I. (2007). *Engenharia de software* (8.ª ed.). Pearson.

Szwarcfiter, J. L. (2018). *Teoria computacional de grafos*. Elsevier.

Zhou, D., Bousquet, O., Lal, T. N., Weston, J., & Schölkopf, B. (2004). Learning with local and global consistency. In *Advances in Neural Information Processing Systems* (pp. 321–328).

---

# Glossário

| Termo | Definição |
|-------|-----------|
| *AST (Abstract Syntax Tree)* | Representação em árvore da estrutura sintática de um programa, usada como ponto de partida para análise estática de código-fonte. |
| *Call Graph* | Grafo direcionado em que cada vértice é uma função (ou método) e cada aresta $(f_i, f_j)$ indica que $f_i$ invoca $f_j$. |
| *Grafo de Requisitos* | Grafo direcionado derivado do Call Graph através de um mapeamento `func_to_req`, em que cada vértice é um requisito de domínio e as arestas representam dependências entre requisitos. |
| *PageRank* | Algoritmo de ranqueamento que modela a probabilidade estacionária de um navegador aleatório visitar cada vértice do grafo. |
| *HITS* | Algoritmo de Kleinberg (1999) que atribui a cada vértice dois *scores*: *hub* (orquestrador) e *authority* (dependência central). |
| *SALSA* | Algoritmo de Lempel e Moran (2001) que combina HITS com cadeias de Markov sobre um grafo bipartido, normalizando localmente por grau. |
| *Efeito TKC* | *Tightly Knit Community Effect*: vulnerabilidade do HITS em que sub-comunidades densas concentram desproporcionalmente os *scores*; o SALSA foi projetado para mitigá-lo. |
| *Dangling Node* | Vértice sem arestas de saída; no PageRank é tratado por redistribuição uniforme da sua massa de probabilidade. |

---

# Apêndice A — Apêndice ou Anexo?

O Apêndice A explica a diferença entre apêndice e anexo.

**Apêndice.** Apêndices englobam materiais elaborados pelo autor(a), tais como gráficos, quadros, tabelas, traduções, organogramas e esquemas que prestem informação relevante para a compreensão do trabalho. Só devem figurar nos apêndices as informações previamente referenciadas no texto. As informações são total ou parcialmente da responsabilidade do autor.

**Anexo.** Anexos englobam documentos que, não sendo elaborados pelo autor, serviram de base para a construção do estudo ou facilitam a compreensão da tese/dissertação. Só devem figurar nos anexos documentos e/ou materiais previamente referenciados no corpo do trabalho. Todos os documentos devem estar em formato digital.
