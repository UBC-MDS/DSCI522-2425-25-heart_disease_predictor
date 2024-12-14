import os

def save_classification_report(report_df, results_dir):
    """
    Saves the classification report to a CSV file with error handling.

    Parameters:
    ------------
    report_df: pandas.DataFrame
        The input classification report dataframe to save
    results_dir: str
        The directory the file saved csv file will be outputted

    Returns:
    ------------
    None

    Example
    ------------
    save_classification_report(report_df, "results/tables/decision_tree")
    """
    try:
        required_columns = ['precision', 'recall', 'f1-score']
        required_indices = ['0', '1', 'accuracy']
        os.makedirs(results_dir, exist_ok=True)

        # Test to see if our input df has all the required columns
        for req_col in required_columns:
            if req_col not in report_df.columns:
                raise ValueError("Missing the required columns")
            
        # Test to see if our input df has all the required indices
        for req_index in required_indices:
            if req_index not in report_df.index:
                raise ValueError("Missing the required indices")

        report_filtered = report_df.loc[required_indices, required_columns]

        report_filtered.to_csv(os.path.join(results_dir, "classification_report.csv"))
    except ValueError as e:
        raise ValueError(f"Input data error: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while saving the classification report: {e}")