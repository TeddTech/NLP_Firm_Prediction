import pytest
import pandas as pd
import numpy as np
from src.preprocessing.label_feature_eng import label_performance


class TestClass:

    def test_up(self):
        assert label_performance(1) == "up", "Error, 'up' labels are not working correctly"

    def test_down(self):
        assert label_performance(-1) == "down", "Error, 'down' labels are not working correctly"

    def test_flat(self):
        assert label_performance(-0.01) == "flat", "Error, 'flat' labels are not working correctly on the downside"
        assert label_performance(0.01) == "flat", "Error, 'flat' labels are not working correctly on the upside"

    def test_different_cutoff(self):
        assert label_performance(1, 0.5) == "up", "Error, 'up' labels are not working correctly"
        assert label_performance(-1, 0.5) == "down", "Error, 'down' labels are not working correctly"
        assert label_performance(0.1, 0.5) == "flat", "Error, 'flat' labels are not working correctly on the downside"
        assert label_performance(-0.1, 0.5) == "flat", "Error, 'flat' labels are not working correctly on the upside"
        

