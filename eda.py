import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import click


@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
@click.option('--preprocessor-to', type=str, help="Path to directory where the preprocessor object will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)

def main(processed_data="Desktop/MDS/Block 3/DSCI_522/Week_3/data/processed_heart_disease_data.csv", plot_to="path/to/save/plots"):
    '''Performs exploratory data analysis on the heart disease dataset and saves the plots'''

    # Load the processed data
    df = pd.read_csv(processed_data)

    if not os.path.exists(plot_to):
        os.makedirs(plot_to)  
        
    print('\nSummary Statistics:')
    print(df.describe())

    plt.figure(figsize=(8, 6))
    sns.countplot(x='diagnosis', data=df)
    plt.title('Figure 1: Distribution of Diagnosis')
    plt.legend(['Diagnosis'], loc='upper right')
    plt.savefig(os.path.join(plot_to, 'diagnosis_distribution.png'))
    plt.close()

    # Correlation heatmap 
    numeric_data = df.select_dtypes(include=['number'])
    plt.figure(figsize=(12, 8))
    sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', cbar_kws={'label': 'Correlation Coefficient'})
    plt.title('Figure 2: Correlation Between Key Health Indicators')
    plt.savefig(os.path.join(plot_to, 'correlation_heatmap.png'))
    plt.close()

    pairplot = sns.pairplot(
        df[['age', 'resting_blood_pressure', 'cholesterol', 'max_heart_rate', 'diagnosis']],
        hue='diagnosis'
    )
    pairplot.fig.suptitle('Figure 3: Relationships Between Health Metrics by Diagnosis', y=1.02)
    pairplot._legend.set_bbox_to_anchor((1, 0.5))
    pairplot._legend.set_title('Diagnosis')
    pairplot.savefig(os.path.join(plot_to, 'pairplot.png'))
    plt.close()


if __name__ == '__main__':
    main(processed_data="Desktop/MDS/Block 3/DSCI_522/Week_3/data/processed_heart_disease_data.csv", plot_to="path/to/save/plots")
