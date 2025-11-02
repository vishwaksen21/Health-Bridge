import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
import joblib

def train_predict_model():
    # Dummy feature & label data (you’ll replace with real embeddings)
    X = np.random.rand(100, 64)
    y = np.random.randint(0, 2, 100)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    preds = rf.predict(X_test)

    auc = roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])
    acc = accuracy_score(y_test, preds)
    print(f"✅ Model trained | AUC: {auc:.3f}, Accuracy: {acc:.3f}")

    joblib.dump(rf, "data/model.pkl")

if __name__ == "__main__":
    train_predict_model()
