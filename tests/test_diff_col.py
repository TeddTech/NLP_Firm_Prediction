import pytest
import pandas as pd
import numpy as np
from src.preprocessing.label_feature_eng import diff_col, annualize



dat = pd.read_csv("data/data_for_test.csv")


dat = annualize(dat)

uni_cik = dat['cik'].sample(1).values[0]

class TestClass:

    def test_diff(self):
        df_diff = diff_col(dat, col_name='fyearq', uid='cik', diffpct=False)

        assert all(df_diff['delta_fyearq'][df_diff['cik'] = uni_cik] == 1) , \
            "Error, value from diff_col was not as expected"

    def test_diff_pct(self):
        df_diff = diff_col(dat,  col_name='fyearq', uid='cik', diffpct=True)
        a = df_diff['delta_fyearq'][df_diff['cik'] = uni_cik]
        assert all(np.isclose(a, 0.0005, atol=0.00005)), \
            "Error, value from diff_col was not as expected"
