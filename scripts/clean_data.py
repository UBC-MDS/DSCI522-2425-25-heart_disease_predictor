# clean_data.py
# author: Yeji Sohn
# date: 2024-12-02

import click
import os
import pandas as pd

@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")

def main(raw_data, data_to):
    """
    Processes the raw heart disease dataset, renaming columns, relabeling categorical values, 
    and cleaning the data (e.g., dropping missing values).

    Parameters:
    raw_data (str): Path to the raw data CSV file.
    data_to (str): Directory where the processed data will be saved.

    Saves the processed dataset as 'processed_heart_disease_data.csv' in the specified directory.
    """
    new_column_names = ["age", "sex", "chest_pain_type", "resting_blood_pressure", "cholesterol", "fasting_blood_sugar", 
                "rest_ecg", "max_heart_rate", "exercise_induced_angina", "st_depression", "slope", 
               "num_of_vessels", "thalassemia", "diagnosis"]

    df = pd.read_csv(raw_data, names=new_column_names, header=None).drop(columns=['id'])

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

    df.to_csv(os.path.join(data_to, "processed_heart_disease_data.csv"), index=False)


if __name__ == '__main__':
    main()