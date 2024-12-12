import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

"""
Creates EDA plots for the pre-processed training data from the Wisconsin breast cancer data. Saves the plots as a PDF and PNG file.

Usage: scripts/eda_function.py --train=<train> --out_dir=<out_dir>

Options:
--train=<train>     Path (including filename) to training data (which needs to be saved as a CSV file)
--out_dir=<out_dir> Path to directory where the plots should be saved
"""
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main(processed_data, plot_to):

    df = pd.read_csv(processed_data)

    if not os.path.exists(plot_to):
        os.makedirs(plot_to)

    # Diagnosis distribution bar chart
    diagnosis_plot_path = os.path.join(plot_to, 'diagnosis_distribution.png')
    plt.figure(figsize=(8, 6))
    sns.countplot(x='diagnosis', data=df, palette='Blues')
    plt.xlabel('Diagnosis')
    plt.ylabel('Count')
    plt.savefig(diagnosis_plot_path)
    plt.close()

    # Correlation heatmap
    heatmap_plot_path = os.path.join(plot_to, 'correlation_heatmap.png')
    plt.figure(figsize=(10, 8))
    numeric_data = df.select_dtypes(include=['number'])
    correlation_matrix = numeric_data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', cbar_kws={'label': 'Correlation Coefficient'})
    plt.savefig(heatmap_plot_path)
    plt.close()

    # Density plots for numeric features grouped by diagnosis
    density_plot_path = os.path.join(plot_to, 'feature_densities_by_diagnosis.png')
    pairplot_data = df[["age", "resting_blood_pressure", "cholesterol", "max_heart_rate", "st_depression", "diagnosis"]]
    pairplot = sns.pairplot(
        pairplot_data,
        hue='diagnosis',
        diag_kind='kde', 
        plot_kws={'alpha': 0.7, 's': 50}, 
        diag_kws={'shade': True}  
    )
    pairplot.savefig(density_plot_path)
    plt.close()


if __name__ == '__main__':
    processed_data = "data/cleaned/cleaned_heart_disease_data.csv"
    plot_to = "results/eda_plots"

    main(processed_data, plot_to)
