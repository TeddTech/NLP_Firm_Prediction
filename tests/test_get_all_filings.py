"""
Tests for the get_all_filings() functions in text_extract.py file.

This file should be run after setting up an appropriate SSH tunnel to the MongoDB server.

If running them FROM the server, adjust the port to 27017 and it should run as expected.
"""

import pytest
import pymongo as mongo
from mongoengine import *
from datetime import date

from src.structures import Filing, filing_from_mongo
from src.preprocessing.text_extract import get_all_filings


# Adjust these details as necessary
host = "127.0.0.1"
port = 27000
url = "mongodb://{}:{}".format(host, port)

client = mongo.MongoClient(url)  # Connect to MongoDB Server
db = client['edgar']  # Select the DB to use.


class TestClass:
    def test_result(self):
        # Test if the function return a correct result
        
        result = list()
        for item in db["edgar-10k-yash"].find().limit(2):
            try:
                result.append(filing_from_mongo(item)) # Iterate over each retrieved document
            except KeyError:
                pass
            
        test = get_all_filings(db['edgar-10k-yash'],2)
        
        assert test = result, "Function has some problem"
        
    def test_limit_number(self):
        # Test if function return more than the limited number
        # It's okay to have less than limited number
        
        lim_num = 5
        test = get_all_filings(db['edgar-10k-yash'], lim_num)
        assert len(test) <= lim_num, "The function returns more than limited number of filings"