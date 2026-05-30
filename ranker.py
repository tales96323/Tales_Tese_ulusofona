"""
ranker.py — Ranqueamento de Requisitos com PageRank, HITS e SALSA.

Carrega grafos de requisitos gerados pelo ReqGraph (JSON ou DOT)
e calcula scores de ranqueamento para cada nó (requisito) utilizando
três algoritmos clássicos de análise de grafos.

Uso:
    python ranker.py testes/simples_stdlib/req_graph.json
    python ranker.py testes/medio_flask/req_graph.dot --format dot
    python ranker.py --all
"""

import argparse
import json
import os
import sys
from collections import defaultdict

import networkx as nx
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Backend não-interativo para geração de PNG
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


# ══════════════════════════════════════════════════════════════════════════════
# 1. CARREGAMENTO DO GRAFO
# ══════════════════════════════════════════════════════════════════════════════

def load_graph_from_json(filepath):
    """
    Carrega um grafo direcionado a partir de um ficheiro JSON
    no formato de lista de adjacência do ReqGraph.

    Formato esperado:
      {"REQ_A": ["REQ_B", "REQ_C"], "REQ_D": ["REQ_A"], ...}

    Retorna um nx.DiGraph com todos os nós (incluindo nós-folha
    que só aparecem como destinos).
    """
    with open(filepath, "r", encoding="utf-8") as f:
        adj = json.load(f)

    G = nx.DiGraph()

    # Adicionar todas as arestas
    for source, targets in adj.items():
        for target in targets:
            G.add_edge(source, target)

    # Garantir que nós sem arestas de saída também estejam presentes
    all_nodes = set(adj.keys())
    for targets in adj.values():
        all_nodes.update(targets)
    for node in all_nodes:
        if node not in G:
            G.add_node(node)

    return G


def load_graph_from_dot(filepath):
    """
    Carrega um grafo direcionado a partir de um ficheiro DOT (Graphviz).
    Requer pydot instalado.
    """
    try:
        G = nx.drawing.nx_pydot.read_dot(filepath)
    except Exception as e:
        print(f"  [ERRO] Falha ao ler DOT: {e}")
        print("  Dica: instale pydot com 'pip install pydot'")
        sys.exit(1)

    # read_dot pode retornar MultiDiGraph; converter para DiGraph
    if isinstance(G, nx.MultiDiGraph):
        G = nx.DiGraph(G)

    # Limpar nomes de nós (remover aspas que o DOT adiciona)
    mapping = {}
    for node in G.nodes():
        clean = str(node).strip('"').strip("'")
        if clean != node:
            mapping[node] = clean
    if mapping:
        G = nx.relabel_nodes(G, mapping)

    return G


def load_graph(filepath, fmt="auto"):
    """Carrega o grafo detectando o formato automaticamente."""
    if fmt == "auto":
        ext = os.path.splitext(filepath)[1].lower()
        fmt = "dot" if ext == ".dot" else "json"

    if fmt == "json":
        return load_graph_from_json(filepath)
    else:
        return load_graph_from_dot(filepath)


# ══════════════════════════════════════════════════════════════════════════════
# 2. ALGORITMOS DE RANQUEAMENTO
# ══════════════════════════════════════════════════════════════════════════════

def compute_pagerank(G, alpha=0.85, max_iter=100, tol=1e-06):
    """
    Calcula o PageRank de cada nó no grafo direcionado G.

    Fórmula:
        PR(v) = (1 - d) / N + d * Σ PR(u) / L(u)
                                   u ∈ B(v)

    onde:
      - d = alpha (fator de amortecimento, padrão 0.85)
      - N = número total de nós
      - B(v) = conjunto de nós que apontam para v
      - L(u) = número de arestas de saída de u

    Parâmetros
    ----------
    G : nx.DiGraph
    alpha : float — fator de amortecimento (probabilidade de seguir um link)
    max_iter : int — número máximo de iterações
    tol : float — tolerância de convergência

    Retorna
    -------
    dict[str, float] — scores de PageRank por nó
    """
    scores = nx.pagerank(G, alpha=alpha, max_iter=max_iter, tol=tol)
    return scores


def compute_hits(G, max_iter=100, tol=1e-08):
    """
    Calcula os scores HITS (Hyperlink-Induced Topic Search) de Kleinberg.

    O algoritmo identifica dois tipos de importância:
      - Authority: nós que são apontados por muitos hubs bons
      - Hub: nós que apontam para muitas authorities boas

    Atualização iterativa:
      a(v) = Σ h(u)    para todo u → v
      h(v) = Σ a(w)    para todo v → w

    Parâmetros
    ----------
    G : nx.DiGraph
    max_iter : int
    tol : float

    Retorna
    -------
    tuple[dict, dict] — (hubs, authorities)
    """
    hubs, authorities = nx.hits(G, max_iter=max_iter, tol=tol)
    return hubs, authorities


def compute_salsa(G):
    """
    Calcula os scores SALSA (Stochastic Approach for Link-Structure Analysis).

    O SALSA combina ideias do PageRank (abordagem probabilística via
    cadeias de Markov) com o HITS (separação hub/authority).

    Algoritmo:
    1. Constrói um grafo bipartido com nós-hub (v_h) e nós-authority (v_a)
    2. Para cada aresta (u, v) no grafo original:
       - u_h → v_a  com peso 1/out_degree(u)  (passeio do hub para authority)
       - v_a → u_h  com peso 1/in_degree(v)   (passeio da authority para hub)
    3. O passeio aleatório hub→auth→hub→... define duas cadeias de Markov:
       - Cadeia de hubs: transição u_h → w_h (via v_a intermediário)
       - Cadeia de authorities: transição v_a → x_a (via u_h intermediário)
    4. A distribuição estacionária de cada cadeia dá os scores finais.

    Resultado teórico (componente fortemente conexa):
      - hub_score(v) = out_degree(v) / total_edges
      - auth_score(v) = in_degree(v) / total_edges

    Para grafos genéricos, computamos via composição de matrizes de transição.

    Parâmetros
    ----------
    G : nx.DiGraph

    Retorna
    -------
    tuple[dict, dict] — (hub_scores, authority_scores)
    """
    nodes = sorted(G.nodes())
    n = len(nodes)

    if n == 0:
        return {}, {}

    node_to_idx = {node: i for i, node in enumerate(nodes)}
    total_edges = G.number_of_edges()

    if total_edges == 0:
        uniform = 1.0 / n
        scores = {node: uniform for node in nodes}
        return scores, scores

    # ── Calcular graus ─────────────────────────────────────────────────────
    out_deg = dict(G.out_degree())
    in_deg = dict(G.in_degree())

    # ── Construir matrizes de transição do grafo bipartido ─────────────────
    # Matriz H→A: transição de hub u para authority v
    # H_to_A[v][u] = 1/out_deg(u) se aresta (u, v) existe
    H_to_A = np.zeros((n, n))
    for u, v in G.edges():
        i_u = node_to_idx[u]
        i_v = node_to_idx[v]
        if out_deg[u] > 0:
            H_to_A[i_v][i_u] = 1.0 / out_deg[u]

    # Matriz A→H: transição de authority v para hub u
    # A_to_H[u][v] = 1/in_deg(v) se aresta (u, v) existe
    A_to_H = np.zeros((n, n))
    for u, v in G.edges():
        i_u = node_to_idx[u]
        i_v = node_to_idx[v]
        if in_deg[v] > 0:
            A_to_H[i_u][i_v] = 1.0 / in_deg[v]

    # ── Cadeia de Markov para hubs: H → A → H ─────────────────────────────
    # Matriz de transição: T_hub = A_to_H @ H_to_A  (hub → auth → hub)
    T_hub = A_to_H @ H_to_A

    # ── Cadeia de Markov para authorities: A → H → A ──────────────────────
    # Matriz de transição: T_auth = H_to_A @ A_to_H (auth → hub → auth)
    T_auth = H_to_A @ A_to_H

    # ── Distribuição estacionária via power iteration ──────────────────────
    hub_scores_vec = _stationary_distribution(T_hub, n)
    auth_scores_vec = _stationary_distribution(T_auth, n)

    hub_scores = {nodes[i]: float(hub_scores_vec[i]) for i in range(n)}
    auth_scores = {nodes[i]: float(auth_scores_vec[i]) for i in range(n)}

    return hub_scores, auth_scores


def _stationary_distribution(T, n, max_iter=200, tol=1e-08):
    """
    Calcula a distribuição estacionária de uma matriz de transição T
    via power iteration.

    Trata nós absorventes (linhas nulas) redistribuindo uniformemente
    (equivalente ao tratamento de dangling nodes no PageRank).
    """
    # Tratar linhas nulas (nós sem transição) → redistribuição uniforme
    row_sums = T.sum(axis=1)
    dangling = row_sums == 0
    if np.any(dangling):
        T = T.copy()
        T[dangling] = 1.0 / n

    # Iniciar com distribuição uniforme
    pi = np.ones(n) / n

    for _ in range(max_iter):
        pi_new = T.T @ pi
        # Normalizar para evitar drift numérico
        total = pi_new.sum()
        if total > 0:
            pi_new /= total
        else:
            pi_new = np.ones(n) / n

        if np.linalg.norm(pi_new - pi, 1) < tol:
            break
        pi = pi_new

    return pi_new


# ══════════════════════════════════════════════════════════════════════════════
# 3. FORMATAÇÃO E EXPORTAÇÃO
# ══════════════════════════════════════════════════════════════════════════════

def scores_to_ranked_list(scores):
    """Converte dict de scores para lista ordenada por score decrescente."""
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [
        {"rank": i + 1, "node": node, "score": round(score, 6)}
        for i, (node, score) in enumerate(ranked)
    ]


def build_results(G, project_name, graph_file):
    """Executa os 3 algoritmos e compila os resultados num dicionário."""

    print(f"\n{'='*64}")
    print(f"  RANQUEAMENTO DE REQUISITOS — {project_name.upper()}")
    print(f"{'='*64}")
    print(f"  Grafo: {graph_file}")
    print(f"  Nós: {G.number_of_nodes()}  |  Arestas: {G.number_of_edges()}")
    print(f"{'='*64}")

    # ── PageRank ───────────────────────────────────────────────────────────
    pr_scores = compute_pagerank(G)
    pr_ranked = scores_to_ranked_list(pr_scores)

    print(f"\n  📊 PageRank (d=0.85)")
    print(f"  {'Rank':<6} {'Requisito':<35} {'Score':<10}")
    print(f"  {'-'*6} {'-'*35} {'-'*10}")
    for item in pr_ranked:
        print(f"  {item['rank']:<6} {item['node']:<35} {item['score']:<10.6f}")

    # Validação: soma dos scores ≈ 1.0
    pr_sum = sum(pr_scores.values())
    print(f"  Soma dos scores: {pr_sum:.6f} (esperado ≈ 1.0)")

    # ── HITS ───────────────────────────────────────────────────────────────
    hits_hubs, hits_auths = compute_hits(G)
    hits_hubs_ranked = scores_to_ranked_list(hits_hubs)
    hits_auths_ranked = scores_to_ranked_list(hits_auths)

    print(f"\n  📊 HITS — Hubs")
    print(f"  {'Rank':<6} {'Requisito':<35} {'Score':<10}")
    print(f"  {'-'*6} {'-'*35} {'-'*10}")
    for item in hits_hubs_ranked:
        print(f"  {item['rank']:<6} {item['node']:<35} {item['score']:<10.6f}")

    print(f"\n  📊 HITS — Authorities")
    print(f"  {'Rank':<6} {'Requisito':<35} {'Score':<10}")
    print(f"  {'-'*6} {'-'*35} {'-'*10}")
    for item in hits_auths_ranked:
        print(f"  {item['rank']:<6} {item['node']:<35} {item['score']:<10.6f}")

    # ── SALSA ──────────────────────────────────────────────────────────────
    salsa_hubs, salsa_auths = compute_salsa(G)
    salsa_hubs_ranked = scores_to_ranked_list(salsa_hubs)
    salsa_auths_ranked = scores_to_ranked_list(salsa_auths)

    print(f"\n  📊 SALSA — Hubs")
    print(f"  {'Rank':<6} {'Requisito':<35} {'Score':<10}")
    print(f"  {'-'*6} {'-'*35} {'-'*10}")
    for item in salsa_hubs_ranked:
        print(f"  {item['rank']:<6} {item['node']:<35} {item['score']:<10.6f}")

    print(f"\n  📊 SALSA — Authorities")
    print(f"  {'Rank':<6} {'Requisito':<35} {'Score':<10}")
    print(f"  {'-'*6} {'-'*35} {'-'*10}")
    for item in salsa_auths_ranked:
        print(f"  {item['rank']:<6} {item['node']:<35} {item['score']:<10.6f}")

    print(f"\n{'='*64}\n")

    # ── Compilar resultado ─────────────────────────────────────────────────
    results = {
        "project": project_name,
        "graph_file": os.path.basename(graph_file),
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "nodes": sorted(G.nodes()),
        "algorithms": {
            "pagerank": {
                "description": "Fator de amortecimento d=0.85, convergência=1e-06",
                "scores": pr_ranked,
            },
            "hits": {
                "description": "HITS de Kleinberg — separação hub/authority",
                "hubs": hits_hubs_ranked,
                "authorities": hits_auths_ranked,
            },
            "salsa": {
                "description": "SALSA — cadeia de Markov sobre grafo bipartido hub/authority",
                "hubs": salsa_hubs_ranked,
                "authorities": salsa_auths_ranked,
            },
        },
    }

    return results


def export_results_json(results, output_path):
    """Exporta os resultados em formato JSON."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"  [OK] Resultados exportados: {output_path}")


# ══════════════════════════════════════════════════════════════════════════════
# 4. VISUALIZAÇÕES PNG
# ══════════════════════════════════════════════════════════════════════════════

# Paleta de cores inspirada em design moderno
COLORS = {
    "pagerank": "#6366F1",       # Indigo vibrante
    "hits_hub": "#F59E0B",       # Âmbar
    "hits_auth": "#10B981",      # Esmeralda
    "salsa_hub": "#EF4444",      # Vermelho
    "salsa_auth": "#3B82F6",     # Azul
    "bg": "#0F172A",             # Slate escuro
    "card": "#1E293B",           # Slate card
    "text": "#F8FAFC",           # Texto claro
    "grid": "#334155",           # Grid sutil
    "subtext": "#94A3B8",        # Texto secundário
}


def generate_ranking_chart(results, output_path):
    """
    Gera um gráfico de barras horizontais com os rankings dos 3 algoritmos.
    Produz um ficheiro PNG de alta resolução.
    """
    project = results["project"]
    pr = results["algorithms"]["pagerank"]["scores"]
    hits_h = results["algorithms"]["hits"]["hubs"]
    hits_a = results["algorithms"]["hits"]["authorities"]
    salsa_h = results["algorithms"]["salsa"]["hubs"]
    salsa_a = results["algorithms"]["salsa"]["authorities"]

    fig, axes = plt.subplots(2, 3, figsize=(22, 12))
    fig.patch.set_facecolor(COLORS["bg"])

    fig.suptitle(
        f"Ranqueamento de Requisitos — {project}",
        fontsize=20,
        fontweight="bold",
        color=COLORS["text"],
        y=0.97,
    )

    datasets = [
        (axes[0, 0], pr, "PageRank (d=0.85)", COLORS["pagerank"], "score"),
        (axes[0, 1], hits_h, "HITS — Hubs", COLORS["hits_hub"], "score"),
        (axes[0, 2], hits_a, "HITS — Authorities", COLORS["hits_auth"], "score"),
        (axes[1, 0], salsa_h, "SALSA — Hubs", COLORS["salsa_hub"], "score"),
        (axes[1, 1], salsa_a, "SALSA — Authorities", COLORS["salsa_auth"], "score"),
    ]

    for ax, data, title, color, key in datasets:
        ax.set_facecolor(COLORS["card"])

        nodes = [item["node"].replace("REQ_", "") for item in reversed(data)]
        scores = [item[key] for item in reversed(data)]

        bars = ax.barh(nodes, scores, color=color, alpha=0.85, height=0.6,
                       edgecolor=color, linewidth=0.5)

        # Adicionar valores nas barras
        max_score = max(scores) if scores else 1
        for bar, score in zip(bars, scores):
            x_pos = bar.get_width() + max_score * 0.02
            ax.text(
                x_pos, bar.get_y() + bar.get_height() / 2,
                f"{score:.4f}",
                va="center", ha="left",
                fontsize=8, color=COLORS["subtext"],
                fontweight="medium",
            )

        ax.set_title(title, fontsize=13, fontweight="bold", color=color, pad=10)
        ax.tick_params(colors=COLORS["text"], labelsize=9)
        ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.3f"))
        ax.set_xlim(0, max_score * 1.25 if max_score > 0 else 1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color(COLORS["grid"])
        ax.spines["left"].set_color(COLORS["grid"])
        ax.xaxis.label.set_color(COLORS["subtext"])
        ax.grid(axis="x", color=COLORS["grid"], alpha=0.3, linestyle="--")

    # Esconder o sexto subplot (2,3 grid com 5 gráficos)
    axes[1, 2].set_visible(False)

    # Adicionar legenda/nota no espaço vazio
    info_ax = fig.add_axes([0.68, 0.05, 0.28, 0.38])
    info_ax.set_facecolor(COLORS["card"])
    info_ax.set_xlim(0, 1)
    info_ax.set_ylim(0, 1)
    info_ax.axis("off")

    info_text = (
        f"Resumo — {project}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Nós: {results['num_nodes']}\n"
        f"Arestas: {results['num_edges']}\n\n"
        f"Top PageRank:\n  {pr[0]['node']} ({pr[0]['score']:.4f})\n\n"
        f"Top HITS Authority:\n  {hits_a[0]['node']} ({hits_a[0]['score']:.4f})\n\n"
        f"Top SALSA Authority:\n  {salsa_a[0]['node']} ({salsa_a[0]['score']:.4f})"
    )
    info_ax.text(
        0.08, 0.92, info_text,
        transform=info_ax.transAxes,
        fontsize=11, color=COLORS["text"],
        verticalalignment="top",
        fontfamily="monospace",
        linespacing=1.5,
        bbox=dict(boxstyle="round,pad=0.5", facecolor=COLORS["bg"], alpha=0.7,
                  edgecolor=COLORS["grid"]),
    )

    plt.tight_layout(rect=[0, 0.03, 1, 0.94])
    fig.savefig(output_path, dpi=150, facecolor=fig.get_facecolor(),
                bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print(f"  [OK] Visualização exportada: {output_path}")


def generate_comparison_chart(all_results, output_path):
    """
    Gera um gráfico comparativo entre os 3 projetos,
    mostrando o top-1 de cada algoritmo lado a lado.
    """
    if len(all_results) < 2:
        return

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.patch.set_facecolor(COLORS["bg"])

    fig.suptitle(
        "Comparação entre Projetos — Top Requisitos por Algoritmo",
        fontsize=18, fontweight="bold", color=COLORS["text"], y=0.97,
    )

    algo_configs = [
        ("PageRank", "pagerank", "scores", COLORS["pagerank"]),
        ("HITS Auth.", "hits", "authorities", COLORS["hits_auth"]),
        ("SALSA Auth.", "salsa", "authorities", COLORS["salsa_auth"]),
    ]

    for ax, (algo_label, algo_key, sub_key, color) in zip(axes, algo_configs):
        ax.set_facecolor(COLORS["card"])

        projects = []
        top_nodes = []
        top_scores = []

        for res in all_results:
            data = res["algorithms"][algo_key]
            items = data[sub_key] if sub_key != "scores" else data["scores"]
            if items:
                projects.append(res["project"].replace("_", "\n"))
                top_nodes.append(items[0]["node"].replace("REQ_", ""))
                top_scores.append(items[0]["score"])

        bars = ax.bar(projects, top_scores, color=color, alpha=0.85, width=0.5,
                      edgecolor=color, linewidth=0.5)

        for bar, node, score in zip(bars, top_nodes, top_scores):
            ax.text(
                bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                f"{node}\n({score:.4f})",
                ha="center", va="bottom",
                fontsize=9, color=COLORS["text"],
                fontweight="bold",
            )

        ax.set_title(algo_label, fontsize=14, fontweight="bold", color=color, pad=12)
        ax.tick_params(colors=COLORS["text"], labelsize=10)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color(COLORS["grid"])
        ax.spines["left"].set_color(COLORS["grid"])
        ax.grid(axis="y", color=COLORS["grid"], alpha=0.3, linestyle="--")
        ax.set_ylabel("Score", color=COLORS["subtext"], fontsize=11)

    plt.tight_layout(rect=[0, 0.03, 1, 0.92])
    fig.savefig(output_path, dpi=150, facecolor=fig.get_facecolor(),
                bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print(f"  [OK] Comparação exportada: {output_path}")


# ══════════════════════════════════════════════════════════════════════════════
# 5. CLI
# ══════════════════════════════════════════════════════════════════════════════

# Projetos de teste conhecidos
TEST_PROJECTS = [
    {
        "name": "simples_stdlib",
        "graph": "testes/simples_stdlib/req_graph.json",
        "label": "🟢 Simples — CPython stdlib",
    },
    {
        "name": "medio_flask",
        "graph": "testes/medio_flask/req_graph.json",
        "label": "🟡 Médio — Flask",
    },
    {
        "name": "complexo_sklearn",
        "graph": "testes/complexo_sklearn/req_graph.json",
        "label": "🔴 Complexo — scikit-learn",
    },
]


def process_single(filepath, fmt="auto", output_dir=None):
    """Processa um único ficheiro de grafo."""
    if not os.path.exists(filepath):
        print(f"  [ERRO] Ficheiro não encontrado: {filepath}")
        return None

    # Determinar nome do projeto
    parent_dir = os.path.basename(os.path.dirname(os.path.abspath(filepath)))
    project_name = parent_dir if parent_dir != "." else "projeto"

    # Carregar grafo
    G = load_graph(filepath, fmt)
    print(f"  [OK] Grafo carregado: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")

    # Executar ranking
    results = build_results(G, project_name, filepath)

    # Determinar diretório de saída
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(filepath))

    # Exportar JSON
    json_path = os.path.join(output_dir, "ranking_results.json")
    export_results_json(results, json_path)

    # Gerar visualização PNG
    png_path = os.path.join(output_dir, "ranking_results.png")
    generate_ranking_chart(results, png_path)

    return results


def process_all(base_dir="."):
    """Processa todos os projetos de teste."""
    print("\n" + "█" * 64)
    print("  ANÁLISE DE RANQUEAMENTO — TODOS OS PROJETOS")
    print("█" * 64)

    all_results = []

    for project in TEST_PROJECTS:
        graph_path = os.path.join(base_dir, project["graph"])
        print(f"\n  ▶ {project['label']}")

        if not os.path.exists(graph_path):
            print(f"    [SKIP] Ficheiro não encontrado: {graph_path}")
            continue

        result = process_single(graph_path)
        if result:
            all_results.append(result)

    # Gerar gráfico comparativo
    if len(all_results) >= 2:
        comp_path = os.path.join(base_dir, "ranking_comparativo.png")
        generate_comparison_chart(all_results, comp_path)

        # Exportar resultado consolidado
        consolidated_path = os.path.join(base_dir, "ranking_consolidado.json")
        with open(consolidated_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Resultado consolidado: {consolidated_path}")

    print(f"\n{'█'*64}")
    print(f"  ANÁLISE COMPLETA — {len(all_results)} projetos processados")
    print(f"{'█'*64}\n")

    return all_results


def main():
    parser = argparse.ArgumentParser(
        description="Ranqueamento de requisitos com PageRank, HITS e SALSA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python ranker.py testes/simples_stdlib/req_graph.json
  python ranker.py testes/medio_flask/req_graph.dot --format dot
  python ranker.py --all
        """,
    )
    parser.add_argument(
        "graph_file",
        nargs="?",
        help="Caminho para o ficheiro do grafo (JSON ou DOT)",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "dot", "auto"],
        default="auto",
        help="Formato do ficheiro de entrada (padrão: auto-detectar)",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Processar todos os projetos de teste",
    )
    parser.add_argument(
        "--output-dir", "-o",
        default=None,
        help="Diretório de saída para os resultados",
    )

    args = parser.parse_args()

    if args.all:
        process_all()
    elif args.graph_file:
        process_single(args.graph_file, args.format, args.output_dir)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
