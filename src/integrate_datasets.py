#!/usr/bin/env python3
"""
Dataset Integration System - Process and integrate Kaggle datasets into the herbal medicine system
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import joblib
import os

class DatasetIntegrator:
    """Integrate multiple Kaggle datasets into the system"""
    
    def __init__(self, data_dir: str = "data/kaggle_datasets"):
        self.data_dir = Path(data_dir)
        self.output_dir = Path("data/integrated_datasets")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process_diabetes_dataset(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Process Pima Indians Diabetes dataset"""
        
        # Map to standard format
        disease_mapping = {
            0: "Normal",
            1: "Diabetes"
        }
        
        symptoms = [
            "High blood sugar",
            "Frequent urination",
            "Increased thirst",
            "Weight loss",
            "Fatigue",
            "Slow healing",
            "Blurred vision"
        ]
        
        # Create symptom-disease pairs
        pairs = []
        for idx, row in df.iterrows():
            disease = disease_mapping.get(row.iloc[-1], "Diabetes")
            
            # Create features-based symptoms
            if row['Glucose'] > 126:
                pairs.append(("High blood sugar", disease))
            if row['BMI'] > 30:
                pairs.append(("Weight-related issues", disease))
            if row['Age'] > 40:
                pairs.append(("Age-related risk", disease))
        
        return pd.DataFrame(pairs, columns=['symptom', 'disease']), {
            "n_samples": len(df),
            "n_features": len(df.columns) - 1,
            "diseases": list(set(disease_mapping.values()))
        }
    
    def process_heart_disease_dataset(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Process Heart Disease dataset"""
        
        symptoms = [
            "Chest pain",
            "Shortness of breath",
            "Heart palpitations",
            "Fatigue",
            "Dizziness",
            "High blood pressure",
            "Irregular heartbeat"
        ]
        
        disease_mapping = {
            0: "Normal",
            1: "Heart Disease"
        }
        
        # Create symptom pairs
        pairs = []
        target_col = df.columns[-1]
        
        for idx, row in df.iterrows():
            disease = disease_mapping.get(int(row[target_col]), "Heart Disease")
            
            if row['cp'] > 0:  # Chest pain type
                pairs.append(("Chest pain", disease))
            if row['trestbps'] > 140:  # Resting blood pressure
                pairs.append(("High blood pressure", disease))
            if row['chol'] > 240:  # Cholesterol
                pairs.append(("High cholesterol", disease))
        
        return pd.DataFrame(pairs, columns=['symptom', 'disease']), {
            "n_samples": len(df),
            "n_features": len(df.columns) - 1,
            "diseases": list(set(disease_mapping.values()))
        }
    
    def process_asthma_dataset(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Process Asthma/Respiratory dataset"""
        
        symptoms = [
            "Shortness of breath",
            "Wheezing",
            "Chest tightness",
            "Cough",
            "Rapid breathing",
            "Difficulty sleeping",
            "Chest pain during breathing"
        ]
        
        pairs = []
        
        for idx, row in df.iterrows():
            disease = "Asthma"
            
            if 'Lung_function' in row and row['Lung_function'] < 70:
                pairs.append(("Shortness of breath", disease))
            if 'Smoking_status' in row and row['Smoking_status'] > 0:
                pairs.append(("Persistent cough", disease))
            if 'Air_pollution' in row and row['Air_pollution'] > 5:
                pairs.append(("Pollution-related symptoms", disease))
        
        return pd.DataFrame(pairs, columns=['symptom', 'disease']), {
            "n_samples": len(df),
            "n_features": len(df.columns),
            "diseases": ["Asthma", "Respiratory Disease"]
        }
    
    def integrate_all_datasets(self):
        """Integrate all downloaded datasets"""
        
        print("""
╔════════════════════════════════════════════════════════════════╗
║         🔗 DATASET INTEGRATION SYSTEM                         ║
╚════════════════════════════════════════════════════════════════╝
        """)
        
        dataset_files = list(self.data_dir.glob("*//*.csv")) + list(self.data_dir.glob("*.csv"))
        
        if not dataset_files:
            print("⚠️  No datasets found in", self.data_dir)
            return
        
        all_symptoms = []
        all_diseases = set()
        
        for dataset_file in dataset_files:
            print(f"\n📊 Processing {dataset_file.name}...")
            
            try:
                df = pd.read_csv(dataset_file)
                
                # Process based on filename
                filename = dataset_file.stem.lower()
                
                if 'diabetes' in filename:
                    symptoms_df, stats = self.process_diabetes_dataset(df)
                elif 'heart' in filename:
                    symptoms_df, stats = self.process_heart_disease_dataset(df)
                elif 'asthma' in filename or 'respiratory' in filename:
                    symptoms_df, stats = self.process_asthma_dataset(df)
                else:
                    print(f"   ⚠️  Unknown dataset format, skipping")
                    continue
                
                all_symptoms.extend(symptoms_df.values.tolist())
                all_diseases.update(stats['diseases'])
                
                print(f"   ✅ Processed {len(symptoms_df)} symptom-disease pairs")
                print(f"   📌 Diseases: {', '.join(stats['diseases'])}")
            
            except Exception as e:
                print(f"   ❌ Error processing {dataset_file}: {str(e)}")
        
        if all_symptoms:
            # Save integrated dataset
            integrated_df = pd.DataFrame(all_symptoms, columns=['symptom', 'disease'])
            output_file = self.output_dir / "integrated_symptoms.csv"
            integrated_df.to_csv(output_file, index=False)
            
            print(f"\n✅ Integrated Dataset Summary")
            print(f"   Total symptom-disease pairs: {len(integrated_df)}")
            print(f"   Unique diseases: {len(all_diseases)}")
            print(f"   Diseases: {', '.join(sorted(all_diseases))}")
            print(f"   Saved to: {output_file}")
            
            return integrated_df
        else:
            print("⚠️  No symptoms extracted from datasets")
            return None


def create_enhanced_knowledge_base():
    """Create enhanced knowledge base with multiple datasets"""
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║       📚 CREATING ENHANCED KNOWLEDGE BASE                     ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    integrator = DatasetIntegrator()
    
    # Integrate datasets
    integrated_df = integrator.integrate_all_datasets()
    
    if integrated_df is not None:
        print("\n✨ Enhanced knowledge base created successfully!")
        print(f"   Ready to use with the herbal medicine system")
    else:
        print("\n⚠️  No datasets to integrate")


if __name__ == "__main__":
    create_enhanced_knowledge_base()
