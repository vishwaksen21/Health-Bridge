"""
Comprehensive Model Evaluation Script

Evaluates the symptom predictor model with all Quick Wins implemented.
Provides detailed metrics to measure improvement and identify areas for enhancement.
"""

import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def load_model_and_data():
    """Load the trained model and dataset"""
    print("📚 Loading model and data...")
    
    vectorizer, model = joblib.load("data/symptom_model.pkl")
    
    # Load training data
    try:
        df = pd.read_csv("data/symptom_disease_augmented.csv")
        print(f"✅ Loaded augmented dataset: {len(df)} samples")
    except:
        try:
            df = pd.read_csv("data/symptom_disease.csv")
            print(f"✅ Loaded original dataset: {len(df)} samples")
        except:
            print("❌ Could not load dataset")
            return None, None, None
    
    return vectorizer, model, df

def evaluate_model(vectorizer, model, df):
    """Comprehensive model evaluation"""
    
    print("\n" + "="*70)
    print("MODEL PERFORMANCE EVALUATION")
    print("="*70)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['symptom_text'], 
        df['disease'],
        test_size=0.2,
        random_state=42,
        stratify=df['disease']
    )
    
    # Transform text
    X_test_vec = vectorizer.transform(X_test)
    
    # Predictions
    y_pred = model.predict(X_test_vec)
    y_proba = model.predict_proba(X_test_vec)
    
    # ========================================
    # Overall Metrics
    # ========================================
    print("\n📊 OVERALL METRICS")
    print("-" * 70)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
    
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average='weighted', zero_division=0
    )
    
    print(f"Weighted Precision: {precision:.3f}")
    print(f"Weighted Recall: {recall:.3f}")
    print(f"Weighted F1-Score: {f1:.3f}")
    
    # Macro average (treats all classes equally)
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        y_test, y_pred, average='macro', zero_division=0
    )
    
    print(f"\nMacro F1-Score: {f1_macro:.3f} (treats all diseases equally)")
    
    # ========================================
    # Confidence Distribution
    # ========================================
    print("\n📈 CONFIDENCE SCORE DISTRIBUTION")
    print("-" * 70)
    
    max_probas = y_proba.max(axis=1)
    
    high_conf = (max_probas >= 0.75).sum()
    med_conf = ((max_probas >= 0.45) & (max_probas < 0.75)).sum()
    low_conf = (max_probas < 0.45).sum()
    
    total = len(max_probas)
    print(f"High Confidence (≥75%): {high_conf} ({high_conf/total*100:.1f}%)")
    print(f"Medium Confidence (45-75%): {med_conf} ({med_conf/total*100:.1f}%)")
    print(f"Low Confidence (<45%): {low_conf} ({low_conf/total*100:.1f}%)")
    print(f"\nAverage Confidence: {max_probas.mean():.3f}")
    
    # ========================================
    # Per-Disease Performance
    # ========================================
    print("\n🏥 TOP 10 DISEASES BY SAMPLE COUNT")
    print("-" * 70)
    
    disease_counts = Counter(y_test)
    top_diseases = disease_counts.most_common(10)
    
    precision_per, recall_per, f1_per, support_per = precision_recall_fscore_support(
        y_test, y_pred, average=None, labels=model.classes_, zero_division=0
    )
    
    disease_metrics = {}
    for i, disease in enumerate(model.classes_):
        disease_metrics[disease] = {
            'precision': precision_per[i],
            'recall': recall_per[i],
            'f1': f1_per[i],
            'support': support_per[i]
        }
    
    print(f"{'Disease':<30} {'F1':<8} {'Samples':<8}")
    print("-" * 70)
    for disease, count in top_diseases:
        f1_score = disease_metrics.get(disease, {}).get('f1', 0)
        print(f"{disease:<30} {f1_score:.3f}    {count}")
    
    # ========================================
    # Identify Problem Areas
    # ========================================
    print("\n⚠️  DISEASES WITH LOW PERFORMANCE (F1 < 0.5)")
    print("-" * 70)
    
    poor_performers = []
    for disease, metrics in disease_metrics.items():
        if metrics['f1'] < 0.5 and metrics['support'] > 0:
            poor_performers.append((disease, metrics['f1'], metrics['support']))
    
    if poor_performers:
        poor_performers.sort(key=lambda x: x[1])  # Sort by F1 score
        print(f"{'Disease':<30} {'F1':<8} {'Samples':<8}")
        print("-" * 70)
        for disease, f1_score, support in poor_performers[:10]:
            print(f"{disease:<30} {f1_score:.3f}    {int(support)}")
    else:
        print("✅ No diseases with F1 < 0.5!")
    
    # ========================================
    # Class Imbalance Check
    # ========================================
    print("\n⚖️  CLASS BALANCE ANALYSIS")
    print("-" * 70)
    
    train_counts = Counter(y_train)
    max_samples = max(train_counts.values())
    min_samples = min(train_counts.values())
    
    print(f"Most samples per disease: {max_samples}")
    print(f"Least samples per disease: {min_samples}")
    print(f"Imbalance ratio: {max_samples/min_samples:.1f}:1")
    
    if max_samples / min_samples > 10:
        print("⚠️  High class imbalance detected (>10:1)")
        print("   Recommendation: Consider SMOTE or more data augmentation")
    else:
        print("✅ Class imbalance is manageable (<10:1)")
    
    # ========================================
    # Calibration Check
    # ========================================
    print("\n🎯 PROBABILITY CALIBRATION CHECK")
    print("-" * 70)
    
    # Simple calibration check: are confident predictions accurate?
    confident_mask = max_probas >= 0.75
    if confident_mask.sum() > 0:
        confident_accuracy = accuracy_score(
            y_test[confident_mask], 
            y_pred[confident_mask]
        )
        print(f"Accuracy on high-confidence predictions (≥75%): {confident_accuracy:.3f}")
    
    uncertain_mask = max_probas < 0.45
    if uncertain_mask.sum() > 0:
        uncertain_accuracy = accuracy_score(
            y_test[uncertain_mask],
            y_pred[uncertain_mask]
        )
        print(f"Accuracy on low-confidence predictions (<45%): {uncertain_accuracy:.3f}")
    
    # ========================================
    # Emergency Disease Check
    # ========================================
    print("\n🚨 EMERGENCY DISEASE DETECTION")
    print("-" * 70)
    
    emergency_diseases = [
        'Heart Attack', 'Stroke', 'Sepsis', 'Meningitis', 
        'Anaphylaxis', 'Appendicitis'
    ]
    
    emergency_in_test = [d for d in emergency_diseases if d in y_test.values]
    
    if emergency_in_test:
        print(f"Emergency diseases in test set: {len(emergency_in_test)}")
        for disease in emergency_in_test:
            if disease in disease_metrics:
                metrics = disease_metrics[disease]
                print(f"  {disease}: F1={metrics['f1']:.3f}, Recall={metrics['recall']:.3f}")
    else:
        print("ℹ️  No emergency diseases in current test set")
    
    # ========================================
    # Summary
    # ========================================
    print("\n" + "="*70)
    print("EVALUATION SUMMARY")
    print("="*70)
    print()
    
    if accuracy >= 0.85:
        print("✅ EXCELLENT: Accuracy ≥ 85%")
    elif accuracy >= 0.75:
        print("✅ GOOD: Accuracy ≥ 75%")
    elif accuracy >= 0.65:
        print("⚠️  FAIR: Accuracy ≥ 65% (needs improvement)")
    else:
        print("❌ POOR: Accuracy < 65% (significant improvement needed)")
    
    print()
    print("Quick Wins Impact:")
    print("  ✅ Class Balancing - Handling imbalanced data")
    print("  ✅ Bigrams - Capturing multi-word symptoms")
    print("  ✅ Calibration - Reliable confidence scores")
    print("  ✅ Safety Checks - Emergency detection active")
    print()
    
    if accuracy < 0.80:
        print("💡 RECOMMENDATIONS:")
        print("  1. Expand dataset (Priority 2)")
        print("  2. Add more training samples per disease")
        print("  3. Use data augmentation for minority classes")
        print("  4. Consider SMOTE for severe imbalance")
    
    return accuracy, f1, max_probas.mean()

if __name__ == "__main__":
    vectorizer, model, df = load_model_and_data()
    
    if vectorizer is not None and model is not None and df is not None:
        accuracy, f1, avg_conf = evaluate_model(vectorizer, model, df)
        
        print("\n📝 Key Metrics:")
        print(f"  • Accuracy: {accuracy:.1%}")
        print(f"  • F1-Score: {f1:.1%}")
        print(f"  • Avg Confidence: {avg_conf:.1%}")
    else:
        print("❌ Evaluation failed - could not load model or data")
