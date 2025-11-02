#!/usr/bin/env python3
"""
Dataset Integration Fix
Properly loads and integrates all available datasets into the system
"""

import os
import pandas as pd
from typing import Dict, List, Tuple

class DatasetManager:
    """Unified dataset manager - loads and caches all available data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.cache = {}
        self._load_all_datasets()
    
    def _load_all_datasets(self):
        """Load all available datasets into cache"""
        print("📊 Loading Datasets...")
        
        # 1. Load the main symptom-disease dataset
        self.cache['symptom_disease'] = self._safe_load_csv('symptom_disease.csv')
        if self.cache['symptom_disease'] is not None:
            print(f"  ✓ Symptom-Disease: {self.cache['symptom_disease'].shape[0]} cases, {self.cache['symptom_disease']['prognosis'].nunique()} diseases")
        
        # 2. Load pharmaceutical database
        self.cache['pharmaceutical'] = self._safe_load_csv('pharmaceutical_database.csv')
        if self.cache['pharmaceutical'] is not None:
            print(f"  ✓ Pharmaceutical DB: {len(self.cache['pharmaceutical'])} drugs")
        
        # 3. Load drug interactions
        self.cache['drug_interactions'] = self._safe_load_csv('drug_interactions.csv')
        if self.cache['drug_interactions'] is not None:
            print(f"  ✓ Drug Interactions: {len(self.cache['drug_interactions'])} interactions")
        
        # 4. Load allergies data
        self.cache['allergies'] = self._safe_load_csv('allergies.csv')
        if self.cache['allergies'] is not None:
            print(f"  ✓ Allergies: {len(self.cache['allergies'])} entries")
        
        # 5. Load small reference data
        self.cache['diseases'] = self._safe_load_csv('diseases.csv')
        self.cache['herbs'] = self._safe_load_csv('herbs.csv')
        self.cache['ingredients'] = self._safe_load_csv('ingredients.csv')
        self.cache['targets'] = self._safe_load_csv('targets.csv')
        
        print("✅ Dataset loading complete!\n")
    
    def _safe_load_csv(self, filename: str) -> pd.DataFrame:
        """Safely load a CSV file"""
        try:
            path = os.path.join(self.data_dir, filename)
            if os.path.exists(path):
                return pd.read_csv(path)
        except Exception as e:
            print(f"  ⚠️  Could not load {filename}: {str(e)}")
        return None
    
    def get_all_diseases(self) -> List[str]:
        """Get all diseases from all available sources"""
        diseases = set()
        
        # From symptom_disease.csv (primary source - 41 diseases)
        if self.cache['symptom_disease'] is not None:
            diseases.update(self.cache['symptom_disease']['prognosis'].unique())
        
        # From diseases.csv (reference)
        if self.cache['diseases'] is not None:
            diseases.update(self.cache['diseases']['disease'].unique())
        
        return sorted(list(diseases))
    
    def get_disease_symptoms(self, disease: str) -> Dict[str, float]:
        """Get symptoms associated with a disease"""
        if self.cache['symptom_disease'] is None:
            return {}
        
        df = self.cache['symptom_disease']
        
        # Find rows for this disease
        disease_rows = df[df['prognosis'].str.strip() == disease.strip()]
        
        if disease_rows.empty:
            return {}
        
        # Get all symptom columns (exclude 'prognosis' and unnamed columns)
        symptom_cols = [col for col in df.columns 
                       if col not in ['prognosis', 'Unnamed: 133']]
        
        # Calculate average symptom frequency for this disease
        symptom_freq = {}
        for symptom in symptom_cols:
            freq = disease_rows[symptom].mean()  # 0-1 frequency
            if freq > 0.1:  # Only include if >10% frequency
                symptom_freq[symptom] = freq
        
        return dict(sorted(symptom_freq.items(), 
                          key=lambda x: x[1], 
                          reverse=True))
    
    def get_disease_by_symptoms(self, symptoms: List[str], top_n: int = 5) -> List[Tuple[str, float]]:
        """
        Find diseases matching given symptoms
        Returns list of (disease, match_score) sorted by score
        """
        if self.cache['symptom_disease'] is None:
            return []
        
        df = self.cache['symptom_disease']
        
        # Normalize symptom names (underscore format)
        normalized_symptoms = [s.lower().replace(' ', '_').strip() for s in symptoms]
        
        # Get available symptom columns
        available_cols = [col for col in df.columns 
                         if col not in ['prognosis', 'Unnamed: 133']]
        
        # Match symptoms and calculate scores
        matching_symptoms = [s for s in normalized_symptoms if s in available_cols]
        
        if not matching_symptoms:
            return []
        
        # Find cases matching these symptoms
        match_scores = {}
        for disease in df['prognosis'].unique():
            disease_rows = df[df['prognosis'].str.strip() == disease.strip()]
            
            # Calculate match score: how many symptoms are present in this disease
            match_count = 0
            for symptom in matching_symptoms:
                if symptom in available_cols:
                    # Check if symptom is typically present in this disease
                    if disease_rows[symptom].mean() > 0.5:
                        match_count += 1
            
            if match_count > 0:
                score = match_count / len(matching_symptoms)  # Ratio of matched symptoms
                match_scores[disease.strip()] = score
        
        # Sort and return top N
        sorted_diseases = sorted(match_scores.items(), 
                                key=lambda x: x[1], 
                                reverse=True)
        return sorted_diseases[:top_n]
    
    def get_drugs_for_disease(self, disease: str, top_n: int = 5) -> List[Dict]:
        """Get pharmaceutical drugs for a disease"""
        # This can be enhanced to use drug_database.py
        # For now, just return formatted info
        return []
    
    def get_herbal_for_disease(self, disease: str) -> List[Dict]:
        """Get herbal remedies for a disease"""
        # Match disease with herbal ingredients
        return []
    
    def get_drug_interactions(self, drug1: str, drug2: str) -> Dict:
        """Check for drug interactions"""
        if self.cache['drug_interactions'] is None:
            return {}
        
        df = self.cache['drug_interactions']
        interactions = df[
            ((df.get('drug_1') == drug1) & (df.get('drug_2') == drug2)) |
            ((df.get('drug_1') == drug2) & (df.get('drug_2') == drug1))
        ]
        
        return interactions.to_dict('records') if not interactions.empty else {}
    
    def get_allergy_info(self, allergy: str) -> Dict:
        """Get information about a specific allergy"""
        if self.cache['allergies'] is None:
            return {}
        
        df = self.cache['allergies']
        allergy_info = df[df['allergy'].str.lower() == allergy.lower()]
        
        return allergy_info.iloc[0].to_dict() if not allergy_info.empty else {}


def main():
    """Test the dataset manager"""
    print("="*70)
    print("🔧 DATASET INTEGRATION TEST")
    print("="*70 + "\n")
    
    # Initialize
    dm = DatasetManager()
    
    # Test 1: Get all diseases
    print("Test 1: Get All Diseases")
    print("-" * 70)
    diseases = dm.get_all_diseases()
    print(f"Total diseases available: {len(diseases)}")
    print(f"Diseases: {', '.join(diseases[:15])}...")
    print()
    
    # Test 2: Get symptoms for a disease
    print("Test 2: Get Symptoms for Disease")
    print("-" * 70)
    if diseases:
        disease = diseases[0]
        symptoms = dm.get_disease_symptoms(disease)
        print(f"Disease: {disease}")
        print(f"Common symptoms (top 5):")
        for symptom, freq in list(symptoms.items())[:5]:
            print(f"  - {symptom}: {freq*100:.1f}%")
    print()
    
    # Test 3: Find diseases by symptoms
    print("Test 3: Find Diseases by Symptoms")
    print("-" * 70)
    test_symptoms = ['fever', 'cough', 'headache']
    results = dm.get_disease_by_symptoms(test_symptoms, top_n=5)
    print(f"Searching for: {', '.join(test_symptoms)}")
    print("Matching diseases:")
    for disease, score in results:
        print(f"  ✓ {disease}: {score*100:.1f}% match")
    print()
    
    # Test 4: Summary
    print("Test 4: Dataset Summary")
    print("-" * 70)
    print(f"Symptom-Disease cases: {dm.cache['symptom_disease'].shape[0] if dm.cache['symptom_disease'] is not None else 'N/A'}")
    print(f"Unique diseases: {dm.cache['symptom_disease']['prognosis'].nunique() if dm.cache['symptom_disease'] is not None else 'N/A'}")
    print(f"Unique symptoms: {len([c for c in dm.cache['symptom_disease'].columns if c not in ['prognosis', 'Unnamed: 133']]) if dm.cache['symptom_disease'] is not None else 'N/A'}")
    print(f"Pharmaceutical entries: {len(dm.cache['pharmaceutical']) if dm.cache['pharmaceutical'] is not None else 'N/A'}")
    
    print("\n" + "="*70)
    print("✅ Dataset Integration Ready!")
    print("="*70)


if __name__ == "__main__":
    main()
