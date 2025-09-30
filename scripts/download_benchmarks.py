#!/usr/bin/env python3
"""
Script to download all MathArena benchmark datasets to a specified directory.
"""

import argparse
import os
from datasets import load_dataset

def download_all_benchmarks(data_dir="data"):
    """Download all benchmark datasets to the specified directory."""
    competition_configs = []
    
    # Find all competition config files
    for root, dirs, files in os.walk("configs/competitions"):
        for file in files:
            if file.endswith(".yaml"):
                competition_configs.append(os.path.join(root, file))
    
    os.makedirs(data_dir, exist_ok=True)
    
    downloaded_datasets = set()
    
    for config_path in competition_configs:
        try:
            import yaml
            with open(config_path, "r") as f:
                comp_config = yaml.safe_load(f)
            
            dataset_path = comp_config["dataset_path"]
            
            # Skip if already downloaded this dataset
            if dataset_path in downloaded_datasets:
                continue
            
            # Check if it's a local path that already exists
            if os.path.exists(dataset_path):
                print(f"Skipping local dataset: {dataset_path}")
                continue
            
            print(f"Downloading {dataset_path}...")
            load_dataset(dataset_path, cache_dir=data_dir)
            downloaded_datasets.add(dataset_path)
            
        except Exception as e:
            print(f"Error processing {config_path}: {e}")
            continue
    
    print(f"Downloaded {len(downloaded_datasets)} benchmark datasets to {data_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=str, default="data", help="Directory to store downloaded datasets")
    args = parser.parse_args()
    
    download_all_benchmarks(args.data_dir)
