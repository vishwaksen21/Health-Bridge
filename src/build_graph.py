import pandas as pd
import networkx as nx

def build_hitd_graph():
    def load_csv(path):
        df = pd.read_csv(path)
        df.columns = df.columns.str.strip().str.lower()  # clean headers
        return df

    herbs = load_csv("data/herbs.csv")
    ingredients = load_csv("data/ingredients.csv")
    targets = load_csv("data/targets.csv")

    if not all(col in herbs.columns for col in ["herb", "ingredient"]):
        raise ValueError(f"❌ herbs.csv must have columns: herb, ingredient. Found: {list(herbs.columns)}")

    if not all(col in ingredients.columns for col in ["ingredient", "target"]):
        raise ValueError(f"❌ ingredients.csv must have columns: ingredient, target. Found: {list(ingredients.columns)}")

    if not all(col in targets.columns for col in ["target", "disease"]):
        raise ValueError(f"❌ targets.csv must have columns: target, disease. Found: {list(targets.columns)}")

    G = nx.Graph()

    # herb-ingredient
    for _, row in herbs.iterrows():
        G.add_edge(row["herb"], row["ingredient"], relation="herb-ingredient")

    # ingredient-target
    for _, row in ingredients.iterrows():
        G.add_edge(row["ingredient"], row["target"], relation="ingredient-target")

    # target-disease
    for _, row in targets.iterrows():
        G.add_edge(row["target"], row["disease"], relation="target-disease")

    nx.write_edgelist(G, "data/HITD_network.edgelist", data=False)
    print(f"✅ Graph built with {len(G.nodes())} nodes and {len(G.edges())} edges.")
    return G

if __name__ == "__main__":
    build_hitd_graph()
