#!/usr/bin/env python3
"""
Sample Medicinal & Drug Data Integration Script

This script adds sample medicinal plants, Ayurvedic properties, and drug data
directly to the database without requiring Kaggle dataset downloads.

Run this to demonstrate the new capabilities while waiting for dataset downloads.
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(__file__) + '/src')

from database_manager import DatabaseManager


def add_sample_medicinal_plants():
    """Add sample medicinal plants to the database"""
    print("\n📌 ADDING SAMPLE MEDICINAL PLANTS")
    print("="*70)
    
    db = DatabaseManager()
    
    # Sample medicinal plants with detailed information
    medicinal_plants = [
        {
            "name": "TURMERIC",
            "scientific_name": "Curcuma longa",
            "properties": json.dumps({
                "common_name": "Turmeric",
                "active_compounds": ["Curcumin", "Demethoxycurcumin"],
                "medicinal_properties": "Anti-inflammatory, Antioxidant, Antimicrobial",
                "traditional_uses": "Inflammation, Arthritis, Digestive disorders, Wound healing",
                "dosage": "500-2000 mg daily",
                "side_effects": "Rare - upset stomach",
                "source": "Medicinal Plants Database"
            }),
            "effectiveness": 0.85
        },
        {
            "name": "GINGER",
            "scientific_name": "Zingiber officinale",
            "properties": json.dumps({
                "active_compounds": ["Gingerol", "Shogaol"],
                "medicinal_properties": "Anti-nausea, Anti-inflammatory",
                "traditional_uses": "Nausea, Vomiting, Arthritis pain",
                "dosage": "1-2 grams daily"
            }),
            "effectiveness": 0.82
        },
        {
            "name": "ASHWAGANDHA",
            "scientific_name": "Withania somnifera",
            "properties": json.dumps({
                "medicinal_properties": "Adaptogen, Stress relief",
                "traditional_uses": "Stress, Anxiety, Sleep disorders",
                "dosage": "300-600 mg daily"
            }),
            "effectiveness": 0.79
        },
        {
            "name": "NEEM",
            "scientific_name": "Azadirachta indica",
            "properties": json.dumps({
                "medicinal_properties": "Antimicrobial, Antifungal",
                "traditional_uses": "Skin conditions, Infections",
                "dosage": "5-10 ml oil topically"
            }),
            "effectiveness": 0.78
        },
        {
            "name": "TULSI",
            "scientific_name": "Ocimum sanctum",
            "properties": json.dumps({
                "medicinal_properties": "Respiratory support, Anti-stress",
                "traditional_uses": "Cough, Cold, Fever",
                "dosage": "1-2 cups tea daily"
            }),
            "effectiveness": 0.81
        },
        {
            "name": "BRAHMI",
            "scientific_name": "Bacopa monnieri",
            "properties": json.dumps({
                "medicinal_properties": "Cognitive enhancement, Memory support",
                "traditional_uses": "Memory loss, Anxiety",
                "dosage": "300-600 mg daily"
            }),
            "effectiveness": 0.76
        }
    ]
    
    added_count = 0
    for plant in medicinal_plants:
        try:
            db.connection.execute("""
                INSERT OR IGNORE INTO herbs (name, scientific_name, properties, effectiveness_rating)
                VALUES (?, ?, ?, ?)
            """, (plant["name"], plant["scientific_name"], plant["properties"], plant["effectiveness"]))
            
            print(f"  ✅ {plant['name']:20} ({plant['scientific_name']})")
            added_count += 1
        except Exception as e:
            print(f"  ⚠️  {plant['name']:20} - {str(e)[:50]}")
    
    db.connection.commit()
    print(f"\n✅ Added {added_count} medicinal plants")
    return True


def add_sample_ayurvedic_plants():
    """Add sample Ayurvedic plants"""
    print("\n📌 ADDING SAMPLE AYURVEDIC PLANTS")
    print("="*70)
    
    db = DatabaseManager()
    
    ayurvedic_plants = [
        {
            "name": "ASHWAGANDHA (AYURVEDA)",
            "scientific_name": "Withania somnifera",
            "properties": json.dumps({
                "rasa": "Bitter, Astringent",
                "veerya": "Heating",
                "vipaka": "Pungent",
                "plant_part": "Root",
                "indications": "Vata disorders, Stress, Insomnia"
            }),
            "effectiveness": 0.85
        },
        {
            "name": "BRAHMI (AYURVEDA)",
            "scientific_name": "Bacopa monnieri",
            "properties": json.dumps({
                "rasa": "Bitter",
                "veerya": "Cooling",
                "vipaka": "Pungent",
                "plant_part": "Whole plant",
                "indications": "Memory, Pitta imbalance"
            }),
            "effectiveness": 0.82
        },
        {
            "name": "TRIPHALA",
            "scientific_name": "Mixture of three fruits",
            "properties": json.dumps({
                "rasa": "All five tastes",
                "veerya": "Neutral",
                "vipaka": "Sweet",
                "indications": "Digestion, Detoxification"
            }),
            "effectiveness": 0.88
        },
        {
            "name": "SHILAJIT",
            "scientific_name": "Mineral Pitch",
            "properties": json.dumps({
                "rasa": "Bitter, Pungent",
                "veerya": "Heating",
                "vipaka": "Pungent",
                "indications": "Energy, Stamina, Aging"
            }),
            "effectiveness": 0.83
        }
    ]
    
    added_count = 0
    for plant in ayurvedic_plants:
        try:
            db.connection.execute("""
                INSERT OR IGNORE INTO herbs (name, scientific_name, properties, effectiveness_rating)
                VALUES (?, ?, ?, ?)
            """, (plant["name"], plant["scientific_name"], plant["properties"], plant["effectiveness"]))
            
            print(f"  ✅ {plant['name']:30}")
            added_count += 1
        except Exception as e:
            print(f"  ⚠️  {plant['name']:30} - {str(e)[:50]}")
    
    db.connection.commit()
    print(f"\n✅ Added {added_count} Ayurvedic plants")
    return True


def add_sample_drugs_with_reviews():
    """Add sample drugs with effectiveness ratings from reviews"""
    print("\n📌 ADDING SAMPLE DRUGS WITH REVIEW RATINGS")
    print("="*70)
    
    db = DatabaseManager()
    
    drugs = [
        {
            "name": "PARACETAMOL",
            "generic_name": "Acetaminophen",
            "dosage": "500-1000 mg",
            "side_effects": "Liver damage if overdosed, Nausea",
            "availability": "OTC",
            "price": "₹5-30",
            "effectiveness": 0.85
        },
        {
            "name": "IBUPROFEN",
            "generic_name": "Ibuprofen",
            "dosage": "200-400 mg",
            "side_effects": "Stomach upset, GI bleeding (rare)",
            "availability": "OTC",
            "price": "₹10-50",
            "effectiveness": 0.88
        },
        {
            "name": "CETIRIZINE",
            "generic_name": "Cetirizine",
            "dosage": "10 mg",
            "side_effects": "Drowsiness, Dry mouth",
            "availability": "OTC",
            "price": "₹10-40",
            "effectiveness": 0.80
        },
        {
            "name": "AMOXICILLIN",
            "generic_name": "Amoxicillin",
            "dosage": "250-500 mg",
            "side_effects": "Allergic reaction, Diarrhea",
            "availability": "Prescription",
            "price": "₹20-80",
            "effectiveness": 0.92
        },
        {
            "name": "OMEPRAZOLE",
            "generic_name": "Omeprazole",
            "dosage": "20-40 mg",
            "side_effects": "Headache, Long-term concerns",
            "availability": "OTC/Rx",
            "price": "₹15-60",
            "effectiveness": 0.87
        }
    ]
    
    added_count = 0
    for drug in drugs:
        try:
            db.connection.execute("""
                INSERT OR IGNORE INTO pharmaceuticals 
                (name, generic_name, dosage, side_effects, availability, price_range)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (drug["name"], drug["generic_name"], drug["dosage"], 
                  drug["side_effects"], drug["availability"], drug["price"]))
            
            print(f"  ✅ {drug['name']:20} (Effectiveness: {drug['effectiveness']*100:.0f}%)")
            added_count += 1
        except Exception as e:
            print(f"  ⚠️  {drug['name']:20} - {str(e)[:50]}")
    
    db.connection.commit()
    print(f"\n✅ Added {added_count} drugs")
    return True


def verify_database():
    """Verify database contents"""
    print("\n📌 VERIFYING DATABASE CONTENTS")
    print("="*70)
    
    db = DatabaseManager()
    
    stats = {
        "herbs": db.connection.execute("SELECT COUNT(*) FROM herbs").fetchone()[0],
        "pharmaceuticals": db.connection.execute("SELECT COUNT(*) FROM pharmaceuticals").fetchone()[0],
        "diseases": db.connection.execute("SELECT COUNT(*) FROM diseases").fetchone()[0],
        "symptoms": db.connection.execute("SELECT COUNT(*) FROM symptoms").fetchone()[0],
    }
    
    print("\n📊 Database Statistics:")
    for table, count in stats.items():
        print(f"  ✅ {table.upper():20} : {count:3d} records")
    
    total = sum(stats.values())
    print(f"\n  🎯 TOTAL RECORDS: {total}")
    
    # Show some sample herbs
    print("\n🌿 Sample Medicinal Plants:")
    herbs = db.connection.execute("SELECT name FROM herbs LIMIT 3").fetchall()
    for herb in herbs:
        print(f"  • {herb[0]}")
    
    # Show some sample drugs
    print("\n💊 Sample Drugs:")
    drugs = db.connection.execute("SELECT name FROM pharmaceuticals LIMIT 3").fetchall()
    for drug in drugs:
        print(f"  • {drug[0]}")


def main():
    """Main execution"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🌿 SAMPLE MEDICINAL & DRUG DATA INTEGRATION                   ║
║                                                                  ║
║   Adds sample data while waiting for Kaggle datasets             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    results = []
    
    try:
        results.append(("Add Sample Medicinal Plants", add_sample_medicinal_plants()))
        results.append(("Add Sample Ayurvedic Plants", add_sample_ayurvedic_plants()))
        results.append(("Add Sample Drugs", add_sample_drugs_with_reviews()))
        verify_database()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    for name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{name}: {status}")
    
    print("\n" + "="*70)
    print("✅ Sample data has been added to the database!")
    print("\n💡 Next steps:")
    print("   1. Test the system: python main.py")
    print("   2. Download Kaggle datasets when ready:")
    print("      • https://www.kaggle.com/datasets/jcanotorr/medicinal-plants-dataset")
    print("      • https://www.kaggle.com/datasets/hamagj/indian-medicinal-plants")
    print("      • https://www.kaggle.com/datasets/sanjaymat/drugs-review-dataset")
    print("      • https://www.kaggle.com/datasets/prathamikjain/medicine-recommendation-using-machine-learning")
    print("\n   3. Run integration: python src/integrate_medicinal_datasets.py")
    print("="*70 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
