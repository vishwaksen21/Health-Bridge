import pandas as pd
import networkx as nx
import random
import os

def expand_graph_v2():
    base_path = "data/HITD_network.edgelist"
    out_path = "data/HITD_network_expanded_v2.edgelist"
    kaggle_path = "data/symptom_disease.csv"

    if not os.path.exists(kaggle_path):
        raise FileNotFoundError("❌ symptom_disease.csv not found. Run fetch_dataset.py first.")

    # --- Load base graph safely ---
    # Parse edgelist line by line to handle multi-word node names correctly
    G = nx.Graph()
    with open(base_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                # Split into two parts: first word is source, rest is target
                source = parts[0]
                target = " ".join(parts[1:])
                G.add_edge(source, target)
    
    print("🧠 Adding diseases from Kaggle dataset...")

    kaggle_df = pd.read_csv(kaggle_path)
    disease_col = None
    for c in kaggle_df.columns:
        if c.lower() in ["disease", "prognosis"]:
            disease_col = c
            break

    if not disease_col:
        raise ValueError("❌ Could not find disease/prognosis column in dataset!")

    diseases = kaggle_df[disease_col].dropna().unique()
    herbs = [n for n in G.nodes if n.lower() not in [d.lower() for d in diseases]]

    print(f"✅ Adding {len(diseases)} diseases to graph...")

    added_edges = 0
    for disease in diseases:
        herb = random.choice(herbs)
        # Add edge only between herb and disease name as plain text
        G.add_edge(str(herb).strip(), str(disease).strip())
        added_edges += 1

    print(f"✅ Added {added_edges} herb–disease links.")

    # --- Write edgelist CLEANLY ---
    with open(out_path, "w") as f:
        for u, v in G.edges():
            f.write(f"{u} {v}\n")

    print(f"📦 Expanded and connected graph saved to {out_path}")

if __name__ == "__main__":
    expand_graph_v2()
