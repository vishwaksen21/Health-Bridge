import networkx as nx
from node2vec import Node2Vec
import os

def generate_node2vec_embeddings():
    # Use the expanded graph instead of the base one
    edgelist_path = "data/HITD_network_expanded_v2.edgelist"
    if not os.path.exists(edgelist_path):
        edgelist_path = "data/HITD_network.edgelist"

    print(f"🚀 Starting Node2Vec embedding generation from {edgelist_path}...")

    # Load graph - parse edgelist line by line to handle multi-word node names
    G = nx.Graph()
    with open(edgelist_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                # Split into two parts: first word is source, rest is target
                source = parts[0]
                target = " ".join(parts[1:])
                G.add_edge(source, target)
    
    print(f"✅ Graph loaded with {len(G.nodes())} nodes and {len(G.edges())} edges")

    # Train Node2Vec
    node2vec = Node2Vec(G, dimensions=64, walk_length=10, num_walks=50, workers=2)
    print("⚙️  Training Node2Vec model...")
    model = node2vec.fit(window=5, min_count=1)
    # Save using gensim's native format which handles multi-word node names
    model.wv.save("data/embeddings.kv")

    print("✅ Embeddings successfully generated and saved to data/embeddings.kv")

if __name__ == "__main__":
    generate_node2vec_embeddings()