import datetime
import mongoengine
import pymongo as mongo
from src.structures import Filing


# Adjust these details as necessary
host = "127.0.0.1"
port = 27000
url = "mongodb://{}:{}".format(host, port)

def connect():
    mongoengine.connect(host=host, port=port)

client = mongo.MongoClient(url)
db = client['edgar']

filings_list = list()

for item in db["edgar-10k-yash"].find().limit(2):  # Iterate over each retrieved document
    for k, v in item.items():
        if k != "_id":  # We don't care about _id, we just need to iterate over the other key
            filings_list.append(Filing(cik=v['header']["CIK"],
                                       period=datetime.date(int(v['header']["PERIOD"][0:4]),
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
                                       item14=v['items']['item14']))


