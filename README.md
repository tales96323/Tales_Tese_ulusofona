# ReqGraph — Rastreabilidade Automática de Requisitos via Análise de Grafos

> 📚 **Dissertação de Mestrado** — Universidade Lusófona  
> Autor: Tales  
> Tema: Rastreabilidade automática de requisitos de software utilizando análise estática de código (AST) e algoritmos de ranqueamento de grafos (PageRank, HITS, SALSA)

---

## 📖 Descrição do Projeto

Este repositório contém o código-fonte e os artefatos da dissertação de mestrado, cujo objetivo é propor e validar uma abordagem automatizada para a **rastreabilidade de requisitos de software**.

O projeto desenvolve dois componentes principais:

### 1. `reqgraph` — Ferramenta de Rastreabilidade Automática

Biblioteca Python que realiza a **extração automática de dependências entre requisitos** a partir do código-fonte. O pipeline funciona da seguinte forma:

```
Código-fonte Python (.py)
        │
        ▼
   Análise via AST (Abstract Syntax Tree)
        │
        ▼
   Call Graph (grafo de chamadas entre funções)
        │
        ▼
   Mapeamento func_to_req (função → requisito)
        │
        ▼
   Grafo de Requisitos (dependências entre requisitos)
        │
        ▼
   Exportação: PNG · JSON · DOT (Graphviz)
```

**Funcionalidades:**
- Extração de Call Graph via análise estática (AST) — sem necessidade de executar o código
- Suporte a funções, métodos de classe, `self.method()` e imports entre módulos
- Derivação automática do Grafo de Requisitos a partir do Call Graph + mapeamento
- Geração de visualizações PNG coloridas com legenda por módulo
- Exportação em formatos JSON e DOT (Graphviz)
- Interface de linha de comando (CLI) completa
- Automação do mapeamento via prompt para LLMs (ChatGPT, Claude, Gemini)

### 2. `ranker.py` — Módulo de Ranqueamento de Requisitos

Módulo de análise que aplica **três algoritmos de ranqueamento de grafos** aos grafos de requisitos gerados pelo ReqGraph, permitindo a **priorização estrutural** dos requisitos:

| Algoritmo | Tipo de Score | Pergunta que Responde |
|-----------|--------------|----------------------|
| **PageRank** | Importância global | "Qual é o requisito mais importante do sistema?" |
| **HITS** | Hub + Authority | "Qual requisito é a dependência central?" / "Qual é o maior integrador?" |
| **SALSA** | Hub + Authority (estocástico) | "Qual requisito tem maior impacto, de forma equilibrada?" |

**Saídas geradas:**
- `ranking_results.json` — Scores completos de todos os algoritmos
- `ranking_results.png` — Gráficos de barras comparativos
- `ranking_comparativo.png` — Comparação entre projetos
- `ranking_consolidado.json` — Resultados consolidados de todos os projetos

---

## 📂 Estrutura do Projeto

```
Tales_Tese_ulusofona/
│
├── reqgraph/                           # 📦 Biblioteca principal (pacote Python)
│   ├── __init__.py                     #     Exports do pacote
│   ├── __main__.py                     #     Entry point: python -m reqgraph
│   ├── cli.py                          #     Interface de linha de comando
│   ├── call_graph.py                   #     Extração de Call Graph via AST
│   ├── req_graph.py                    #     Derivação do Grafo de Requisitos
│   ├── visualize.py                    #     Geração de visualizações PNG
│   ├── setup.py                        #     Configuração de instalação pip
│   ├── requirements.txt                #     Dependências do pacote
│   ├── llm_prompt_mapping.md           #     Prompt para geração automática de mapeamento via LLM
│   └── README.md                       #     Documentação detalhada do pacote
│
├── ranker.py                           # 📊 Módulo de ranqueamento (PageRank, HITS, SALSA)
├── run_ranking.py                      # 🏃 Script auxiliar para executar rankings
├── run_tests.py                        # 🧪 Script de testes automatizados
├── run_tests.bat                       # 🪟 Wrapper Windows para testes
│
├── testes/                             # 📁 Projetos de teste (código real do GitHub)
│   ├── simples_stdlib/                 #     🟢 CPython stdlib (argparse + http.server)
│   │   ├── argparse.py                 #         Fonte: python/cpython → Lib/argparse.py
│   │   ├── server.py                   #         Fonte: python/cpython → Lib/http/server.py
│   │   └── mapeamento.py              #         10 domínios de requisito
│   ├── medio_flask/                    #     🟡 Flask (app + cli + blueprints)
│   │   ├── app.py                      #         Fonte: pallets/flask → src/flask/app.py
│   │   ├── cli.py                      #         Fonte: pallets/flask → src/flask/cli.py
│   │   ├── blueprints.py              #         Fonte: pallets/flask → src/flask/blueprints.py
│   │   └── mapeamento.py              #         13 domínios de requisito
│   └── complexo_sklearn/               #     🔴 scikit-learn (pipeline + modelos)
│       ├── pipeline.py                 #         Fonte: scikit-learn → sklearn/pipeline.py
│       ├── _base.py                    #         Fonte: scikit-learn → sklearn/linear_model/_base.py
│       ├── _logistic.py               #         Fonte: scikit-learn → sklearn/linear_model/_logistic.py
│       ├── _classes.py                #         Fonte: scikit-learn → sklearn/tree/_classes.py
│       └── mapeamento.py              #         9 domínios de requisito
│
├── explicacao_algoritmos.md            # 📖 Documentação técnica dos algoritmos de ranqueamento
├── RESULTADOS_TESTES.md                # 📋 Relatório detalhado dos resultados dos testes
├── ranking_comparativo.png             # 📊 Gráfico comparativo entre projetos
├── ranking_consolidado.json            # 📄 Resultados consolidados (JSON)
├── requirements.txt                    # 📦 Dependências do projeto raiz
├── .gitignore                          # 🚫 Regras de exclusão do Git
└── README.md                           # 📖 Este ficheiro
```

---

## ⚙️ Instalação

### Pré-requisitos

- **Python 3.8+**
- **pip** (gerenciador de pacotes)

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/Tales_Tese_ulusofona.git
cd Tales_Tese_ulusofona
```

### 2. Criar e ativar ambiente virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
# Instalar dependências do ranking (raiz)
pip install -r requirements.txt

# Instalar o pacote reqgraph em modo editável
pip install -e reqgraph/
```

**Dependências principais:**
| Pacote | Versão | Uso |
|--------|--------|-----|
| `networkx` | ≥ 3.0.0 | Manipulação e análise de grafos |
| `matplotlib` | ≥ 3.5.0 | Geração de visualizações PNG |
| `numpy` | ≥ 1.24.0 | Computação numérica (matrizes SALSA) |
| `scipy` | ≥ 1.10.0 | Estruturas de dados esparsas |

---

## 🚀 Como Usar

### Análise de Requisitos com `reqgraph`

#### Passo 1 — Criar o mapeamento `func_to_req`

Crie um arquivo `mapeamento.py` no seu projeto com o dicionário de mapeamento:

```python
func_to_req = {
    "login":        "REQ_AUTENTICACAO",
    "query_user":   "REQ_BANCO_DE_DADOS",
    "checkout":     "REQ_PAGAMENTOS",
    "send_email":   "REQ_NOTIFICACOES",
}
```

> 💡 **Dica:** Use o prompt em [`reqgraph/llm_prompt_mapping.md`](reqgraph/llm_prompt_mapping.md) para gerar o mapeamento automaticamente com ChatGPT, Claude ou Gemini.

#### Passo 2 — Executar a análise

```bash
# Via módulo Python
python -m reqgraph <caminho_do_projeto> --mapping <caminho_do_mapeamento.py>

# Exemplo concreto
python -m reqgraph testes/simples_stdlib/ --mapping testes/simples_stdlib/mapeamento.py
```

#### Artefatos gerados

| Arquivo | Descrição |
|---------|-----------|
| `call_graph.png` | Visualização do grafo de chamadas (funções coloridas por módulo) |
| `req_graph.png` | Visualização do grafo de requisitos derivado |
| `req_graph.json` | Grafo de requisitos em formato JSON (lista de adjacência) |
| `req_graph.dot` | Grafo de requisitos em formato Graphviz DOT |

---

### Ranqueamento de Requisitos com `ranker.py`

#### Analisar um projeto específico

```bash
python ranker.py testes/simples_stdlib/req_graph.json
```

#### Analisar todos os projetos de teste

```bash
python ranker.py --all
# ou
python run_ranking.py
```

#### Analisar por nível

```bash
python run_ranking.py simples      # 🟢 CPython stdlib
python run_ranking.py medio        # 🟡 Flask
python run_ranking.py complexo     # 🔴 scikit-learn
```

---

### Executar Suite Completa de Testes

```bash
# Todos os níveis
python run_tests.py

# Nível específico
python run_tests.py simples
python run_tests.py medio
python run_tests.py complexo

# Windows (via batch)
run_tests.bat
```

---

## 🧪 Validação — Projetos de Teste

A ferramenta foi validada com **3 projetos reais de código aberto do GitHub**, organizados por nível de complexidade crescente:

| Nível | Projeto | Arquivos | Funções | Arestas (Call) | Requisitos | Arestas (Req) |
|-------|---------|----------|---------|---------------|------------|---------------|
| 🟢 Simples | CPython stdlib | 2 | 298 | 130 | 10 | 9 |
| 🟡 Médio | Flask | 3 | 125 | 47 | 13 | 11 |
| 🔴 Complexo | scikit-learn | 4 | 210 | 80 | 9 | 17 |

**Resultados detalhados:** Ver [`RESULTADOS_TESTES.md`](RESULTADOS_TESTES.md)  
**Explicação dos algoritmos:** Ver [`explicacao_algoritmos.md`](explicacao_algoritmos.md)

---

## 📊 Algoritmos de Ranqueamento

### PageRank (Brin & Page, 1998)

Modela a probabilidade de um "navegador aleatório" visitar cada nó do grafo. Requisitos com **alto PageRank** são dependências fundamentais do sistema — alterações neles têm impacto sistémico.

$$PR(v) = \frac{1 - d}{N} + d \sum_{u \in B(v)} \frac{PR(u)}{L(u)}$$

### HITS (Kleinberg, 1999)

Identifica dois papéis: **Authorities** (requisitos que são dependência de muitos) e **Hubs** (requisitos que orquestram muitos outros). Revela a dualidade producer/consumer nos requisitos.

### SALSA (Lempel & Moran, 2001)

Combina a separação hub/authority do HITS com cadeias de Markov. Normaliza localmente (por grau de nó), evitando que clusters densos dominem o ranking — produz resultados mais equilibrados.

> 📖 **Documentação matemática completa:** [`explicacao_algoritmos.md`](explicacao_algoritmos.md)

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** — Linguagem principal
- **AST (Abstract Syntax Tree)** — Análise estática de código-fonte
- **NetworkX** — Manipulação e análise de grafos
- **Matplotlib** — Visualização e geração de gráficos
- **NumPy / SciPy** — Computação numérica (implementação SALSA)

---

## 📄 Licença

Este projeto foi desenvolvido como parte de uma dissertação de mestrado na **Universidade Lusófona**. Para uso acadêmico.

---

## 📞 Contacto

Para questões sobre o projeto ou a dissertação, entre em contacto com o autor.
