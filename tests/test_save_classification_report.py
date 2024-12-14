import pytest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.save_classification_report import save_classification_report

def test_missing_dataframe(tmp_path):
    """
    Test that an error is thrown when the dataframe is not passed to save_classification_report
    """

    with pytest.raises(Exception):
        save_classification_report(results_dir=tmp_path)

def test_wrong_columns(tmp_path):
    """
    Test that an error is thrown when a dataframe with the wrong columns is passed to save_classification_report
    """

    # Wrong/Missing columns in df passed
    wrong_df = pd.DataFrame(
        {
            'wrong_column_name': [1, 2, 3],
            'recall': [4, 5, 6],
            'f1-score': [7, 8, 9]
        }
    )

    with pytest.raises(ValueError):
        save_classification_report(wrong_df, tmp_path)

def test_wrong_indices(tmp_path):
    """
    Test that an error is thrown when a dataframe with the wrong indices is passed to save_classification_report
    """

    # Wrong/Missing columns in df passed
    wrong_df = pd.DataFrame(
        {
            'wrong_column_name': [1, 2, 3],
            'recall': [4, 5, 6],
            'f1-score': [7, 8, 9]
        },
        index=["fake","index","stuff"]
    )

    with pytest.raises(ValueError):
        save_classification_report(wrong_df, tmp_path)


def test_successful(tmp_path):
    """
    Test that there should be no errors when a correct dataframe is passed to save_classification_report
    """

    # Correct dataframe structure
    correct_df = pd.DataFrame({
        'precision': [1, 2, 3],
        'recall': [4, 5, 6],
        'f1-score': [7, 8, 9]
        },
        index=["0","1","accuracy"]
    )

    save_classification_report(correct_df, tmp_path)

    