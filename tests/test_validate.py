import pytest
import pandas as pd
import sys
import requests
from requests.exceptions import HTTPError
import os
import pandera as pa
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from validate_data import check_proportions, validate_csv_schema

MOCK_DATA = pd.DataFrame({
    "age": [63, 67, 67, 37, 41, 56, 62],
    "sex": [1, 1, 1, 1, 0, 0, 0],
    "chest_pain_type": ["typical angina", "typical angina", "asymptomatic", "non-anginal pain", "typical angina", "atypical angina", "non-anginal pain"],
    "resting_blood_pressure": [145, 160, 120, 130, 130, 120, 140],
    "cholesterol": [233, 286, 229, 250, 204, 236, 275],
    "fasting_blood_sugar": [1, 0, 0, 0, 0, 0, 0],
    "rest_ecg": ["normal", "normal", "normal", "normal", "normal", "normal", "normal"],
    "max_heart_rate": [150, 108, 129, 187, 172, 178, 148],
    "exercise_induced_angina": ["no", "yes", "no", "no", "yes", "no", "no"],
    "st_depression": [2.3, 3.1, 2.2, 3.0, 1.5, 2.6, 2.9],
    "slope": ["flat", "downsloping", "flat", "upsloping", "upsloping", "flat", "downsloping"],
    "num_of_vessels": [2, 3, 1, 0, 0, 1, 0],
    "thalassemia": ["fixed defect", "reversable defect", "normal", "fixed defect", "fixed defect", "reversable defect", "fixed defect"],
    "diagnosis": [1, 1, 1, 0, 1, 0, 0]
})

def test_check_proportions():
    # Balanced case
    balanced_series = pd.Series([0, 1, 0, 1, 0, 1, 0])
    assert check_proportions(balanced_series) == True
    
    # Imbalanced case
    imbalanced_series = pd.Series([0, 0, 0, 1, 1, 0, 0])
    assert check_proportions(imbalanced_series) == False
    
    # Edge case with empty series
    empty_series = pd.Series([])
    assert check_proportions(empty_series) == True

# Test validate_csv_schema with mocked data
@pytest.fixture
def mock_dataframe():
    return MOCK_DATA

# Test validate_csv_schema with missing values above threshold (should fail)
def test_missing_values_check(mock_dataframe, tmp_path):
    invalid_df = mock_dataframe.copy()
    num_rows = len(invalid_df)
    # Seelct 99% of rows
    num_nan_rows = int(num_rows * 0.99) 
    nan_indices = np.random.choice(invalid_df.index, size=num_nan_rows, replace=False)
    # Set selected rows to nan
    invalid_df.loc[nan_indices, 'num_of_vessels'] = np.nan

    csv_file = tmp_path / "mock_data.csv"
    invalid_df.to_csv(csv_file, index=False)

    with pytest.raises(pa.errors.SchemaError):
        validate_csv_schema(str(csv_file))

# Test validate_csv_schema with missing column (should fail)
def test_validate_csv_schema_missing_column(mock_dataframe, tmp_path):
    invalid_df = mock_dataframe.copy()
    invalid_df = invalid_df.drop(columns=["age"])  

    csv_file = tmp_path / "mock_data.csv"
    invalid_df.to_csv(csv_file, index=False)

    with pytest.raises(pa.errors.SchemaError):
        validate_csv_schema(str(csv_file))

# Test validate_csv_schema for valid categorical columns (should pass)
def test_validate_csv_schema_valid_categorical(mock_dataframe, tmp_path):
    csv_file = tmp_path / "mock_data.csv"
    mock_dataframe.to_csv(csv_file, index=False)

    try:
        validate_csv_schema(str(csv_file))
    except Exception as e:
        assert False, f"Validation failed with error: {e}"

# Test validate_csv_schema for invalid categorical values (should fail)
def test_validate_csv_schema_invalid_categorical(mock_dataframe, tmp_path):
    invalid_df = mock_dataframe.copy()
    invalid_df.loc[0, 'chest_pain_type'] = 'unknown'  # Invalid category

    csv_file = tmp_path / "mock_data.csv"
    invalid_df.to_csv(csv_file, index=False)

    with pytest.raises(pa.errors.SchemaError):
        validate_csv_schema(str(csv_file))

# Test validate_csv_schema for numerical column outliers (should pass)
def test_validate_csv_schema_numerical_outliers(mock_dataframe, tmp_path):
    csv_file = tmp_path / "mock_data.csv"
    mock_dataframe.to_csv(csv_file, index=False)

    try:
        validate_csv_schema(str(csv_file))
    except Exception as e:
        assert False, f"Validation failed with error: {e}"

# Test validate_csv_schema for invalid numerical column values (should fail)
def test_validate_csv_schema_invalid_numerical(mock_dataframe, tmp_path):
    invalid_df = mock_dataframe.copy()
    invalid_df.loc[0, 'age'] = 150  # Invalid age value

    csv_file = tmp_path / "mock_data.csv"
    invalid_df.to_csv(csv_file, index=False)


    with pytest.raises(pa.errors.SchemaError):
        validate_csv_schema(str(csv_file))

# pytest tests/test_validate.py