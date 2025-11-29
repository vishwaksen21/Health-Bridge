#!/usr/bin/env python3
"""
Comprehensive Evaluation Script for Quick Wins Implementation
Tests all 4 Quick Wins: Class Balancing, TF-IDF Bigrams, Calibration, Safety Checks
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import joblib
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from src.symptom_predictor import clean_text
from src.safety_checks import check_emergency_keywords, check_confidence_threshold
import numpy as np

def load_model_and_data():
    """Load the trained model and dataset"""
    print("📂 Loading model and dataset...")
    
    model_path = 'data/symptom_model.pkl'
    data_path = 'data/symptom_disease.csv'
    
    vectorizer, model = joblib.load(model_path)
    df = pd.read_csv(data_path)
    
    print(f"✅ Model loaded: {model_path}")
    print(f"✅ Dataset loaded: {data_path} ({len(df)} samples)")
    
    return vectorizer, model, df

def test_emergency_detection():
    """Test Quick Win #4A: Emergency Detection"""
    print("\n" + "="*70)
    print("🚨 TEST 1: Emergency Keyword Detection (Quick Win #4A)")
    print("="*70)
    
    emergency_cases = [
        "I'm having severe chest pain and sweating",
        "My heart feels like it's being crushed",
        "I can't breathe properly",
        "I'm coughing up blood",
        "I think I'm having a stroke - my face is numb",
        "Severe bleeding from my arm won't stop",
        "Sudden vision loss in one eye"
    ]
    
    normal_cases = [
        "I have a mild headache",
        "Feeling tired and sleepy",
        "Slight fever and runny nose",
        "My knee hurts when I walk"
    ]
    
    print("\n🔴 Testing EMERGENCY cases (should trigger alert):")
    emergency_pass = 0
    for case in emergency_cases:
        result = check_emergency_keywords(case)
        status = "✅" if result['is_emergency'] else "❌"
        print(f"{status} '{case[:50]}...' → Emergency: {result['is_emergency']}")
        if result['is_emergency']:
            emergency_pass += 1
    
    print(f"\n🟢 Testing NORMAL cases (should NOT trigger alert):")
    normal_pass = 0
    for case in normal_cases:
        result = check_emergency_keywords(case)
        status = "✅" if not result['is_emergency'] else "❌"
        print(f"{status} '{case[:50]}' → Emergency: {result['is_emergency']}")
        if not result['is_emergency']:
            normal_pass += 1
    
    total_pass = emergency_pass + normal_pass
    total_cases = len(emergency_cases) + len(normal_cases)
    accuracy = (total_pass / total_cases) * 100
    
    print(f"\n📊 Emergency Detection Results:")
    print(f"   Emergency Cases: {emergency_pass}/{len(emergency_cases)} correct")
    print(f"   Normal Cases: {normal_pass}/{len(normal_cases)} correct")
    print(f"   Overall Accuracy: {accuracy:.1f}% ({total_pass}/{total_cases})")
    
    return accuracy >= 90.0

def test_confidence_warnings():
    """Test Quick Win #4B: Low Confidence Warnings"""
    print("\n" + "="*70)
    print("⚠️  TEST 2: Confidence Threshold Warnings (Quick Win #4B)")
    print("="*70)
    
    test_cases = [
        (0.95, False, "Very high confidence - no warning needed"),
        (0.75, False, "High confidence - no warning"),
        (0.50, False, "Moderate confidence - no warning"),
        (0.44, True, "Below threshold - should warn"),
        (0.30, True, "Low confidence - should warn"),
        (0.15, True, "Very low confidence - should warn")
    ]
    
    threshold = 0.45
    print(f"\n🎯 Confidence Threshold: {threshold} (45%)")
    print(f"   Warnings shown for predictions below {threshold}")
    
    passed = 0
    for confidence, should_warn, description in test_cases:
        result = check_confidence_threshold(confidence, threshold)
        status = "✅" if result['show_warning'] == should_warn else "❌"
        warning_status = "WARNING" if result['show_warning'] else "OK"
        print(f"{status} {confidence*100:5.1f}% → {warning_status:7s} | {description}")
        if result['show_warning'] == should_warn:
            passed += 1
    
    accuracy = (passed / len(test_cases)) * 100
    print(f"\n📊 Confidence Warning Results:")
    print(f"   Correct: {passed}/{len(test_cases)} ({accuracy:.1f}%)")
    
    return accuracy == 100.0

def test_model_performance():
    """Test Quick Wins #1-3: Class Balancing, Bigrams, Calibration"""
    print("\n" + "="*70)
    print("🧠 TEST 3: Model Performance Evaluation")
    print("="*70)
    
    vectorizer, model, df = load_model_and_data()
    
    # Check Quick Win #2: TF-IDF Bigrams
    print(f"\n📝 Quick Win #2 Verification: TF-IDF Bigrams")
    print(f"   ngram_range: {vectorizer.ngram_range}")
    print(f"   max_features: {vectorizer.max_features}")
    bigrams_ok = vectorizer.ngram_range == (1, 2)
    print(f"   {'✅' if bigrams_ok else '❌'} Bigrams enabled: {bigrams_ok}")
    
    # Check Quick Win #3: Calibration
    print(f"\n🎯 Quick Win #3 Verification: Probability Calibration")
    model_type = type(model).__name__
    is_calibrated = 'Calibrated' in model_type
    print(f"   Model type: {model_type}")
    print(f"   {'✅' if is_calibrated else '❌'} Calibration enabled: {is_calibrated}")
    
    # Check Quick Win #1: Class Balancing (test on actual predictions)
    print(f"\n⚖️  Quick Win #1 Verification: Class Balancing")
    base_model = model.calibrated_classifiers_[0].estimator if is_calibrated else model
    class_weight = getattr(base_model, 'class_weight', None)
    print(f"   Class weight strategy: {class_weight}")
    balanced_ok = class_weight == 'balanced'
    print(f"   {'✅' if balanced_ok else '❌'} Class balancing enabled: {balanced_ok}")
    
    # Test predictions on dataset
    print(f"\n📊 Performance Evaluation on Training Data:")
    print(f"   Dataset: {len(df)} samples, {df['disease'].nunique()} diseases")
    
    X = df['symptom_text'].apply(clean_text).tolist()
    y_true = df['disease'].tolist()
    
    X_vec = vectorizer.transform(X)
    y_pred = model.predict(X_vec)
    y_proba = model.predict_proba(X_vec)
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    print(f"\n   Overall Accuracy: {accuracy*100:.2f}%")
    
    # Confidence distribution
    max_probas = y_proba.max(axis=1)
    print(f"\n   Confidence Distribution:")
    print(f"      High (>75%):     {np.sum(max_probas > 0.75)} predictions ({np.sum(max_probas > 0.75)/len(max_probas)*100:.1f}%)")
    print(f"      Moderate (45-75%): {np.sum((max_probas >= 0.45) & (max_probas <= 0.75))} predictions")
    print(f"      Low (<45%):      {np.sum(max_probas < 0.45)} predictions ({np.sum(max_probas < 0.45)/len(max_probas)*100:.1f}%)")
    
    # Per-class accuracy
    print(f"\n   Per-Disease Performance (top 10 by sample count):")
    disease_counts = df['disease'].value_counts()
    top_diseases = disease_counts.head(10).index
    
    for disease in top_diseases:
        disease_mask = df['disease'] == disease
        disease_accuracy = accuracy_score(
            df[disease_mask]['disease'].tolist(),
            pd.Series(y_pred)[disease_mask].tolist()
        )
        sample_count = disease_counts[disease]
        print(f"      {disease:<30s} {disease_accuracy*100:5.1f}% ({sample_count:3d} samples)")
    
    # Check if calibration improved probability estimates
    if is_calibrated:
        print(f"\n🎯 Calibration Quality Check:")
        # Well-calibrated models should have confidence close to actual accuracy
        confidence_bins = [(0, 0.5), (0.5, 0.75), (0.75, 1.0)]
        for low, high in confidence_bins:
            mask = (max_probas >= low) & (max_probas < high)
            if np.sum(mask) > 0:
                bin_accuracy = accuracy_score(
                    np.array(y_true)[mask],
                    np.array(y_pred)[mask]
                )
                avg_confidence = max_probas[mask].mean()
                calibration_error = abs(avg_confidence - bin_accuracy)
                print(f"      {low*100:.0f}-{high*100:.0f}% confidence: "
                      f"Avg={avg_confidence*100:.1f}%, Acc={bin_accuracy*100:.1f}%, "
                      f"Error={calibration_error*100:.1f}%")
    
    return {
        'bigrams_enabled': bigrams_ok,
        'calibrated': is_calibrated,
        'class_balanced': balanced_ok,
        'accuracy': accuracy,
        'low_confidence_count': np.sum(max_probas < 0.45)
    }

def test_bigram_examples():
    """Test specific bigram feature extraction"""
    print("\n" + "="*70)
    print("📖 TEST 4: Bigram Feature Examples")
    print("="*70)
    
    vectorizer, _, _ = load_model_and_data()
    
    test_phrases = [
        "severe chest pain",
        "high fever with chills",
        "persistent dry cough",
        "shortness of breath"
    ]
    
    print("\n🔍 Checking if bigrams are captured:")
    for phrase in test_phrases:
        processed = clean_text(phrase)
        vec = vectorizer.transform([processed])
        
        # Get feature names for non-zero entries
        feature_indices = vec.nonzero()[1]
        feature_names = [vectorizer.get_feature_names_out()[i] for i in feature_indices]
        
        # Separate unigrams and bigrams
        unigrams = [f for f in feature_names if ' ' not in f]
        bigrams = [f for f in feature_names if ' ' in f]
        
        print(f"\n   '{phrase}' →")
        print(f"      Unigrams: {', '.join(unigrams)}")
        if bigrams:
            print(f"      Bigrams:  {', '.join(bigrams)} ✅")
        else:
            print(f"      Bigrams:  None found ❌")

def main():
    """Run all Quick Wins tests"""
    print("\n" + "="*70)
    print("🎯 COMPREHENSIVE QUICK WINS EVALUATION")
    print("="*70)
    print("\nTesting all 4 Quick Wins:")
    print("   #1: Class Balancing (class_weight='balanced')")
    print("   #2: TF-IDF Bigrams (ngram_range=(1,2))")
    print("   #3: Probability Calibration (CalibratedClassifierCV)")
    print("   #4: Safety Checks (emergency + confidence warnings)")
    
    results = {}
    
    # Test 1: Emergency Detection
    results['emergency_detection'] = test_emergency_detection()
    
    # Test 2: Confidence Warnings
    results['confidence_warnings'] = test_confidence_warnings()
    
    # Test 3: Model Performance
    model_results = test_model_performance()
    results.update(model_results)
    
    # Test 4: Bigram Examples
    test_bigram_examples()
    
    # Summary
    print("\n" + "="*70)
    print("📋 FINAL SUMMARY")
    print("="*70)
    
    print("\n✅ Quick Win Implementation Status:")
    print(f"   #1 Class Balancing:    {'✅ PASS' if results['class_balanced'] else '❌ FAIL'}")
    print(f"   #2 TF-IDF Bigrams:     {'✅ PASS' if results['bigrams_enabled'] else '❌ FAIL'}")
    print(f"   #3 Calibration:        {'✅ PASS' if results['calibrated'] else '❌ FAIL'}")
    print(f"   #4 Safety Checks:      {'✅ PASS' if results['emergency_detection'] and results['confidence_warnings'] else '❌ FAIL'}")
    
    print(f"\n📊 Performance Metrics:")
    print(f"   Model Accuracy:        {results['accuracy']*100:.2f}%")
    print(f"   Emergency Detection:   {results['emergency_detection']}")
    print(f"   Confidence Warnings:   {results['confidence_warnings']}")
    print(f"   Low Confidence Cases:  {results['low_confidence_count']} predictions (<45%)")
    
    all_passed = (
        results['class_balanced'] and
        results['bigrams_enabled'] and
        results['calibrated'] and
        results['emergency_detection'] and
        results['confidence_warnings']
    )
    
    if all_passed:
        print("\n🎉 ALL QUICK WINS SUCCESSFULLY IMPLEMENTED!")
        print("   System ready for production testing")
    else:
        print("\n⚠️  SOME QUICK WINS NEED ATTENTION")
        print("   Review failed tests above")
    
    return results

if __name__ == '__main__':
    main()
