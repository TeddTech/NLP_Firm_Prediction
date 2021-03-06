import pytest
import pymongo as mongo
from mongoengine import *
from datetime import date
from src.structures import Filing, filing_from_mongo

# Adjust these details as necessary
host = "127.0.0.1"
port = 27000
url = "mongodb://{}:{}".format(host, port)

client = mongo.MongoClient(url)  # Connect to MongoDB Server
db = client['edgar']  # Select the DB to use.


class TestClass:

    def test_output(self):
        # Ensure the filing_from_mongo function works correctly.
        result = db['edgar-10k-yash'].find().limit(1)[0]
        filing_auto = filing_from_mongo(result)  # Transform that
        for k, v in result.items():
            if k != "_id":
                filing_man = Filing(cik=v['header']["CIK"],
                                    period=date(int(v['header']["PERIOD"][0:4]),
                                                int(v['header']["PERIOD"][4:6]),
                                                int(v['header']["PERIOD"][6:8])),
                                    item1=v['items']['item1'],
                                    item2=v['items']['item2'],
                                    item3=v['items']['item3'],
                                    item4=v['items']['item4'],
                                    item5=v['items']['item5'],
                                    item6=v['items']['item6'],
                                    item7=v['items']['item7'],
                                    item8=v['items']['item8'],
                                    item9=v['items']['item9'],
                                    item10=v['items']['item10'],
                                    item11=v['items']['item11'],
                                    item12=v['items']['item12'],
                                    item13=v['items']['item13'],
                                    item14=v['items']['item14'])
        for i in filing_auto:
            assert filing_auto[i] == filing_man[i]