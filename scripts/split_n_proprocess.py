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

    scoring = {
        "accuracy": 'accuracy',
        "precision": make_scorer(precision_score, pos_label=1),
        "recall": make_scorer(recall_score, pos_label=1),
        "f1": make_scorer(f1_score, pos_label=1)
    }

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_enc, y_train)

    y_pred = model.predict(X_test_enc)

   
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

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
    

if __name__ == '__main__':
    main()
