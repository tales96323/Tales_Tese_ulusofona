"""
gen_reqgraph_figures.py — Regenera as figuras dos Grafos de Requisitos
(Capítulo 4, Resultados) no estilo limpo dos grafos do Capítulo 2.

Lê as adjacências reais de cada caso de estudo a partir de
``testes/<proj>/req_graph.json`` (produzidas pelo ``python -m reqgraph``)
e desenha-as com ``reqgraph.visualize.visualize_req_graph``, agora no
estilo do Capítulo 2 (fundo branco, setas escuras proeminentes que param
na borda do nó, rótulos a negrito).

Saída: figures/req_graph_simples_stdlib.png,
       figures/req_graph_medio_flask.png,
       figures/req_graph_complexo_sklearn.png

Uso:   python scripts/gen_reqgraph_figures.py
"""

import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
FIG_DIR = os.path.normpath(os.path.join(HERE, "..", "figures"))
sys.path.insert(0, REPO_ROOT)

from reqgraph.visualize import visualize_req_graph          # noqa: E402

PROJECTS = [
    ("simples_stdlib",   "req_graph_simples_stdlib.png",   "Grafo de Requisitos — CPython stdlib"),
    ("medio_flask",      "req_graph_medio_flask.png",      "Grafo de Requisitos — Flask"),
    ("complexo_sklearn", "req_graph_complexo_sklearn.png", "Grafo de Requisitos — scikit-learn"),
]


def load_req_graph(proj):
    path = os.path.join(REPO_ROOT, "testes", proj, "req_graph.json")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


if __name__ == "__main__":
    print(">> Regenerando Grafos de Requisitos (estilo Cap. 2)...")
    for proj, out_name, title in PROJECTS:
        rg = load_req_graph(proj)
        out = os.path.join(FIG_DIR, out_name)
        visualize_req_graph(rg, output_path=out, title=title)
    print(">> Concluído.")
