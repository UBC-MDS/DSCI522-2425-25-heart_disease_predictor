import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.create_dir_if_not_exist import create_dir_if_not_exist

test_dir = 'tests/folder_1'

def create_dir_if_not_exist():

    actual = create_dir_if_not_exist(test_dir)


    assert os.path.exists(test_dir), "The directory wasn't created when it should have been."
    assert os.path.isdir(test_dir), "The created path is not recognized as a directory."
    assert actual == test_dir, f"Expected path {test_dir}, but got {actual}"

    if os.path.exists(test_dir):
        os.rmdir(test_dir)
