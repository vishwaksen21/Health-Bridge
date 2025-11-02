import pandas as pd
import networkx as nx

def expand_graph():
    base_graph = nx.read_edgelist("data/HITD_network.edgelist")
    kaggle_df = pd.read_csv("data/symptom_disease.csv")

    # Add Kaggle diseases as nodes
    diseases = kaggle_df['prognosis'].unique()
    print(f"Adding {len(diseases)} diseases to graph...")

    for d in diseases:
        if not base_graph.has_node(d):
            base_graph.add_node(d)

    nx.write_edgelist(base_graph, "data/HITD_network_expanded.edgelist")
    print("✅ Expanded graph saved to data/HITD_network_expanded.edgelist")

if __name__ == "__main__":
    expand_graph()
