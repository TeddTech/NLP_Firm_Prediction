"""
Tests for the filings_to_json() function in filings_to_json.py file.
This file should be run after setting up an appropriate SSH tunnel to the MongoDB server.
If running them FROM the server, adjust the port to 27017 and it should run as expected.
"""

import pytest
import pymongo as mongo
from mongoengine import *

from src.filings_to_json import filings_to_json

# Adjust these details as necessary
host = "127.0.0.1"
port = 27000
url = "mongodb://{}:{}".format(host, port)

client = mongo.MongoClient(url)  # Connect to MongoDB Server
db = client['edgar']  # Select the DB to use.

# set limit and json_path for test:
fil_limit = 1
json_path = "filings.json"

filling_man = db["edgar-10k-yash"].find().limit(fil_limit) # import data from MongoDB to compare

filling_func_out = filings_to_json(coll = db["edgar-10k-yash"] , lim = fil_limit, path = json_path)

class TestClass:
    def test_result_len(self):
        """ Test if filings_to_json outputs correct amount of files:"""
        assert len(filling_man) == len(filling_func_out) "Function does not output correct number of fillings"

    def test_result(self):
        """ Test if filings_to_json() returns the right result:"""
        assert filling_man[0] == filling_func_out[0]  "Function does not work well"

    def test_json_file(self):
        """ Test if filings_to_json outputs a correct json file into the specified path"""
        with open(json_path) as f:
            output_json = json.load(f)
        assert output_json[0] == filling_man[0] "Function does not produce json file as expected"
