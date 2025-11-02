import shap
import joblib
import numpy as np
import matplotlib.pyplot as plt

def explain_model():
    model = joblib.load("data/model.pkl")
    X = np.random.rand(20, 64)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    shap.summary_plot(shap_values, X, show=False)
    plt.title("Feature Importance Explanation (SHAP)")
    plt.savefig("data/shap_summary.png")
    print("✅ SHAP explanation saved to data/shap_summary.png")

if __name__ == "__main__":
    explain_model()
