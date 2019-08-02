#!/usr/bin/python
"""
    Creates differences in each year within a specified column in labeled the subset compustat data

    Sample usage from terminal:
            ```
            python create_financial_features_script.py compustat.csv uid compustat_w_features.csv
            --toDifference=to_diff.csv --toSubtract=to_sub.JSON --toRatio=to_ratio.JSON --diffpct=True
            ```

        Args:
            input (.csv) : Path to the input data which is in .csv format
            uid (str): Unique identifier for the passed .csv. Should be convertible to a string.
            output (.csv): Deisred path to save the output .csv with created features.

            toDifference (.csv): Path to a .csv file containing the names of columns to perform first differencing.
            toSubtract (.json): Path to a .json file with the following schema:
                                {'new_col_name": (col_to_subtract, col_being_subtracted)}
            toRatio (.json): Path to a .json file with the following schema:
                             {'new_col_name": ("numerator_col_name", "denominator_col_name")}
            diffpct(bool): Default=True. Determines whether or not diff_col should also compute percentages.
            crsp (str): Path to a file containing CRSP data. If passed, will also compute volatility
            loggingLevel (int): Default=3. 1-5 scale determining the logging messages to save.
                                5 is only CRITICAL, 1 is all messages
            loggingPath (dir): Default=logs/{script_name}_{unix_time}.log
                               Path to the desired location to store logs
        Returns:
            outputFile (csv) : path to save the dataset with differenced columns in csv

"""
import sys
import time
import json
import argparse
import pandas as pd
import numpy as np
from src.models import create_features
from src.preprocessing import vol
from src.utils import logging_wrapper, format_dates


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required Args
    parser.add_argument("input", help="Input File Path", type=str)
    parser.add_argument("uid", help="Unique identifier for the dataframe", type=str)
    parser.add_argument("output", help="Output File Path", type=str)

    # Optional Args
    parser.add_argument("-tD", "--toDifference", help="Path to columns to compute first differences.",
                        type=str, default=None)
    parser.add_argument("-tS", "--toSubtract", help="Path to JSON for subtracting.",
                        type=str, default=None)
    parser.add_argument("-tR", "--toRatio", help="Path to JSON for creating ratio.",
                        type=str, default=None)
    parser.add_argument("-dp", "--diffpct", help="Compute percentages for differences.",
                        type=bool, default=True)
    parser.add_argument("-crsp", "--crsp", help="Path to CRSP data for computing volatility (will drop majority of columns if used)",
                        type=str, default=None)

    parser.add_argument("-ll", "--loggingLevel", help="Level of logging desired",
                        type=str, default=3)
    parser.add_argument("-lp", "--loggingPath", help="Path for desired log file",
                        type=str, default="logs/create_financial_features_script_{}.log".format(round(time.time())))

    # Parse arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parseArguments().__dict__
    logger = logging_wrapper(args["loggingLevel"], args["loggingPath"])

    # Read input DataFrame
    logger.info("Reading in dataframe. UID is: {}".format(args['uid']))
    dat = pd.read_csv(args['input'])
    dat[args['uid']] = dat[args['uid']].astype(str)

    # Read in all necessary files for creating features:
    if args['toDifference']:
        logger.info("Reading in toDifference file at: {}".format(args['toDifference']))
        with open(args['toDifference'], "r") as f:
            args['toDifference'] = f.read()
        args['toDifference'] = args['toDifference'].split("\n")  # read column_names

    if args['toSubtract']:
        logger.info("Reading in toSubtract file at: {}".format(args['toSubtract']))
        with open(args['toSubtract']) as f:
            args['toSubtract'] = json.load(f)

    if args['toRatio']:
        logger.info("Reading in toRatio file at: {}".format(args['toRatio']))
        with open(args['toRatio']) as f:
            args['toRatio'] = json.load(f)

    logger.info("Creating features from the files found above")
    out_df = create_features(dat, args['uid'], to_diff=args['toDifference'],
                             to_sub=args['toSubtract'], to_div=args['toRatio'], diffpct=True, logger=logger)

    if args["crsp"]:
        logger.info("Computing 12-month historical volatility")
        out_df = vol(args["crsp"], out_df, logger=logger)

    logger.info("Dataframe has {} observation".format(out_df.shape[0]))

    out_df['period'] = out_df['datadate'].apply(format_dates, args=("/",""))

    # Save the file to a .csv in the desired location.
    logger.info("Saving created features to: {}".format(args['output']))
    out_df.to_csv(args['output'], index=False)
