import pytest
import pandas as pd
import numpy as np
from src.preprocessing.label_feature_eng import annualize, diff_label



dat = pd.read_csv("data/data_for_test.csv")


dat = annualize(dat)


class TestClass:

    def test_label_shift(self):
        df_labelled = diff_label(dat, uid='cik', p='prccq', cutoff=0.1, diffpct=True)

        assert df_labelled.iloc[1]['label'] == 'up' and df_labelled.iloc[2]['diffpct'] > 0.1, \
            "Error, 'up' with percentage is incorrectly labelled"
        assert df_labelled.iloc[50]['label'] == 'down' and df_labelled.iloc[51]['diffpct'] < -0.1, \
            "Error, 'down' with percentage is incorrectly labelled"
        assert (df_labelled.iloc[200]['label'] == 'flat' and
                -0.1 < df_labelled.iloc[201]['diffpct'] < 0.1), \
            "Error, 'flat' with percentage is incorrectly labelled"

    def test_not_pct(self):
        df_labelled = diff_label(dat, uid='cik', cutoff=5, p='prccq', diffpct=False)
        assert df_labelled.iloc[1]['label'] == 'up' and df_labelled.iloc[2]['diff'] > 5, \
            "Error, 'up' with percentage is incorrectly labelled"
        assert df_labelled.iloc[382]['label'] == 'down' and df_labelled.iloc[383]['diff'] < -5, \
            "Error, 'down' with percentage is incorrectly labelled"
        assert (df_labelled.iloc[200]['label'] == 'flat' and
               -5 < df_labelled.iloc[201]['diff'] < 5), \
            "Error, 'flat' with percentage is incorrectly labelled"



