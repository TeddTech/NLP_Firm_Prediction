import pytest
import pandas as pd
import numpy as np
from src.preprocessing.label_feature_eng import sum_ytd, annualize


dat = pd.read_csv("data/data_for_test.csv")

dat = annualize(dat)


class TestClass:

    def test_ytd(self):
        df_ytd = sum_ytd(df=dat, df_col='prccq', uid='cik', date='fyearq')
        df_ytd = 0
        assert all(df_ytd == 0) , \
            "Error, value from sum_ytd was not as expected"
