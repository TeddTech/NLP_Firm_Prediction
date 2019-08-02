"""
    Script to extract the topic from the selected item of SEC filings from MongoDB

    Sample usage from terminal:
        python src/scripts/topic_modelling_script.py data/filings_list.pickle "gensim" 7 20 data/item_7_20_topic_features.csv --stop_word_list=data/stopwordlist.csv
         --save_model=True --save_feature=True --random_state=39 --model_path=results/item_7_20_topic_model.pickle --feature_path

    Args:
        f1 (.pickle)        :  Python Object containing a list of Filings (e.g. filings_list.pickle)
        model (str)         :  Type of topic modelling method that user want to use. Possible values are:  ["gensim", "cv_lda","tfidf_nmf"]
        item_num(int)       :  Item from filing object that user want to perfrom topic modelling on
        topic_number(int)   :  Number of topic user wants to extract

    Optional:
        stop_word_list(path):  Path to list of stopword
        save_model(bool)    :  Option to also return the model (default is False)
        save_feature(bool)  :  Option to also return feature (default is False)
        random_state(int)   :  Default=None. Fix the random state of the LDA model.
        model_path(pickle)  : Path to save the model in pickle
        feature_path(pickle): Path to save the feature in pickle

    Return:
        outputFile(csv)     : Path to save the dataframe with CIK, period and topic weights of each document.


"""

import sys
import pickle
import argparse
import nltk.corpus
import pandas as pd
from time import time
import pymongo as mongo
from mongoengine import *
from src.utils import logging_wrapper
from src.models import extract_topics


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required Args
    parser.add_argument("f1", help="Input File 1 Path",
                        type=str, required=True)
    parser.add_argument("model", help="Topic Modeling Method", choices=["gensim", "cv_lda", "tfidf_nmf"],
                        type=str, required=True)
    parser.add_argument("item_num", help="Item from filing object that user want to perfrom topic modelling on",
                        type=int, required=True)
    parser.add_argument("topic_number", help="Number of topic user wants to extract",
                        type=int, required=True)
    parser.add_argument('output', help="Path to desired output location",
                        type=str, required=True)

    # Optional Args
    parser.add_argument("-ll", "--loggingLevel", help="Level of logging desired",
                        type=str, default=3)
    parser.add_argument("-lp", "--loggingPath", help="Path for desired log file",
                        type=str, default="logs/create_label_script_{}.log".format(round(time())))
    parser.add_argument("-sw", "--stop_word_list", help="Path to list of stopword", nargs="*", type=str,
                        default=nltk.corpus.stopwords.words('english'))
    parser.add_argument("-sm", "--save_model", help="Whether or not saving the model", nargs="*", type=bool,
                        default=False)
    parser.add_argument("-sf", "--save_features", help="Whether or not saving the feature", nargs="*", type=bool,
                        default=False)
    parser.add_argument("-rs", "--random_state", help="Fix the random state of the topic model, should be integer",
                        nargs="*", type=str, default=None)
    parser.add_argument("-mp", "--model_path", help="Path to save the model", nargs="*", type=str,
                        default="model.pickle")
    parser.add_argument("-fp", "--features_path", help="Path to save the feature", nargs="*", type=str,
                        default="features.pickle")

    # Parse arguments
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parseArguments().__dict__
    logger = logging_wrapper(args["loggingLevel"], args["loggingPath"])

    logger.info("Start reading in filing list from pickle...")
    print("Start reading in filing list from pickle...")

    t0 = time()
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
    logger.info("Finish reading in filing list from pickle...")
    print("Finish reading in filing list from pickle...")

    if type(args["stop_word_list"]) == list:
        sw_list = args["stop_word_list"]
    else:
        sw_list = pd.read_csv(args["stop_word_list"], header=None)

    result = extract_topics(args["model"], filings_list, args["item_num"], args["topic_number"], sw_list,
                              args["random_state"], args["save_model"], args["save_features"], logger=logger)
    logger.info("done in {}s.".format(round(time() - t0, 3)))
    print("done in {}s.".format(round(time() - t0, 3)))

    logger.info("Saving the result into a dataframe in {}".format(args["output"]))
    print("Saving the result into a dataframe in {}".format(args["output"]))

    if args["save_model"] == True:
        with open(args["model_path"], 'wb') as handle:
            pickle.dump(result[1], handle)
        if args["save_features"] == True:
            with open(args["features_path"], 'wb') as handle:
                pickle.dump(result[2], handle)
            result[0].to_csv(args["output"])
        else:
            result[0].to_csv(args["output"])
    else:
        if args["save_features"] == True:
            with open(args["features_path"], 'wb') as handle:
                pickle.dump(result[1], handle)
            result[0].to_csv(args["output"])
        else:
            result.to_csv(args["output"])
