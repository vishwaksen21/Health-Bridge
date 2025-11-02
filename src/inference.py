import re
import joblib
import numpy as np
from gensim.models import KeyedVectors
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# Load models and embeddings
# -----------------------------
emb = KeyedVectors.load("data/embeddings.kv")
model = joblib.load("data/shap_rf.pkl")

# Basic disease vocabulary (you can expand this!)
DISEASE_KEYWORDS = [
    "fever", "inflammation", "pain", "infection", "cold", "cough",
    "headache", "diabetes", "ulcer", "hypertension", "asthma"
]

def extract_disease_keywords(user_input):
    """Extract disease-like words from long sentences."""
    text = user_input.lower()
    found = []
    for keyword in DISEASE_KEYWORDS:
        if re.search(rf"\b{keyword}\b", text):
            found.append(keyword)
    return found

def recommend_ingredients(disease_name, top_n=5):
    """Get top natural ingredients for a given disease."""
    if disease_name not in emb.key_to_index:
        print(f"⚠️ '{disease_name}' not found in embeddings.")
        return []

    candidates = [w for w in emb.key_to_index if not w.lower() == disease_name]
    scores = []
    for c in candidates:
        if c in emb.key_to_index:
            x = np.multiply(emb[c], emb[disease_name]).reshape(1, -1)
            prob = model.predict_proba(x)[0][1]
            scores.append((c, prob))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("🧬 AI Natural Health Recommender 🌿")
    user_input = input("Describe your problem: ")

    diseases = extract_disease_keywords(user_input)
    if not diseases:
        print(f"❌ '{user_input}' not found in the disease database.")
    else:
        for dis in diseases:
            print(f"\n💡 Based on your input, related disease: **{dis.capitalize()}**")
            recs = recommend_ingredients(dis)
            if recs:
                print("🌿 Top natural ingredients that may help:")
                for ingr, score in recs:
                    print(f"  • {ingr} — confidence: {score:.2f}")
            else:
                print(f"⚠️ No ingredients found for {dis}.")