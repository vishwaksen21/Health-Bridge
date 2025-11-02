import numpy as np
import pandas as pd
from gensim.models import KeyedVectors
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, roc_curve, confusion_matrix, ConfusionMatrixDisplay
import joblib
import random
import os
import matplotlib.pyplot as plt

# ---------------------- Embeddings ----------------------
def load_embeddings(kv_path="data/embeddings.kv"):
    return KeyedVectors.load(kv_path)

def hadamard(u, v):
    return np.multiply(u, v)

# ---------------------- Dataset Builder ----------------------
def build_pair_dataset(emb, data_dir="data", negative_ratio=1):
    ingredients_df = pd.read_csv(f"{data_dir}/ingredients.csv")
    targets_df = pd.read_csv(f"{data_dir}/targets.csv")

    ingredients_df.columns = ingredients_df.columns.str.strip().str.lower()
    targets_df.columns = targets_df.columns.str.strip().str.lower()

    t2d = dict(zip(targets_df['target'].astype(str).str.strip(),
                   targets_df['disease'].astype(str).str.strip()))

    pos_pairs = []
    for _, r in ingredients_df.iterrows():
        ing = str(r['ingredient']).strip()
        tgt = str(r['target']).strip()
        if tgt in t2d:
            dis = t2d[tgt]
            pos_pairs.append((ing, dis))

    pos_pairs = [p for p in pos_pairs if p[0] in emb.key_to_index and p[1] in emb.key_to_index]
    pos_pairs = list(set(pos_pairs))
    print(f"✅ Found {len(pos_pairs)} positive ingredient–disease pairs with embeddings.")

    all_ingredients = [l.strip() for l in open(f"{data_dir}/nodes_ingredients.txt").read().splitlines() if l.strip()]
    all_diseases = [l.strip() for l in open(f"{data_dir}/nodes_diseases.txt").read().splitlines() if l.strip()]

    neg_pairs = set()
    target_neg_count = len(pos_pairs) * negative_ratio
    tries = 0
    while len(neg_pairs) < target_neg_count and tries < target_neg_count * 10:
        i = random.choice(all_ingredients)
        d = random.choice(all_diseases)
        if (i, d) not in pos_pairs and i in emb.key_to_index and d in emb.key_to_index:
            neg_pairs.add((i, d))
        tries += 1
    neg_pairs = list(neg_pairs)
    print(f"✅ Sampled {len(neg_pairs)} negative pairs.")

    X, y = [], []
    for a, b in pos_pairs:
        X.append(hadamard(emb[a], emb[b])); y.append(1)
    for a, b in neg_pairs:
        X.append(hadamard(emb[a], emb[b])); y.append(0)

    return np.vstack(X), np.array(y), pos_pairs

# ---------------------- Model Training ----------------------
def train_models(kv_path="data/embeddings.kv", data_dir="data", out_dir="data"):
    emb = load_embeddings(kv_path)
    X, y, pos_pairs = build_pair_dataset(emb, data_dir=data_dir, negative_ratio=2)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Base models
    rf1 = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    rf2 = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=7, n_jobs=-1)
    estimators = [('rf1', rf1), ('rf2', rf2)]
    final_estimator = LogisticRegression(max_iter=1000)

    # Adaptive CV setting
    min_class = min(sum(y_train == 0), sum(y_train == 1))
    cv_folds = min(3, min_class) if min_class < 5 else 5
    print(f"⚙️  Using cv={cv_folds} for stacking (based on dataset size).")

    stack = StackingClassifier(
        estimators=estimators,
        final_estimator=final_estimator,
        passthrough=False,
        n_jobs=-1,
        cv=cv_folds
    )

    stack.fit(X_train, y_train)

    # Train SHAP-friendly single RF
    shap_rf = RandomForestClassifier(n_estimators=300, random_state=123, n_jobs=-1)
    shap_rf.fit(X_train, y_train)

    # Evaluation
    preds_proba = stack.predict_proba(X_test)[:, 1]
    preds = (preds_proba >= 0.5).astype(int)
    auc = roc_auc_score(y_test, preds_proba)
    acc = accuracy_score(y_test, preds)
    print(f"✅ Ensemble trained | AUC: {auc:.3f}, Accuracy: {acc:.3f}")

    # Save models
    os.makedirs(out_dir, exist_ok=True)
    joblib.dump(stack, f"{out_dir}/stack_model.pkl")
    joblib.dump(shap_rf, f"{out_dir}/shap_rf.pkl")
    print(f"💾 Models saved to {out_dir}/stack_model.pkl and shap_rf.pkl")

    # Visualization
    try:
        cm = confusion_matrix(y_test, preds)
        ConfusionMatrixDisplay(cm).plot(cmap="Blues")
        plt.title("Confusion Matrix")
        plt.savefig(f"{out_dir}/confusion_matrix.png")
        fpr, tpr, _ = roc_curve(y_test, preds_proba)
        plt.figure()
        plt.plot(fpr, tpr, label=f"AUC={auc:.2f}")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curve")
        plt.legend()
        plt.savefig(f"{out_dir}/roc_curve.png")
        print("📊 Evaluation plots saved (confusion_matrix.png, roc_curve.png)")
    except Exception as e:
        print(f"⚠️ Skipped visualization: {e}")

    return stack, shap_rf

if __name__ == "__main__":
    print("🚀 Training AI Predictor...")
    train_models()