import pytest
import pandas as pd
import numpy as np
from src.models.extract_sentiment import extract_sentiment

# 500_filings_for_test.pickle is a test file containing Filings List:
filings_list = []
    with (open("./data/500_filings_for_test.pickle", "rb")) as openfile:
        while True:
            try:
                filings_list.append(pickle.load(openfile))
            except EOFError:
                break


class TestClass:
    def test_result(self):
        """Test if extract_sentiment return the right results"""

