import networkx as nx
from node2vec import Node2Vec

def generate_embeddings():
    G = nx.read_edgelist("data/HITD_network.edgelist", data=False)

    node2vec = Node2Vec(G, dimensions=64, walk_length=10, num_walks=50, workers=2)
    model = node2vec.fit(window=5, min_count=1)
    model.wv.save_word2vec_format("data/embeddings.txt")

    print(f"✅ Embeddings generated for {len(G.nodes())} nodes.")
    return model

if __name__ == "__main__":
    generate_embeddings()
