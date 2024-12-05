import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
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
    
    # Load raw data
    df = pd.read_csv(raw_data)

    # Splitting the data into features X and target y
    X = df.drop(columns=["diagnosis"])
    y = df["diagnosis"]

    # Splitting data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)

    # Defining numeric and categorical features
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

    # Creating transformers for numeric and categorical features
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(drop="if_binary", handle_unknown="ignore")

    # Creating column transformer
    preprocessor = make_column_transformer(
        (numeric_transformer, numeric_features),
        (categorical_transformer, categorical_features)
    )

    # Apply preprocessing pipeline to the training data
    X_train_enc = pd.DataFrame(preprocessor.fit_transform(X_train), columns=preprocessor.get_feature_names_out())
    X_test_enc = pd.DataFrame(preprocessor.transform(X_test), columns=preprocessor.get_feature_names_out())
    
    # Scoring metrics
    scoring = {
        "accuracy": 'accuracy',
        "precision": make_scorer(precision_score, pos_label=1),
        "recall": make_scorer(recall_score, pos_label=1),
        "f1": make_scorer(f1_score, pos_label=1)
    }

    # Train a model (example with Logistic Regression)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_enc, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test_enc)

    # Evaluate the model
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    disp.plot(cmap="Blues")
    plt.title("Confusion Matrix")
    plt.show()

    try:
        pickle.dump(model, open(os.path.join(data_to, "model.pickle"), "wb"))
    except: 
        os.mkdir(data_to)
        pickle.dump(model, open(os.path.join(data_to, "model.pickle"), "wb"))

    try:
        pickle.dump(preprocessor, open(os.path.join(preprocessor_to, "preprocessor.pickle"), "wb"))
    except: 
        os.mkdir(preprocessor_to)
        pickle.dump(preprocessor, open(os.path.join(preprocessor_to, "preprocessor.pickle"), "wb"))

    try:
        X_train_enc.to_csv(os.path.join(data_to, "X_train_transformed.csv"), index=False)
        X_test_enc.to_csv(os.path.join(data_to, "X_test_transformed.csv"), index=False)
        y_train.to_csv(os.path.join(data_to, "y_train.csv"), index=False)
        y_test.to_csv(os.path.join(data_to, "y_test.csv"), index=False)
    except:
        os.mkdir(data_to)
        X_train_enc.to_csv(os.path.join(data_to, "X_train_transformed.csv"), index=False)
        X_test_enc.to_csv(os.path.join(data_to, "X_test_transformed.csv"), index=False)
        y_train.to_csv(os.path.join(data_to, "y_train.csv"), index=False)
        y_test.to_csv(os.path.join(data_to, "y_test.csv"), index=False)
        
if __name__ == '__main__':
    main()
