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

def load_data(x_train_path, y_train_path):
    """Loads the training data from CSV files with error handling."""
    try:
        X_train = pd.read_csv(x_train_path)
        y_train = pd.read_csv(y_train_path).squeeze()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e}")
    return X_train, y_train

def create_directories(base_dir, model_name):
    """Creates necessary directories for saving models and tables with error handling."""
    try:
        model_dir = os.path.join(base_dir, "models")
        tables_dir = os.path.join(base_dir, "tables", model_name)
        os.makedirs(model_dir, exist_ok=True)
        os.makedirs(tables_dir, exist_ok=True)
    except Exception as e:
        raise Exception(f"An error occurred while creating directories to save models and tables: {e}")
    return model_dir, tables_dir

def train_and_evaluate_model(X_train, y_train, model_name, random_state):
    """Trains a model using cross-validation and returns the trained pipeline and cross-validation results with error handling."""
    try:
        if model_name == 'decision_tree':
            estimator = DecisionTreeClassifier(random_state=random_state)
        elif model_name == 'logistic_regression':
            estimator = LogisticRegression(random_state=random_state, max_iter=1000)
        else:
            raise ValueError("Invalid model name. Choose 'decision_tree' or 'logistic_regression'.")
        
        pipeline = make_pipeline(estimator)
        
        # Cross-validation
        scoring = ['accuracy', 'precision', 'recall', 'f1']
        cross_val_results = pd.DataFrame(
            cross_validate(pipeline, X_train, y_train, scoring=scoring, cv=5, return_train_score=True)
        ).agg(['mean', 'std']).round(3).T
        
        # Fit final model on the full training data
        pipeline.fit(X_train, y_train)
    
    except Exception as e:
        raise Exception(f"An error occurred while training the model: {e}")
    
    return pipeline, cross_val_results

def save_model_and_results(pipeline, cross_val_results, model_dir, tables_dir, model_name, X_train, y_train):
    """Saves the trained model, cross-validation results, and generates confusion matrix and coefficient plots with error handling."""
    try:
        model_file = os.path.join(model_dir, f"{model_name}.pkl")
        pickle.dump(pipeline, open(model_file, 'wb'))
        
        # Save cross-validation results
        cross_val_results.to_csv(os.path.join(tables_dir, f"{model_name}_cv_results.csv"))
        
        # Predict and display confusion matrix
        y_pred = cross_val_predict(pipeline, X_train, y_train, cv=5)
        ConfusionMatrixDisplay.from_predictions(y_train, y_pred)
        plt.title(f"{model_name.capitalize()} Confusion Matrix")
        plt.savefig(os.path.join(tables_dir, f"{model_name}_confusion_matrix.png"))
        plt.close()
        
        # For Logistic Regression, extract and visualize coefficients
        if model_name == 'logistic_regression':
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
    except Exception as e:
        raise Exception(f"An error occurred while saving model and results: {e}")

@click.command()
@click.option('--x-train', type=str, help="Path to the preprocessed training features (CSV file)", required=True)
@click.option('--y-train', type=str, help="Path to the training target labels (CSV file)", required=True)
@click.option('--model', type=click.Choice(['decision_tree', 'logistic_regression']), help="Model to use", required=True)
@click.option('--output-dir', type=str, help="Base directory to save results and plots", required=True)
@click.option('--random-state', type=int, default=123, help="Random seed for reproducibility")
def main(x_train, y_train, model, output_dir, random_state):
    """Train a model on separate features and labels and evaluate its performance with error handling."""
    try:
        np.random.seed(random_state)
        
        # Load training data
        X_train, y_train = load_data(x_train, y_train)
        
        # Create necessary directories
        model_dir, tables_dir = create_directories(output_dir, model)
        
        # Train and evaluate the model
        pipeline, cross_val_results = train_and_evaluate_model(X_train, y_train, model, random_state)
        
        # Save model and evaluation results
        save_model_and_results(pipeline, cross_val_results, model_dir, tables_dir, model, X_train, y_train)
        
        click.echo(f"Model training and evaluation completed. Results saved in {output_dir}")
    except Exception as e:
        raise Exception(f"An error occurred in the main function: {e}")

if __name__ == '__main__':
    main()
