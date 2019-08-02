"""
    Subsetting the Compustat data

    Sample usage from terminal:
            python subset_data_script.py compustat_199501-201803.csv "cik" "str" compustat_selected_cols.csv common_cik_list.csv compustat_subset.csv

        Args:

            input_file (csv) : Path to original compustat data
            uid (str) : Unique identifier of firm. Examples: "cik", "tic"
            uid_type (str) : The data type of the the uid selected. Examples: "int", "str"
            column_names (str) : Path to column name file
            uid_list (str) : Path to common UID list
            loggingLevel (int): Default=3. 1-5 scale determining the logging messages to save.
                                5 is only CRITICAL, 1 is all messages
            loggingPath (dir): Default=logs/{script_name}_{unix_time}.log
                               Path to the desired location to store logs

        Returns:
            outputFile (csv) : path to save the cleaned up compustat dataset in csv
"""
import sys
import time
import argparse
import pandas as pd
from src.utils import logging_wrapper
from src.preprocessing import subset_cols, subset_rows

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required Args
    parser.add_argument("input", help="Input File Path", type=str)
    parser.add_argument("uid", help="Unique identifier for the dataframe", type=str)
    parser.add_argument("uid_type", help="Data type of selected UID", type=str, choices=["int", "str", "float"])
    parser.add_argument('col_names', help="Path to .csv file containing desired column names", type=str)
    parser.add_argument("uid_list", help="Path to .csv file containing all desired UIDs", type=str)
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

    logger.info("Beginning to subset columns")
    subset_cols(args["input"], args["uid"], args["col_names"], "temp.csv", logger=logger)

    logger.info("Beginning to subset rows")
    subset_rows("temp.csv", args["uid"], args["uid_list"], args["output"], args["uid_type"], logger=logger)
