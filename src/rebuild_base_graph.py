import networkx as nx

def rebuild_base_graph():
    # Define base relationships
    edges = [
        ("Tulsi", "Eugenol"),
        ("Neem", "Azadirachtin"),
        ("Ashwagandha", "Withaferin A"),
        ("Turmeric", "Curcumin"),
        ("Eugenol", "TNF"),
        ("Azadirachtin", "IL6"),
        ("Withaferin A", "TP53"),
        ("Curcumin", "NFE2L2"),
        ("TNF", "Inflammation"),
        ("IL6", "Fever"),
        ("TP53", "Cancer"),
        ("NFE2L2", "Diabetes")
    ]

    G = nx.Graph()
    G.add_edges_from(edges)

    # Write cleanly
    with open("data/HITD_network.edgelist", "w") as f:
        for u, v in G.edges():
            f.write(f"{u} {v}\n")

    print("✅ Rebuilt clean HITD_network.edgelist with", len(G.nodes()), "nodes and", len(G.edges()), "edges.")

if __name__ == "__main__":
    rebuild_base_graph()
