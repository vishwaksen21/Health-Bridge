#!/usr/bin/env python3
"""
Complete Dataset Setup & Download Script
Downloads all Kaggle datasets and sets up the unified data system
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Tuple
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class DatasetSetupManager:
    """Manage complete dataset setup and download"""
    
    def __init__(self):
        self.base_dir = Path("data")
        self.kaggle_dir = self.base_dir / "kaggle_datasets"
        self.kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    
    def check_kaggle_api(self) -> bool:
        """Check if Kaggle API is properly configured"""
        if not self.kaggle_json.exists():
            logger.error("❌ Kaggle API credentials not found!")
            logger.error(f"   Expected location: {self.kaggle_json}")
            return False
        
        try:
            import kaggle
            logger.info("✅ Kaggle API is installed and configured")
            return True
        except ImportError:
            logger.error("❌ Kaggle library not installed")
            return False
    
    def setup_kaggle_api(self) -> bool:
        """Setup Kaggle API"""
        logger.info("\n" + "=" * 70)
        logger.info("🔧 KAGGLE API SETUP")
        logger.info("=" * 70)
        logger.info("\n1. Go to: https://www.kaggle.com/settings/account")
        logger.info("2. Click 'Create New API Token'")
        logger.info("3. This will download kaggle.json")
        logger.info(f"4. Move it to: {self.kaggle_json}")
        logger.info("5. Run: chmod 600 ~/.kaggle/kaggle.json\n")
        
        input("Press Enter when you've completed the setup...")
        
        # Install kaggle package if needed
        try:
            import kaggle
        except ImportError:
            logger.info("Installing kaggle package...")
            subprocess.run(["pip", "install", "kaggle"], check=True)
        
        return self.check_kaggle_api()
    
    def create_directories(self):
        """Create necessary directories"""
        logger.info("\n📁 Creating directories...")
        self.kaggle_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for each dataset
        datasets = [
            "diabetes", "heart_disease", "respiratory", "mental_health",
            "covid19", "medicinal_plants", "indian_medicinal_plants",
            "drug_reviews", "liver_disease", "cancer", "skin_disease",
            "medicine_recommendation"
        ]
        
        for dataset in datasets:
            dataset_dir = self.kaggle_dir / dataset
            dataset_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"✅ Directories created in {self.kaggle_dir}")
    
    def download_all_datasets(self) -> bool:
        """Download all Kaggle datasets"""
        from kaggle_dataset_loader import KaggleDatasetLoader
        
        loader = KaggleDatasetLoader()
        datasets = loader.KAGGLE_DATASETS
        
        logger.info("\n" + "=" * 70)
        logger.info("📥 DOWNLOADING KAGGLE DATASETS")
        logger.info("=" * 70)
        
        total = len(datasets)
        failed = []
        
        for idx, (name, info) in enumerate(datasets.items(), 1):
            logger.info(f"\n[{idx}/{total}] Downloading {name}...")
            logger.info(f"     Dataset ID: {info['kaggle_id']}")
            
            try:
                dataset_dir = self.kaggle_dir / name
                cmd = [
                    "kaggle", "datasets", "download",
                    "-d", info['kaggle_id'],
                    "-p", str(dataset_dir),
                    "--unzip"
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    logger.info(f"✅ {name}: Downloaded successfully")
                else:
                    logger.warning(f"⚠️  {name}: Download had issues")
                    logger.warning(f"   Error: {result.stderr[:100]}")
                    failed.append(name)
                    
            except subprocess.TimeoutExpired:
                logger.warning(f"⏱️  {name}: Download timed out")
                failed.append(name)
            except Exception as e:
                logger.error(f"❌ {name}: Failed - {e}")
                failed.append(name)
        
        logger.info("\n" + "=" * 70)
        logger.info(f"📊 Download Summary")
        logger.info("=" * 70)
        logger.info(f"Total: {total}")
        logger.info(f"Successful: {total - len(failed)}")
        logger.info(f"Failed: {len(failed)}")
        
        if failed:
            logger.warning(f"⚠️  Failed datasets: {', '.join(failed)}")
            return False
        
        logger.info("✅ All datasets downloaded successfully!")
        return True
    
    def verify_local_datasets(self) -> bool:
        """Verify local datasets are present"""
        logger.info("\n" + "=" * 70)
        logger.info("🔍 VERIFYING LOCAL DATASETS")
        logger.info("=" * 70)
        
        required_files = [
            "diseases.csv",
            "herbs.csv",
            "ingredients.csv",
            "targets.csv",
            "symptom_disease.csv",
            "pharmaceutical_database.csv",
            "drug_interactions.csv",
            "allergies.csv"
        ]
        
        missing = []
        for file in required_files:
            file_path = self.base_dir / file
            if file_path.exists():
                size = file_path.stat().st_size
                size_mb = size / (1024 * 1024)
                logger.info(f"✅ {file}: {size_mb:.2f} MB")
            else:
                logger.warning(f"❌ {file}: Missing")
                missing.append(file)
        
        if missing:
            logger.warning(f"\n⚠️  Missing files: {', '.join(missing)}")
            return False
        
        logger.info("\n✅ All local datasets verified!")
        return True
    
    def test_data_orchestrator(self) -> bool:
        """Test the data orchestrator"""
        logger.info("\n" + "=" * 70)
        logger.info("🧪 TESTING DATA ORCHESTRATOR")
        logger.info("=" * 70)
        
        try:
            from data_orchestrator import DataOrchestrator
            
            logger.info("\nInitializing data orchestrator...")
            orchestrator = DataOrchestrator()
            
            logger.info("\nTesting functionality...")
            
            # Test 1: Get all diseases
            diseases = orchestrator.get_all_diseases()
            logger.info(f"✅ Total diseases: {len(diseases)}")
            
            # Test 2: Find disease by symptoms
            test_symptoms = ["fever", "cough", "headache"]
            matches = orchestrator.find_disease_by_symptoms(test_symptoms)
            logger.info(f"✅ Disease matching: {len(matches)} matches found for {test_symptoms}")
            
            # Test 3: Get system report
            report = orchestrator.generate_system_report()
            print(report)
            
            logger.info("✅ Data orchestrator working correctly!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Data orchestrator test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def create_setup_summary(self):
        """Create setup summary file"""
        summary = {
            "setup_date": datetime.now().isoformat(),
            "local_datasets": {
                "status": "verified" if self.verify_local_datasets() else "incomplete",
                "location": str(self.base_dir)
            },
            "kaggle_datasets": {
                "status": "downloaded" if (self.kaggle_dir / "diabetes").exists() else "pending",
                "location": str(self.kaggle_dir),
                "total_datasets": 12
            },
            "next_steps": [
                "Run: python src/unified_dataset_loader.py",
                "Run: python src/kaggle_dataset_loader.py",
                "Run: python src/data_orchestrator.py",
                "Update ai_assistant.py to use DataOrchestrator"
            ]
        }
        
        summary_file = Path("SETUP_SUMMARY.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"\n✅ Setup summary saved to {summary_file}")
    
    def run_complete_setup(self):
        """Run complete setup process"""
        logger.info("\n" + "=" * 80)
        logger.info("🚀 COMPLETE DATASET SETUP")
        logger.info("=" * 80)
        
        # Step 1: Verify local datasets
        if not self.verify_local_datasets():
            logger.error("\n❌ Local datasets verification failed!")
            logger.error("   Please ensure all CSV files are in the data/ directory")
            return False
        
        # Step 2: Setup Kaggle API
        if not self.check_kaggle_api():
            logger.info("\n🔧 Kaggle API not configured. Setting up now...")
            if not self.setup_kaggle_api():
                logger.error("\n❌ Kaggle API setup failed!")
                logger.error("   You can still use local datasets")
                return False
        
        # Step 3: Create directories
        self.create_directories()
        
        # Step 4: Download datasets
        logger.info("\n📥 Ready to download Kaggle datasets?")
        response = input("Continue with download? (yes/no): ").lower()
        
        if response == "yes":
            if not self.download_all_datasets():
                logger.warning("\n⚠️  Some datasets failed to download")
                logger.warning("   You can try downloading them manually")
        else:
            logger.info("\nSkipping Kaggle dataset download")
            logger.info("You can download them later by running this script again")
        
        # Step 5: Test
        self.test_data_orchestrator()
        
        # Step 6: Summary
        self.create_setup_summary()
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ SETUP COMPLETE!")
        logger.info("=" * 80)
        logger.info("\nNext steps:")
        logger.info("1. Review the generated SETUP_SUMMARY.json")
        logger.info("2. Run: python src/data_orchestrator.py")
        logger.info("3. Update ai_assistant.py to use the new data system")
        logger.info("4. Test the system with: python main.py")
        logger.info("\n")


def main():
    try:
        manager = DatasetSetupManager()
        manager.run_complete_setup()
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Setup interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
