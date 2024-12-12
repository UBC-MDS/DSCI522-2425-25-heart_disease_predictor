import pandas as pd

def load_data(x_data_path, y_data_path):
    """
    Loads data from CSV files with error handling.
    
    Parameters:
    x_data_path (str): Path to the features CSV file.
    y_data_path (str): Path to the labels CSV file.
    
    Returns:
    X_data (DataFrame): The loaded feature data.
    y_data (Series): The loaded target data as a Series.
    
    Raises:
    FileNotFoundError: If either of the files are not found.
    """
    try:
        X_data = pd.read_csv(x_data_path)
        y_data = pd.read_csv(y_data_path).squeeze()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e}")
    return X_data, y_data
