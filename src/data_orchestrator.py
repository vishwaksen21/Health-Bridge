#!/usr/bin/env python3
"""
Data Orchestrator
Unifies local datasets, Kaggle datasets, and medicinal datasets
Provides comprehensive medical knowledge base for AI system
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
from src.unified_dataset_loader import DatasetManager
from src.kaggle_dataset_loader import KaggleDatasetLoader

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataOrchestrator:
    """Unified data orchestrator for all medical datasets"""
    
    def __init__(self, base_dir: str = "data"):
        """Initialize data orchestrator with all data sources"""
        self.base_dir = Path(base_dir)
        
        # Initialize all data sources
        logger.info("Initializing data sources...")
        
        try:
            self.local_data = DatasetManager(data_dir=str(self.base_dir))
            logger.info("✓ Local datasets loaded")
        except Exception as e:
            logger.error(f"Failed to load local datasets: {e}")
            self.local_data = None
        
        try:
            self.kaggle_data = KaggleDatasetLoader(base_dir=str(self.base_dir))
            logger.info("✓ Kaggle dataset loader initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Kaggle loader: {e}")
            self.kaggle_data = None
        
        # Data source metadata
        self.data_sources = {
            "local": {
                "status": "online" if self.local_data else "offline",
                "description": "Local CSV datasets (symptom-disease, drugs, interactions, allergies)",
                "priority": 1
            },
            "kaggle": {
                "status": "online" if self.kaggle_data else "offline",
                "description": "Kaggle medical datasets (diabetes, heart disease, cancer, etc.)",
                "priority": 2
            }
        }
    
    def get_all_diseases(self) -> List[str]:
        """Get all diseases from all sources"""
        diseases = set()
        
        # Local diseases
        if self.local_data:
            try:
                diseases.update(self.local_data.get_all_diseases())
            except Exception as e:
                logger.warning(f"Could not get local diseases: {e}")
        
        # Kaggle diseases
        if self.kaggle_data:
            try:
                diseases.update(self.kaggle_data.get_all_diseases_from_kaggle())
            except Exception as e:
                logger.warning(f"Could not get Kaggle diseases: {e}")
        
        return sorted(list(diseases))
    
    def get_disease_info(self, disease: str) -> Dict:
        """Get comprehensive info about a disease from all sources"""
        info = {
            "disease": disease,
            "sources": {},
            "combined_symptoms": set(),
            "confidence": 0.0
        }
        
        # Try local source
        if self.local_data:
            try:
                local_symptoms = self.local_data.get_disease_symptoms(disease)
                if local_symptoms:
                    info["sources"]["local"] = {
                        "symptoms": local_symptoms,
                        "status": "found"
                    }
                    info["combined_symptoms"].update(local_symptoms.keys())
            except Exception as e:
                logger.debug(f"Could not get local info for {disease}: {e}")
        
        # Try Kaggle source
        if self.kaggle_data:
            try:
                kaggle_df = self.kaggle_data.get_disease_data(disease)
                if kaggle_df is not None:
                    info["sources"]["kaggle"] = {
                        "rows": len(kaggle_df),
                        "columns": list(kaggle_df.columns),
                        "status": "found"
                    }
            except Exception as e:
                logger.debug(f"Could not get Kaggle info for {disease}: {e}")
        
        # Calculate confidence based on sources
        info["confidence"] = len(info["sources"]) / 2.0  # Max 1.0 with both sources
        info["combined_symptoms"] = list(info["combined_symptoms"])
        
        return info
    
    def find_disease_by_symptoms(self, symptoms: List[str], threshold: float = 0.5) -> Dict[str, float]:
        """Find diseases matching symptoms using all data sources"""
        matches = {}
        
        # Try local source (primary)
        if self.local_data:
            try:
                local_matches = self.local_data.get_disease_by_symptoms(symptoms)
                matches.update(local_matches)
            except Exception as e:
                logger.warning(f"Could not search local data: {e}")
        
        # Try Kaggle source if local has no good matches
        if self.kaggle_data and len(matches) < 3:
            try:
                # Would need to implement symptom search in Kaggle data
                pass
            except Exception as e:
                logger.warning(f"Could not search Kaggle data: {e}")
        
        # Filter by threshold
        filtered = {disease: score for disease, score in matches.items() 
                   if score >= threshold}
        
        return dict(sorted(filtered.items(), key=lambda x: x[1], reverse=True))
    
    def get_drug_interactions(self, drug1: str, drug2: str) -> Optional[Dict]:
        """Get drug interaction info"""
        if self.local_data:
            try:
                return self.local_data.get_drug_interactions(drug1, drug2)
            except Exception as e:
                logger.warning(f"Could not get drug interactions: {e}")
        return None
    
    def get_allergy_info(self, substance: str) -> Optional[Dict]:
        """Get allergy information"""
        if self.local_data:
            try:
                return self.local_data.get_allergy_info(substance)
            except Exception as e:
                logger.warning(f"Could not get allergy info: {e}")
        return None
    
    def get_medicinal_plants(self) -> Optional[pd.DataFrame]:
        """Get medicinal plants from Kaggle"""
        if self.kaggle_data:
            try:
                return self.kaggle_data.get_medicinal_plants()
            except Exception as e:
                logger.warning(f"Could not get medicinal plants: {e}")
        return None
    
    def get_comprehensive_health_profile(self, symptoms: List[str], allergies: List[str] = None) -> Dict:
        """Get comprehensive health profile for a patient"""
        profile = {
            "symptoms": symptoms,
            "allergies": allergies or [],
            "possible_diseases": {},
            "safe_drugs": [],
            "unsafe_drugs": [],
            "recommendations": []
        }
        
        # Find possible diseases
        diseases = self.find_disease_by_symptoms(symptoms)
        profile["possible_diseases"] = diseases
        
        # Check allergies
        if allergies:
            for allergy in allergies:
                allergy_info = self.get_allergy_info(allergy)
                if allergy_info:
                    profile["unsafe_drugs"].extend(allergy_info.get("associated_drugs", []))
        
        # Generate recommendations
        if diseases:
            top_disease = list(diseases.keys())[0]
            profile["recommendations"].append(f"Primary concern: {top_disease}")
        
        return profile
    
    def get_data_statistics(self) -> Dict:
        """Get statistics about all data sources"""
        stats = {
            "local_data": {},
            "kaggle_data": {},
            "combined": {}
        }
        
        # Local stats
        if self.local_data:
            try:
                local_diseases = self.local_data.get_all_diseases()
                stats["local_data"] = {
                    "diseases": len(local_diseases),
                    "disease_list": local_diseases[:10],  # First 10
                    "status": "online"
                }
            except Exception as e:
                logger.warning(f"Could not get local stats: {e}")
                stats["local_data"]["status"] = "error"
        
        # Kaggle stats
        if self.kaggle_data:
            try:
                summary = self.kaggle_data.get_dataset_summary()
                stats["kaggle_data"] = {
                    "total_datasets": summary["total_datasets"],
                    "downloaded": summary["downloaded"],
                    "diseases": len(self.kaggle_data.get_all_diseases_from_kaggle()),
                    "status": "online"
                }
            except Exception as e:
                logger.warning(f"Could not get Kaggle stats: {e}")
                stats["kaggle_data"]["status"] = "error"
        
        # Combined stats
        all_diseases = self.get_all_diseases()
        stats["combined"] = {
            "total_diseases": len(all_diseases),
            "active_sources": sum(1 for s in self.data_sources.values() if s["status"] == "online"),
            "data_sources": self.data_sources
        }
        
        return stats
    
    def generate_system_report(self) -> str:
        """Generate comprehensive system report"""
        report = "\n" + "=" * 80 + "\n"
        report += "📊 DATA ORCHESTRATOR SYSTEM REPORT\n"
        report += "=" * 80 + "\n\n"
        
        stats = self.get_data_statistics()
        
        # Data sources
        report += "📡 DATA SOURCES STATUS\n"
        report += "-" * 80 + "\n"
        for source, status in self.data_sources.items():
            emoji = "✅" if status["status"] == "online" else "❌"
            report += f"{emoji} {source.upper()}: {status['description']}\n"
            report += f"   Status: {status['status'].upper()}\n\n"
        
        # Statistics
        report += "📈 DATASET STATISTICS\n"
        report += "-" * 80 + "\n"
        
        if "local_data" in stats and stats["local_data"]:
            report += f"LOCAL DATA:\n"
            report += f"  • Diseases: {stats['local_data'].get('diseases', 'N/A')}\n"
            report += f"  • Status: {stats['local_data'].get('status', 'N/A').upper()}\n\n"
        
        if "kaggle_data" in stats and stats["kaggle_data"]:
            report += f"KAGGLE DATA:\n"
            report += f"  • Datasets Available: {stats['kaggle_data'].get('total_datasets', 'N/A')}\n"
            report += f"  • Downloaded: {stats['kaggle_data'].get('downloaded', 'N/A')}\n"
            report += f"  • Diseases: {stats['kaggle_data'].get('diseases', 'N/A')}\n"
            report += f"  • Status: {stats['kaggle_data'].get('status', 'N/A').upper()}\n\n"
        
        if "combined" in stats:
            report += f"COMBINED COVERAGE:\n"
            report += f"  • Total Diseases: {stats['combined'].get('total_diseases', 'N/A')}\n"
            report += f"  • Active Sources: {stats['combined'].get('active_sources', 'N/A')}\n"
        
        report += "\n" + "=" * 80 + "\n"
        
        return report


def main():
    """Test data orchestrator"""
    print("\n" + "=" * 80)
    print("🎯 DATA ORCHESTRATOR TEST")
    print("=" * 80 + "\n")
    
    orchestrator = DataOrchestrator()
    
    # Test 1: Get all diseases
    print("Test 1: All Available Diseases")
    print("-" * 80)
    all_diseases = orchestrator.get_all_diseases()
    print(f"Total diseases: {len(all_diseases)}")
    print(f"Sample: {', '.join(all_diseases[:10])}")
    print()
    
    # Test 2: Get disease info
    print("Test 2: Disease Information")
    print("-" * 80)
    test_disease = "Diabetes"
    disease_info = orchestrator.get_disease_info(test_disease)
    print(f"Disease: {disease_info['disease']}")
    print(f"Sources: {list(disease_info['sources'].keys())}")
    print(f"Combined Symptoms: {len(disease_info['combined_symptoms'])} found")
    print()
    
    # Test 3: Find disease by symptoms
    print("Test 3: Find Disease by Symptoms")
    print("-" * 80)
    test_symptoms = ["fever", "cough", "headache"]
    matches = orchestrator.find_disease_by_symptoms(test_symptoms)
    print(f"Searching for: {', '.join(test_symptoms)}")
    print("Matches:")
    for disease, score in list(matches.items())[:5]:
        print(f"  • {disease}: {score:.2%}")
    print()
    
    # Test 4: Get system report
    print("Test 4: System Report")
    print("-" * 80)
    report = orchestrator.generate_system_report()
    print(report)
    
    # Test 5: Get medicinal plants
    print("Test 5: Medicinal Plants")
    print("-" * 80)
    plants = orchestrator.get_medicinal_plants()
    if plants is not None:
        print(f"✅ Medicinal plants dataset loaded: {plants.shape[0]} rows × {plants.shape[1]} columns")
    else:
        print("❌ Medicinal plants dataset not available (Kaggle not downloaded)")
    print()
    
    print("=" * 80)
    print("✅ Data Orchestrator Ready!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
