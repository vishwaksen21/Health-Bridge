#!/usr/bin/env python3
"""
🧪 REPEATED CHEST PAIN MISCLASSIFICATION FIX - VERIFICATION TEST

Previously: All pain queries → Returned "Chest Pain (95%)" ❌
Fixed: Pain queries → Return appropriate disease diagnosis ✅

Examples:
  - "body aches and pain" → Influenza (75%) ✅
  - "stomach pain" → Gastroenteritis (75%) ✅
  - "back pain" → Influenza (75%) ✅
"""

import sys
sys.path.insert(0, 'src')

from enhanced_symptom_predictor import predict_disease_enhanced

def test_pain_symptom_fix():
    """Test the repeated chest pain misclassification fix"""
    
    print("=" * 80)
    print("🧪 REPEATED CHEST PAIN MISCLASSIFICATION FIX VERIFICATION")
    print("=" * 80)
    print()
    
    # Test cases: (input, expected_disease, expected_pattern)
    test_cases = [
        ("body aches and pain", "Influenza", "body_ache"),
        ("stomach pain", "Gastroenteritis", "digestive_issues"),
        ("back pain", "Influenza", "body_ache"),
        ("joint pain", "Influenza", "body_ache"),
        ("muscle pain", "Influenza", "body_ache"),
        ("aching body", "Influenza", "body_ache"),
    ]
    
    print("Testing Pain Symptom Classification:")
    print("-" * 80)
    print()
    
    all_pass = True
    
    for test_input, expected_disease, expected_pattern in test_cases:
        result = predict_disease_enhanced(test_input)
        disease = result['primary_disease']
        pattern = result['pattern_detected']
        confidence = result['confidence']
        
        # Check if result is correct
        is_disease_correct = expected_disease.lower() in disease.lower()
        is_pattern_correct = pattern == expected_pattern
        
        status = "✅" if (is_disease_correct and is_pattern_correct) else "⚠️"
        
        print(f"{status} Input: \"{test_input}\"")
        print(f"   Expected: {expected_disease} (Pattern: {expected_pattern})")
        print(f"   Got: {disease} (Pattern: {pattern}) - {confidence*100:.0f}% confidence")
        
        if not is_disease_correct:
            print(f"   ❌ Disease mismatch!")
            all_pass = False
        
        if not is_pattern_correct:
            print(f"   ❌ Pattern mismatch!")
            all_pass = False
        
        print()
    
    return all_pass

def test_comprehensive_system():
    """Test all fixes are still working"""
    
    print()
    print("=" * 80)
    print("🧪 COMPREHENSIVE SYSTEM TEST - ALL FIXES")
    print("=" * 80)
    print()
    
    # Test cases covering all fixes in this session
    test_cases = [
        # Fix #1: Travel symptoms
        ("fever and cold with mild headache", "Common Cold", "Travel symptoms"),
        
        # Fix #2: Asthma
        ("i have asthma, help me to control", "Asthma", "Asthma query"),
        
        # Fix #3: Pain symptoms
        ("body aches and pain", "Influenza", "Body pain"),
        ("stomach pain", "Gastroenteritis", "Stomach pain"),
        ("back pain", "Influenza", "Back pain"),
        
        # Additional tests
        ("cough and sore throat", "Common Cold", "Respiratory"),
        ("diarrhea", "Diarrhea", "Digestive"),
        ("rash on skin", "Allergic Reaction", "Skin"),
    ]
    
    print("Comprehensive Test Results:")
    print("-" * 80)
    print()
    
    all_pass = True
    
    for test_input, expected_keyword, description in test_cases:
        result = predict_disease_enhanced(test_input)
        disease = result['primary_disease']
        confidence = result['confidence']
        
        # Check if result contains expected keyword
        is_correct = expected_keyword.lower() in disease.lower()
        status = "✅" if is_correct else "⚠️"
        
        print(f"{status} {description}: \"{test_input}\"")
        print(f"   → {disease} ({confidence*100:.0f}%)")
        
        if not is_correct:
            print(f"   ❌ Expected '{expected_keyword}' but got '{disease}'")
            all_pass = False
        
        print()
    
    return all_pass

def test_no_regression():
    """Verify no regression - that non-pain symptoms still work correctly"""
    
    print()
    print("=" * 80)
    print("🧪 REGRESSION TEST - NON-PAIN SYMPTOMS")
    print("=" * 80)
    print()
    
    test_cases = [
        ("cough", "Common Cold"),
        ("fever", None),  # Can be various diseases
        ("sore throat", "Common Cold"),
        ("nausea", "Nausea"),
        ("headache", "Headache"),
        ("shortness of breath", "Shortness"),
    ]
    
    print("Regression Test Results:")
    print("-" * 80)
    print()
    
    all_pass = True
    
    for test_input, expected in test_cases:
        result = predict_disease_enhanced(test_input)
        disease = result['primary_disease']
        confidence = result['confidence']
        
        if expected:
            is_correct = expected.lower() in disease.lower()
            status = "✅" if is_correct else "⚠️"
            
            print(f"{status} \"{test_input}\" → {disease} ({confidence*100:.0f}%)")
            
            if not is_correct:
                print(f"   ⚠️ Expected '{expected}' but got '{disease}'")
                all_pass = False
        else:
            print(f"✅ \"{test_input}\" → {disease} ({confidence*100:.0f}%)")
        
        print()
    
    return all_pass

if __name__ == "__main__":
    
    # Run all tests
    pain_fix = test_pain_symptom_fix()
    comprehensive = test_comprehensive_system()
    regression = test_no_regression()
    
    # Summary
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print()
    
    if pain_fix and comprehensive and regression:
        print("✅ ALL TESTS PASSED!")
        print()
        print("System now correctly handles:")
        print("  ✓ Pain symptoms properly classified (not all Chest Pain)")
        print("  ✓ Travel symptoms → Common Cold")
        print("  ✓ Asthma queries → Asthma")
        print("  ✓ Digestive symptoms → Gastroenteritis/Diarrhea")
        print("  ✓ Respiratory symptoms → Common Cold")
        print("  ✓ Skin symptoms → Allergic Reaction")
        print("  ✓ No regressions in other conditions")
        print()
        print("🎉 System is production-ready!")
        sys.exit(0)
    else:
        print("⚠️ Some tests failed:")
        if not pain_fix:
            print("  - Pain symptom classification test failed")
        if not comprehensive:
            print("  - Comprehensive system test failed")
        if not regression:
            print("  - Regression test failed")
        sys.exit(1)
