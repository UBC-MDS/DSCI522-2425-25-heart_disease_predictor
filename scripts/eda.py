import click
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

@click.command()
@click.option('--processed-data', type=str, help="Path to processed heart disease data")
@click.option('--plot-to', type=str, help="Path to directory where the plots will be saved")

def main(processed_data, plot_to):
    '''Creates and saves EDA plots: diagnosis distribution bar chart, correlation heatmap, 
       and density plots of numeric features grouped by diagnosis.'''


    df = pd.read_csv(processed_data)


    if not os.path.exists(plot_to):
        os.makedirs(plot_to)
        
    plt.figure(figsize=(8, 6))
    sns.countplot(x='diagnosis', data=df, palette='Blues')
    plt.xlabel('Diagnosis')
    plt.ylabel('Count')
    diagnosis_plot_path = os.path.join(plot_to, 'diagnosis_distribution.png')
    plt.savefig(diagnosis_plot_path)
    plt.close()

   
    plt.figure(figsize=(10, 8))
    numeric_data = df.select_dtypes(include=['number']) 
    correlation_matrix = numeric_data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', cbar_kws={'label': 'Correlation Coefficient'})
    heatmap_plot_path = os.path.join(plot_to, 'correlation_heatmap.png')
    plt.savefig(heatmap_plot_path)
    plt.close()


    df_melted = df.melt(
        id_vars=['diagnosis'], 
        var_name='predictor', 
        value_name='value'
    )
    df_melted['predictor'] = df_melted['predictor'].str.replace('_', ' ') 
    pairplot_data = df[["age", "resting_blood_pressure", "cholesterol", "max_heart_rate", "st_depression", "diagnosis"]]
    pairplot = sns.pairplot(
        pairplot_data,
        hue='diagnosis',
        diag_kind='kde', 
        plot_kws={'alpha': 0.7, 's': 50}, 
        diag_kws={'shade': True}  
    )


    plot_path = os.path.join(plot_to, "feature_densities_by_diagnosis.png")
    pairplot.savefig(plot_path)
    plt.close()


if __name__ == '__main__':
    main()

    