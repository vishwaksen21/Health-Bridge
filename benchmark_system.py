#!/usr/bin/env python3
"""
Performance Benchmarking Script
Measures improvements in the Kaggle integration system
"""

import sys
import os
import time
import tempfile
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from dataset_manager import KaggleDatasetManager


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(title):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{title:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_metric(name, value, unit="", threshold=None):
    """Print a metric with formatting"""
    if threshold and isinstance(value, (int, float)):
        color = Colors.GREEN if value < threshold else Colors.YELLOW
    else:
        color = Colors.CYAN
    
    print(f"{name:.<40} {color}{value:>12.2f}{Colors.ENDC} {unit}")


def benchmark_dataset_operations():
    """Benchmark dataset operations"""
    print_header("BENCHMARK 1: Dataset Operations Performance")
    
    results = {}
    temp_dir = tempfile.mkdtemp()
    manager = KaggleDatasetManager(data_dir=temp_dir)
    
    try:
        # Test 1: List datasets
        start = time.time()
        for _ in range(100):
            datasets = manager.list_available_datasets()
        time_list = (time.time() - start) / 100
        results['list_datasets_avg'] = time_list * 1000  # ms
        print_metric("Average time to list datasets", results['list_datasets_avg'], "ms", 5)
        
        # Test 2: Get disease mapping
        start = time.time()
        for _ in range(100):
            mapping = manager.get_disease_mapping()
        time_mapping = (time.time() - start) / 100
        results['disease_mapping_avg'] = time_mapping * 1000
        print_metric("Average time for disease mapping", results['disease_mapping_avg'], "ms", 5)
        
        # Test 3: Check dataset status
        start = time.time()
        for _ in range(100):
            status = manager.get_dataset_status()
        time_status = (time.time() - start) / 100
        results['check_status_avg'] = time_status * 1000
        print_metric("Average time to check status", results['check_status_avg'], "ms", 5)
        
        # Test 4: Create and integrate mock dataset
        df = pd.DataFrame({
            'Glucose': np.random.randint(50, 200, 1000),
            'BMI': np.random.uniform(18, 55, 1000),
            'Age': np.random.randint(21, 81, 1000),
            'Outcome': np.random.randint(0, 2, 1000)
        })
        
        start = time.time()
        result = manager.integrate_dataset("diabetes", df)
        time_integrate = time.time() - start
        results['integrate_dataset'] = time_integrate
        print_metric("Time to integrate 1000-row dataset", results['integrate_dataset'] * 1000, "ms")
        
        # Test 5: Load dataset
        start = time.time()
        loaded = manager.load_dataset("diabetes")
        time_load = time.time() - start
        results['load_dataset'] = time_load
        print_metric("Time to load 1000-row dataset", results['load_dataset'] * 1000, "ms")
        
        # Test 6: Get dataset summary
        start = time.time()
        summary = manager.get_dataset_summary()
        time_summary = time.time() - start
        results['get_summary'] = time_summary
        print_metric("Time to get dataset summary", results['get_summary'] * 1000, "ms")
        
        print(f"\n{Colors.GREEN}✅ All benchmarks completed{Colors.ENDC}")
        
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    return results


def benchmark_dataset_merging():
    """Benchmark dataset merging performance"""
    print_header("BENCHMARK 2: Dataset Merging Performance")
    
    results = {}
    temp_dir = tempfile.mkdtemp()
    manager = KaggleDatasetManager(data_dir=temp_dir)
    
    try:
        # Create test datasets using available dataset names
        test_datasets = ["diabetes", "heart_disease", "respiratory", "mental_health"]
        sizes = [100, 500, 1000, 5000]
        
        for dataset_name, size in zip(test_datasets, sizes):
            df = pd.DataFrame({
                f'col_{i}': np.random.randn(size) for i in range(10)
            })
            manager.integrate_dataset(dataset_name, df)
        
        # Test merging performance
        start = time.time()
        merged = manager.merge_datasets(test_datasets)
        merge_time = time.time() - start
        
        results['merge_time'] = merge_time
        results['merged_rows'] = len(merged)
        results['merged_cols'] = len(merged.columns)
        
        print_metric("Time to merge 4 datasets", merge_time * 1000, "ms")
        print_metric("Total rows in merged dataset", results['merged_rows'], "rows")
        print_metric("Total columns in merged dataset", results['merged_cols'], "cols")
        
        # Calculate merge efficiency
        efficiency = results['merged_rows'] / merge_time
        results['merge_efficiency'] = efficiency
        print_metric("Merge efficiency", efficiency, "rows/sec")
        
        print(f"\n{Colors.GREEN}✅ Merge benchmarks completed{Colors.ENDC}")
        
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    return results


def benchmark_memory_usage():
    """Benchmark memory usage"""
    print_header("BENCHMARK 3: Memory Usage Analysis")
    
    results = {}
    temp_dir = tempfile.mkdtemp()
    manager = KaggleDatasetManager(data_dir=temp_dir)
    
    try:
        import psutil
        import os
        process = psutil.Process(os.getpid())
        
        # Baseline memory
        baseline = process.memory_info().rss / 1024 / 1024  # MB
        print_metric("Baseline memory usage", baseline, "MB")
        
        # Create large dataset
        df_large = pd.DataFrame({
            f'col_{i}': np.random.randn(10000) for i in range(50)
        })
        
        mem_after_create = process.memory_info().rss / 1024 / 1024
        memory_for_dataset = mem_after_create - baseline
        results['memory_for_large_dataset'] = memory_for_dataset
        print_metric("Memory for 10K×50 dataset", memory_for_dataset, "MB")
        
        # Integrate dataset
        manager.integrate_dataset("large_test", df_large)
        
        mem_after_integrate = process.memory_info().rss / 1024 / 1024
        memory_for_integration = mem_after_integrate - mem_after_create
        results['memory_for_integration'] = memory_for_integration
        print_metric("Memory for integration", memory_for_integration, "MB")
        
        # Load dataset back
        loaded = manager.load_dataset("large_test")
        
        mem_after_load = process.memory_info().rss / 1024 / 1024
        memory_for_load = mem_after_load - mem_after_integrate
        results['memory_for_load'] = memory_for_load
        print_metric("Memory for loading dataset", memory_for_load, "MB")
        
        print(f"\n{Colors.GREEN}✅ Memory benchmarks completed{Colors.ENDC}")
        
    except ImportError:
        print(f"{Colors.YELLOW}⚠️  psutil not installed, skipping memory benchmarks{Colors.ENDC}")
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    return results


def benchmark_error_handling():
    """Benchmark error handling performance"""
    print_header("BENCHMARK 4: Error Handling Performance")
    
    results = {}
    temp_dir = tempfile.mkdtemp()
    manager = KaggleDatasetManager(data_dir=temp_dir)
    
    try:
        # Test 1: Invalid dataset handling
        start = time.time()
        for _ in range(1000):
            try:
                manager.load_dataset("nonexistent")
            except FileNotFoundError:
                pass
        time_error = (time.time() - start) / 1000
        results['error_handling_time'] = time_error * 1000
        print_metric("Average time to handle error", results['error_handling_time'], "ms")
        
        # Test 2: Validation
        start = time.time()
        result = manager.integrate_dataset("invalid", None)
        time_validation = time.time() - start
        results['validation_time'] = time_validation * 1000
        print_metric("Time for dataset validation", results['validation_time'], "ms")
        
        print(f"\n{Colors.GREEN}✅ Error handling benchmarks completed{Colors.ENDC}")
        
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    return results


def benchmark_metadata_operations():
    """Benchmark metadata operations"""
    print_header("BENCHMARK 5: Metadata Operations Performance")
    
    results = {}
    temp_dir = tempfile.mkdtemp()
    manager = KaggleDatasetManager(data_dir=temp_dir)
    
    try:
        # Create test data
        for i in range(5):
            df = pd.DataFrame({
                'col_1': np.random.randn(1000),
                'col_2': np.random.randn(1000),
            })
            manager.integrate_dataset(f"dataset_{i}", df)
        
        # Test 1: Save metadata
        start = time.time()
        for _ in range(100):
            manager.save_metadata()
        time_save = (time.time() - start) / 100
        results['save_metadata_avg'] = time_save * 1000
        print_metric("Average metadata save time", results['save_metadata_avg'], "ms")
        
        # Test 2: Load metadata
        start = time.time()
        for _ in range(100):
            manager.load_metadata()
        time_load = (time.time() - start) / 100
        results['load_metadata_avg'] = time_load * 1000
        print_metric("Average metadata load time", results['load_metadata_avg'], "ms")
        
        # Test 3: Update metadata
        start = time.time()
        for _ in range(100):
            manager.metadata['test_key'] = 'test_value'
            manager.save_metadata()
        time_update = (time.time() - start) / 100
        results['update_metadata_avg'] = time_update * 1000
        print_metric("Average metadata update time", results['update_metadata_avg'], "ms")
        
        print(f"\n{Colors.GREEN}✅ Metadata benchmarks completed{Colors.ENDC}")
        
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    return results


def print_summary(all_results):
    """Print benchmark summary"""
    print_header("BENCHMARK SUMMARY")
    
    print(f"\n{Colors.BOLD}Performance Metrics:{Colors.ENDC}\n")
    
    for category, results in all_results.items():
        if results:
            print(f"{Colors.CYAN}{category}:{Colors.ENDC}")
            for key, value in results.items():
                if isinstance(value, float):
                    print(f"  • {key}: {value:.4f}")
                else:
                    print(f"  • {key}: {value}")
            print()
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✨ All benchmarks completed!{Colors.ENDC}\n")


def main():
    """Run all benchmarks"""
    print_header("🏃 KAGGLE INTEGRATION SYSTEM BENCHMARKS")
    print(f"Timestamp: {datetime.now().isoformat()}\n")
    
    all_results = {
        "Dataset Operations": benchmark_dataset_operations(),
        "Dataset Merging": benchmark_dataset_merging(),
        "Memory Usage": benchmark_memory_usage(),
        "Error Handling": benchmark_error_handling(),
        "Metadata Operations": benchmark_metadata_operations(),
    }
    
    print_summary(all_results)


if __name__ == "__main__":
    main()
