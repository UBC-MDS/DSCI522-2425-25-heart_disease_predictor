# fit_heart_disease_predictor.py
# author: Anna Nandar, Brian Chang, Celine Habashy, Yeji Sohn
# date: 2024-12-06
# reference: ttimbers/breast-cancer-predictor

import click
import os
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import pickle

@click.command()
@click.option('--x-train', type=str, help="Path to the preprocessed training features (CSV file)", required=True)
@click.option('--y-train', type=str, help="Path to the training target labels (CSV file)", required=True)
@click.option('--model', type=click.Choice(['decision_tree', 'logistic_regression']), help="Model to use", required=True)
@click.option('--output-dir', type=str, help="Base directory to save results and plots", required=True)
@click.option('--random-state', type=int, default=123, help="Random seed for reproducibility")
def main(x_train, y_train, model, output_dir, random_state):
    """Train a model on separate features and labels and evaluate its performance."""
    np.random.seed(random_state)

    # Load training data
    X_train = pd.read_csv(x_train)
    y_train = pd.read_csv(y_train).squeeze()  

    # Define scoring metrics
    scoring = ['accuracy', 'precision', 'recall', 'f1']

    # Set up the model
    if model == 'decision_tree':
        estimator = DecisionTreeClassifier(random_state=random_state)
    elif model == 'logistic_regression':
        estimator = LogisticRegression(random_state=random_state, max_iter=1000)

    pipeline = make_pipeline(estimator)

    # Create subdirectories
    model_dir = os.path.join(output_dir, "models")
    tables_dir = os.path.join(output_dir, "tables", model)
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)

    model_file = os.path.join(model_dir, f"{model}.pkl")

    # Cross-validation
    cross_val_results = pd.DataFrame(
        cross_validate(pipeline, X_train, y_train, scoring=scoring, cv=5, return_train_score=True)
    ).agg(['mean', 'std']).round(3).T

    cross_val_results.to_csv(os.path.join(tables_dir, f"{model}_cv_results.csv"))

    # Fit the model and save the pipeline
    pipeline.fit(X_train, y_train)
    pickle.dump(pipeline, open(model_file, 'wb'))

    # Predict and display confusion matrix using cross-validated predictions
    y_pred = cross_val_predict(pipeline, X_train, y_train, cv=5)
    ConfusionMatrixDisplay.from_predictions(y_train, y_pred)
    plt.title(f"{model.capitalize()} Confusion Matrix")
    plt.savefig(os.path.join(tables_dir, f"{model}_confusion_matrix.png"))
    plt.close()

    # For Logistic Regression, extract and visualize coefficients
    if model == 'logistic_regression':
        logreg_model = pipeline.named_steps['logisticregression']
        coefficients = pd.DataFrame({
            "Feature": X_train.columns,
            "Coefficient": logreg_model.coef_.ravel()
        }).sort_values(by="Coefficient", ascending=False)

        coefficients.to_csv(os.path.join(tables_dir, "logreg_coefficients.csv"), index=False)

        plt.figure(figsize=(10, 8))
        plt.barh(coefficients["Feature"], coefficients["Coefficient"], color='skyblue')
        plt.title("Logistic Regression Coefficients")
        plt.xlabel("Coefficient Value")
        plt.ylabel("Feature")
        plt.tight_layout()
        plt.savefig(os.path.join(tables_dir, "logreg_coefficients.png"))
        plt.close()

    click.echo(f"Model training and evaluation completed. Results saved in {output_dir}")

if __name__ == '__main__':
    main()
