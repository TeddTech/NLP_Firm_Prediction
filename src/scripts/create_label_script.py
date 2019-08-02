"""

    Labelling the subset compustat data

    Sample usage from terminal:
            `python create_label_script.py compustat_subset.csv compustat_labeled.csv`

        Args:
            input_file (csv) : Path to the subset of compustat data
            loggingLevel (int): Default=3. 1-5 scale determining the logging messages to save.
                                5 is only CRITICAL, 1 is all messages
            loggingPath (dir): Default=logs/{script_name}_{unix_time}.log
                               Path to the desired location to store logs

        Returns:
            outputFile (csv) : path to save the labeled compustat dataset in csv

"""
import sys
import time
import argparse
import numpy as np
import pandas as pd
from src.utils import logging_wrapper
from src.preprocessing import label_performance, diff_label, annualize, filter_nan


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
                        type=str, default="logs/create_label_script_{}.log".format(round(time.time())))

    # Parse arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parseArguments().__dict__

    logger = logging_wrapper(args['loggingLevel'], args['loggingPath'])

    logger.info("Annualizing data and creating labels")
    labeled_dat = diff_label(annualize(pd.read_csv(args["input"])))  # Performs all annualizing, shifting, etc.

    labeled_dat = filter_nan(labeled_dat, thresh=0.8, output_file=None, logger=logger)

    # Save the file to a .csv in the desired location.
    logger.info("Saving labelled data to: {}".format(args['output']))

    labeled_dat.to_csv(args["output"], index=False)
