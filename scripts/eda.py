import click
import os
import altair as alt
import pandas as pd

@click.command()
@click.option('--processed-data', type=str, help="Path to processed heart disease data")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")
def main(processed_data, plot_to):
    '''Plots the densities of each numeric feature in the processed heart disease data
       by diagnosis and displays them as a grid of plots. Also saves the plot.'''

    df = pd.read_csv(processed_data)

    df_melted = df.melt(
        id_vars=['diagnosis'],
        var_name='predictor',
        value_name='value'
    )

    df_melted['predictor'] = df_melted['predictor'].str.replace('_', ' ')

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

    if not os.path.exists(plot_to):
        os.makedirs(plot_to)

    plot_path = os.path.join(plot_to, "feature_densities_by_diagnosis.png")
    plot.save(plot_path, scale_factor=2.0)

if __name__ == '__main__':
    main()
