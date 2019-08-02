import sys
import time
import argparse
import pandas as pd
from src.utils import logging_wrapper
from src.preprocessing import subset_cols, subset_rows

"""
    Train/Test Split.
    
    Due to the nature of financial data, we do not want to create a train/test split randomly in the standard way. 
    We instead want to use only information from the past in our future predictions. We do so by splitting on year.

    This script will be run twice, once to extract the training set and again to extract the test set.
    
    Sample usage from terminal:
            python year_split_script.py merged_labelled.csv "fyearq" "str" train_years.csv train.csv

        Args:

            input_file (csv) : Path to original compustat data
            year_col (str) : Column name for the year in the dataset
            year_type (str) : The data type of the the uid selected. Examples: "int", "str"
            year_list (str) : Path to the list of desired years
            loggingLevel (int): Default=3. 1-5 scale determining the logging messages to save.
                                5 is only CRITICAL, 1 is all messages
            loggingPath (dir): Default=logs/{script_name}_{unix_time}.log
                               Path to the desired location to store logs

        Returns:
            outputFile (csv) : path to save the split data.
"""


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required Args
    parser.add_argument("input", help="Input File Path", type=str)
    parser.add_argument("year_col", help="Name of the year column in the dataframe", type=str)
    parser.add_argument("year_type", help="Data type of year in this dataframe", type=str, choices=["int", "str"])
    parser.add_argument("year_list", help="Path to .csv file containing all desired years", type=str)
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
    logger = logging_wrapper(args["loggingLevel"], args["loggingPath"])

    logger.info("Beginning to subset rows")
    subset_rows(args['input'], args["year_col"], args["year_list"], args["output"], args["year_type"], logger=logger)

