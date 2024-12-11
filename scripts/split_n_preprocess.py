import pandas as pd
import numpy as np
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os
import click

@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
@click.option('--preprocessor-to', type=str, help="Path to directory where the preprocessor object will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)

def main(raw_data, data_to, preprocessor_to, seed):
    '''This script splits the raw data into train and test sets, 
    and then preprocesses the data for use in model training.
    It also saves the preprocessor to be used in the model training script.'''
    
    np.random.seed(seed)
    
    df = pd.read_csv(raw_data)

    X = df.drop(columns=["diagnosis"])
    y = df["diagnosis"]

   
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)

    numeric_features = [
        "age", 
        "resting_blood_pressure", 
        "fasting_blood_sugar", 
        "cholesterol", 
        "max_heart_rate", 
        "st_depression", 
        "sex"
    ]
    categorical_features = [
        "chest_pain_type", 
        "rest_ecg", 
        "exercise_induced_angina", 
        "slope", 
        "num_of_vessels", 
        "thalassemia"
    ]

    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(drop="if_binary", handle_unknown="ignore")

    preprocessor = make_column_transformer(
        (numeric_transformer, numeric_features),
        (categorical_transformer, categorical_features)
    )

    X_train_enc = pd.DataFrame(preprocessor.fit_transform(X_train), columns=preprocessor.get_feature_names_out())
    X_test_enc = pd.DataFrame(preprocessor.transform(X_test), columns=preprocessor.get_feature_names_out())

    try:
        pickle.dump(preprocessor, open(os.path.join(preprocessor_to, "preprocessor.pickle"), "wb"))
    except: 
        os.makedirs(preprocessor_to)
        pickle.dump(preprocessor, open(os.path.join(preprocessor_to, "preprocessor.pickle"), "wb"))

    try:
        X_train_enc.to_csv(os.path.join(data_to, "X_train_transformed.csv"), index=False)
        X_test_enc.to_csv(os.path.join(data_to, "X_test_transformed.csv"), index=False)
        y_train.to_csv(os.path.join(data_to, "y_train.csv"), index=False)
        y_test.to_csv(os.path.join(data_to, "y_test.csv"), index=False)
        X_train.to_csv(os.path.join(data_to, "X_train.csv"), index=False)
        X_test.to_csv(os.path.join(data_to, "X_test.csv"), index=False)
    except: 
        os.makedirs(data_to)
        X_train_enc.to_csv(os.path.join(data_to, "X_train_transformed.csv"), index=False)
        X_test_enc.to_csv(os.path.join(data_to, "X_test_transformed.csv"), index=False)
        y_train.to_csv(os.path.join(data_to, "y_train.csv"), index=False)
        y_test.to_csv(os.path.join(data_to, "y_test.csv"), index=False)
        X_train.to_csv(os.path.join(data_to, "X_train.csv"), index=False)
        X_test.to_csv(os.path.join(data_to, "X_test.csv"), index=False)
    

if __name__ == '__main__':
    main()
