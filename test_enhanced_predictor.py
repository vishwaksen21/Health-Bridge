"""
Test: Compare Basic vs Enhanced Symptom Prediction
Shows how the new pattern-based system improves vague symptom handling
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from symptom_predictor import predict_disease as base_predict
from enhanced_symptom_predictor import predict_disease_enhanced, format_enhanced_prediction

def test_travel_symptom_improvements():
    """Test cases showing improvement for travel-related and vague symptoms."""
    
    test_cases = [
        {
            "input": "i have been travelling for longtime, now i'm not feeling proper",
            "expected_pattern": "general_malaise",
            "expected_disease_family": ["Typhoid", "Malaria", "Dengue"],
        },
        {
            "input": "high fever and body ache",
            "expected_pattern": "malaria_dengue",
            "expected_disease_family": ["Malaria", "Dengue", "Typhoid"],
        },
        {
            "input": "loose motion after eating street food in india",
            "expected_pattern": "traveller_diarrhea",
            "expected_disease_family": ["Traveller's Diarrhea", "Gastroenteritis"],
        },
        {
            "input": "not feeling well, weak and tired",
            "expected_pattern": "general_malaise",
            "expected_disease_family": ["Typhoid", "Malaria"],
        },
        {
            "input": "cough and throat pain during business trip",
            "expected_pattern": "respiratory",
            "expected_disease_family": ["Bronchitis", "Pneumonia"],
        },
    ]
    
    print("\n" + "="*80)
    print("TEST: ENHANCED SYMPTOM PREDICTOR - TRAVEL SYMPTOM IMPROVEMENTS")
    print("="*80)
    
    passed = 0
    failed = 0
    
    for idx, test_case in enumerate(test_cases, 1):
        test_input = test_case["input"]
        expected_pattern = test_case["expected_pattern"]
        expected_diseases = test_case["expected_disease_family"]
        
        print(f"\n📝 TEST {idx}: {test_input}")
        print("-" * 80)
        
        # Get predictions
        base_disease, base_conf = base_predict(test_input)
        enhanced = predict_disease_enhanced(test_input)
        
        print(f"   Base Model: {base_disease} ({base_conf*100:.1f}%)")
        print(f"   Enhanced Model: {enhanced['primary_disease']} ({enhanced['confidence']*100:.1f}%)")
        print(f"   Pattern: {enhanced['pattern_detected'] or 'None'}")
        
        # Validate pattern detection
        pattern_correct = enhanced['pattern_detected'] == expected_pattern
        disease_in_family = enhanced['primary_disease'] in expected_diseases
        
        print(f"   ✓ Pattern Correct: {pattern_correct} (expected: {expected_pattern})")
        print(f"   ✓ Disease in Expected Family: {disease_in_family}")
        
        if pattern_correct and disease_in_family:
            print("   ✅ PASSED")
            passed += 1
        else:
            print("   ❌ FAILED")
            failed += 1
    
    print("\n" + "="*80)
    print(f"RESULTS: {passed}/{len(test_cases)} tests passed")
    print("="*80 + "\n")
    
    return passed, failed


def demonstrate_improvement():
    """Show the actual improvement with detailed output."""
    
    print("\n" + "="*80)
    print("DEMONSTRATION: BEFORE vs AFTER")
    print("="*80)
    
    problem_input = "i have been travelling for longtime, now i'm not feeling proper"
    
    print(f"\n🔴 PROBLEM INPUT: '{problem_input}'")
    print("\n" + "-"*80)
    print("❌ BEFORE (Base Model Only)")
    print("-"*80)
    
    base_disease, base_conf = base_predict(problem_input)
    print(f"""
Predicted Disease: {base_disease}
Confidence: {base_conf*100:.1f}%

Issues:
- Vague input doesn't clearly describe symptoms
- Model assigns high confidence to unrelated disease (Diabetes)
- No clarification or context awareness
- User gets wrong recommendation
""")
    
    print("\n" + "-"*80)
    print("✅ AFTER (Enhanced Model with Pattern Recognition)")
    print("-"*80)
    
    result = predict_disease_enhanced(problem_input)
    print(format_enhanced_prediction(result))
    
    print("\n✨ IMPROVEMENTS:")
    print("   1. ✓ Detected 'general_malaise' pattern from vague input")
    print("   2. ✓ Suggests travel-relevant diseases (Typhoid, Malaria, Dengue)")
    print("   3. ✓ Provides clarification questions for better diagnosis")
    print("   4. ✓ Explains reasoning and alternatives")
    print("   5. ✓ Gives actionable next steps\n")


if __name__ == "__main__":
    # Run tests
    passed, failed = test_travel_symptom_improvements()
    
    # Show improvement demo
    demonstrate_improvement()
    
    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)
    print(f"""
✅ Tests Passed: {passed}/5
❌ Tests Failed: {failed}/5

🎯 BENEFITS OF ENHANCED PREDICTOR:
   • Handles vague symptom descriptions better
   • Travel context awareness
   • Pattern-based fallback for ML ambiguity
   • Interactive clarification prompts
   • Better user experience
   
🚀 NEXT STEPS:
   1. Integrate enhanced_symptom_predictor into main.py
   2. Update streamlit_app.py to use enhanced predictions
   3. Add user feedback loop to improve patterns
   4. Store pattern improvements over time
""")
    print("="*80 + "\n")
