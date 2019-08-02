"""
Tests for the extract_topics() functions in extract_topics.py file.

This file should be run after setting up a given list of filing object 

This function uses topic modelling method from either gensim library or scikit learn library
"""

import pytest
from src.models import extract_topics, lda_model

filings_list = []
with (open(args["f1"], "rb")) as openfile:
    while True:
    # This loop is to make sure all objects serialized in the pickle file is loaded.
        try:
            filings_list.append(pickle.load(openfile))
        except EOFError:
            # Reache the end of pickle file, break the loop.
            break

filings_list = filings_list[0]

lda = lda_model(doc, 2, 42)
test = lda[0].print_topics(2)

class TestClass:
    def test_result(self):
        """Test if extract_topic function works properly"""
    
        result = extract_topics(doc, 2)
        assert result = test, "Function does not work properly"
    
    def test_num_topic(self):
        """Test if the number of topic produced is the same as the number of topic specified"""
        
        result = extract_topics(doc, 2)
        assert len(result) == 2, "The number of topics produced is not correct"
        
        
    