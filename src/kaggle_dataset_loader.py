#!/usr/bin/env python3
"""
Kaggle Dataset Loader
Handles downloading and integrating all Kaggle medical datasets
"""

import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KaggleDatasetLoader:
    """Load and integrate Kaggle datasets for medical conditions"""
    
    # Kaggle dataset configurations
    KAGGLE_DATASETS = {
        "diabetes": {
            "kaggle_id": "uciml/pima-indians-diabetes-database",
            "description": "Diabetes prediction dataset from Pima Indian population",
            "diseases": ["Diabetes"],
            "file": "diabetes.csv",
            "target_column": "Outcome",
            "condition_value": 1
        },
        "heart_disease": {
            "kaggle_id": "datasets/johnsmith88/heart-disease-dataset",
            "description": "Heart disease dataset",
            "diseases": ["Heart Disease", "Hypertension"],
            "file": "heart.csv",
            "target_column": "target",
            "condition_value": 1
        },
        "respiratory": {
            "kaggle_id": "datasets/ayushggarg/asthma-disease-data-set",
            "description": "Respiratory/Asthma disease dataset",
            "diseases": ["Asthma", "Bronchitis", "COPD"],
            "file": "respiratory_disease_survey_data.csv",
            "target_column": "Disease",
            "condition_value": 1
        },
        "mental_health": {
            "kaggle_id": "datasets/osmi/mental-health-in-tech-survey",
            "description": "Mental health in tech industry survey",
            "diseases": ["Depression", "Anxiety", "Stress"],
            "file": "survey.csv",
            "target_column": "mental_health_consequence",
            "condition_value": "Yes"
        },
        "covid19": {
            "kaggle_id": "datasets/allen-institute-for-ai/CORD-19-research-challenge",
            "description": "COVID-19 research dataset",
            "diseases": ["COVID-19", "Pneumonia"],
            "file": "metadata.csv",
            "target_column": "severity",
            "condition_value": None  # Variable
        },
        "medicinal_plants": {
            "kaggle_id": "datasets/jcanotorr/medicinal-plants-dataset",
            "description": "Comprehensive medicinal plants database",
            "diseases": ["Herbal_Medicine"],
            "file": "medicinal_plants.csv",
            "target_column": "medicinal_classification",
            "condition_value": None
        },
        "indian_medicinal_plants": {
            "kaggle_id": "datasets/hamagj/indian-medicinal-plants",
            "description": "Indian medicinal plants with Ayurvedic properties",
            "diseases": ["Ayurveda"],
            "file": "indian_medicinal_plants_dataset.csv",
            "target_column": "ayurvedic_category",
            "condition_value": None
        },
        "drug_reviews": {
            "kaggle_id": "datasets/sanjaymat/drugs-review-dataset",
            "description": "Drug reviews with effectiveness ratings",
            "diseases": ["Drug_Effectiveness"],
            "file": "drugsComTrain_raw.tsv",
            "target_column": "rating",
            "condition_value": None
        },
        "liver_disease": {
            "kaggle_id": "datasets/uciml/indian-liver-patient-records",
            "description": "Indian liver patient records",
            "diseases": ["Liver Disease"],
            "file": "indian_liver_patient.csv",
            "target_column": "Dataset",
            "condition_value": 1
        },
        "cancer": {
            "kaggle_id": "datasets/uciml/breast-cancer-wisconsin-data",
            "description": "Breast cancer dataset",
            "diseases": ["Breast Cancer"],
            "file": "data.csv",
            "target_column": "diagnosis",
            "condition_value": "M"  # Malignant
        },
        "skin_disease": {
            "kaggle_id": "datasets/nodoubttome/skin-disease-image-dataset",
            "description": "Skin disease image dataset",
            "diseases": ["Skin Disease"],
            "file": "skin_disease_dataset.csv",
            "target_column": "class",
            "condition_value": None
        },
        "medicine_recommendation": {
            "kaggle_id": "datasets/prathamikjain/medicine-recommendation-using-machine-learning",
            "description": "Medicine recommendation dataset",
            "diseases": ["Medicine_Recommendation"],
            "file": "medicine_recommendation_dataset.csv",
            "target_column": "recommended_medicine",
            "condition_value": None
        }
    }
    
    def __init__(self, base_dir: str = "data"):
        """Initialize Kaggle dataset loader"""
        self.base_dir = Path(base_dir)
        self.kaggle_dir = self.base_dir / "kaggle_datasets"
        self.kaggle_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.kaggle_dir / "kaggle_metadata.json"
        self.cache = {}
        self._load_metadata()
        logger.info(f"Initialized KaggleDatasetLoader with base_dir: {self.base_dir}")
    
    def _load_metadata(self):
        """Load existing metadata"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
                logger.info("Loaded existing metadata")
            except Exception as e:
                logger.warning(f"Could not load metadata: {e}")
                self.metadata = {}
        else:
            self.metadata = {}
    
    def _save_metadata(self):
        """Save metadata"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save metadata: {e}")
    
    def get_download_status(self) -> Dict[str, bool]:
        """Get status of all Kaggle datasets"""
        status = {}
        for dataset_name, info in self.KAGGLE_DATASETS.items():
            dataset_dir = self.kaggle_dir / dataset_name
            is_downloaded = dataset_dir.exists() and any(dataset_dir.glob("*.*"))
            status[dataset_name] = is_downloaded
        return status
    
    def get_download_instructions(self) -> str:
        """Get instructions for downloading Kaggle datasets"""
        instructions = """
🔗 KAGGLE DATASETS - DOWNLOAD INSTRUCTIONS

1. Setup Kaggle API (one-time):
   a) Go to https://www.kaggle.com/settings/account
   b) Click "Create New API Token" (downloads kaggle.json)
   c) Place in ~/.kaggle/kaggle.json
   d) chmod 600 ~/.kaggle/kaggle.json

2. Install kaggle CLI:
   pip install kaggle

3. Download individual datasets:
"""
        for name, info in self.KAGGLE_DATASETS.items():
            instructions += f"   kaggle datasets download -d {info['kaggle_id']} -p data/kaggle_datasets/{name}/\n"
        
        instructions += """
4. Extract datasets:
   cd data/kaggle_datasets
   for dir in */; do unzip -q "$dir"*.zip -d "$dir"; done
   rm -rf */*.zip

5. Or download all at once:
   python src/kaggle_dataset_loader.py
"""
        return instructions
    
    def load_dataset(self, dataset_name: str) -> Optional[pd.DataFrame]:
        """Load a specific Kaggle dataset"""
        if dataset_name not in self.KAGGLE_DATASETS:
            logger.error(f"Unknown dataset: {dataset_name}")
            return None
        
        # Check cache
        if dataset_name in self.cache:
            logger.info(f"Loading {dataset_name} from cache")
            return self.cache[dataset_name]
        
        info = self.KAGGLE_DATASETS[dataset_name]
        dataset_dir = self.kaggle_dir / dataset_name
        
        # Look for the data file
        data_file = dataset_dir / info['file']
        
        if not data_file.exists():
            # Try to find any CSV file
            csv_files = list(dataset_dir.glob("*.csv"))
            tsv_files = list(dataset_dir.glob("*.tsv"))
            all_files = csv_files + tsv_files
            
            if all_files:
                data_file = all_files[0]
                logger.warning(f"Using alternative file: {data_file}")
            else:
                logger.error(f"Dataset file not found: {data_file}")
                return None
        
        try:
            # Load based on file type
            if str(data_file).endswith('.tsv'):
                df = pd.read_csv(data_file, sep='\t')
            else:
                df = pd.read_csv(data_file)
            
            logger.info(f"Loaded {dataset_name}: {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Cache it
            self.cache[dataset_name] = df
            
            # Update metadata
            if dataset_name not in self.metadata:
                self.metadata[dataset_name] = {
                    "description": info["description"],
                    "diseases": info["diseases"],
                    "n_rows": len(df),
                    "n_columns": len(df.columns),
                    "loaded_at": pd.Timestamp.now().isoformat()
                }
                self._save_metadata()
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to load {dataset_name}: {e}")
            return None
    
    def get_medicinal_plants(self) -> Optional[pd.DataFrame]:
        """Load medicinal plants dataset"""
        df = self.load_dataset("medicinal_plants")
        if df is not None:
            return df
        
        # Try Indian medicinal plants
        df = self.load_dataset("indian_medicinal_plants")
        return df
    
    def get_disease_data(self, disease: str) -> Optional[pd.DataFrame]:
        """Get data for a specific disease"""
        for dataset_name, info in self.KAGGLE_DATASETS.items():
            if disease in info['diseases']:
                return self.load_dataset(dataset_name)
        return None
    
    def get_all_diseases_from_kaggle(self) -> List[str]:
        """Get all diseases available from Kaggle datasets"""
        diseases = set()
        for info in self.KAGGLE_DATASETS.values():
            diseases.update(info['diseases'])
        return sorted(list(diseases))
    
    def get_dataset_summary(self) -> Dict:
        """Get summary of Kaggle datasets"""
        status = self.get_download_status()
        
        summary = {
            "total_datasets": len(self.KAGGLE_DATASETS),
            "downloaded": sum(1 for v in status.values() if v),
            "datasets": {}
        }
        
        for name, info in self.KAGGLE_DATASETS.items():
            summary["datasets"][name] = {
                "description": info["description"],
                "diseases": info["diseases"],
                "downloaded": status[name],
                "kaggle_id": info["kaggle_id"]
            }
        
        return summary
    
    def list_available_datasets(self) -> Dict:
        """List all available Kaggle datasets"""
        return self.KAGGLE_DATASETS.copy()
    
    def extract_symptoms_from_dataset(self, dataset_name: str) -> List[str]:
        """Extract symptom columns from a dataset"""
        df = self.load_dataset(dataset_name)
        if df is None:
            return []
        
        # Try to identify symptom columns (exclude IDs, targets, etc.)
        exclude_keywords = ['id', 'target', 'disease', 'class', 'outcome', 'diagnosis']
        symptom_cols = [col for col in df.columns 
                       if not any(kw in col.lower() for kw in exclude_keywords)]
        
        return symptom_cols[:10]  # Return top 10


def main():
    """Test Kaggle dataset loader"""
    print("=" * 70)
    print("🔗 KAGGLE DATASET LOADER TEST")
    print("=" * 70 + "\n")
    
    loader = KaggleDatasetLoader()
    
    # Test 1: Check download status
    print("Test 1: Download Status")
    print("-" * 70)
    status = loader.get_download_status()
    for name, is_downloaded in status.items():
        emoji = "✅" if is_downloaded else "❌"
        print(f"  {emoji} {name}: {'Downloaded' if is_downloaded else 'Not downloaded'}")
    print()
    
    # Test 2: List available datasets
    print("Test 2: Available Datasets")
    print("-" * 70)
    datasets = loader.list_available_datasets()
    print(f"Total datasets available: {len(datasets)}")
    print("Datasets:")
    for name, info in list(datasets.items())[:5]:
        print(f"  • {name}: {info['description'][:50]}...")
    print()
    
    # Test 3: Get all diseases from Kaggle
    print("Test 3: Available Diseases from Kaggle")
    print("-" * 70)
    diseases = loader.get_all_diseases_from_kaggle()
    print(f"Total diseases: {len(diseases)}")
    print(f"Diseases: {', '.join(diseases)}")
    print()
    
    # Test 4: Summary
    print("Test 4: Dataset Summary")
    print("-" * 70)
    summary = loader.get_dataset_summary()
    print(f"Total datasets: {summary['total_datasets']}")
    print(f"Downloaded: {summary['downloaded']}")
    print(f"Coverage: {summary['downloaded']}/{summary['total_datasets']} datasets")
    print()
    
    # Test 5: Download instructions
    print("Test 5: Download Instructions")
    print("-" * 70)
    print(loader.get_download_instructions())
    
    print("\n" + "=" * 70)
    print("✅ Kaggle Dataset Loader Ready!")
    print("=" * 70)


if __name__ == "__main__":
    main()
