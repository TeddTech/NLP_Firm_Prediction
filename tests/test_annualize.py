import pytest
import pandas as pd
import numpy as np
from src.preprocessing.label_feature_eng import annualize


dat = pd.read_csv("data/data_for_test.csv")


class TestClass:

    def test_df_out_size(self):
        """ Tests that the output of annualize() is the correct size."""
        df_out = annualize(dat, period_label="fqtr", period_val=4)

        assert df_out.shape[1] == dat[dat['fqtr'] == 4], "Error, the produced DataFrame is not the correct size"


    def test_df_contents(self):
        """ Tests that the annualize function has correctly chosen the data needed"""
        df_out = annualize(dat, period_label="fqtr", period_val=4)

        assert all(df_out['fqtr'] == 4), "Error, the DataFrame has data from the wrong period."

