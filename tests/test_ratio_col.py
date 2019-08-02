import pytest
import pandas as pd
import numpy as np
from src.preprocessing.label_feature_eng import ratio_col



a = np.random.randint(0,100, size = 100)
d = {'col1': a, 'col2': a}
dat = pd.DataFrame(data=d)




class TestClass:

    def test_ratio(self):
        df_ratio = ratio_col(dat, ('col1','col2'))
        assert all(df_ratio == 1) , \
            "Error, value from bi_col was not as expected"
