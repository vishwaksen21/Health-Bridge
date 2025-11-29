"""
Test script to verify herbal and pharmaceutical recommendations are showing properly
"""

from src.ai_assistant import load_knowledge_base, generate_comprehensive_answer

def test_recommendations(symptom: str):
    """Test if recommendations are generated for a given symptom"""
    kb = load_knowledge_base()
    response = generate_comprehensive_answer(symptom, kb, use_ai=False, include_drugs=True)
    
    disease = response.get('detected_disease', 'Unknown')
    confidence = response.get('confidence', 0)
    herbal = response.get('herbal_recommendations', [])
    drugs = response.get('drug_recommendations', [])
    
    print(f"\n{'='*70}")
    print(f"Symptom: {symptom}")
    print(f"{'='*70}")
    print(f"✓ Detected: {disease} ({confidence*100:.1f}% confidence)")
    print(f"✓ Herbal recommendations: {len(herbal)}")
    if herbal:
        for h in herbal[:3]:
            print(f"   - {h['ingredient']}")
    print(f"✓ Drug recommendations: {len(drugs)}")
    if drugs:
        for d in drugs[:3]:
            print(f"   - {d['name']}")
    
    # Check if recommendations are present
    status = "✅ PASS" if (herbal and drugs) else "❌ FAIL"
    print(f"\nStatus: {status}")
    
    return len(herbal) > 0 and len(drugs) > 0

if __name__ == "__main__":
    test_cases = [
        "fever and headache",
        "severe back pain with blood in urine",
        "stomach pain and diarrhea",
        "cough and cold",
        "joint pain and swelling",
        "muscle strain from exercise",
    ]
    
    print("="*70)
    print("TESTING HERBAL & PHARMACEUTICAL RECOMMENDATIONS")
    print("="*70)
    
    passed = 0
    total = len(test_cases)
    
    for symptom in test_cases:
        if test_recommendations(symptom):
            passed += 1
    
    print(f"\n{'='*70}")
    print(f"FINAL RESULT: {passed}/{total} tests passed")
    print(f"{'='*70}")
    
    if passed == total:
        print("✅ All tests passed! Herbal and pharma recommendations working correctly.")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Some recommendations may be missing.")
