import streamlit as st
import joblib
import numpy as np
from gensim.models import KeyedVectors

# -------------------- Helper Function --------------------
def recommend_ingredients(problem, emb_path="data/embeddings.kv", model_path="data/stack_model.pkl"):
    emb = KeyedVectors.load_word2vec_format(emb_path, binary=False)
    model = joblib.load(model_path)

    problem = problem.lower().strip().capitalize()

    if problem not in emb.key_to_index:
        matches = [w for w in emb.key_to_index.keys() if problem in w.lower()]
        if matches:
            problem = matches[0]
        else:
            return [], f"❌ '{problem}' not found in the disease database."

    disease_vec = emb[problem]
    possible_ingredients = [w for w in emb.key_to_index if w != problem]

    preds = []
    for ingredient in possible_ingredients:
        pair_vec = np.multiply(emb[ingredient], disease_vec)
        prob = model.predict_proba([pair_vec])[0, 1]
        preds.append((ingredient, prob))

    top = sorted(preds, key=lambda x: x[1], reverse=True)[:5]
    return top, None

# -------------------- Streamlit UI --------------------
def main():
    st.set_page_config(page_title="AI Natural Compound Recommender 🌿", page_icon="🧬")
    st.title("🧬 AI Natural Compound Recommender")
    st.caption("Discover natural ingredients linked to your health problem using Explainable AI 🌿")

    st.divider()
    user_problem = st.text_input("Enter your health problem (e.g., inflammation, fever, diabetes):")

    if st.button("🔍 Find Natural Ingredients"):
        if not user_problem.strip():
            st.warning("Please enter a health problem first.")
            return

        with st.spinner("Analyzing connections... 🤖"):
            results, err = recommend_ingredients(user_problem)
            if err:
                st.error(err)
            elif results:
                st.success(f"🌿 Top natural ingredient suggestions for **{user_problem.capitalize()}**:")
                for i, (ing, prob) in enumerate(results, start=1):
                    st.markdown(f"**{i}. {ing}** — confidence: `{prob:.2f}`")
            else:
                st.info("No matching ingredients found. Try a simpler or known disease term.")

    st.divider()
    st.caption("Built with ❤️ by Vishwak Sena | AI Drug Discovery Project")

if __name__ == "__main__":
    main()