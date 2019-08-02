"""
      Sentiment Analysis on Filing Documents
        Sample usage from terminal:
            python extract_sentiment_script.py filings_list.pickle sentiment_scores.csv -p item7 -s item7 -c item1 item7
        Args:
            input (.pickle):  Python Object containing a list of Filings (e.g. filings_list.pickle)
            polarity (list):  List of text items for polarity analysis. None by Default. (e.g. item7)
            subjectivity (list):  List of text items for subjectivity analysis. None by Default. (e.g. item7)
            certainty (list):  List of text items for certainty analysis. None by Default.
        Returns:
            output (.csv): Path to desired location for un in .csv format (e.g. sentiment_scores.csv)
"""
import sys
import time
import pickle
import logging
import argparse
import pandas as pd
from src.utils import logging_wrapper
from src.models import extract_sentiment

t0 = time.time()

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required Args
    parser.add_argument("input", help="Input File Path", type=str)
    parser.add_argument("output", help="Output File Path", type=str)

    # Optional Args
    parser.add_argument("-p", "--polarity", help="List of text items for polarity analysis",
                            nargs="*", type=str, default=None)
    parser.add_argument("-s", "--subjectivity", help="List of text items for subjectivity analysis",
                            nargs = "*", type=str, default=None)
    parser.add_argument("-c", "--certainty", help="List of text items for certainty analysis",
                            nargs = "*", type=str, default=None)
    parser.add_argument("-ll", "--loggingLevel", help="Level of logging desired",
                        type=str, default=3)
    parser.add_argument("-lp", "--loggingPath", help="Path for desired log file",
                        type=str, default="logs/text_uncertainty_script_{}.log".format(round(time.time())))

    # Parse arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parseArguments().__dict__
    logger = logging_wrapper(args["loggingLevel"], args["loggingPath"])

    logger.info("Reading in data")

    filings_list = []
    with (open(args["input"], "rb")) as openfile:
        while True:
            try:
                filings_list.append(pickle.load(openfile))
            except EOFError:
                break

    filings_list = filings_list[0]

    result = extract_sentiment(filings_list, polarity=args["polarity"],
                               subjectivity=args["subjectivity"], certainty=args["certainty"], logger=logger)

    logger.info("Uncertainty scores are calculated, saving to {}".format(args['output']))
    result.to_csv(args['output'], index=False)

logging.info("Sentiment Analysis took {}s".format(time.time()-t0))
print("Sentiment Analysis took {}s".format(time.time()-t0))
