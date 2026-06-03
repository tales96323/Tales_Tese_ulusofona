"""
gen_callgraph_figures.py — Gera, para cada caso de estudo, TRÊS
representações visuais do mesmo Call Graph, todas com os nomes das
funções/métodos rotulados nas arestas (i.e., nos vértices que cada
aresta liga):

  (1) ``full``       — o Call Graph completo, com todos os vértices
                       rotulados (visão de escala/densidade);
  (2) ``componente`` — a maior componente conexa, rotulada e legível
                       (visão da estrutura principal);
  (3) ``excerto``    — um excerto representativo (~12 vértices) no
                       estilo limpo dos grafos do Capítulo 2, com
                       setas escuras e proeminentes que param na borda
                       do nó (visão pedagógica, totalmente legível).

São gerados 3 ficheiros por projeto (9 no total), em ``figures/``:
    call_graph_<proj>_full.png
    call_graph_<proj>_componente.png
    call_graph_<proj>_excerto.png

Estilo das setas alinhado com ``gen_example_figures.py`` (Cap. 2):
escuras (#263238), com cabeça grande e terminando na borda do nó.

Uso:   python scripts/gen_callgraph_figures.py
"""

import os
import re
import sys
import collections

import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
FIG_DIR = os.path.normpath(os.path.join(HERE, "..", "figures"))
sys.path.insert(0, REPO_ROOT)

from reqgraph.call_graph import CallGraphBuilder          # noqa: E402
from reqgraph.visualize import (                          # noqa: E402
    _hierarchical_layout, _assign_colors, MODULE_COLORS,
)

# Estilo de aresta (coerente com o Capítulo 2)
EDGE_DARK = "#263238"

PROJECTS = [
    ("simples_stdlib",   "CPython stdlib"),
    ("medio_flask",      "Flask"),
    ("complexo_sklearn", "scikit-learn"),
]


def build_graph(proj):
    """Extrai o Call Graph real do projeto via AST."""
    builder = CallGraphBuilder()
    path = os.path.join(REPO_ROOT, "testes", proj)
    cg = builder.analyze_project(path, ignore_files={"mapeamento.py"})
    G = nx.DiGraph()
    for caller, callees in cg.items():
        G.add_node(caller)
        for callee in callees:
            G.add_edge(caller, callee)
    return G


def short_label(name):
    """'modulo.funcao' -> 'funcao'; 'modulo.Classe.metodo' -> 'Classe.metodo'."""
    parts = name.split(".")
    return ".".join(parts[1:]) if len(parts) > 1 else name


def wrap_label(s, width):
    """
    Quebra rótulos longos em várias linhas, sempre em fronteiras naturais
    (depois de '.' ou '_'), de forma a que cada linha tenha no máximo
    ~``width`` caracteres. Mantém os nomes legíveis sem saírem do nó.
    """
    tokens = [t for t in re.split(r"(?<=[._])", s) if t]
    lines, cur = [], ""
    for t in tokens:
        if cur and len(cur) + len(t) > width:
            lines.append(cur)
            cur = t
        else:
            cur += t
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def module_colors(G):
    modules = {n: n.split(".")[0] for n in G.nodes}
    cmap = _assign_colors(modules.values(), MODULE_COLORS)
    node_colors = [cmap[modules[n]] for n in G.nodes]
    return cmap, node_colors


def representative_excerpt(G, target=12):
    """
    Seleciona um excerto conexo e representativo de forma determinística:
    parte do vértice de maior grau (saída+entrada) na maior componente
    fraca e expande por BFS não-dirigido até ~``target`` vértices.
    """
    comps = sorted(nx.weakly_connected_components(G),
                   key=lambda c: (-len(c), sorted(c)[0]))
    big = G.subgraph(comps[0])
    seed = max(sorted(big.nodes),
               key=lambda n: (big.out_degree(n) + big.in_degree(n)))
    und = big.to_undirected()
    chosen, frontier = [], [seed]
    seen = {seed}
    while frontier and len(chosen) < target:
        node = frontier.pop(0)
        chosen.append(node)
        for nb in sorted(und.neighbors(node)):
            if nb not in seen:
                seen.add(nb)
                frontier.append(nb)
    return G.subgraph(chosen).copy()


def draw(G, pos, output_path, *, title, node_colors, color_map,
         font_size, node_size, edge_width, arrow_size, figsize,
         wrap_width=16, label_bbox=False, show_legend=True, margins=0.12):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color=EDGE_DARK,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=arrow_size,
        width=edge_width,
        node_size=node_size,                 # faz a seta parar na borda do nó
        connectionstyle="arc3,rad=0.10",
        min_source_margin=2,
        min_target_margin=2,
        alpha=0.85,
    )
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color=node_colors,
        node_size=node_size,
        edgecolors="#37474F",
        linewidths=1.2,
    )
    labels = {n: wrap_label(short_label(n), wrap_width) for n in G.nodes}
    bbox = (dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.65)
            if label_bbox else None)
    nx.draw_networkx_labels(
        G, pos, labels=labels, ax=ax,
        font_size=font_size,
        font_weight="bold",
        font_family="monospace",
        bbox=bbox,
    )

    if show_legend and color_map:
        handles = [mpatches.Patch(color=color_map[m], label=m)
                   for m in sorted(color_map)]
        ax.legend(handles=handles, loc="upper left", title="Módulo",
                  fontsize=8, framealpha=0.9)

    if title:
        ax.set_title(title, fontsize=14, fontweight="bold", pad=14)
    ax.margins(margins)
    ax.axis("off")
    plt.tight_layout()
    fig.savefig(output_path, dpi=150, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] {output_path}")


def gen_full(G, proj, title):
    pos, n_layers, max_width = _hierarchical_layout(G)
    color_map, node_colors = module_colors(G)
    fig_w = max(16, min(46, max_width * 0.62))
    fig_h = max(9, min(26, n_layers * 2.0))
    draw(G, pos, os.path.join(FIG_DIR, f"call_graph_{proj}_full.png"),
         title=f"{title} — Call Graph completo ({G.number_of_nodes()} vértices)",
         node_colors=node_colors, color_map=color_map,
         font_size=5, node_size=240, edge_width=0.8, arrow_size=8,
         figsize=(fig_w, fig_h), wrap_width=13, label_bbox=False,
         show_legend=True, margins=0.10)


def gen_componente(G, proj, title):
    comps = sorted(nx.weakly_connected_components(G),
                   key=lambda c: (-len(c), sorted(c)[0]))
    H = G.subgraph(comps[0]).copy()
    pos, n_layers, max_width = _hierarchical_layout(H)
    color_map, node_colors = module_colors(H)
    fig_w = max(12, min(30, max_width * 1.05))
    fig_h = max(7, min(20, n_layers * 2.0))
    draw(H, pos, os.path.join(FIG_DIR, f"call_graph_{proj}_componente.png"),
         title=f"{title} — maior componente ({H.number_of_nodes()} vértices)",
         node_colors=node_colors, color_map=color_map,
         font_size=6.5, node_size=560, edge_width=1.3, arrow_size=13,
         figsize=(fig_w, fig_h), wrap_width=14, label_bbox=True,
         show_legend=True, margins=0.14)


def _best_spread_layout(H, k=2.8, iterations=400, seeds=range(40)):
    """
    Escolhe, entre vários ``seed`` do spring_layout, o que maximiza a
    distância mínima entre quaisquer dois vértices — evitando, de forma
    determinística, que dois nós (e.g., dois hubs simétricos) fiquem
    sobrepostos.
    """
    import math
    nodes = list(H.nodes)
    best_pos, best_min = None, -1.0
    for s in seeds:
        pos = nx.spring_layout(H, k=k, iterations=iterations, seed=s)
        dmin = min(
            math.dist(pos[a], pos[b])
            for i, a in enumerate(nodes) for b in nodes[i + 1:]
        )
        if dmin > best_min:
            best_min, best_pos = dmin, pos
    return best_pos


def _de_overlap(pos, min_dist=0.5, iters=80):
    """
    Afasta iterativamente pares de vértices cujos centros fiquem mais
    próximos do que ``min_dist``, garantindo que nenhum par (incluindo
    hubs estruturalmente quase coincidentes) se sobrepõe na figura.
    """
    import math
    p = {n: list(xy) for n, xy in pos.items()}
    nodes = list(p)
    for _ in range(iters):
        moved = False
        for i, a in enumerate(nodes):
            for b in nodes[i + 1:]:
                dx, dy = p[a][0] - p[b][0], p[a][1] - p[b][1]
                d = math.hypot(dx, dy) or 1e-6
                if d < min_dist:
                    shift = (min_dist - d) / 2.0
                    ux, uy = dx / d, dy / d
                    p[a][0] += ux * shift; p[a][1] += uy * shift
                    p[b][0] -= ux * shift; p[b][1] -= uy * shift
                    moved = True
        if not moved:
            break
    return {n: tuple(xy) for n, xy in p.items()}


def gen_excerto(G, proj, title):
    H = representative_excerpt(G, target=10)
    color_map, node_colors = module_colors(H)
    # distribuição uniforme e bem espaçada (melhor seed do spring) +
    # anti-sobreposição (afasta hubs quase coincidentes)
    pos = _de_overlap(_best_spread_layout(H), min_dist=0.62)
    draw(H, pos, os.path.join(FIG_DIR, f"call_graph_{proj}_excerto.png"),
         title=f"{title} — excerto representativo ({H.number_of_nodes()} vértices)",
         node_colors=node_colors, color_map=color_map,
         font_size=8.5, node_size=1500, edge_width=2.2, arrow_size=22,
         figsize=(11.0, 7.5), wrap_width=15, label_bbox=True,
         show_legend=True, margins=0.26)


if __name__ == "__main__":
    print(">> Regenerando representações do Call Graph (3 por projeto)...")
    for proj, title in PROJECTS:
        print(f"-- {proj}")
        G = build_graph(proj)
        gen_full(G, proj, title)
        gen_componente(G, proj, title)
        gen_excerto(G, proj, title)
    print(">> Concluído.")
