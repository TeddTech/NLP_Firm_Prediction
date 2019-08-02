import pytest
import pandas as pd
import numpy as np
from src.preprocessing.label_feature_eng import diff_label, diff_col, vol
from src.preprocessing.feature_aggregation import vol

dat = pd.read_csv("data/data_for_test.csv")

class TestClass:

    def test_vol(self):
        df_vol = vol(dat, dat)

        for i in range(df_vol.shape[0]):
            j = np.random.randint(i)
            if df_vol.iloc[i,:]['tic'] != df_vol.iloc[j,:]['tic']:
                assert np.isnan(df_vol.iloc[i,:]['vol']) , \
                    "Error, value from test_vol was not as expected"
