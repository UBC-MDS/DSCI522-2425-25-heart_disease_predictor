# download_data.py
# author: Yeji Sohn
# date: 2024-12-02

import click
import os
import pandas as pd

@click.command()
@click.option('--url', type=str, help=".csv URL of dataset to be downloaded")
@click.option('--write-to', type=str, help="Path to directory where raw data will be written to")

def main(url, write_to):
    """
    Downloads a CSV file from the specified URL and saves it to a local directory.
    
    Args:
        url (str): The URL of the CSV file to download.
        write_to (str): The directory path where the file should be saved.
        
    Saves:
        raw_heart_disease_data.csv (str): The CSV file saved in the specified directory.
        
    If the directory does not exist, it is created.
    """
    try:
        df = pd.read_csv(url)
        df.to_csv("" + write_to + "raw_heart_disease_data.csv", index=False)
    except:
        os.makedirs(write_to)
        df = pd.read_csv(url)
        df.to_csv("" + write_to + "raw_heart_disease_data.csv", index=False)

if __name__ == '__main__':
    main()