# evaluate_heart_disease_predictor.py
# author: Anna Nandar, Brian Chang, Celine Habashy, Yeji Sohn
# date: 2024-12-06
# reference: ttimbers/breast-cancer-predictor

import click
import os
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import classification_report
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.load_data import load_data

def load_pipeline(pipeline_path):
    """Loads a saved pipeline object from a Pickle file with error handling."""
    try:
        with open(pipeline_path, 'rb') as f:
            pipeline = pickle.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Pipeline file not found: {e}")
    return pipeline

def evaluate_model(pipeline, X_test, y_test):
    """Generates predictions and classification report with error handling."""
    try:
        y_pred = pipeline.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
    except Exception as e:
        raise Exception(f"An error occurred during model evaluation: {e}")
    return report_df

def save_classification_report(report_df, results_dir):
    """Saves the classification report to a CSV file with error handling."""
    try:
        os.makedirs(results_dir, exist_ok=True)
        report_filtered = report_df.loc[['0', '1', 'accuracy'], ['precision', 'recall', 'f1-score']]
        report_filtered.to_csv(os.path.join(results_dir, "classification_report.csv"))
    except Exception as e:
        raise Exception(f"An error occurred while saving the classification report: {e}")

@click.command()
@click.option('--x-test', type=str, help="Path to the test features (CSV file)", required=True)
@click.option('--y-test', type=str, help="Path to the test target labels (CSV file)", required=True)
@click.option('--pipeline-from', type=str, help="Path to the saved pipeline object (Pickle file)", required=True)
@click.option('--results-to', type=str, help="Directory to save evaluation results", required=True)
@click.option('--seed', type=int, default=123, help="Random seed for reproducibility")
def main(x_test, y_test, pipeline_from, results_to, seed):
    """Evaluate a classifier on the test data and save the classification report with error handling."""
    try:
        np.random.seed(seed)
        
        # Load test data and saved pipeline
        X_test, y_test = load_data(x_test, y_test)
        pipeline = load_pipeline(pipeline_from)
        
        # Evaluate the model
        report_df = evaluate_model(pipeline, X_test, y_test)
        
        # Save the classification report
        save_classification_report(report_df, results_to)
        
        click.echo(f"Classification report saved in {results_to}")
    except Exception as e:
        raise Exception(f"An error occurred in the main function: {e}")

if __name__ == '__main__':
    main()
