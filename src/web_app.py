import streamlit as st
import joblib

st.title("🌿 AI-based Natural Compound Recommender")

disease = st.text_input("Enter disease (e.g., Cancer, Diabetes):")

if st.button("Find Compounds"):
    model = joblib.load("data/model.pkl")
    st.write(f"🔍 Searching for natural compounds related to: **{disease}**")

    # Placeholder output (you’ll replace with predictions)
    st.success(f"✅ Suggested compounds for {disease}: Curcumin, Withaferin A")
    st.image("data/shap_summary.png", caption="Model Explanation (SHAP)")
