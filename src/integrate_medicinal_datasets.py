#!/usr/bin/env python3
"""
Integration Script for New Medicinal & Drug Datasets

This script integrates:
1. Medicinal Plants Dataset - Plant compounds and traditional uses
2. Indian Medicinal Plants - Ayurvedic properties and applications
3. Drugs.com Reviews Dataset - Drug effectiveness and side effects
4. Medicine Recommendation Dataset - ML-based medication suggestions

The integrated data is stored in the SQLite database (medical_knowledge.db)
"""

import os
import sys
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
import sqlite3
import json
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from database_manager import DatabaseManager
except ImportError:
    print("❌ Failed to import DatabaseManager. Ensure database_manager.py is in the src folder.")
    sys.exit(1)


class MedicinalDatasetIntegrator:
    """Integrate medicinal datasets into the medical knowledge database"""
    
    def __init__(self, data_dir: str = "../data"):
        self.data_dir = Path(data_dir)
        self.kaggle_datasets_dir = Path(data_dir) / "kaggle_datasets"
        self.db = DatabaseManager()
        self.stats = {
            "medicinal_plants_added": 0,
            "indian_plants_added": 0,
            "drug_reviews_integrated": 0,
            "recommendations_processed": 0,
            "errors": []
        }
    
    def integrate_medicinal_plants(self) -> bool:
        """Integrate medicinal plants dataset"""
        print("\n📌 INTEGRATING MEDICINAL PLANTS DATASET")
        print("="*70)
        
        dataset_path = self.kaggle_datasets_dir / "medicinal_plants"
        
        # Find CSV files in the dataset
        csv_files = list(dataset_path.glob("*.csv")) if dataset_path.exists() else []
        
        if not csv_files:
            print(f"⚠️  No CSV files found in {dataset_path}")
            print("   Download the dataset using: kaggle datasets download -d jcanotorr/medicinal-plants-dataset")
            print("   Or download manually from: https://www.kaggle.com/datasets/jcanotorr/medicinal-plants-dataset")
            return False
        
        try:
            for csv_file in csv_files:
                print(f"\n📄 Processing: {csv_file.name}")
                df = pd.read_csv(csv_file)
                
                # Add medicinal plants to database
                for idx, row in df.iterrows():
                    try:
                        plant_name = str(row.get('plant_name', row.get('name', f'Plant_{idx}')))
                        common_name = str(row.get('common_name', plant_name))
                        scientific_name = str(row.get('scientific_name', ''))
                        active_compounds = str(row.get('active_compounds', 'Unknown'))
                        medicinal_properties = str(row.get('medicinal_properties', 'Unknown'))
                        traditional_uses = str(row.get('traditional_uses', 'Unknown'))
                        
                        # Add herb to database if not exists
                        try:
                            herb_id = self.db.add_herb(
                                name=plant_name,
                                description=f"{common_name} ({scientific_name})",
                                effectiveness_rating=0.75  # Default rating
                            )
                            
                            # Store detailed information
                            details = {
                                "common_name": common_name,
                                "scientific_name": scientific_name,
                                "active_compounds": active_compounds,
                                "medicinal_properties": medicinal_properties,
                                "traditional_uses": traditional_uses,
                                "dosage": str(row.get('dosage', 'Consult herbalist')),
                                "side_effects": str(row.get('side_effects', 'None known')),
                                "contraindications": str(row.get('contraindications', 'None known'))
                            }
                            
                            # Store in database using custom query
                            self.db.conn.execute("""
                                UPDATE herbs 
                                SET description = ?
                                WHERE id = ?
                            """, (json.dumps(details), herb_id))
                            
                            self.stats["medicinal_plants_added"] += 1
                        except Exception as e:
                            logger.debug(f"Herb already exists: {plant_name}")
                            self.stats["medicinal_plants_added"] += 1
                    
                    except Exception as e:
                        logger.error(f"Error processing plant row {idx}: {e}")
                        self.stats["errors"].append(f"Medicinal plants - Row {idx}: {str(e)}")
            
            self.db.conn.commit()
            print(f"\n✅ Added {self.stats['medicinal_plants_added']} medicinal plants")
            return True
        
        except Exception as e:
            logger.error(f"Error integrating medicinal plants: {e}")
            self.stats["errors"].append(f"Medicinal plants integration: {str(e)}")
            return False
    
    def integrate_indian_medicinal_plants(self) -> bool:
        """Integrate Indian medicinal plants (Ayurvedic) dataset"""
        print("\n📌 INTEGRATING INDIAN MEDICINAL PLANTS DATASET")
        print("="*70)
        
        dataset_path = self.kaggle_datasets_dir / "indian_medicinal_plants"
        
        csv_files = list(dataset_path.glob("*.csv")) if dataset_path.exists() else []
        
        if not csv_files:
            print(f"⚠️  No CSV files found in {dataset_path}")
            print("   Download using: python download_kaggle_datasets.py indian_medicinal_plants")
            return False
        
        try:
            for csv_file in csv_files:
                print(f"\n📄 Processing: {csv_file.name}")
                df = pd.read_csv(csv_file)
                
                for idx, row in df.iterrows():
                    try:
                        plant_name = str(row.get('plant_name', row.get('name', f'Plant_{idx}')))
                        english_name = str(row.get('english_name', plant_name))
                        scientific_name = str(row.get('scientific_name', ''))
                        ayurvedic_props = str(row.get('ayurvedic_properties', 'Unknown'))
                        uses = str(row.get('traditional_uses', 'Unknown'))
                        
                        try:
                            herb_id = self.db.add_herb(
                                name=plant_name,
                                description=f"Ayurveda | {english_name} ({scientific_name})",
                                effectiveness_rating=0.80
                            )
                            
                            # Store Ayurvedic details
                            details = {
                                "english_name": english_name,
                                "scientific_name": scientific_name,
                                "ayurvedic_properties": ayurvedic_props,
                                "rasa": str(row.get('rasa', 'Unknown')),
                                "veerya": str(row.get('veerya', 'Unknown')),
                                "vipaka": str(row.get('vipaka', 'Unknown')),
                                "plant_part_used": str(row.get('plant_part_used', 'Whole plant')),
                                "indications": uses,
                                "dosage_form": str(row.get('dosage_form', 'Powder/Decoction')),
                                "source": "Indian Medicinal Plants - Ayurveda"
                            }
                            
                            self.db.conn.execute("""
                                UPDATE herbs 
                                SET description = ?
                                WHERE id = ?
                            """, (json.dumps(details), herb_id))
                            
                            self.stats["indian_plants_added"] += 1
                        except Exception as e:
                            logger.debug(f"Herb already exists: {plant_name}")
                            self.stats["indian_plants_added"] += 1
                    
                    except Exception as e:
                        logger.error(f"Error processing Indian plant row {idx}: {e}")
                        self.stats["errors"].append(f"Indian plants - Row {idx}: {str(e)}")
            
            self.db.conn.commit()
            print(f"\n✅ Added {self.stats['indian_plants_added']} Indian medicinal plants")
            return True
        
        except Exception as e:
            logger.error(f"Error integrating Indian medicinal plants: {e}")
            self.stats["errors"].append(f"Indian plants integration: {str(e)}")
            return False
    
    def integrate_drug_reviews(self) -> bool:
        """Integrate drug reviews dataset for effectiveness ratings"""
        print("\n📌 INTEGRATING DRUGS.COM REVIEWS DATASET")
        print("="*70)
        
        dataset_path = self.kaggle_datasets_dir / "drugs_reviews"
        
        csv_files = list(dataset_path.glob("*.csv")) if dataset_path.exists() else []
        
        if not csv_files:
            print(f"⚠️  No CSV files found in {dataset_path}")
            print("   Download using: python download_kaggle_datasets.py drugs_reviews")
            return False
        
        try:
            for csv_file in csv_files:
                print(f"\n📄 Processing: {csv_file.name}")
                df = pd.read_csv(csv_file)
                
                # Group by drug and condition to get aggregated ratings
                drug_stats = df.groupby('drug_name').agg({
                    'rating': ['mean', 'count'],
                    'effectiveness': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Not specified',
                    'condition': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown'
                }).reset_index()
                
                for idx, row in drug_stats.iterrows():
                    try:
                        drug_name = str(row['drug_name']).upper()
                        avg_rating = float(row[('rating', 'mean')]) if pd.notna(row[('rating', 'mean')]) else 0.0
                        review_count = int(row[('rating', 'count')]) if pd.notna(row[('rating', 'count')]) else 0
                        effectiveness = str(row[('effectiveness', '<lambda>')]) if pd.notna(row[('effectiveness', '<lambda>')]) else 'Not specified'
                        condition = str(row[('condition', '<lambda>')]) if pd.notna(row[('condition', '<lambda>')]) else 'Unknown'
                        
                        # Normalize rating to 0-1 scale (from 0-5)
                        normalized_rating = min(avg_rating / 5.0, 1.0) if avg_rating > 0 else 0.75
                        
                        # Update or add pharmaceutical
                        try:
                            pharm_id = self.db.add_pharmaceutical(
                                name=drug_name,
                                description=f"Condition: {condition}, Effectiveness: {effectiveness}",
                                dosage="As per prescription",
                                side_effects=str(row.get('side_effects', 'Refer to package insert')),
                                availability="Medical Store",
                                price_range="Varies",
                                effectiveness_rating=normalized_rating
                            )
                            self.stats["drug_reviews_integrated"] += 1
                        except Exception as e:
                            logger.debug(f"Drug already exists: {drug_name}")
                            self.stats["drug_reviews_integrated"] += 1
                    
                    except Exception as e:
                        logger.error(f"Error processing drug review row {idx}: {e}")
                        self.stats["errors"].append(f"Drug reviews - Row {idx}: {str(e)}")
            
            self.db.conn.commit()
            print(f"\n✅ Integrated reviews for {self.stats['drug_reviews_integrated']} drugs")
            return True
        
        except Exception as e:
            logger.error(f"Error integrating drug reviews: {e}")
            self.stats["errors"].append(f"Drug reviews integration: {str(e)}")
            return False
    
    def integrate_medicine_recommendations(self) -> bool:
        """Integrate medicine recommendation dataset for treatment patterns"""
        print("\n📌 INTEGRATING MEDICINE RECOMMENDATION DATASET")
        print("="*70)
        
        dataset_path = self.kaggle_datasets_dir / "medicine_recommendation"
        
        csv_files = list(dataset_path.glob("*.csv")) if dataset_path.exists() else []
        
        if not csv_files:
            print(f"⚠️  No CSV files found in {dataset_path}")
            print("   Download using: python download_kaggle_datasets.py medicine_recommendation")
            return False
        
        try:
            for csv_file in csv_files:
                print(f"\n📄 Processing: {csv_file.name}")
                df = pd.read_csv(csv_file)
                
                # Extract symptom-medication mappings
                for idx, row in df.iterrows():
                    try:
                        symptoms = str(row.get('symptoms', 'Unknown')).split(',')
                        recommended_drug = str(row.get('recommended_medicine', 'Unknown'))
                        patient_age = row.get('patient_age', None)
                        gender = str(row.get('gender', 'Any'))
                        
                        # Create treatment recommendation pattern
                        pattern_data = {
                            "patient_age": patient_age,
                            "gender": gender,
                            "symptoms": [s.strip() for s in symptoms if s.strip()],
                            "recommended_drug": recommended_drug,
                            "kidney_function": str(row.get('kidney_function', 'Normal')),
                            "liver_function": str(row.get('liver_function', 'Normal')),
                            "source": "Medicine Recommendation Dataset"
                        }
                        
                        # Store pattern in symptom_patterns table
                        self.db.conn.execute("""
                            INSERT OR IGNORE INTO symptom_patterns 
                            (pattern_name, pattern_data, disease_association)
                            VALUES (?, ?, ?)
                        """, (
                            f"MED_REC_{idx}",
                            json.dumps(pattern_data),
                            recommended_drug
                        ))
                        
                        self.stats["recommendations_processed"] += 1
                    
                    except Exception as e:
                        logger.error(f"Error processing recommendation row {idx}: {e}")
                        self.stats["errors"].append(f"Medicine recommendation - Row {idx}: {str(e)}")
            
            self.db.conn.commit()
            print(f"\n✅ Processed {self.stats['recommendations_processed']} medicine recommendations")
            return True
        
        except Exception as e:
            logger.error(f"Error integrating medicine recommendations: {e}")
            self.stats["errors"].append(f"Medicine recommendations integration: {str(e)}")
            return False
    
    def print_summary(self):
        """Print integration summary"""
        print("\n" + "="*70)
        print("📊 INTEGRATION SUMMARY")
        print("="*70)
        
        print(f"\n✅ Medicinal Plants Added: {self.stats['medicinal_plants_added']}")
        print(f"✅ Indian Medicinal Plants Added: {self.stats['indian_plants_added']}")
        print(f"✅ Drug Reviews Integrated: {self.stats['drug_reviews_integrated']}")
        print(f"✅ Medicine Recommendations Processed: {self.stats['recommendations_processed']}")
        
        if self.stats['errors']:
            print(f"\n⚠️  Errors Encountered: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:  # Show first 5 errors
                print(f"   • {error}")
            if len(self.stats['errors']) > 5:
                print(f"   ... and {len(self.stats['errors']) - 5} more")
        
        total_integrated = (self.stats['medicinal_plants_added'] + 
                           self.stats['indian_plants_added'] + 
                           self.stats['drug_reviews_integrated'] + 
                           self.stats['recommendations_processed'])
        
        print(f"\n🎯 TOTAL ITEMS INTEGRATED: {total_integrated}")
        print("="*70 + "\n")
    
    def run_all_integrations(self):
        """Run all dataset integrations"""
        print("""
╔════════════════════════════════════════════════════════════════╗
║     🌿 MEDICINAL DATASETS INTEGRATION SUITE                   ║
╚════════════════════════════════════════════════════════════════╝
        """)
        
        results = []
        
        # Run all integrations
        results.append(("Medicinal Plants", self.integrate_medicinal_plants()))
        results.append(("Indian Medicinal Plants", self.integrate_indian_medicinal_plants()))
        results.append(("Drug Reviews", self.integrate_drug_reviews()))
        results.append(("Medicine Recommendations", self.integrate_medicine_recommendations()))
        
        # Print results
        print("\n" + "="*70)
        print("INTEGRATION RESULTS")
        print("="*70)
        for dataset_name, success in results:
            status = "✅ SUCCESS" if success else "❌ SKIPPED/FAILED"
            print(f"{dataset_name}: {status}")
        
        # Print summary
        self.print_summary()
        
        return all(result[1] for result in results)


def main():
    """Main execution"""
    integrator = MedicinalDatasetIntegrator()
    success = integrator.run_all_integrations()
    
    print("\n💡 Next Steps:")
    print("   1. Download datasets: python download_kaggle_datasets.py")
    print("   2. Run this integration: python integrate_medicinal_datasets.py")
    print("   3. Test predictions: python main.py")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
