import networkx as nx
import matplotlib.pyplot as plt
import os


def build_capability_tree(results):
   

    tree = {}

    for r in results:
        cap = r["capability"]
        api = r["api"]

        if cap not in tree:
            tree[cap] = {
                "type": "statement",
                "value": "or",
                "children": []
            }

        tree[cap]["children"].append({
            "type": "feature",
            "value": api,
            "evidence": r["evidence"]
        })

    return tree


def add_nodes_recursive(G, parent, node):
   

    if node["type"] == "statement":
        label = node["value"]

        stmt_id = f"{parent}_{label}_{id(node)}"
        G.add_node(stmt_id, label=label)
        G.add_edge(parent, stmt_id)

        current_parent = stmt_id

    elif node["type"] == "feature":
        label = f"{node['value']}\n({node['evidence']})"

        feat_id = f"{parent}_{node['value']}_{id(node)}"
        G.add_node(feat_id, label=label)
        G.add_edge(parent, feat_id)

        return

    else:
        return

   
    for child in node.get("children", []):
        add_nodes_recursive(G, current_parent, child)


def visualize(results):

    G = nx.DiGraph()

    tree = build_capability_tree(results)

    for cap, node in tree.items():

        # root node
        G.add_node(cap, label=cap)

        # build hierarchy
        add_nodes_recursive(G, cap, node)

    # better layout for readability
    pos = nx.spring_layout(G, k=0.8, seed=42)

    labels = nx.get_node_attributes(G, "label")

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=2000, font_size=8)

    plt.title("Hierarchical Capability Correlation")

    # ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # save instead of blocking UI
    plt.savefig("output/graph.png")
    print("Graph saved to output/graph.png")

    plt.close()