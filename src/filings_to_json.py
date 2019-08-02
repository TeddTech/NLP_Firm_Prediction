import datetime
import mongoengine
import pymongo as mongo
from src.structures import Filing
import json

# Adjust these details as necessary
host = "127.0.0.1"
port = 27000
url = "mongodb://{}:{}".format(host, port)

def connect():
    mongoengine.connect(host=host, port=port)

client = mongo.MongoClient(url)
db = client['edgar']
# db["edgar-10k-yash"].find({"cik": {"$in": []}}).limit(2)
def filing_to_json(coll = db["edgar-10k-yash"] , lim=2, path = "filings_json.json"):      # Tested [Y]
    """
    Takes collection and number of filings requested and saves them into a json file
    Args:
        coll (MongoDB collection)  : Collection of company filings.
        lim (int) : Number of filings requested to be saved. Default is 2.
        path (str) : Path for output json file.
    Returns:
       filings_json(json): A json file for requested collection
    """
    filings_list = list()
    filings_json = list()
    counter = 0
    # with open(path, 'w') as fp: # to save into a file
    for item in coll.find().limit(lim):  # Iterate over each retrieved document
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
        #json.dump(filings_list[counter].__dict__, fp, default=str) # dump into a json file
        filings_json[counter] = filings_list[counter].__dict__
        counter += 1
    with open(path, 'w') as fp:
        json.dump(filings_list, fp, default=str)

    return filings_list # returns filings
