"""
Tests for the gensim_model() functions in extract_topic.py file.

This file should be run after setting up a given list of filing object 

This function uses LDA model from gensim library
"""

import pytest
from src.models import gensim_model

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

class TestClass:
    def test_resutl(self):
        """Test if gensim_model() returns the right result"""
        result = gensim_model(filings_list, 1, 10)
        
        assert type(result[0]) == gensim.models.ldamodel.LdaModel, "Function does not produce LDA model"
        assert type(result[1]) == list, "Function does not produce corpus list properly"
        assert type(result[2]) == gensim.corpora.dictionary.Dictionary, "Function does not produce Dictionary"
        
    def test_corpus(self):
        """Test if the number of corpus produced is correct"""
        
        result = gensim_model(filings_list, 1, 10)
        assert len(result[1]) == 10, "Function produce wrong number of corpus"