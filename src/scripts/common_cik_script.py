"""
        Find common CIKs of Compustat CIK and EDGAR CIK

        Sample usage from terminal:
            python common_cik_script.py CIK_edgar.csv cik_list_compustat.csv common_cik_list.csv

        Args:
            edgar (.csv): Path to unique CIK list from Edgar data
            compustat (.csv): Path to unique CIK list from Compustat data
            loggingLevel (int): Default=3. 1-5 scale determining the logging messages to save.
                                5 is only CRITICAL, 1 is all messages
            loggingPath (dir): Default=logs/{script_name}_{unix_time}.log
                               Path to the desired location to store logs

        Returns:
            (.csv): File containing a list of common CIKs from the EDGAR and Compustat datasets
"""

import sys
import time
import argparse
import pandas as pd
from src.utils import logging_wrapper


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required Args
    parser.add_argument("edgar", help="Path ro EDGAR CIKs", type=str)
    parser.add_argument("compustat", help="Path to Compustat CIKs", type=str)
    parser.add_argument("output", help="Output File Path", type=str)

    # Optional Args:
    parser.add_argument("-ll", "--loggingLevel", help="Level of logging desired",
                        type=str, default=3)
    parser.add_argument("-lp", "--loggingPath", help="Path for desired log file",
                        type=str, default="logs/common_cik_script_{}.log".format(round(time.time())))

    # Parse arguments
    args = parser.parse_args()


    return args


if __name__ == "__main__":
    args = parseArguments().__dict__
    logger = logging_wrapper(args["loggingLevel"], args["loggingPath"])

    logger.info("Reading in data")
    edgar = pd.read_csv(args["edgar"], low_memory=False)
    compustat = pd.read_csv(args["compustat"], low_memory=False)

    c = set(compustat["cik"])
    e = set(edgar["CIK"])
    match = e & c

    logger.info("Found common CIKs, saving to {}".format(args["output"]))
    pd.DataFrame(data=list(match), columns=["cik"]).astype(int).astype(str).to_csv(args["output"], index=False)
