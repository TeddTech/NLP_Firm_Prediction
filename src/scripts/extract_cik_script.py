"""
        Unique CIK Extractor from Compustat Data

        Sample usage from terminal:
            python extract_cik_script.py compustat_199501-201803.csv compustat_cik_list.csv

        Args:
            input (.csv):  Path to data with the `cik` column (e.g. Compustat Data )
            loggingLevel (int): Default=3. 1-5 scale determining the logging messages to save.
                                5 is only CRITICAL, 1 is all messages
            loggingPath (dir): Default=logs/{script_name}_{unix_time}.log
                               Path to the desired location to store logs
        Returns:
            output (.csv): Path to desired location for the unique CIK list in .csv format
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
    parser.add_argument("input", help="Input File Path", type=str)
    parser.add_argument("output", help="Output File Path", type=str)

    # Optional Args
    parser.add_argument("-ll", "--loggingLevel", help="Level of logging desired",
                        type=str, default=3)
    parser.add_argument("-lp", "--loggingPath", help="Path for desired log file",
                        type=str, default="logs/extract_cik_script_{}.log".format(round(time.time())))

    # Parse arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parseArguments().__dict__
    logger = logging_wrapper(args["loggingLevel"], args["loggingPath"])

    logger.info("Reading in data")
    data = pd.read_csv(args["input"], low_memory=False)

    # drop NA cik values:
    data = data[data['cik'].isnull()==False]

    # unique cik list:
    cik_list = data.cik.unique()

    logger.info("Found unique CIKs, saving to {}".format(args['output']))
    pd.DataFrame(data=cik_list, columns=["cik"]).astype(int).astype(str).to_csv(args['output'], index=False)
