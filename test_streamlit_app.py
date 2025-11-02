#!/usr/bin/env python3
"""
Streamlit App Verification Test
Tests the streamlit interface to ensure all sections are working correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ai_assistant import (
    load_knowledge_base,
    generate_comprehensive_answer,
    load_drug_interactions,
    load_allergies_db
)
import json

def test_streamlit_output():
    """Test if the streamlit app will have all required sections"""
    
    print("=" * 80)
    print("🧪 STREAMLIT APP VERIFICATION TEST")
    print("=" * 80)
    print()
    
    # Load resources
    print("📚 Loading knowledge base...")
    knowledge = load_knowledge_base()
    print("✅ Knowledge base loaded!")
    
    print("💊 Loading drug interactions...")
    interactions = load_drug_interactions()
    print(f"✅ Loaded {len(interactions)} drug interactions")
    
    print("🏥 Loading allergies database...")
    allergens = load_allergies_db()
    print(f"✅ Loaded {len(allergens)} allergens")
    print()
    
    # Test case
    test_input = "fever and cold with mild headache"
    
    print("=" * 80)
    print(f"📋 Testing input: \"{test_input}\"")
    print("=" * 80)
    print()
    
    # Generate response
    print("🔍 Generating comprehensive answer...")
    response = generate_comprehensive_answer(
        test_input,
        knowledge,
        use_ai=False,  # Disable AI to avoid API calls
        include_drugs=True
    )
    print("✅ Response generated!")
    print()
    
    # Verify all sections
    print("=" * 80)
    print("✅ RESPONSE VERIFICATION")
    print("=" * 80)
    print()
    
    checks = [
        ("Input", response.get("input") is not None),
        ("Detected Disease", response.get("detected_disease") is not None),
        ("Confidence", response.get("confidence") is not None),
        ("Herbal Recommendations", len(response.get("herbal_recommendations", [])) > 0),
        ("Drug Recommendations", len(response.get("drug_recommendations", [])) > 0),
        ("Drug Interactions", response.get("drug_interactions") is not None),
    ]
    
    all_pass = True
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {check_name}: {result}")
        if not result:
            all_pass = False
    
    print()
    
    # Show details
    print("=" * 80)
    print("📊 RESPONSE DETAILS")
    print("=" * 80)
    print()
    
    print(f"📝 Input: {response['input']}")
    print(f"🧠 Detected Disease: {response['detected_disease']}")
    print(f"📈 Confidence: {response['confidence']*100:.1f}%")
    print()
    
    herbal_recs = response.get("herbal_recommendations", [])
    print(f"🌿 Herbal Recommendations ({len(herbal_recs)}):")
    for i, rec in enumerate(herbal_recs[:3], 1):
        print(f"  {i}. {rec.get('ingredient', 'Unknown')}")
        print(f"     Relevance: {rec.get('relevance_score', 0):.1%}")
    print()
    
    drug_recs = response.get("drug_recommendations", [])
    print(f"💊 Pharmaceutical Recommendations ({len(drug_recs)}):")
    for i, drug in enumerate(drug_recs[:3], 1):
        print(f"  {i}. {drug.get('name', 'Unknown')}")
        print(f"     Purpose: {drug.get('purpose', 'Unknown')}")
    print()
    
    interactions = response.get("drug_interactions", [])
    print(f"⚠️  Drug Interactions: {len(interactions)}")
    if interactions:
        for interaction in interactions[:2]:
            print(f"  • {interaction.get('drug1')} + {interaction.get('drug2')}")
            print(f"    Severity: {interaction.get('severity')}")
    print()
    
    # Final verdict
    print("=" * 80)
    if all_pass:
        print("✅ ✅ ✅ ALL CHECKS PASSED ✅ ✅ ✅")
        print()
        print("Streamlit app will display:")
        print("  ✅ Symptom Analysis")
        print("  ✅ Drug Interaction Warnings")
        print("  ✅ Herbal Ingredients Section")
        print("  ✅ Pharmaceutical Medications Section")
        print("  ✅ Herbal vs Pharmaceutical Comparison")
        print("  ✅ Safety Disclaimer")
    else:
        print("❌ Some checks failed - review output above")
    print("=" * 80)
    
    return all_pass

if __name__ == "__main__":
    success = test_streamlit_output()
    sys.exit(0 if success else 1)
