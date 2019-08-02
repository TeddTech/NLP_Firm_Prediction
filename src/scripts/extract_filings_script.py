"""
    Script to query the MongoDB containing SEC filings and extract the necessary information from those filings which fit
    our criteria to be part of the model.

    As of now, this criteria is the CIKs which occur in all of our data sources.

    Sample usage from terminal:
	    python src/scripts/extract_fiings_script.py 127.0.0.1 27017 "cik" "str" data/common_cik_list.csv data/filings_list.pickle

    Args:
        host (str)  : Hostname of computer server that stores the database
        port (str)  : SSH port of computer server that stores the database
        uid (str) : Unique identifier of firm. Examples: "cik", "tic"
        uid_type (str) : The data type of the the uid selected. Examples: "int", "str"
        valid_uids (str) : Path to common UID list
        loggingLevel (int): Default=3. 1-5 scale determining the logging messages to save.
                                5 is only CRITICAL, 1 is all messages
        loggingPath (dir): Default=logs/{script_name}_{unix_time}.log
                           Path to the desired location to store logs
        

    Return:
        outputFile (pickle) : Path to save the filing list in pickle
        
"""
import sys
import time
import pickle
import argparse
import pandas as pd
import pymongo as mongo
from mongoengine import *
from src.utils import logging_wrapper
from src.preprocessing import tokenize_filings, get_all_filings

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required Args
    parser.add_argument("host", help="Mongo Host IP address", type=str)
    parser.add_argument("port", help="MongoDB listening port", type=str)
    parser.add_argument("uid", help="Database unique identifier", type=str)
    parser.add_argument("uid_type", help="Datatype of the unique identifier", type=str,
                        choices=["int", "str", "float"])
    parser.add_argument("valid_uids", help="Path to a .csv file containing newline separated valid UIDs", type=str)
    parser.add_argument("output", help="Output File Path", type=str)

    # Optional Args
    parser.add_argument("-ll", "--loggingLevel", help="Level of logging desired",
                        type=str, default=3)
    parser.add_argument("-lp", "--loggingPath", help="Path for desired log file",
                        type=str, default="logs/create_label_script_{}.log".format(round(time.time())))

    # Parse arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parseArguments().__dict__
    logger = logging_wrapper(args['loggingLevel'], args['loggingPath'])

    with open(args["valid_uids"], 'r') as f:
        valid_uids = f.read()

    logger.info("Successfully read in valid UIDs")

    # Currently this also drops the last row as a result of how Pandas saves .csvs
    valid_uids = valid_uids.split("\n")[0:-1]

    # Ensure that valid uids are the correct type so that comparisons make sense.
    if args["uid_type"] == "int":  # Branch A
        valid_uids = [int(i) for i in valid_uids]
    elif args["uid_type"] == "float":  # Branch B
        valid_uids = [float(i) for i in valid_uids]

    url = "mongodb://{}:{}".format(args["host"], args["port"])
    client = mongo.MongoClient(url)
    db = client['edgar']

    logger.info("Connected to MongoDB at {}".format(url))

    logger.info("Extracting filings")
    filings_list = get_all_filings(db['edgar-10k-yash'], filter=valid_uids, logger=logger)

    filings_list = [i.__dict__ for i in filings_list]

    logger.info("")
    with open(args["output"], 'wb') as handle:
        pickle.dump(filings_list, handle)

