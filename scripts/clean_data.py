# clean_data.py
# author: Yeji Sohn
# date: 2024-12-06

import click
import os
import pandas as pd
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from validate_data import validate_csv_schema

import warnings
warnings.filterwarnings('ignore')

def clean_data(raw_data, write_to):
    """
    Processes the raw heart disease dataset, renaming columns, relabeling categorical values, 
    and cleaning the data (e.g., dropping missing values).

    Parameters:
    raw_data (str): Path to the raw data CSV file.
    write_to (str): Directory where the processed data will be saved.

    Saves the processed dataset as 'processed_heart_disease_data.csv' in the specified directory.
    """

    df = pd.read_csv(raw_data)

    # rename columns
    new_column_names = ["age", "sex", "chest_pain_type", "resting_blood_pressure", "cholesterol", "fasting_blood_sugar", 
                "rest_ecg", "max_heart_rate", "exercise_induced_angina", "st_depression", "slope", 
               "num_of_vessels", "thalassemia", "diagnosis"]
    
    df.columns = new_column_names

    # re-label classes
    df.loc[(df['chest_pain_type'] == 1), 'chest_pain_type'] = 'typical angina'
    df.loc[(df['chest_pain_type'] == 2), 'chest_pain_type'] = 'atypical angina'
    df.loc[(df['chest_pain_type'] == 3), 'chest_pain_type'] = 'non-anginal pain'
    df.loc[(df['chest_pain_type'] == 4), 'chest_pain_type'] = 'asymptomatic'

    df.loc[(df['fasting_blood_sugar'] == 'yes'), 'fasting_blood_sugar'] = 1
    df.loc[(df['fasting_blood_sugar'] == 'no'), 'fasting_blood_sugar'] = 0

    df.loc[(df['rest_ecg'] == 0), 'rest_ecg'] = 'normal'
    df.loc[(df['rest_ecg'] == 1), 'rest_ecg'] = 'ST-T wave abnormality'
    df.loc[(df['rest_ecg'] == 2), 'rest_ecg'] = 'left ventricular hypertrophy'

    df.loc[(df['exercise_induced_angina'] == 0), 'exercise_induced_angina'] = 'no'
    df.loc[(df['exercise_induced_angina'] == 1), 'exercise_induced_angina'] = 'yes'

    df.loc[(df['slope'] == 1), 'slope'] = 'upsloping'
    df.loc[(df['slope'] == 2), 'slope'] = 'flat'
    df.loc[(df['slope'] == 3), 'slope'] = 'downsloping'

    df.loc[(df['thalassemia'] == 3.), 'thalassemia'] = 'normal'
    df.loc[(df['thalassemia'] == 6.), 'thalassemia'] = 'fixed defect'
    df.loc[(df['thalassemia'] == 7.), 'thalassemia'] = 'reversable defect'

    df.loc[(df['diagnosis'] == 2), 'diagnosis'] = 1
    df.loc[(df['diagnosis'] == 3), 'diagnosis'] = 1
    df.loc[(df['diagnosis'] == 4), 'diagnosis'] = 1

    # drop null values
    df = df.dropna()

    try:
        df.to_csv(os.path.join(write_to, "cleaned_heart_disease_data.csv"), index=False)
    except:
        os.mkdir(write_to)
        df.to_csv(os.path.join(write_to, "cleaned_heart_disease_data.csv"), index=False)

@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")
@click.option('--write-to', type=str, help="Path to directory where processed data will be written to")
def main(raw_data, write_to):

    clean_data(raw_data, write_to)
    validate_csv_schema(os.path.join(write_to, "cleaned_heart_disease_data.csv"))
    


if __name__ == '__main__':
    main()