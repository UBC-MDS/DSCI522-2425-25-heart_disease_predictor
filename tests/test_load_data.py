import pytest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.load_data import load_data

# Create Sample data for testing
X_sample = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6]})
y_sample = pd.DataFrame({'target': [0, 1, 0]})

def test_load_data_success(tmp_path):
    """Test that load_data successfully reads CSV files."""
    X_path = tmp_path / "X_data.csv"
    y_path = tmp_path / "y_data.csv"
    X_sample.to_csv(X_path, index=False)
    y_sample.to_csv(y_path, index=False)
    
    X_data, y_data = load_data(X_path, y_path)
    assert X_data.equals(X_sample)
    assert y_data.equals(y_sample.squeeze())

def test_load_data_file_not_found():
    """Test that load_data raises FileNotFoundError if files are missing."""
    with pytest.raises(FileNotFoundError):
        load_data('non_existent_X.csv', 'non_existent_y.csv')

def test_load_data_squeeze(tmp_path):
    """Test that y_data is squeezed to a Series if it has one column."""
    y = pd.DataFrame({'target': [0, 1, 0]})
    y_path = tmp_path / "y_data.csv"
    y.to_csv(y_path, index=False)
    X_path = tmp_path / "X_data.csv"
    X_sample.to_csv(X_path, index=False) 
    _, y_data = load_data(X_path, y_path)
    assert isinstance(y_data, pd.Series)

# pytest tests/test_load_data.py

