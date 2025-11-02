#!/usr/bin/env python3
"""
Quick Reference: Using the New Medicinal & Drug Datasets

Examples showing how to leverage the integrated datasets for:
1. Herbal recommendations
2. Drug effectiveness data
3. Medicine recommendations based on patient profiles
"""

from src.database_manager import DatabaseManager
import json


def example_1_herbal_recommendations():
    """Example 1: Get herbal recommendations for a condition"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Herbal Recommendations")
    print("="*70)
    
    db = DatabaseManager()
    
    print("\n🌿 Ayurvedic Herbs for Inflammation:")
    herbs = db.conn.execute("""
        SELECT name, description 
        FROM herbs 
        WHERE name LIKE '%turmeric%' 
           OR name LIKE '%ginger%'
           OR name LIKE '%ashwagandha%'
        LIMIT 5
    """).fetchall()
    
    for herb_name, description in herbs:
        print(f"\n  Plant: {herb_name}")
        try:
            details = json.loads(description)
            print(f"    Scientific: {details.get('scientific_name', 'N/A')}")
            print(f"    Properties: {details.get('medicinal_properties', 'N/A')}")
            print(f"    Uses: {details.get('traditional_uses', 'N/A')}")
            print(f"    Dosage: {details.get('dosage', 'N/A')}")
        except:
            print(f"    Details: {description[:100]}")


def example_2_effective_drugs():
    """Example 2: Find highly-rated drugs from patient reviews"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Highly Effective Drugs (from Drugs.com Reviews)")
    print("="*70)
    
    db = DatabaseManager()
    
    print("\n💊 Top-Rated Medications (effectiveness >= 0.8):")
    drugs = db.conn.execute("""
        SELECT name, effectiveness_rating, description
        FROM pharmaceuticals
        WHERE effectiveness_rating >= 0.8
        ORDER BY effectiveness_rating DESC
        LIMIT 10
    """).fetchall()
    
    for drug_name, rating, description in drugs:
        print(f"\n  Drug: {drug_name}")
        print(f"    Effectiveness Rating: ⭐ {rating*5:.1f}/5.0")
        print(f"    Info: {description[:80]}")


def example_3_herbal_vs_pharmaceutical():
    """Example 3: Compare herbal vs pharmaceutical options"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Herbal vs Pharmaceutical Comparison")
    print("="*70)
    
    db = DatabaseManager()
    
    # Get herbs for fever
    print("\n🌿 HERBAL OPTIONS (for fever):")
    herbs_for_fever = db.conn.execute("""
        SELECT name, description
        FROM herbs
        WHERE description LIKE '%fever%'
           OR description LIKE '%temperature%'
           OR description LIKE '%anti-inflammatory%'
        LIMIT 3
    """).fetchall()
    
    for herb, desc in herbs_for_fever:
        print(f"  • {herb}")
        try:
            details = json.loads(desc)
            print(f"    Dosage: {details.get('dosage', 'Consult herbalist')}")
        except:
            pass
    
    # Get pharmaceutical options
    print("\n💊 PHARMACEUTICAL OPTIONS (for fever):")
    drugs_for_fever = db.conn.execute("""
        SELECT name, effectiveness_rating
        FROM pharmaceuticals
        WHERE name IN ('PARACETAMOL', 'IBUPROFEN', 'ASPIRIN')
        ORDER BY effectiveness_rating DESC
        LIMIT 3
    """).fetchall()
    
    for drug, rating in drugs_for_fever:
        print(f"  • {drug}")
        print(f"    Effectiveness: ⭐ {rating*5:.1f}/5.0")


def example_4_personalized_medicine():
    """Example 4: Query medicine recommendations based on patient profile"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Personalized Medicine Recommendations")
    print("="*70)
    
    db = DatabaseManager()
    
    print("\n🎯 Sample Patient Profiles (from ML dataset):")
    patterns = db.conn.execute("""
        SELECT pattern_name, pattern_data, disease_association
        FROM symptom_patterns
        WHERE pattern_name LIKE 'MED_REC_%'
        LIMIT 5
    """).fetchall()
    
    for idx, (pattern_name, pattern_data, recommended_drug) in enumerate(patterns, 1):
        try:
            profile = json.loads(pattern_data)
            print(f"\n  Profile {idx}:")
            print(f"    Age: {profile.get('patient_age', 'N/A')}")
            print(f"    Gender: {profile.get('gender', 'N/A')}")
            print(f"    Symptoms: {', '.join(profile.get('symptoms', []))}")
            print(f"    Kidney Function: {profile.get('kidney_function', 'Normal')}")
            print(f"    Liver Function: {profile.get('liver_function', 'Normal')}")
            print(f"    💊 Recommended: {recommended_drug}")
        except:
            print(f"    Data: {pattern_data[:100]}")


def example_5_drug_interactions():
    """Example 5: Check drug interactions from database"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Drug Interaction Checking")
    print("="*70)
    
    db = DatabaseManager()
    
    print("\n⚠️  Sample Drug Interactions:")
    interactions = db.conn.execute("""
        SELECT drug1, drug2, severity, recommendation
        FROM drug_interactions
        LIMIT 5
    """).fetchall()
    
    for drug1, drug2, severity, rec in interactions:
        severity_emoji = "🔴" if severity == "HIGH" else "🟡" if severity == "MEDIUM" else "🟢"
        print(f"\n  {drug1} + {drug2}")
        print(f"    Severity: {severity_emoji} {severity}")
        print(f"    Recommendation: {rec[:80]}")


def example_6_advanced_query():
    """Example 6: Advanced query - Find natural alternatives"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Advanced - Natural Alternatives Finder")
    print("="*70)
    
    db = DatabaseManager()
    
    # Find herbs and their pharmaceutical equivalents
    print("\n🔄 Natural Alternatives for Common Conditions:")
    
    conditions = ["inflammation", "pain", "fever", "anxiety"]
    
    for condition in conditions:
        print(f"\n  📋 {condition.upper()}:")
        
        # Search herbs
        print(f"     🌿 Herbal: ", end="")
        herbs = db.conn.execute(f"""
            SELECT name FROM herbs 
            WHERE description LIKE '%{condition}%'
            LIMIT 2
        """).fetchall()
        if herbs:
            print(", ".join([h[0] for h in herbs]))
        else:
            print("(not found)")
        
        # Search drugs
        print(f"     💊 Pharmaceutical: ", end="")
        drugs = db.conn.execute(f"""
            SELECT name FROM pharmaceuticals 
            WHERE description LIKE '%{condition}%'
            LIMIT 2
        """).fetchall()
        if drugs:
            print(", ".join([d[0] for d in drugs]))
        else:
            print("(not found)")


def example_7_statistics():
    """Example 7: Database statistics"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Database Statistics")
    print("="*70)
    
    db = DatabaseManager()
    
    print("\n📊 Dataset Integration Summary:\n")
    
    stats = {
        "diseases": db.conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0],
        "symptoms": db.conn.execute("SELECT COUNT(*) FROM symptoms").fetchone()[0],
        "herbs": db.conn.execute("SELECT COUNT(*) FROM herbs").fetchone()[0],
        "pharmaceuticals": db.conn.execute("SELECT COUNT(*) FROM pharmaceuticals").fetchone()[0],
        "drug_interactions": db.conn.execute("SELECT COUNT(*) FROM drug_interactions").fetchone()[0],
        "symptom_patterns": db.conn.execute("SELECT COUNT(*) FROM symptom_patterns").fetchone()[0],
    }
    
    for category, count in stats.items():
        print(f"  ✅ {category.upper()}: {count} records")
    
    total = sum(stats.values())
    print(f"\n  🎯 TOTAL RECORDS: {total}")


def main():
    """Run all examples"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   📚 MEDICINAL DATASETS - USAGE EXAMPLES                        ║
║                                                                  ║
║   Quick reference for querying integrated datasets               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    examples = [
        ("Herbal Recommendations", example_1_herbal_recommendations),
        ("Effective Drugs from Reviews", example_2_effective_drugs),
        ("Herbal vs Pharmaceutical", example_3_herbal_vs_pharmaceutical),
        ("Personalized Medicine", example_4_personalized_medicine),
        ("Drug Interactions", example_5_drug_interactions),
        ("Find Natural Alternatives", example_6_advanced_query),
        ("Database Statistics", example_7_statistics),
    ]
    
    for idx, (title, func) in enumerate(examples, 1):
        try:
            print(f"\n▶️  RUNNING EXAMPLE {idx}: {title}")
            func()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
            print(f"     Make sure datasets are integrated first:")
            print(f"     python src/integrate_medicinal_datasets.py")
    
    print("\n" + "="*70)
    print("💡 For more examples, check DATASETS_INTEGRATION_GUIDE.md")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
