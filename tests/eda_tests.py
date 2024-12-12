import os
import pandas as pd
import pytest
import sys
"""
Creates EDA plots for the pre-processed training data from the Wisconsin breast cancer data. Saves the plots as a PDF and PNG file.

Usage: scripts/eda_function.py --train=<train> --out_dir=<out_dir>

Options:
--train=<train>     Path (including filename) to training data (which needs to be saved as a CSV file)
--out_dir=<out_dir> Path to directory where the plots should be saved
"""

# Import the main function from the eda_function module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.eda_function import main

# Test data
valid_data = pd.DataFrame({
    "diagnosis": ["Healthy", "Diseased", "Healthy", "Diseased"],
    "age": [50, 60, 45, 70],
    "resting_blood_pressure": [120, 140, 110, 130],
    "cholesterol": [200, 240, 180, 260],
    "max_heart_rate": [150, 120, 160, 110],
    "st_depression": [1.0, 2.5, 0.5, 3.0]
})

empty_data = pd.DataFrame()

missing_column_data = pd.DataFrame({
    "age": [50, 60, 45, 70],
    "resting_blood_pressure": [120, 140, 110, 130],
    "cholesterol": [200, 240, 180, 260],
    "max_heart_rate": [150, 120, 160, 110],
    "st_depression": [1.0, 2.5, 0.5, 3.0]
})

# Expected Outputs
expected_output_files = [
    "diagnosis_distribution.png",
    "correlation_heatmap.png",
    "feature_densities_by_diagnosis.png"
]

# Test for successful plot creation
def test_main_creates_plots(tmp_path):
    csv_path = tmp_path / "valid_data.csv"
    output_dir = tmp_path / "output"
    valid_data.to_csv(csv_path, index=False)
    
    main(csv_path, output_dir)
    
    for file_name in expected_output_files:
        assert os.path.exists(output_dir / file_name), f"{file_name} was not created."
