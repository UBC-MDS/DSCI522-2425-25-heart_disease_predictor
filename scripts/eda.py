import click
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@click.command()
@click.option('--processed-data', type=str, help="Path to processed heart disease data")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to

def main(processed_data, plot_to):
    '''Creates a pair plot with density plots on the diagonal for numeric features by diagnosis.'''

    df = pd.read_csv(processed_data)

    if not os.path.exists(plot_to):
        os.makedirs(plot_to)

    numeric_columns = ['age', 'resting_blood_pressure', 'cholesterol', 'max_heart_rate', 'st_depression']
    pairplot_data = df[numeric_columns + ['diagnosis']]

    pairplot = sns.pairplot(
        pairplot_data,
        hue='diagnosis',
        diag_kind='kde',
        plot_kws={'alpha': 0.7, 's': 50}, 
        diag_kws={'shade': True}
    )

    pairplot.fig.suptitle('Figure: Relationships Between Health Metrics by Diagnosis', y=1.02)

    plot_path = os.path.join(plot_to, "feature_densities_by_diagnosis.png")
    pairplot.savefig(plot_path)
    plt.close()

if __name__ == '__main__':
    main()
