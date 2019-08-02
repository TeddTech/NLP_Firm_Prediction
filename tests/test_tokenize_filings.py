"""
Tests for the tokenize_filings() functions in text_extract.py file.

This file should be run after setting up an appropriate SSH tunnel to the MongoDB server.

If running them FROM the server, adjust the port to 27017 and it should run as expected.
"""

import pytest
import pymongo as mongo
from mongoengine import *

from src.structures import Filing, filing_from_mongo
from src.preprocessing.text_extract import get_all_filings, tokenize_filings

# Adjust these details as necessary
host = "127.0.0.1"
port = 27000
url = "mongodb://{}:{}".format(host, port)

client = mongo.MongoClient(url)  # Connect to MongoDB Server
db = client['edgar']  # Select the DB to use.

doc1 = Filing(cik='0000065011',period=date(2010,3,3),item1="The cat is very expensive")
doc2 = Filing(cik='0000065011',period=date(2011,3,3),item1="They have two funny Husky, one Great Dane and a cute Corgi")

doc = [doc1,doc2]

class TestClass:
    def test_result(self):
        # Test if tokenize_filings() returns the right result
        result = [['the', 'cat', 'expensive'],['they', 'two', 'funny', 'husky', 'one', 'great', 'dane', 'cute', 'corgi']]
        test = tokenize_filings(doc,1)
        
        assert test == result, "Function does not work well"
        
    def check_blank_list(self):
        """Test if the result list still contains blank list"""
        
        test = tokenize_filings(doc,1)
        assert [] not in test, "Blank list is still in the result"