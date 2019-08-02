"""
Tests for function substeting the columns in the subset_data.py file.

"""
import pandas as pd
from src.preprocessing.subset_data import subset_cols, subset_rows

# Read in which column name to keep:
with open("../data/compustat_selected_cols.csv", "r") as f:
    column_names = f.read()
column_names = column_names.split("\n")

# List of selected companies for test purpose
valid_uids = ['1750', '319126', '2880']

input_file  = "../data/data_for_test.csv"

class TestClass:

    # Test for subset_cols()
    def test_output(self):
        """Ensure the subset_cols() function return a dataframe"""

        result = subset_cols(input_file, "cik", column_names)
        assert type(result) == pd.DataFrame, "Output is not a dataframe"

    def test_cols_number(self):
        """Test that the number of column in output dataframe is the same as the number of column specified"""

        result = subset_cols(input_file, "cik", column_names)

        assert len(column_names) == result.shape[1], "The result does not contain all specified columns"

    def test_blank(self):
        """Test that the result dataframe is not blank"""

        result = subset_cols(input_file, "cik", column_names)
        assert result.shape[0] != 0, "The result dataframe is blank"

   
        
