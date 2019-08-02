import pytest
import pandas as pd
import numpy as np
from src.preprocessing.label_feature_eng import bi_col



dat = pd.read_csv("data/data_for_test.csv")


dat = annualize(dat)


class TestClass:

    def test_bi_thresh(self):
        df_bi = bi_col(dat, thresh=10, df_col='xrdy', greater=True)

        assert all(type(df_bi) == 'bool') , \
            "Error, value from bi_col was not as expected"

    def test_bi(self):
        df_bi = bi_col(dat, thresh=False, df_col='xrdy', greater=True)

        assert all(type(df_bi) == 'bool') , \
            "Error, value from bi_col was not as expected"
