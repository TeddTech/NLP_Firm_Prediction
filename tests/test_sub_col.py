import pytest
import pandas as pd
import numpy as np
from src.preprocessing.label_feature_eng import sub_col

n = 100

a = np.random.randint(0,100, size = n)
d = {'col1': a, 'col2': a, 'col3': a}
dat = pd.DataFrame(data=d)




class TestClass:

    def test_sub_col(self):
        df_ratio = sub_col(dat, ('col1', 'col2'))
        assert all(df_ratio == 0) , \
            "Error, value from sub_col was not as expected"
