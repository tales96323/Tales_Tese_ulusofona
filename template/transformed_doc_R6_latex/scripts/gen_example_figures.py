"""
gen_example_figures.py — Regenera as figuras de exemplo de grafos
DIRECIONADOS do Capítulo 2 (Conceitos Teóricos) com setas claras e
proeminentes.

Motivação (Anotacoes_R5, ponto 4): nas versões anteriores as setas dos
grafos direcionados eram cinzentas, finas e ficavam escondidas sob os
nós — ao reduzir a figura no PDF, deixavam de ser visíveis. Aqui as
arestas usam cor escura, cabeça de seta grande e terminam na borda do
nó (parâmetro ``node_size`` em ``draw_networkx_edges``).

Adicionalmente, corrige uma incoerência: o grafo usado para ilustrar o
PageRank (image8) e o HITS (image9) não correspondia ao grafo descrito
no texto. Todas as ilustrações PageRank/HITS/SALSA passam a usar o
mesmo grafo do texto: arestas A->B, A->C, B->C, C->A (graus de saída
A:2, B:1, C:1).

Saída: figures/image4.png, image8.png, image9.png, image10.png
Uso:   python scripts/gen_example_figures.py
"""

import os
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.normpath(os.path.join(HERE, "..", "figures"))

# Estilo das setas — escuras, grossas e bem visíveis mesmo reduzidas
EDGE_COLOR = "#263238"
NODE_SIZE = 2000
ARROW_SIZE = 26
EDGE_WIDTH = 2.2

LIGHT_BLUE = "#A8D5E2"
LIGHT_GREEN = "#A8E6A1"


def _draw_digraph(G, pos, node_color, title, labels=None,
                  sublabels=None, sublabel_color=None, figsize=(6.0, 4.2)):
    """Desenha um digrafo com setas proeminentes que param na borda do nó."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color=EDGE_COLOR,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=ARROW_SIZE,
        width=EDGE_WIDTH,
        node_size=NODE_SIZE,            # faz a seta terminar na borda do nó
        connectionstyle="arc3,rad=0.12",  # separa arestas recíprocas (A<->C)
        min_source_margin=2,
        min_target_margin=2,
    )
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color=node_color,
        node_size=NODE_SIZE,
        edgecolors="#37474F",
        linewidths=1.5,
    )
    nx.draw_networkx_labels(
        G, pos, ax=ax,
        labels=labels,
        font_size=15,
        font_weight="bold",
    )

    # Rótulos auxiliares (scores / graus) por baixo de cada nó
    if sublabels:
        for node, text in sublabels.items():
            x, y = pos[node]
            ax.text(x, y - 0.34, text, ha="center", va="top",
                    fontsize=10, color=sublabel_color or "#B71C1C",
                    fontweight="bold")

    if title:
        ax.set_title(title, fontsize=14, pad=14)
    ax.margins(0.18)
    ax.axis("off")
    plt.tight_layout()
    out = os.path.join(FIG_DIR, _draw_digraph.out_name)
    fig.savefig(out, dpi=150, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] {out}")


# ---------------------------------------------------------------------------
# Grafo canónico do texto: A->B, A->C, B->C, C->A
# (graus de saída A:2, B:1, C:1; A<->C é um par recíproco)
# ---------------------------------------------------------------------------
EDGES = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "A")]
POS = {"A": (1.4, 0.2), "B": (0.6, -1.4), "C": (-1.2, 0.9)}


def gen_pagerank():
    G = nx.DiGraph(EDGES)
    pr = nx.pagerank(G, alpha=0.85)
    sub = {n: f"{pr[n]:.3f}" for n in G.nodes}
    _draw_digraph.out_name = "image8.png"
    _draw_digraph(G, POS, LIGHT_BLUE,
                  "Exemplo de grafo para cálculo do PageRank",
                  sublabels=sub, sublabel_color="#B71C1C")


def gen_hits():
    G = nx.DiGraph(EDGES)
    hubs, auth = nx.hits(G, max_iter=1000, normalized=True)
    sub = {n: f"hub {hubs[n]:.2f} / auth {auth[n]:.2f}" for n in G.nodes}
    _draw_digraph.out_name = "image9.png"
    _draw_digraph(G, POS, LIGHT_BLUE,
                  "HITS: Autoridades e Hubs",
                  sublabels=sub, sublabel_color="#1A237E")


def gen_salsa():
    G = nx.DiGraph(EDGES)
    sub = {n: f"hub {G.out_degree(n)} / auth {G.in_degree(n)}" for n in G.nodes}
    _draw_digraph.out_name = "image10.png"
    _draw_digraph(G, POS, LIGHT_GREEN,
                  "SALSA: Autoridade (grau de entrada) e Hub (grau de saída)",
                  sublabels=sub, sublabel_color="#1A237E")


def gen_directed_type():
    """Subfigura 'Direcionado' da figura de tipos de grafos (4 nós)."""
    G = nx.DiGraph([("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")])
    pos = {"A": (-1.2, -1.0), "B": (1.3, -1.2), "C": (-0.7, 0.4), "D": (0.2, 1.4)}
    _draw_digraph.out_name = "image4.png"
    _draw_digraph(G, pos, LIGHT_GREEN, "Grafo direcionado", figsize=(5.2, 4.0))


if __name__ == "__main__":
    print(">> Regenerando figuras de exemplo (grafos direcionados, Cap. 2)...")
    gen_directed_type()
    gen_pagerank()
    gen_hits()
    gen_salsa()
    print(">> Concluído.")
