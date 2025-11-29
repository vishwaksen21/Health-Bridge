"""
Train Model V2 with Expanded Dataset

Trains a new symptom predictor model using the expanded dataset (4300 samples).
Maintains all Priority 1 Quick Wins improvements.
"""

import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import re

def clean_text(text):
    """Clean and normalize symptom text"""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = ' '.join(text.split())
    return text

def train_model_v2():
    """Train model with expanded dataset"""
    
    print("="*70)
    print("TRAINING MODEL V2 WITH EXPANDED DATASET")
    print("="*70)
    
    # Load expanded dataset
    print("\n📚 Loading expanded dataset...")
    try:
        df = pd.read_csv("data/symptom_disease_expanded_v2.csv")
        print(f"✅ Loaded: {len(df)} samples, {df['disease'].nunique()} diseases")
    except FileNotFoundError:
        print("❌ Could not find expanded dataset")
        return
    
    # Clean text
    print("\n🧹 Cleaning text data...")
    df['symptom_text_clean'] = df['symptom_text'].apply(clean_text)
    
    # Split data
    print("\n✂️  Splitting into train/test (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        df['symptom_text_clean'],
        df['disease'],
        test_size=0.2,
        random_state=42,
        stratify=df['disease']
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # ===================================
    # PRIORITY 1 QUICK WINS IMPLEMENTED
    # ===================================
    
    print("\n🚀 Training with Priority 1 Quick Wins:")
    print("  ✅ Quick Win #1: Class Balancing")
    print("  ✅ Quick Win #2: TF-IDF Bigrams (8000 features)")
    print("  ✅ Quick Win #3: Probability Calibration")
    print("  ✅ Quick Win #4: Safety Checks (already in main.py)")
    
    # Quick Win #2: TF-IDF with bigrams
    print("\n🔤 Building TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=8000,  # Increased from default
        ngram_range=(1, 2),  # Include bigrams
        sublinear_tf=True
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"Feature matrix shape: {X_train_vec.shape}")
    print(f"Bigrams in vocabulary: {sum(1 for term in vectorizer.vocabulary_ if ' ' in term)}")
    
    # Quick Win #1: Class balancing
    print("\n⚖️  Training Logistic Regression with class balancing...")
    base_model = LogisticRegression(
        class_weight='balanced',  # Handle class imbalance
        max_iter=1000,
        random_state=42,
        n_jobs=-1
    )
    
    # Quick Win #3: Probability calibration
    print("\n🎯 Applying probability calibration...")
    model = CalibratedClassifierCV(
        base_model,
        method='sigmoid',  # Platt scaling
        cv=5,
        n_jobs=-1
    )
    
    print("\n🏋️  Training model...")
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    print("\n📊 Evaluating model...")
    y_pred = model.predict(X_test_vec)
    y_proba = model.predict_proba(X_test_vec)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n✅ Test Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
    
    # Confidence analysis
    max_probas = y_proba.max(axis=1)
    high_conf = (max_probas >= 0.75).sum()
    med_conf = ((max_probas >= 0.45) & (max_probas < 0.75)).sum()
    low_conf = (max_probas < 0.45).sum()
    
    print(f"\n📈 Confidence Distribution:")
    print(f"High (≥75%): {high_conf} ({high_conf/len(max_probas)*100:.1f}%)")
    print(f"Medium (45-75%): {med_conf} ({med_conf/len(max_probas)*100:.1f}%)")
    print(f"Low (<45%): {low_conf} ({low_conf/len(max_probas)*100:.1f}%)")
    print(f"Average: {max_probas.mean():.3f}")
    
    # Save model
    print("\n💾 Saving model...")
    joblib.dump((vectorizer, model), "data/symptom_model_v2.pkl")
    print("✅ Saved to: data/symptom_model_v2.pkl")
    
    # Detailed report
    print("\n📋 Classification Report (Top 10 diseases):")
    print("="*70)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Show sample of diseases
    disease_names = list(set(y_test))[:10]
    for disease in sorted(disease_names):
        if disease in report:
            metrics = report[disease]
            print(f"{disease:<30} P:{metrics['precision']:.3f} R:{metrics['recall']:.3f} F1:{metrics['f1-score']:.3f}")
    
    print("\n" + "="*70)
    print("MODEL V2 TRAINING COMPLETE!")
    print("="*70)
    print(f"\n📊 Final Stats:")
    print(f"  • Training samples: {len(X_train)}")
    print(f"  • Test accuracy: {accuracy:.1%}")
    print(f"  • Avg confidence: {max_probas.mean():.1%}")
    print(f"  • All Quick Wins: ✅ Active")
    
    return accuracy, max_probas.mean()

if __name__ == "__main__":
    accuracy, confidence = train_model_v2()
    
    print("\n✅ Next step: Run comparison evaluation")
    print("   python scripts/compare_models.py")
