import kagglehub
import os
import shutil
import pandas as pd

def fetch_symptom_dataset():
    print("📦 Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download("kaushil268/disease-prediction-using-machine-learning")
    print("✅ Downloaded successfully!")
    print("Path to dataset files:", path)

    source_file = os.path.join(path, "Training.csv")
    dest_file = "data/symptom_disease.csv"

    os.makedirs("data", exist_ok=True)
    shutil.copy(source_file, dest_file)
    print(f"✅ Copied Training.csv → {dest_file}")

    # Quick check
    df = pd.read_csv(dest_file)
    print(f"📊 Loaded {len(df)} rows and {len(df.columns)} columns")
    print("Columns:", df.columns.tolist()[:10])

if __name__ == "__main__":
    fetch_symptom_dataset()