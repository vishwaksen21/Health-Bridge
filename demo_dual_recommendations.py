"""
Demonstration script showing the complete herbal + pharmaceutical recommendation system.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from ai_assistant import (
        load_knowledge_base, 
        generate_comprehensive_answer,
        format_answer_for_display
    )
except ImportError:
    from symptom_predictor import predict_disease
    from ai_assistant import (
        load_knowledge_base, 
        generate_comprehensive_answer,
        format_answer_for_display
    )


def demonstrate_dual_recommendations():
    """Demonstrate the dual recommendation system."""
    
    print("\n" + "="*70)
    print("🏥 HERBAL + PHARMACEUTICAL RECOMMENDATION SYSTEM - DEMO")
    print("="*70)
    
    # Load knowledge base
    print("\n📦 Loading medical knowledge base...")
    knowledge = load_knowledge_base()
    print(f"   ✅ Loaded {len(knowledge['diseases'])} diseases")
    print(f"   ✅ Loaded {len(knowledge['herbs'])} herbs")
    print(f"   ✅ Loaded {len(knowledge['ingredients'])} ingredients")
    print(f"   ✅ Loaded {len(knowledge['targets'])} targets")
    
    # Test cases
    test_cases = [
        ("I have a high fever and severe cough", "Respiratory illness with fever"),
        ("Chest pain and shortness of breath", "Cardiac-related symptoms"),
        ("Persistent sad mood and anxiety", "Mental health concerns"),
        ("Dry cough and wheezing", "Respiratory disease"),
        ("Fever and chills for 2 days", "General fever symptoms"),
    ]
    
    for i, (symptoms, description) in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"CASE {i}: {description}")
        print(f"{'='*70}")
        print(f"Patient Input: \"{symptoms}\"")
        
        # Generate recommendations
        response = generate_comprehensive_answer(
            symptoms,
            knowledge,
            use_ai=False,  # Skip LLM to avoid API calls
            include_drugs=True
        )
        
        # Display formatted answer
        formatted = format_answer_for_display(response)
        print(formatted)
        
        # Also show JSON structure
        print("\n📊 JSON Structure Summary:")
        print(f"   Disease: {response['detected_disease']}")
        print(f"   Confidence: {response['confidence']:.2%}")
        print(f"   Herbal Recs: {len(response['herbal_recommendations'])}")
        print(f"   Drug Recs: {len(response['drug_recommendations'])}")


def demonstrate_feature_comparison():
    """Show a comparison of herbal vs pharmaceutical approaches."""
    
    print("\n" + "="*70)
    print("📊 SYSTEM FEATURES & CAPABILITIES")
    print("="*70)
    
    print("""
🌿 HERBAL MEDICINE MODULE:
   • Knowledge Graph with 59 nodes (herbs, compounds, diseases)
   • Node2Vec embeddings (64-dimensional)
   • Ingredient-disease mapping
   • Benefits and usage information
   • Active compound extraction
   
💊 PHARMACEUTICAL MODULE:
   • 9 disease categories covered
   • 45+ medications with:
     - Generic and brand names
     - Dosage recommendations
     - Availability status
     - Price ranges (Indian market)
     - Common side effects
   
🔄 UNIFIED RECOMMENDATION ENGINE:
   • Single symptom input
   • Automatic disease detection
   • Dual recommendation output
   • Relevance scoring
   • Medical store availability
   • Side-by-side comparison
   
🤖 OPTIONAL AI ENHANCEMENTS:
   • Azure AI Inference SDK support
   • GitHub Models integration
   • LLM-powered insights
   • Evidence-based explanations
""")


def show_available_diseases():
    """Show all diseases covered in the system."""
    
    from drug_database import DrugDatabase
    
    print("\n" + "="*70)
    print("📋 PHARMACEUTICAL DISEASES COVERED")
    print("="*70)
    
    db = DrugDatabase()
    diseases = db.get_available_diseases()
    
    print(f"\nTotal Diseases: {len(diseases)}\n")
    
    for i, disease in enumerate(diseases, 1):
        disease_data = db.get_drugs_for_disease(disease)
        num_drugs = len(disease_data.get("drugs", []))
        description = disease_data.get("description", "")
        
        print(f"{i}. {disease}")
        print(f"   Description: {description}")
        print(f"   Drugs Available: {num_drugs}")
        
        # Show first 3 drugs
        drugs = disease_data.get("drugs", [])[:3]
        for drug in drugs:
            print(f"      • {drug['name']}")
        print()


def main():
    """Main demonstration function."""
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Herbal & Pharmaceutical Recommendation System Demo"
    )
    parser.add_argument(
        "--demo",
        choices=["full", "cases", "features", "diseases"],
        default="full",
        help="Type of demonstration to run"
    )
    
    args = parser.parse_args()
    
    if args.demo in ["full", "cases"]:
        demonstrate_dual_recommendations()
    
    if args.demo in ["full", "features"]:
        demonstrate_feature_comparison()
    
    if args.demo in ["full", "diseases"]:
        show_available_diseases()
    
    print("\n" + "="*70)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
