#!/usr/bin/env python3
"""
Automated Kaggle Dataset Downloader
Run this to download all available disease datasets

Features:
  • Verifies Kaggle CLI installation and credentials
  • Downloads datasets with progress tracking
  • Handles errors gracefully with retry logic
  • Provides detailed logging
"""

import os
import subprocess
import sys
import logging
import time
from pathlib import Path
from typing import List, Dict
from dataset_manager import KaggleDatasetManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_kaggle_cli():
    """Check if Kaggle CLI is installed"""
    try:
        result = subprocess.run(
            ["kaggle", "--version"], 
            capture_output=True, 
            check=True,
            timeout=5
        )
        logger.info("Kaggle CLI verified")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Kaggle CLI not available: {e}")
        return False
    except subprocess.TimeoutExpired:
        logger.error("Kaggle CLI check timed out")
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking Kaggle CLI: {e}")
        return False

def check_kaggle_credentials():
    """Check if Kaggle API credentials are set up"""
    kaggle_dir = Path.home() / ".kaggle"
    credentials_file = kaggle_dir / "kaggle.json"
    
    if not credentials_file.exists():
        logger.error(f"Credentials file not found: {credentials_file}")
        return False
    
    try:
        # Verify credentials file is readable
        with open(credentials_file, 'r') as f:
            pass
        logger.info("Kaggle credentials verified")
        return True
    except Exception as e:
        logger.error(f"Failed to read credentials file: {e}")
        return False

def download_datasets(dataset_names: List[str] = None, max_retries: int = 3):
    """Download datasets from Kaggle with retry logic"""
    
    manager = KaggleDatasetManager()
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║         📥 KAGGLE DATASET DOWNLOADER                          ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Check prerequisites
    print("🔍 Checking prerequisites...\n")
    
    if not check_kaggle_cli():
        print("❌ Kaggle CLI not installed")
        print("   Install with: pip install kaggle")
        logger.error("Kaggle CLI check failed")
        return False
    print("✅ Kaggle CLI installed\n")
    
    if not check_kaggle_credentials():
        print("❌ Kaggle credentials not found")
        print("   Setup instructions:")
        print("   1. Go to https://www.kaggle.com/settings/account")
        print("   2. Click 'Create New API Token'")
        print("   3. Save to ~/.kaggle/kaggle.json")
        print("   4. Run: chmod 600 ~/.kaggle/kaggle.json")
        logger.error("Kaggle credentials check failed")
        return False
    print("✅ Kaggle credentials configured\n")
    
    # Select datasets to download
    all_datasets = manager.list_available_datasets()
    
    if dataset_names is None:
        dataset_names = list(all_datasets.keys())
    
    print(f"📦 Found {len(dataset_names)} datasets to download\n")
    
    # Download each dataset
    results = {
        "successful": [],
        "failed": [],
        "skipped": []
    }
    
    for idx, dataset_name in enumerate(dataset_names, 1):
        if dataset_name not in all_datasets:
            print(f"⚠️  Unknown dataset: {dataset_name}")
            results["skipped"].append(dataset_name)
            logger.warning(f"Skipped unknown dataset: {dataset_name}")
            continue
        
        info = all_datasets[dataset_name]
        kaggle_id = info["kaggle_id"]
        dataset_dir = manager.data_dir / dataset_name
        
        print(f"[{idx}/{len(dataset_names)}] 📥 {dataset_name.upper()}")
        print(f"   Kaggle ID: {kaggle_id}")
        
        # Attempt download with retries
        download_success = False
        for attempt in range(1, max_retries + 1):
            try:
                # Create dataset directory
                dataset_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Attempt {attempt}/{max_retries} to download {dataset_name}")
                
                # Download dataset
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
                    timeout=300  # 5 minute timeout
                )
                
                if result.returncode == 0:
                    print(f"   ✅ Downloaded successfully (attempt {attempt})")
                    results["successful"].append(dataset_name)
                    logger.info(f"Successfully downloaded {dataset_name}")
                    download_success = True
                    break
                else:
                    if attempt < max_retries:
                        wait_time = attempt * 2
                        print(f"   ⏳ Retrying in {wait_time}s... (attempt {attempt})")
                        time.sleep(wait_time)
                    else:
                        print(f"   ❌ Download failed after {max_retries} attempts")
                        print(f"   Error: {result.stderr[:200]}")
                        logger.error(f"Download failed for {dataset_name}: {result.stderr}")
                        results["failed"].append(dataset_name)
            
            except subprocess.TimeoutExpired:
                if attempt < max_retries:
                    print(f"   ⏳ Timeout, retrying... (attempt {attempt})")
                    time.sleep(5)
                else:
                    print(f"   ❌ Download timed out after {max_retries} attempts")
                    logger.error(f"Download timeout for {dataset_name}")
                    results["failed"].append(dataset_name)
            
            except Exception as e:
                if attempt < max_retries:
                    print(f"   ⏳ Error, retrying... (attempt {attempt})")
                    time.sleep(5)
                else:
                    print(f"   ❌ Error: {str(e)}")
                    logger.error(f"Download error for {dataset_name}: {str(e)}")
                    results["failed"].append(dataset_name)
        
        print()
    
    # Summary
    print("════════════════════════════════════════════════════════════════")
    print("📊 DOWNLOAD SUMMARY")
    print("════════════════════════════════════════════════════════════════\n")
    
    print(f"✅ Successful: {len(results['successful'])}/{len(dataset_names)}")
    if results["successful"]:
        for name in results["successful"]:
            print(f"   • {name}")
    
    if results["failed"]:
        print(f"\n❌ Failed: {len(results['failed'])}")
        for name in results["failed"]:
            print(f"   • {name}")
    
    if results["skipped"]:
        print(f"\n⏭️  Skipped: {len(results['skipped'])}")
        for name in results["skipped"]:
            print(f"   • {name}")
    
    print("\n════════════════════════════════════════════════════════════════")
    print(f"Next: python src/integrate_datasets.py")
    print("════════════════════════════════════════════════════════════════\n")
    
    logger.info(f"Download complete: {len(results['successful'])} successful, {len(results['failed'])} failed")
    return len(results["failed"]) == 0


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        datasets_to_download = sys.argv[1:]
    else:
        datasets_to_download = None
    
    success = download_datasets(datasets_to_download)
    sys.exit(0 if success else 1)
