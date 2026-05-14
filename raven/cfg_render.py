# raven/cfg_render.py

from graphviz import Digraph


def render_cfg(cfg_nodes, output="cfg"):

    dot = Digraph()

    for node in cfg_nodes:

        dot.node(
            str(node.id),
            node.label
        )

        for edge in node.edges:

            dot.edge(
                str(node.id),
                str(edge.id)
            )

    dot.render(output, format="png", cleanup=True)