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

CSV_DATA = pd.DataFrame({
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
    assert check_proportions(balanced_series) is True
    
    # Imbalanced case
    imbalanced_series = pd.Series([0, 0, 0, 1, 1, 0, 0])
    assert check_proportions(imbalanced_series) is False
    
    # Edge case with empty series
    empty_series = pd.Series([])
    assert check_proportions(empty_series) is True

# Test validate_csv_schema with mocked data
@pytest.fixture
def mock_dataframe():
    return CSV_DATA

# Test validate_csv_schema with missing values above threshold (should fail)
def test_missing_values_check(mock_dataframe):
    invalid_df = mock_dataframe.copy()
    invalid_df.loc[0, 'num_of_vessels'] = np.nan
    invalid_df.loc[1, 'num_of_vessels'] = np.nan
    try:
        validate_csv_schema(invalid_df)
        pytest.fail("Validation should have failed due to too many missing values.")
    except pa.errors.SchemaError:
        pass 

# Test validate_csv_schema with missing column (should fail)
def test_validate_csv_schema_missing_column():
    invalid_df = CSV_DATA.drop(columns=["age"])  
    with pytest.raises(pa.errors.SchemaError):
        validate_csv_schema(invalid_df)

# Test validate_csv_schema for valid categorical columns (should pass)
def test_validate_csv_schema_valid_categorical():
    try:
        validate_csv_schema(CSV_DATA)
    except Exception as e:
        assert False, f"Validation failed unexpectedly with error: {e}"

# Test validate_csv_schema for invalid categorical values (should fail)
def test_validate_csv_schema_invalid_categorical():
    invalid_df = CSV_DATA.copy()
    invalid_df.loc[0, 'chest_pain_type'] = 'unknown'  # Invalid category
    with pytest.raises(pa.errors.SchemaError):
        validate_csv_schema(invalid_df)

# Test validate_csv_schema for numerical column outliers (should pass)
def test_validate_csv_schema_numerical_outliers():
    try:
        validate_csv_schema(CSV_DATA)
    except Exception as e:
        assert False, f"Validation failed unexpectedly with error: {e}"

# Test validate_csv_schema for invalid numerical column values (should fail)
def test_validate_csv_schema_invalid_numerical():
    invalid_df = CSV_DATA.copy()
    invalid_df.loc[0, 'age'] = 150  # Invalid age value
    with pytest.raises(pa.errors.SchemaError):
        validate_csv_schema(invalid_df)

# pytest tests/test_validate.py