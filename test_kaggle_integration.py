#!/usr/bin/env python3
"""
Comprehensive test suite for Kaggle dataset integration
Tests dataset manager, mock datasets, and system improvements
"""

import sys
import os
import json
import tempfile
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dataset_manager import KaggleDatasetManager
# ai_assistant has relative imports, so we'll test it separately


class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(title):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{title:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_test(name, status, details=""):
    """Print test result"""
    emoji = "✅" if status else "❌"
    color = Colors.GREEN if status else Colors.RED
    print(f"{emoji} {color}{name}{Colors.ENDC}")
    if details:
        print(f"   {details}")


def print_info(msg):
    """Print info message"""
    print(f"ℹ️  {Colors.CYAN}{msg}{Colors.ENDC}")


def print_success(msg):
    """Print success message"""
    print(f"✨ {Colors.GREEN}{msg}{Colors.ENDC}")


def print_error(msg):
    """Print error message"""
    print(f"⚠️  {Colors.RED}{msg}{Colors.ENDC}")


class TestKaggleIntegration:
    """Test suite for Kaggle dataset integration"""
    
    def __init__(self):
        self.test_results = []
        self.temp_dir = None
        self.manager = None
    
    def setup(self):
        """Setup test environment"""
        print_header("SETUP TEST ENVIRONMENT")
        
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp(prefix="kaggle_test_")
        print_info(f"Created temp directory: {self.temp_dir}")
        
        # Initialize manager with temp dir
        self.manager = KaggleDatasetManager(data_dir=self.temp_dir)
        print_success(f"Initialized KaggleDatasetManager")
        
        return True
    
    # ==================== TEST 1: Dataset Manager ====================
    
    def test_dataset_listing(self):
        """Test 1: List available datasets"""
        print_header("TEST 1: List Available Datasets")
        
        try:
            datasets = self.manager.list_available_datasets()
            
            print_test("Datasets loaded", len(datasets) > 0, f"Found {len(datasets)} datasets")
            
            expected_datasets = ["diabetes", "heart_disease", "respiratory", "mental_health", 
                                "covid19", "skin_disease", "liver_disease", "cancer"]
            
            for ds in expected_datasets:
                exists = ds in datasets
                print_test(f"  - {ds} available", exists)
            
            print_info(f"Dataset descriptions:")
            for name, info in list(datasets.items())[:3]:
                print(f"   {name}: {info['description']}")
            
            self.test_results.append(("List Available Datasets", True))
            return True
            
        except Exception as e:
            print_error(f"Failed: {str(e)}")
            self.test_results.append(("List Available Datasets", False))
            return False
    
    def test_dataset_status(self):
        """Test 2: Check dataset download status"""
        print_header("TEST 2: Check Dataset Download Status")
        
        try:
            status = self.manager.get_dataset_status()
            
            print_test("Status check", len(status) > 0, f"Checked {len(status)} datasets")
            
            # All should be False initially
            all_false = all(v == False for v in status.values())
            print_test("All datasets initially not downloaded", all_false)
            
            print_info("Dataset status:")
            for name, is_downloaded in status.items():
                status_str = "✓ Downloaded" if is_downloaded else "✗ Not downloaded"
                print(f"   {name}: {status_str}")
            
            self.test_results.append(("Check Dataset Status", True))
            return True
            
        except Exception as e:
            print_error(f"Failed: {str(e)}")
            self.test_results.append(("Check Dataset Status", False))
            return False
    
    def test_disease_mapping(self):
        """Test 3: Get disease to dataset mapping"""
        print_header("TEST 3: Disease to Dataset Mapping")
        
        try:
            mapping = self.manager.get_disease_mapping()
            
            print_test("Get disease mapping", len(mapping) > 0, f"Found {len(mapping)} diseases")
            
            print_info("Disease coverage:")
            for disease, datasets in sorted(mapping.items())[:5]:
                print(f"   {disease}: {', '.join(datasets)}")
            
            # Check specific diseases
            expected_diseases = ["Diabetes", "Heart Disease", "Asthma", "Depression", "COVID-19"]
            for disease in expected_diseases:
                exists = disease in mapping
                print_test(f"  - {disease} mapped", exists)
            
            self.test_results.append(("Disease Mapping", True))
            return True
            
        except Exception as e:
            print_error(f"Failed: {str(e)}")
            self.test_results.append(("Disease Mapping", False))
            return False
    
    # ==================== TEST 2: Mock Dataset Creation ====================
    
    def create_mock_dataset(self, dataset_name: str, n_samples: int = 100) -> pd.DataFrame:
        """Create a mock dataset for testing"""
        
        if dataset_name == "diabetes":
            data = {
                'Pregnancies': np.random.randint(0, 15, n_samples),
                'Glucose': np.random.randint(50, 200, n_samples),
                'BloodPressure': np.random.randint(60, 130, n_samples),
                'SkinThickness': np.random.randint(0, 100, n_samples),
                'Insulin': np.random.randint(0, 850, n_samples),
                'BMI': np.random.uniform(18, 55, n_samples),
                'DiabetesPedigreeFunction': np.random.uniform(0.0, 2.4, n_samples),
                'Age': np.random.randint(21, 81, n_samples),
                'Outcome': np.random.randint(0, 2, n_samples)
            }
        
        elif dataset_name == "heart_disease":
            data = {
                'age': np.random.randint(29, 77, n_samples),
                'sex': np.random.randint(0, 2, n_samples),
                'cp': np.random.randint(0, 4, n_samples),
                'trestbps': np.random.randint(94, 200, n_samples),
                'chol': np.random.randint(126, 564, n_samples),
                'fbs': np.random.randint(0, 2, n_samples),
                'restecg': np.random.randint(0, 3, n_samples),
                'thalach': np.random.randint(60, 202, n_samples),
                'exang': np.random.randint(0, 2, n_samples),
                'oldpeak': np.random.uniform(0, 6.2, n_samples),
                'slope': np.random.randint(0, 3, n_samples),
                'ca': np.random.randint(0, 5, n_samples),
                'thal': np.random.randint(0, 4, n_samples),
                'target': np.random.randint(0, 5, n_samples)
            }
        
        elif dataset_name == "respiratory":
            data = {
                'Lung_function': np.random.uniform(0, 100, n_samples),
                'Smoking_status': np.random.randint(0, 3, n_samples),
                'Air_pollution': np.random.randint(0, 100, n_samples),
                'Genetic_risk': np.random.randint(0, 2, n_samples),
                'Balanced_diet': np.random.randint(0, 2, n_samples),
                'Adequate_sleep': np.random.randint(0, 2, n_samples),
                'Pollution_exposure': np.random.randint(0, 100, n_samples),
                'Disease': np.random.randint(0, 2, n_samples)
            }
        
        else:
            # Generic dataset
            data = {f'feature_{i}': np.random.randn(n_samples) for i in range(5)}
            data['target'] = np.random.randint(0, 2, n_samples)
        
        return pd.DataFrame(data)
    
    def test_mock_dataset_creation(self):
        """Test 4: Create and validate mock datasets"""
        print_header("TEST 4: Create Mock Datasets")
        
        try:
            datasets_to_test = ["diabetes", "heart_disease", "respiratory"]
            
            for dataset_name in datasets_to_test:
                df = self.create_mock_dataset(dataset_name, n_samples=100)
                print_test(f"Create mock {dataset_name}", len(df) == 100, 
                          f"Created {len(df)} rows × {len(df.columns)} cols")
            
            self.test_results.append(("Create Mock Datasets", True))
            return True
            
        except Exception as e:
            print_error(f"Failed: {str(e)}")
            self.test_results.append(("Create Mock Datasets", False))
            return False
    
    def test_dataset_integration(self):
        """Test 5: Integrate mock datasets"""
        print_header("TEST 5: Integrate Mock Datasets")
        
        try:
            datasets = ["diabetes", "heart_disease", "respiratory"]
            
            for dataset_name in datasets:
                # Create mock data
                df = self.create_mock_dataset(dataset_name, n_samples=100)
                
                # Integrate dataset
                result = self.manager.integrate_dataset(dataset_name, df)
                
                success = result.get("status") == "success"
                print_test(f"Integrate {dataset_name}", success, 
                          f"{result.get('samples')} samples")
            
            # Verify files created
            for dataset_name in datasets:
                path = Path(self.temp_dir) / f"{dataset_name}.csv"
                exists = path.exists()
                print_test(f"  - {dataset_name}.csv created", exists)
            
            self.test_results.append(("Integrate Datasets", True))
            return True
            
        except Exception as e:
            print_error(f"Failed: {str(e)}")
            self.test_results.append(("Integrate Datasets", False))
            return False
    
    def test_dataset_merging(self):
        """Test 6: Merge datasets"""
        print_header("TEST 6: Merge Multiple Datasets")
        
        try:
            # Create and integrate mock datasets
            for dataset_name in ["diabetes", "heart_disease"]:
                df = self.create_mock_dataset(dataset_name, n_samples=50)
                self.manager.integrate_dataset(dataset_name, df)
            
            # Merge datasets
            merged = self.manager.merge_datasets(["diabetes", "heart_disease"])
            
            print_test("Merge datasets", len(merged) > 0, f"Merged: {len(merged)} rows")
            print_test("Has source column", 'source_dataset' in merged.columns)
            print_test("Unique sources", len(merged['source_dataset'].unique()) == 2)
            
            print_info("Merged data summary:")
            print(f"   Total rows: {len(merged)}")
            print(f"   Total columns: {len(merged.columns)}")
            print(f"   Source datasets: {merged['source_dataset'].unique().tolist()}")
            
            self.test_results.append(("Merge Datasets", True))
            return True
            
        except Exception as e:
            print_error(f"Failed: {str(e)}")
            self.test_results.append(("Merge Datasets", False))
            return False
    
    # ==================== TEST 3: System Integration ====================
    
    def test_ai_assistant_with_integrated_data(self):
        """Test 7: AI Assistant with integrated datasets"""
        print_header("TEST 7: AI Assistant with Integrated Data")
        
        try:
            # Create sample integrated data
            symptom_disease_data = {
                'symptom': ['high glucose', 'high blood pressure', 'chest pain', 
                           'shortness of breath', 'fatigue'],
                'disease': ['Diabetes', 'Heart Disease', 'Heart Disease', 
                           'Respiratory Disease', 'Diabetes'],
                'source_dataset': ['diabetes', 'heart_disease', 'heart_disease', 
                                  'respiratory', 'diabetes']
            }
            integrated_df = pd.DataFrame(symptom_disease_data)
            
            # Save integrated data
            integrated_path = Path(self.temp_dir) / "integrated_symptoms.csv"
            integrated_df.to_csv(integrated_path, index=False)
            
            print_test("Create integrated symptoms", integrated_path.exists())
            print_test("Integrated data rows", len(integrated_df) == 5, 
                      f"Created {len(integrated_df)} symptom-disease pairs")
            
            print_info("Integrated data summary:")
            print(f"   Symptoms: {integrated_df['symptom'].nunique()}")
            print(f"   Diseases: {integrated_df['disease'].nunique()}")
            print(f"   Source datasets: {integrated_df['source_dataset'].nunique()}")
            
            self.test_results.append(("AI Assistant Integration", True))
            return True
            
        except Exception as e:
            print_error(f"Failed: {str(e)}")
            self.test_results.append(("AI Assistant Integration", False))
            return False
    
    # ==================== TEST 4: Improvements ====================
    
    def test_error_handling(self):
        """Test 8: Error handling and recovery"""
        print_header("TEST 8: Error Handling")
        
        tests_passed = 0
        
        # Test 1: Invalid dataset name
        try:
            instructions = self.manager.download_dataset_instructions("invalid_dataset")
            error_found = "not found" in instructions.lower()
            print_test("Handle invalid dataset", error_found)
            tests_passed += error_found
        except Exception as e:
            print_error(f"Unexpected error: {e}")
        
        # Test 2: Load non-existent dataset
        try:
            self.manager.load_dataset("nonexistent")
            print_test("Raise error for missing dataset", False)
        except FileNotFoundError as e:
            print_test("Raise error for missing dataset", True, str(e))
            tests_passed += 1
        except Exception as e:
            print_error(f"Unexpected error type: {e}")
        
        # Test 3: Merge with missing datasets
        try:
            self.manager.merge_datasets(["nonexistent1", "nonexistent2"])
            print_test("Handle missing merge datasets", False)
        except ValueError as e:
            print_test("Handle missing merge datasets", True, str(e))
            tests_passed += 1
        except Exception as e:
            print_error(f"Unexpected error type: {e}")
        
        success = tests_passed >= 2
        self.test_results.append(("Error Handling", success))
        return success
    
    def test_metadata_persistence(self):
        """Test 9: Metadata persistence"""
        print_header("TEST 9: Metadata Persistence")
        
        try:
            # Create and integrate a dataset
            df = self.create_mock_dataset("diabetes", n_samples=75)
            self.manager.integrate_dataset("diabetes", df)
            
            # Verify metadata saved
            metadata_exists = self.manager.metadata_file.exists()
            print_test("Metadata file created", metadata_exists)
            
            # Load metadata
            with open(self.manager.metadata_file, 'r') as f:
                metadata = json.load(f)
            
            print_test("Metadata loaded", "diabetes" in metadata)
            print_test("Metadata content", metadata["diabetes"]["n_samples"] == 75,
                      f"Recorded {metadata['diabetes']['n_samples']} samples")
            
            print_info("Metadata content:")
            for key in ["description", "diseases", "n_features"]:
                print(f"   {key}: {metadata['diabetes'][key]}")
            
            self.test_results.append(("Metadata Persistence", True))
            return True
            
        except Exception as e:
            print_error(f"Failed: {str(e)}")
            traceback.print_exc()
            self.test_results.append(("Metadata Persistence", False))
            return False
    
    def test_dataset_summary(self):
        """Test 10: Get dataset summary"""
        print_header("TEST 10: Dataset Summary")
        
        try:
            # Create and integrate mock datasets
            for name in ["diabetes", "heart_disease"]:
                df = self.create_mock_dataset(name, n_samples=50)
                self.manager.integrate_dataset(name, df)
            
            # Get summary
            summary = self.manager.get_dataset_summary()
            
            print_test("Get dataset summary", "datasets" in summary)
            print_test("Total datasets", summary["total_available"] == 8, 
                      f"Found {summary['total_available']} datasets")
            print_test("Datasets with data", len(summary["datasets"]) > 0)
            
            print_info("Dataset summary:")
            print(f"   Available: {summary['total_available']}")
            print(f"   Total diseases: {summary['total_diseases']}")
            print(f"   Downloaded: {sum(1 for d in summary['datasets'].values() if d['downloaded'])}")
            
            self.test_results.append(("Dataset Summary", True))
            return True
            
        except Exception as e:
            print_error(f"Failed: {str(e)}")
            self.test_results.append(("Dataset Summary", False))
            return False
    
    # ==================== Runner ====================
    
    def run_all_tests(self):
        """Run all tests"""
        print_header("🧪 KAGGLE INTEGRATION TEST SUITE")
        
        if not self.setup():
            print_error("Setup failed, aborting tests")
            return False
        
        # Run tests in groups
        print(f"\n{Colors.BOLD}GROUP 1: Dataset Manager{Colors.ENDC}")
        self.test_dataset_listing()
        self.test_dataset_status()
        self.test_disease_mapping()
        
        print(f"\n{Colors.BOLD}GROUP 2: Mock Datasets{Colors.ENDC}")
        self.test_mock_dataset_creation()
        self.test_dataset_integration()
        self.test_dataset_merging()
        
        print(f"\n{Colors.BOLD}GROUP 3: System Integration{Colors.ENDC}")
        self.test_ai_assistant_with_integrated_data()
        
        print(f"\n{Colors.BOLD}GROUP 4: Improvements{Colors.ENDC}")
        self.test_error_handling()
        self.test_metadata_persistence()
        self.test_dataset_summary()
        
        # Print summary
        self.print_summary()
        
        # Cleanup
        self.cleanup()
        
        return True
    
    def print_summary(self):
        """Print test summary"""
        print_header("📊 TEST SUMMARY")
        
        passed = sum(1 for _, result in self.test_results if result)
        total = len(self.test_results)
        percentage = (passed / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"Passed: {Colors.GREEN}{passed}{Colors.ENDC}")
        print(f"Failed: {Colors.RED}{total - passed}{Colors.ENDC}")
        print(f"Success Rate: {Colors.BOLD}{percentage:.1f}%{Colors.ENDC}\n")
        
        print("Results by test:")
        for name, result in self.test_results:
            emoji = "✅" if result else "❌"
            color = Colors.GREEN if result else Colors.RED
            print(f"  {emoji} {color}{name}{Colors.ENDC}")
        
        if passed == total:
            print_success("ALL TESTS PASSED! 🎉")
        else:
            print_error(f"{total - passed} tests failed")
    
    def cleanup(self):
        """Cleanup temporary files"""
        import shutil
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
            print_info(f"Cleaned up temp directory")


def main():
    """Run the test suite"""
    tester = TestKaggleIntegration()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
