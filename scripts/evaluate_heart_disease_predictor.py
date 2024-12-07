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

@click.command()
@click.option('--x-test', type=str, help="Path to the test features (CSV file)", required=True)
@click.option('--y-test', type=str, help="Path to the test target labels (CSV file)", required=True)
@click.option('--pipeline-from', type=str, help="Path to the saved pipeline object (Pickle file)", required=True)
@click.option('--results-to', type=str, help="Directory to save evaluation results", required=True)
@click.option('--seed', type=int, default=123, help="Random seed for reproducibility")

def main(x_test, y_test, pipeline_from, results_to, seed):
    """Evaluate a classifier on the test data and save the classification report."""
    np.random.seed(seed)

    # Load test data and saved pipeline
    X_test = pd.read_csv(x_test)
    y_test = pd.read_csv(y_test).squeeze()  
    
    with open(pipeline_from, 'rb') as f:
        pipeline = pickle.load(f)

    # Predict using the loaded model
    y_pred = pipeline.predict(X_test)

    # Generate classification report
    report = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()

    # Filter relevant metrics
    report_filtered = report_df.loc[['0', '1', 'accuracy'], ['precision', 'recall', 'f1-score']]

    # Save classification report
    os.makedirs(results_to, exist_ok=True)
    report_filtered.to_csv(os.path.join(results_to, "classification_report.csv"))

    click.echo(f"Classification report saved in {results_to}")

if __name__ == '__main__':
    main()
