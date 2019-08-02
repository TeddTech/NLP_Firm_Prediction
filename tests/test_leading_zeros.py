import pytest
import pandas as pd
import numpy as np
from src.preprocessing.label_feature_eng import leading_zeros, annualize


dat = pd.read_csv("data/data_for_test.csv")

dat = annualize(dat)


class TestClass:

    def test_leadingzeros(self):
        df_test = leading_zeros(df=dat, df_col='cik')

        assert all(len(df_test[df_col]) == 10) , \
            "Error, value from leading_zeros was not as expected"
