"""
Kaggle Dataset Manager - Download and integrate multiple medical datasets

Features:
  • Manages 8 major disease datasets from Kaggle
  • Tracks dataset download and integration status
  • Provides disease-to-dataset mapping
  • Handles errors gracefully with detailed messages
  • Persistent metadata tracking
"""

import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import requests
import logging
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class KaggleDatasetManager:
    """Manage multiple Kaggle datasets for medical conditions"""
    
    # Available Kaggle datasets for diseases
    AVAILABLE_DATASETS = {
        "diabetes": {
            "kaggle_id": "uciml/pima-indians-diabetes-database",
            "description": "Diabetes prediction dataset",
            "diseases": ["Diabetes"],
            "features": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", 
                        "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
            "target": "Outcome"
        },
        "heart_disease": {
            "kaggle_id": "datasets/johnsmith88/heart-disease-dataset",
            "description": "Heart disease classification dataset",
            "diseases": ["Heart Disease", "Heart Attack"],
            "features": ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
                        "thalach", "exang", "oldpeak", "slope", "ca", "thal"],
            "target": "target"
        },
        "respiratory": {
            "kaggle_id": "datasets/ayushggarg/asthma-disease-data-set",
            "description": "Respiratory disease dataset",
            "diseases": ["Asthma", "Bronchitis", "COPD"],
            "features": ["Lung_function", "Smoking_status", "Air_pollution", 
                        "Genetic_risk", "Balanced_diet", "Adequate_sleep", "Pollution_exposure"],
            "target": "Disease"
        },
        "mental_health": {
            "kaggle_id": "datasets/osmi/mental-health-in-tech-survey",
            "description": "Mental health and tech industry dataset",
            "diseases": ["Depression", "Anxiety", "Stress"],
            "features": ["Age", "Gender", "Country", "self_employed", "family_history", 
                        "treatment", "work_interfere"],
            "target": "mental_health_consequence"
        },
        "covid19": {
            "kaggle_id": "datasets/allen-institute-for-ai/CORD-19-research-challenge",
            "description": "COVID-19 research dataset",
            "diseases": ["COVID-19", "Pneumonia"],
            "features": ["symptoms", "severity", "age", "comorbidities"],
            "target": "severity"
        },
        "skin_disease": {
            "kaggle_id": "datasets/nodoubttome/skin-disease-image-dataset",
            "description": "Skin disease image dataset",
            "diseases": ["Melanoma", "Psoriasis", "Eczema"],
            "features": ["image_path", "color", "texture", "size"],
            "target": "disease_type"
        },
        "liver_disease": {
            "kaggle_id": "datasets/uciml/indian-liver-patient-records",
            "description": "Liver disease dataset",
            "diseases": ["Liver Disease", "Hepatitis"],
            "features": ["Age", "Gender", "Total_Bilirubin", "Direct_Bilirubin", 
                        "Alkaline_Phosphotase", "Alamine_Aminotransferase", 
                        "Aspartate_Aminotransferase", "Total_Protiens", "Albumin", 
                        "Albumin_and_Globulin_Ratio"],
            "target": "Dataset"
        },
        "cancer": {
            "kaggle_id": "datasets/uciml/breast-cancer-wisconsin-data",
            "description": "Cancer (breast) prediction dataset",
            "diseases": ["Breast Cancer", "Malignant Tumor"],
            "features": ["radius_mean", "texture_mean", "perimeter_mean", "area_mean", 
                        "smoothness_mean", "compactness_mean", "concavity_mean"],
            "target": "diagnosis"
        },
        "medicinal_plants": {
            "kaggle_id": "datasets/jcanotorr/medicinal-plants-dataset",
            "description": "Comprehensive medicinal plants dataset with properties, uses, and active compounds",
            "diseases": ["Herbal_Treatment", "Natural_Remedies", "Plant_Based_Medicine"],
            "features": ["plant_name", "common_name", "scientific_name", "plant_family", 
                        "active_compounds", "medicinal_properties", "traditional_uses", 
                        "preparation_methods", "dosage", "side_effects", "contraindications"],
            "target": "medicinal_classification"
        },
        "indian_medicinal_plants": {
            "kaggle_id": "datasets/hamagj/indian-medicinal-plants",
            "description": "Indian medicinal plants database with Ayurvedic properties and uses",
            "diseases": ["Ayurveda", "Traditional_Medicine", "Herbal_Remedies"],
            "features": ["plant_name", "english_name", "hindi_name", "scientific_name", 
                        "plant_part_used", "ayurvedic_properties", "rasa", "veerya", "vipaka",
                        "traditional_uses", "dosage_form", "indications"],
            "target": "ayurvedic_category"
        },
        "drugs_reviews": {
            "kaggle_id": "datasets/sanjaymat/drugs-review-dataset",
            "description": "Comprehensive drug reviews dataset with ratings and effectiveness data",
            "diseases": ["Drug_Reviews", "Medication_Effectiveness", "Patient_Feedback"],
            "features": ["drug_name", "condition", "review", "rating", "date", "useful_count",
                        "effectiveness", "side_effects_reported", "user_experience"],
            "target": "effectiveness_rating"
        },
        "medicine_recommendation": {
            "kaggle_id": "datasets/prathamikjain/medicine-recommendation-using-machine-learning",
            "description": "Medicine recommendation dataset with patient conditions and optimal medications",
            "diseases": ["Multi_Disease", "Medication_Recommendation", "Clinical_Decision"],
            "features": ["patient_age", "gender", "symptoms", "medical_history", "allergies",
                        "current_medications", "kidney_function", "liver_function", 
                        "blood_pressure", "diabetes_status"],
            "target": "recommended_medicine"
        }
    }
    
    def __init__(self, data_dir: str = "data/kaggle_datasets"):
        """Initialize the dataset manager"""
        self.data_dir = Path(data_dir)
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Initialized dataset manager with data_dir: {self.data_dir}")
        except Exception as e:
            logger.error(f"Failed to create data directory: {e}")
            raise
        
        self.metadata_file = self.data_dir / "dataset_metadata.json"
        self.load_metadata()
    
    def load_metadata(self):
        """Load existing metadata"""
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
                logger.debug(f"Loaded metadata for {len(self.metadata)} datasets")
            else:
                self.metadata = {}
                logger.debug("No existing metadata found, starting fresh")
        except Exception as e:
            logger.warning(f"Failed to load metadata: {e}. Starting with empty metadata.")
            self.metadata = {}
    
    def save_metadata(self):
        """Save metadata to file"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            logger.debug(f"Saved metadata for {len(self.metadata)} datasets")
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
            raise
    
    def list_available_datasets(self) -> Dict:
        """List all available datasets"""
        return self.AVAILABLE_DATASETS
    
    def get_dataset_status(self) -> Dict[str, bool]:
        """Check which datasets have been downloaded"""
        status = {}
        for name in self.AVAILABLE_DATASETS.keys():
            dataset_path = self.data_dir / f"{name}.csv"
            status[name] = dataset_path.exists()
            
            if status[name]:
                try:
                    df = pd.read_csv(dataset_path, nrows=1)
                    logger.debug(f"Dataset {name} verified: {dataset_path}")
                except Exception as e:
                    logger.warning(f"Dataset {name} exists but may be corrupted: {e}")
                    status[name] = False
        
        return status
    
    def download_dataset_instructions(self, dataset_name: str) -> str:
        """Get instructions for downloading a dataset"""
        
        if dataset_name not in self.AVAILABLE_DATASETS:
            return f"Dataset '{dataset_name}' not found"
        
        dataset_info = self.AVAILABLE_DATASETS[dataset_name]
        kaggle_id = dataset_info["kaggle_id"]
        
        instructions = f"""
MANUAL DOWNLOAD INSTRUCTIONS for {dataset_name.upper()}:

1. Install Kaggle API:
   pip install kaggle

2. Setup Kaggle API credentials:
   - Go to: https://www.kaggle.com/settings/account
   - Click "Create New API Token"
   - Save kaggle.json to ~/.kaggle/

3. Download the dataset:
   kaggle datasets download -d {kaggle_id} -p {self.data_dir}/{dataset_name}/

4. Extract the dataset:
   unzip {self.data_dir}/{dataset_name}/*.zip -d {self.data_dir}/{dataset_name}/

Dataset Info:
   - Description: {dataset_info['description']}
   - Diseases: {', '.join(dataset_info['diseases'])}
   - Features: {len(dataset_info['features'])} features
   - Kaggle ID: {kaggle_id}
"""
        return instructions
    
    def load_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Load a downloaded dataset"""
        dataset_path = self.data_dir / f"{dataset_name}.csv"
        
        if not dataset_path.exists():
            logger.error(f"Dataset {dataset_name} not found at {dataset_path}")
            raise FileNotFoundError(f"Dataset {dataset_name} not found at {dataset_path}")
        
        try:
            df = pd.read_csv(dataset_path)
            logger.info(f"Loaded dataset {dataset_name}: {df.shape[0]} rows × {df.shape[1]} cols")
            return df
        except Exception as e:
            logger.error(f"Failed to load dataset {dataset_name}: {e}")
            raise
    
    def integrate_dataset(self, dataset_name: str, df: pd.DataFrame) -> Dict:
        """Integrate a dataset into the project"""
        
        if dataset_name not in self.AVAILABLE_DATASETS:
            msg = f"Unknown dataset: {dataset_name}"
            logger.error(msg)
            return {"error": msg}
        
        try:
            dataset_info = self.AVAILABLE_DATASETS[dataset_name]
            
            # Validate dataset
            if df is None or len(df) == 0:
                raise ValueError("Dataset is empty")
            
            # Save processed dataset
            output_path = self.data_dir / f"{dataset_name}.csv"
            df.to_csv(output_path, index=False)
            logger.info(f"Saved dataset {dataset_name} to {output_path}")
            
            # Update metadata
            self.metadata[dataset_name] = {
                "description": dataset_info["description"],
                "diseases": dataset_info["diseases"],
                "n_samples": len(df),
                "n_features": len(dataset_info["features"]),
                "features": dataset_info["features"],
                "target": dataset_info["target"],
                "path": str(output_path),
                "integrated_at": datetime.now().isoformat()
            }
            self.save_metadata()
            
            result = {
                "status": "success",
                "dataset": dataset_name,
                "samples": len(df),
                "features": len(dataset_info["features"]),
                "diseases": dataset_info["diseases"]
            }
            logger.info(f"Successfully integrated {dataset_name}: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to integrate dataset {dataset_name}: {e}")
            return {"error": str(e)}
    
    def merge_datasets(self, dataset_names: List[str]) -> pd.DataFrame:
        """Merge multiple datasets into one"""
        
        dfs = []
        skipped = []
        
        for name in dataset_names:
            try:
                df = self.load_dataset(name)
                # Add source column
                df['source_dataset'] = name
                dfs.append(df)
                logger.info(f"Added dataset {name} to merge pool: {len(df)} rows")
            except FileNotFoundError:
                logger.warning(f"Skipping {name} (not found)")
                skipped.append(name)
            except Exception as e:
                logger.warning(f"Skipping {name}: {e}")
                skipped.append(name)
        
        if not dfs:
            msg = f"No datasets found to merge. Skipped: {skipped}"
            logger.error(msg)
            raise ValueError(msg)
        
        if skipped:
            logger.info(f"Skipped {len(skipped)} datasets: {skipped}")
        
        # Merge datasets
        merged = pd.concat(dfs, ignore_index=True)
        logger.info(f"Merged {len(dfs)} datasets: {merged.shape[0]} total rows × {merged.shape[1]} cols")
        return merged
    
    def get_disease_mapping(self) -> Dict[str, List[str]]:
        """Get mapping of diseases to datasets"""
        mapping = {}
        for dataset_name, info in self.AVAILABLE_DATASETS.items():
            for disease in info["diseases"]:
                if disease not in mapping:
                    mapping[disease] = []
                mapping[disease].append(dataset_name)
        return mapping
    
    def get_dataset_summary(self) -> Dict:
        """Get summary of all datasets"""
        summary = {
            "total_available": len(self.AVAILABLE_DATASETS),
            "total_diseases": len(self.get_disease_mapping()),
            "datasets": {},
            "generated_at": datetime.now().isoformat()
        }
        
        for name, info in self.AVAILABLE_DATASETS.items():
            try:
                path = self.data_dir / f"{name}.csv"
                if path.exists():
                    df = pd.read_csv(path, nrows=1000)  # Read only first 1000 rows for speed
                    n_rows = len(pd.read_csv(path))
                    summary["datasets"][name] = {
                        "description": info["description"],
                        "diseases": info["diseases"],
                        "n_features": len(info["features"]),
                        "downloaded": True,
                        "n_samples": n_rows
                    }
                else:
                    summary["datasets"][name] = {
                        "description": info["description"],
                        "diseases": info["diseases"],
                        "n_features": len(info["features"]),
                        "downloaded": False,
                        "n_samples": 0
                    }
            except Exception as e:
                logger.warning(f"Error reading dataset {name}: {e}")
                summary["datasets"][name] = {
                    "description": info["description"],
                    "error": str(e),
                    "downloaded": False
                }
        
        logger.info(f"Generated summary for {len(summary['datasets'])} datasets")
        return summary


def print_dataset_instructions():
    """Print instructions for downloading all datasets"""
    
    manager = KaggleDatasetManager()
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║          📊 KAGGLE DATASET DOWNLOAD INSTRUCTIONS              ║
╚════════════════════════════════════════════════════════════════╝

STEP 1: Setup Kaggle API
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Install Kaggle API:
     pip install kaggle

  2. Get API credentials:
     - Go to https://www.kaggle.com/settings/account
     - Click "Create New API Token"
     - This downloads kaggle.json

  3. Move credentials:
     mkdir -p ~/.kaggle
     mv ~/Downloads/kaggle.json ~/.kaggle/
     chmod 600 ~/.kaggle/kaggle.json

STEP 2: Available Datasets
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    datasets = manager.list_available_datasets()
    for i, (name, info) in enumerate(datasets.items(), 1):
        print(f"\n{i}. {name.upper()}")
        print(f"   Description: {info['description']}")
        print(f"   Diseases: {', '.join(info['diseases'])}")
        print(f"   Kaggle ID: {info['kaggle_id']}")
        print(f"   Download command:")
        print(f"   $ kaggle datasets download -d {info['kaggle_id']} -p data/kaggle_datasets/{name}/")

    print("""

STEP 3: Download All Datasets (Automated)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Run the download script:
    python src/download_kaggle_datasets.py

STEP 4: Check Downloaded Datasets
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Check status:
    python -c "from src.dataset_manager import KaggleDatasetManager; \\
               m = KaggleDatasetManager(); \\
               print(m.get_dataset_status())"

════════════════════════════════════════════════════════════════
    """)


if __name__ == "__main__":
    print_dataset_instructions()
