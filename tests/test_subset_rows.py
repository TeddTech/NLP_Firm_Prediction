"""
Tests for subset_rows function.
"""

import pytest
import pandas as pd
from src.preprocessing.subset_data import subset_rows

# Read in which column name to keep:
with open("../data/compustat_selected_cols.csv", "r") as f:
    column_names = f.read()
column_names = column_names.split("\n")

# List of selected companies for test purpose
valid_uids = ['1750', '319126', '2880']

input_file = "../data/data_for_test.csv"


class TestClass:
    
    def test_csv(self):
        """Checks if input_file is a .csv"""
          
        good_file = 'df.csv'
        bad_file = 'df.tsv'

        # return no error
        assert good_file[-3:] == 'csv', "input_file must be a .csv file"

        # raise type error for invalid file format
        with pytest.raises(AttributeError):
            subset_rows(bad_file)

 # Test for subset_rows()
    def test_output(self):
        """Ensure the subset_rows() function return a dataframe"""

        result = subset_rows(input_file, "cik", valid_uids)
        assert type(result) == pd.DataFrame, "Output is not a dataframe"

    def test_rows_blank(self):
        """Test that the result dataframe is not blank"""

        result = subset_rows(input_file, "cik", valid_uids)
        assert result.shape[0] != 0, "The result dataframe is blank"

    def test_rows_number(self):
        """Test that the number of company in output dataframe is the same as the number of company (CIK) specified"""

        result = subset_rows(input_file, "cik", valid_uids)

        assert len(valid_uids) == len(result.cik.unique()), "The result does not contain all specified companies"

    def test_rows_branch(self):
        """Test the function does well in all branches"""

        result = subset_rows(input_file, "cik", valid_uids)

        valid_uids = [1750, 319126, 2880]
        result_int = subset_rows(input_file, "cik", valid_uids, uid_type = "int")

        valid_uids = [1750.0, 319126.0, 2880.0]
        result_float = subset_rows(input_file, "cik", valid_uids, uid_type = "float")

        assert result == result_int, "Branch A does not function well"
        assert result == result_float, "Branch B does not function well"