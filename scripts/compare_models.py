"""
Compare Model V1 vs V2 Performance

Comprehensive comparison of original model (1935 samples) vs expanded (4300 samples)
"""

import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix
)
from collections import Counter

def load_models():
    """Load both model versions"""
    print("📚 Loading models...")
    
    try:
        vec1, model1 = joblib.load("data/symptom_model.pkl")
        print("✅ Loaded Model V1 (original)")
    except:
        print("❌ Could not load Model V1")
        return None, None, None, None
    
    try:
        vec2, model2 = joblib.load("data/symptom_model_v2.pkl")
        print("✅ Loaded Model V2 (expanded)")
    except:
        print("❌ Could not load Model V2")
        return None, None, None, None
    
    return vec1, model1, vec2, model2

def evaluate_on_common_test_set(vec1, model1, vec2, model2):
    """Evaluate both models on the same test set"""
    
    print("\n" + "="*70)
    print("MODEL COMPARISON: V1 vs V2")
    print("="*70)
    
    # Load original dataset for fair comparison
    df1 = pd.read_csv("data/symptom_disease_augmented.csv")
    df2 = pd.read_csv("data/symptom_disease_expanded_v2.csv")
    
    print(f"\nDataset Sizes:")
    print(f"  V1: {len(df1)} samples")
    print(f"  V2: {len(df2)} samples")
    print(f"  Expansion: +{len(df2) - len(df1)} samples ({len(df2)/len(df1):.2f}x)")
    
    # Use V1 dataset as common test set
    X_train1, X_test, y_train1, y_test = train_test_split(
        df1['symptom_text'],
        df1['disease'],
        test_size=0.2,
        random_state=42,
        stratify=df1['disease']
    )
    
    print(f"\nCommon Test Set: {len(X_test)} samples")
    
    # ===================================
    # Model V1 Evaluation
    # ===================================
    print("\n" + "-"*70)
    print("MODEL V1 (Original - 1935 samples)")
    print("-"*70)
    
    X_test_vec1 = vec1.transform(X_test)
    y_pred1 = model1.predict(X_test_vec1)
    y_proba1 = model1.predict_proba(X_test_vec1)
    
    acc1 = accuracy_score(y_test, y_pred1)
    p1, r1, f1_v1, _ = precision_recall_fscore_support(y_test, y_pred1, average='weighted')
    max_proba1 = y_proba1.max(axis=1)
    
    print(f"Accuracy: {acc1:.3f} ({acc1*100:.1f}%)")
    print(f"F1-Score: {f1_v1:.3f}")
    print(f"Avg Confidence: {max_proba1.mean():.3f}")
    
    high_conf1 = (max_proba1 >= 0.75).sum()
    low_conf1 = (max_proba1 < 0.45).sum()
    print(f"High Confidence (≥75%): {high_conf1} ({high_conf1/len(max_proba1)*100:.1f}%)")
    print(f"Low Confidence (<45%): {low_conf1} ({low_conf1/len(max_proba1)*100:.1f}%)")
    
    # ===================================
    # Model V2 Evaluation
    # ===================================
    print("\n" + "-"*70)
    print("MODEL V2 (Expanded - 4300 samples)")
    print("-"*70)
    
    X_test_vec2 = vec2.transform(X_test)
    y_pred2 = model2.predict(X_test_vec2)
    y_proba2 = model2.predict_proba(X_test_vec2)
    
    acc2 = accuracy_score(y_test, y_pred2)
    p2, r2, f1_v2, _ = precision_recall_fscore_support(y_test, y_pred2, average='weighted')
    max_proba2 = y_proba2.max(axis=1)
    
    print(f"Accuracy: {acc2:.3f} ({acc2*100:.1f}%)")
    print(f"F1-Score: {f1_v2:.3f}")
    print(f"Avg Confidence: {max_proba2.mean():.3f}")
    
    high_conf2 = (max_proba2 >= 0.75).sum()
    low_conf2 = (max_proba2 < 0.45).sum()
    print(f"High Confidence (≥75%): {high_conf2} ({high_conf2/len(max_proba2)*100:.1f}%)")
    print(f"Low Confidence (<45%): {low_conf2} ({low_conf2/len(max_proba2)*100:.1f}%)")
    
    # ===================================
    # Direct Comparison
    # ===================================
    print("\n" + "="*70)
    print("COMPARISON SUMMARY")
    print("="*70)
    
    print(f"\n{'Metric':<30} {'V1 (1935)':<15} {'V2 (4300)':<15} {'Change':<15}")
    print("-"*70)
    
    acc_change = (acc2 - acc1) * 100
    f1_change = (f1_v2 - f1_v1) * 100
    conf_change = (max_proba2.mean() - max_proba1.mean()) * 100
    high_conf_change = ((high_conf2/len(max_proba2)) - (high_conf1/len(max_proba1))) * 100
    
    print(f"{'Accuracy':<30} {acc1*100:>6.2f}%         {acc2*100:>6.2f}%         {acc_change:>+6.2f}%")
    print(f"{'F1-Score':<30} {f1_v1*100:>6.2f}%         {f1_v2*100:>6.2f}%         {f1_change:>+6.2f}%")
    print(f"{'Avg Confidence':<30} {max_proba1.mean()*100:>6.2f}%         {max_proba2.mean()*100:>6.2f}%         {conf_change:>+6.2f}%")
    print(f"{'High Confidence Rate':<30} {high_conf1/len(max_proba1)*100:>6.2f}%         {high_conf2/len(max_proba2)*100:>6.2f}%         {high_conf_change:>+6.2f}%")
    
    # ===================================
    # Agreement Analysis
    # ===================================
    print("\n📊 MODEL AGREEMENT ANALYSIS")
    print("-"*70)
    
    agreement = (y_pred1 == y_pred2).sum()
    agreement_rate = agreement / len(y_test)
    
    print(f"Predictions in agreement: {agreement}/{len(y_test)} ({agreement_rate*100:.1f}%)")
    
    # Where they disagree, which is correct?
    disagree_mask = y_pred1 != y_pred2
    if disagree_mask.sum() > 0:
        v1_correct_on_disagree = (y_pred1[disagree_mask] == y_test[disagree_mask]).sum()
        v2_correct_on_disagree = (y_pred2[disagree_mask] == y_test[disagree_mask]).sum()
        
        print(f"\nOn {disagree_mask.sum()} disagreements:")
        print(f"  V1 correct: {v1_correct_on_disagree} ({v1_correct_on_disagree/disagree_mask.sum()*100:.1f}%)")
        print(f"  V2 correct: {v2_correct_on_disagree} ({v2_correct_on_disagree/disagree_mask.sum()*100:.1f}%)")
        print(f"  Both wrong: {disagree_mask.sum() - v1_correct_on_disagree - v2_correct_on_disagree}")
    
    # ===================================
    # Feature Space Analysis
    # ===================================
    print("\n🔍 FEATURE SPACE COMPARISON")
    print("-"*70)
    
    vocab1_size = len(vec1.vocabulary_)
    vocab2_size = len(vec2.vocabulary_)
    
    print(f"V1 Vocabulary Size: {vocab1_size}")
    print(f"V2 Vocabulary Size: {vocab2_size}")
    print(f"Change: {vocab2_size - vocab1_size:+d} features")
    
    # Bigrams
    bigrams1 = sum(1 for term in vec1.vocabulary_ if ' ' in term)
    bigrams2 = sum(1 for term in vec2.vocabulary_ if ' ' in term)
    
    print(f"\nV1 Bigrams: {bigrams1}")
    print(f"V2 Bigrams: {bigrams2}")
    print(f"Change: {bigrams2 - bigrams1:+d} bigrams")
    
    # ===================================
    # Recommendation
    # ===================================
    print("\n" + "="*70)
    print("RECOMMENDATION")
    print("="*70)
    
    if acc2 >= acc1 and max_proba2.mean() >= max_proba1.mean():
        print("\n✅ RECOMMENDED: Use Model V2 (Expanded)")
        print("   - Equal or better accuracy")
        print("   - Higher confidence scores")
        print("   - More robust with larger training set")
    elif acc1 > acc2 and (acc1 - acc2) > 0.02:
        print("\n⚠️  RECOMMENDED: Keep Model V1 (Original)")
        print(f"   - Significantly higher accuracy (+{(acc1-acc2)*100:.1f}%)")
        print("   - Data augmentation may have introduced noise")
        print("   - Consider improving augmentation quality")
    else:
        print("\n🤔 MIXED RESULTS:")
        print("   - Models perform similarly")
        print("   - V2 has more training data but similar performance")
        print("   - Consider: Use V2 for production (more robust)")
        print("   - Or: Improve augmentation strategy")
    
    return acc1, acc2, max_proba1.mean(), max_proba2.mean()

if __name__ == "__main__":
    vec1, model1, vec2, model2 = load_models()
    
    if all([vec1, model1, vec2, model2]):
        evaluate_on_common_test_set(vec1, model1, vec2, model2)
    else:
        print("\n❌ Could not complete comparison - missing models")
