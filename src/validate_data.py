# scripts/validate_data.py
# author: Yeji Sohn
# date: 2024-12-06

import pandas as pd
import numpy as np
import pandera as pa
from pandera import Column, Check, DataFrameSchema
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import FeatureLabelCorrelation, FeatureFeatureCorrelation, PredictionDrift

def check_proportions(series, tolerance=0.1):
    """
    Checks if the proportions of class labels (0 and 1) in a given pandas Series 
    are approximately balanced within a specified tolerance.

    Parameters:
    series (pandas.Series): A pandas Series containing binary class labels (0s and 1s).
    tolerance (float, optional): The acceptable tolerance for the proportions of each class.
                                 The default is 0.1, meaning the proportions of 0 and 1 
                                 must be within 0.1 of 0.5 to return True.

    Returns:
    bool: True if the proportions of class 0 and class 1 are approximately equal 
          (within the specified tolerance), False otherwise.
    """

    # Calculate the normalized proportions of the unique values
    proportions = series.value_counts(normalize=True)

    # Check if the proportions of 0 and 1 are within the acceptable tolerance of 0.5
    return np.abs(proportions.get(0, 0) - 0.5) <= tolerance and np.abs(proportions.get(1, 0) - 0.5) <= tolerance

def validate_csv_schema(file_path):
    """
    Validate CSV schema.

    Parameters:
        file_path (str): Path to the CSV file.

    Raises:
        ValueError: If the file cannot be read.
        Exeption: If data is not cleaned.
    """

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise FileNotFoundError(f"❌ Error reading the CSV file: {e}")
    
    # 3. Check for empty observations
    empty_obs_schema = pa.DataFrameSchema(
        checks=[
            Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found.")
        ]
    )

    try:
        empty_obs_schema.validate(df)
        print("Validation passed: No empty observations found.")
    except pa.errors.SchemaError as e:
        print(f"Validation failed: {e}")

    # 4. Missingness not beyond expected threshold
    missingness_threshold_schema = pa.DataFrameSchema(
        {
            # a. Numeric columns with no missing values allowed
            "age": pa.Column(int, pa.Check.between(0, 120), nullable=False),
            "sex": pa.Column(int, pa.Check.isin([0, 1]), nullable=False),

            # b. Numeric columns with missing values allowed up to 5%
            "st_depression": Column(
                float,

                nullable=True
            ),
            "num_of_vessels": Column(
                float,
                checks=[
                    Check(lambda s: np.isnan(s) | (
                        (s >= 0) & (s <= 4)), element_wise=True),
                    Check(lambda s: np.isnan(s).mean() <= 0.05, element_wise=False,
                        error="Too many null values in 'num_of_vessels' column.")
                ],
                nullable=True
            ),

            # c. Categorical column with missing values allowed up to 5%
            "thalassemia": Column(
                str,
                checks=[
                    Check.isin(["normal", "fixed defect", "reversable defect"]),
                    Check(lambda s: s.isna().mean() <= 0.05, element_wise=False,
                        error="Too many null values in 'thalassemia' column."),
                ],
                nullable=True
            )
        }
    )

    try:
        missingness_threshold_schema.validate(df)
        print("Validation passed: No missingness beyond expected threshold.")
    except pa.errors.SchemaError as e:
        print(f"Validation failed: {e}")

    # 2 & 5. Check for correct column names and correct data types in each column
    column_type_schema = pa.DataFrameSchema(
        {
            "age": pa.Column(pa.Int),
            "sex": pa.Column(pa.Int),
            "chest_pain_type": pa.Column(pa.String),
            "resting_blood_pressure": pa.Column(pa.Int),
            "cholesterol": pa.Column(pa.Int),
            "fasting_blood_sugar": pa.Column(pa.Int),
            "rest_ecg": pa.Column(pa.String),
            "max_heart_rate": pa.Column(pa.Int),
            "exercise_induced_angina": pa.Column(pa.String),
            "st_depression": pa.Column(pa.Float),
            "slope": pa.Column(pa.String),
            "num_of_vessels": pa.Column(pa.Float),
            "thalassemia": pa.Column(pa.String),
            "diagnosis": pa.Column(pa.Int)
        }
    )

    try:
        column_type_schema.validate(df)
        print("Validation passed: All columns have correct data types.")
    except pa.errors.SchemaError as e:
        print(f"Validation failed: {e}")

    # 6. No duplicate observations
    duplicate_schema = pa.DataFrameSchema(
        checks=[
            Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found.")
        ]
    )

    try:
        duplicate_schema.validate(df)
        print("Validation passed: No duplicates found.")
    except pa.errors.SchemaError as e:
        print(f"Validation failed: {e}")

    # 7. No Outlier or Anamalous Values
    numerical_schema = pa.DataFrameSchema(
        {
            "age": Column(int, Check.between(0, 120), nullable=True),
            "resting_blood_pressure": Column(int, Check.between(70, 200), nullable=True),
            "cholesterol": Column(int, Check.between(100, 600), nullable=True),
            "max_heart_rate": Column(int, Check.between(60, 220), nullable=True),
            "fasting_blood_sugar": pa.Column(int, pa.Check.isin([0, 1]), nullable=False)  
        }
    )

    try:
        numerical_schema.validate(df)
        print("Validation passed: No outliers found.")
    except pa.errors.SchemaError as e:
        print(f"Validation failed: {e}")

    # 8: Correct Category Levels
    map_categorical_schema = pa.DataFrameSchema(
        {
            "chest_pain_type": Column(
                str, Check.isin(["typical angina", "atypical angina",
                                "non-anginal pain", "asymptomatic"])
            ),
            "fasting_blood_sugar": Column(
                int, Check.isin([0, 1])
            ),
            "rest_ecg": Column(
                str, Check.isin(["normal", "ST-T wave abnormality",
                                "left ventricular hypertrophy"])
            ),
            "exercise_induced_angina": Column(
                str, Check.isin(["no", "yes"])
            ),
            "slope": Column(
                str, Check.isin(["upsloping", "flat", "downsloping"])
            ),
            "thalassemia": Column(
                str, Check.isin(["normal", "fixed defect", "reversable defect"])
            ),
            "diagnosis": Column(
                int, Check.isin([0, 1])
            )
        }
    )

    try:
        map_categorical_schema.validate(df)
        print("Validation passed: All categorical mappings are correct.")
    except pa.errors.SchemaError as e:
        print(f"Validation failed: {e}")

    # 9. Check Target/Response Variable Data Distribution
    proportion_check_schema = pa.DataFrameSchema(
        {
            "diagnosis": Column(
                int,
                Check(lambda s: check_proportions(s),
                    error="Class proportions are not balanced.")
            )
        }
    )

    try:
        proportion_check_schema.validate(df)
        print("Validation passed: Class proportions are as expected.")
    except pa.errors.SchemaError as e:
        print(f"Validation failed: {e}")

    # 10. Deep check anomalous correlations between target/response variable and features/explanatory variables
    deepchecks_dataset = Dataset(
        df,
        label="diagnosis",
        cat_features=[]
    )

    check_feat_lab_corr = FeatureLabelCorrelation()

    check_feat_lab_corr = (check_feat_lab_corr
                        .add_condition_feature_pps_less_than(0.9))

    result = check_feat_lab_corr.run(dataset=deepchecks_dataset)

    if not result.passed_conditions():
        raise ValueError(
            "Feature-Label correlation exceeds the acceptable threshold."
        )

    # 11. Deep check anomalous correlations between features/explanatory variables

    deepchecks_dataset = Dataset(
        df,
        label="diagnosis",
        cat_features=[]
    )

    check_feat_feat_corr = FeatureFeatureCorrelation(threshold=0.9)
    result = check_feat_feat_corr.run(dataset=deepchecks_dataset)

    if not result.passed_conditions():
        raise ValueError(
            "Anomalous correlations between features found."
            "Some feature correlations exceed the acceptable threshold."
        )