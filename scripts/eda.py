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
    plt.title('Figure 1: Distribution of Diagnosis')
    plt.xlabel('Diagnosis')
    plt.ylabel('Count')
    diagnosis_plot_path = os.path.join(plot_to, 'diagnosis_distribution.png')
    plt.savefig(diagnosis_plot_path)
    plt.close()

   
    plt.figure(figsize=(10, 8))
    numeric_data = df.select_dtypes(include=['number'])  # Select only numeric columns
    correlation_matrix = numeric_data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', cbar_kws={'label': 'Correlation Coefficient'})
    plt.title('Figure 2: Correlation Between Key Health Indicators')
    heatmap_plot_path = os.path.join(plot_to, 'correlation_heatmap.png')
    plt.savefig(heatmap_plot_path)
    plt.close()


    df_melted = df.melt(
        id_vars=['diagnosis'], 
        var_name='predictor', 
        value_name='value'
    )
    df_melted['predictor'] = df_melted['predictor'].str.replace('_', ' ')  # Make predictor names prettier


    plot = alt.Chart(df_melted, width=150, height=100).transform_density(
        'value',
        groupby=['diagnosis', 'predictor']
    ).mark_area(opacity=0.7).encode(
        x=alt.X("value:Q"),
        y=alt.Y('density:Q', stack=False),
        color='diagnosis:N'
    ).facet(
        'predictor:N',
        columns=3
    ).resolve_scale(
        y='independent'
    )


    density_plot_path = os.path.join(plot_to, "feature_densities_by_diagnosis.html")
    plot.save(density_plot_path)

    print(f"Plots saved to: {plot_to}")

if __name__ == '__main__':
    main()

