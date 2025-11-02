# src/build_graph_v2.py
import pandas as pd
import networkx as nx

def load_csv_clean(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    return df

def build_hitd_graph(data_dir="data"):
    herbs = load_csv_clean(f"{data_dir}/herbs.csv")
    ingredients = load_csv_clean(f"{data_dir}/ingredients.csv")
    targets = load_csv_clean(f"{data_dir}/targets.csv")
    diseases = load_csv_clean(f"{data_dir}/diseases.csv")

    # Validate
    if not set(["herb","ingredient"]).issubset(set(herbs.columns)):
        raise ValueError("herbs.csv must have columns: herb,ingredient")
    if not set(["ingredient","target"]).issubset(set(ingredients.columns)):
        raise ValueError("ingredients.csv must have columns: ingredient,target")
    if not set(["target","disease"]).issubset(set(targets.columns)):
        raise ValueError("targets.csv must have columns: target,disease")
    if not set(["disease"]).issubset(set(diseases.columns)):
        raise ValueError("diseases.csv must have column: disease")

    G = nx.Graph()

    # Add edges (no attributes) — simpler edgelist
    for _, r in herbs.iterrows():
        G.add_edge(str(r['herb']).strip(), str(r['ingredient']).strip())
    for _, r in ingredients.iterrows():
        G.add_edge(str(r['ingredient']).strip(), str(r['target']).strip())
    for _, r in targets.iterrows():
        G.add_edge(str(r['target']).strip(), str(r['disease']).strip())

    # Save lists for later convenience
    nx.write_edgelist(G, f"{data_dir}/HITD_network.edgelist", data=False)

    # Save node-type lists (heuristic via CSVs)
    herbs_nodes = herbs['herb'].astype(str).str.strip().unique().tolist()
    ingredient_nodes = pd.concat([herbs['ingredient'], ingredients['ingredient']]).astype(str).str.strip().unique().tolist()
    target_nodes = targets['target'].astype(str).str.strip().unique().tolist()
    disease_nodes = pd.concat([targets['disease'], diseases['disease']]).astype(str).str.strip().unique().tolist()

    pd.Series(herbs_nodes).to_csv(f"{data_dir}/nodes_herbs.txt", index=False, header=False)
    pd.Series(ingredient_nodes).to_csv(f"{data_dir}/nodes_ingredients.txt", index=False, header=False)
    pd.Series(target_nodes).to_csv(f"{data_dir}/nodes_targets.txt", index=False, header=False)
    pd.Series(disease_nodes).to_csv(f"{data_dir}/nodes_diseases.txt", index=False, header=False)

    print(f"✅ Graph built with {len(G.nodes())} nodes and {len(G.edges())} edges.")
    return G

if __name__ == "__main__":
    build_hitd_graph()
