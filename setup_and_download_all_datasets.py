#!/usr/bin/env python3
"""
Complete Setup & Download Script for All Datasets

This script automates:
1. Checking Kaggle credentials
2. Downloading all medical datasets (8 original + 4 new medicinal/drug datasets)
3. Integrating datasets into SQLite database
4. Verifying data integrity
"""

import os
import sys
import subprocess
from pathlib import Path
import time


def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def check_kaggle_setup():
    """Check if Kaggle CLI is properly configured"""
    print_header("🔍 CHECKING KAGGLE SETUP")
    
    # Check if kaggle is installed
    try:
        result = subprocess.run(
            ["kaggle", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print("✅ Kaggle CLI installed")
    except FileNotFoundError:
        print("❌ Kaggle CLI not installed")
        print("\n📦 Install with:")
        print("   pip install kaggle")
        return False
    except Exception as e:
        print(f"❌ Error checking Kaggle CLI: {e}")
        return False
    
    # Check credentials
    kaggle_dir = Path.home() / ".kaggle"
    credentials_file = kaggle_dir / "kaggle.json"
    
    if not credentials_file.exists():
        print("❌ Kaggle credentials not found")
        print(f"\n📋 Setup Instructions:")
        print("   1. Go to: https://www.kaggle.com/settings/account")
        print("   2. Click 'Create New API Token'")
        print("   3. This downloads kaggle.json")
        print(f"   4. Move it to: {kaggle_dir}/")
        print("   5. Run: chmod 600 ~/.kaggle/kaggle.json")
        return False
    
    print("✅ Kaggle credentials configured")
    return True


def setup_directories():
    """Create necessary directories"""
    print_header("📁 SETTING UP DIRECTORIES")
    
    dirs = [
        Path("data/kaggle_datasets"),
        Path("data/kaggle_datasets/medicinal_plants"),
        Path("data/kaggle_datasets/indian_medicinal_plants"),
        Path("data/kaggle_datasets/drugs_reviews"),
        Path("data/kaggle_datasets/medicine_recommendation"),
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ {dir_path}")
    
    return True


def download_datasets():
    """Download all datasets"""
    print_header("📥 DOWNLOADING DATASETS")
    
    if not check_kaggle_setup():
        print("\n⚠️  Skipping downloads - Kaggle not configured")
        return False
    
    datasets = {
        "medicinal_plants": "jcanotorr/medicinal-plants-dataset",
        "indian_medicinal_plants": "hamagj/indian-medicinal-plants",
        "drugs_reviews": "sanjaymat/drugs-review-dataset",
        "medicine_recommendation": "prathamikjain/medicine-recommendation-using-machine-learning"
    }
    
    print("Starting dataset downloads...\n")
    
    for dataset_name, kaggle_id in datasets.items():
        print(f"📦 Downloading: {dataset_name}")
        print(f"   Kaggle ID: {kaggle_id}")
        
        dataset_dir = Path(f"data/kaggle_datasets/{dataset_name}")
        
        try:
            cmd = [
                "kaggle", "datasets", "download",
                "-d", kaggle_id,
                "-p", str(dataset_dir),
                "--unzip"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print(f"   ✅ Downloaded successfully\n")
            else:
                print(f"   ⚠️  Download failed: {result.stderr[:100]}\n")
        
        except subprocess.TimeoutExpired:
            print(f"   ⏱️  Download timed out\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
    
    return True


def integrate_datasets():
    """Run the integration script"""
    print_header("🔗 INTEGRATING DATASETS INTO DATABASE")
    
    try:
        result = subprocess.run(
            ["python3", "src/integrate_medicinal_datasets.py"],
            capture_output=False,
            text=True,
            cwd="."
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Integration failed: {e}")
        return False


def verify_database():
    """Verify database contents"""
    print_header("✔️  VERIFYING DATABASE")
    
    try:
        import sqlite3
        db_path = Path("data/medical_knowledge.db")
        
        if not db_path.exists():
            print("❌ Database file not found")
            return False
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"✅ Database found: {db_path.stat().st_size / 1024:.1f} KB")
        print(f"✅ Tables: {len(tables)}")
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   • {table[0]}: {count} records")
        
        conn.close()
        return True
    
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False


def main():
    """Main execution"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🌿 MEDICAL DATASETS COMPLETE SETUP & INTEGRATION              ║
║                                                                  ║
║   Downloads:                                                     ║
║   • Medicinal Plants Dataset                                    ║
║   • Indian Medicinal Plants (Ayurveda)                          ║
║   • Drugs.com Reviews Dataset                                   ║
║   • Medicine Recommendation Dataset                              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    steps = [
        ("Setup Directories", setup_directories),
        ("Check Kaggle Configuration", check_kaggle_setup),
        ("Download Datasets", download_datasets),
        ("Integrate Datasets", integrate_datasets),
        ("Verify Database", verify_database),
    ]
    
    results = {}
    
    for step_name, step_func in steps:
        try:
            print(f"\n▶️  Step: {step_name}")
            results[step_name] = step_func()
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error in {step_name}: {e}")
            results[step_name] = False
    
    # Final summary
    print_header("📊 FINAL SUMMARY")
    
    for step_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ SKIPPED/FAILED"
        print(f"{step_name}: {status}")
    
    all_success = all(results.values())
    
    print("\n" + "="*70)
    if all_success:
        print("🎉 ALL STEPS COMPLETED SUCCESSFULLY!")
        print("\n✅ Your system is ready with:")
        print("   • Medicinal Plants Database")
        print("   • Indian Medicinal Plants (Ayurvedic)")
        print("   • Drug Reviews Integration")
        print("   • Medicine Recommendations")
        print("\n💡 Next: Run 'python main.py' to start the health recommendation system")
    else:
        print("⚠️  Some steps were skipped or failed")
        print("   Check the setup guide for more information")
    print("="*70 + "\n")
    
    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
