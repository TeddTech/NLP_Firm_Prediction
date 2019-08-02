import pytest
import pandas as pd
import numpy as np
from src.preprocessing.label_feature_eng import mrk_cap

n = 100

a = np.random.randint(0,100, size = n)
b = [100**100]*n
d = {'col1': a, 'col2': a, 'col3': b}
dat = pd.DataFrame(data=d)




class TestClass:

    def test_mrk_cap(self):
        df_ratio = mrk_cap(dat, col='col3', list_cols=['col1','col2'])
        assert all(np.isclose(df_ratio, 0).any(0)) , \
            "Error, value from bi_col was not as expected"
