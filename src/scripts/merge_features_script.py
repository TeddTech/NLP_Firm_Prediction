import sys
import time
import argparse
import pandas as pd
from src.utils import logging_wrapper

"""
        Merges two .csv files on shared columns. Used for combining text and numeric features into a single file.

        Sample usage from terminal:
            python merge_features_script.py compustat_features.csv text_features.csv merged_features.csv -m cik datadate

        Args:
            f1(.csv): Path to the .csv containing the left DataFrame
            f2(.csv): Path to the .csv containing the right DataFrame
            output (.csv): Path to desired output file
            merge_on (str or list of str): Default="0". Column names to merge on. 
                                           Can pass multiple space separated arguments
            loggingLevel (int): Default=3. 1-5 scale determining the logging messages to save. 
                                5 is only CRITICAL, 1 is all messages
            loggingPath (dir): Default=logs/{script_name}_{unix_time}.log
                               Path to the desired location to store logs                              
        Returns:
            (.csv): File containing the merged DataFrames
"""


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required Args
    parser.add_argument("f1", help="Input File 1 Path", type=str)
    parser.add_argument("f2", help="Input File 2 Path", type=str)
    parser.add_argument('output', help="Path to desired output location", type=str)

    # Optional Args
    parser.add_argument("-m", "--merge_on", help="Column(s) to merge on. Names in each dataframe must be a string",
                        nargs="*", type=str, default="0")
    parser.add_argument("-ll", "--loggingLevel", help="Level of logging desired",
                        type=str, default=3)
    parser.add_argument("-lp", "--loggingPath", help="Path for desired log file",
                        type=str, default="logs/merge_text_features_script_{}.log".format(round(time.time())))

    # Parse arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parseArguments().__dict__
    logger = logging_wrapper(args['loggingLevel'], args['loggingPath'])

    df1 = pd.read_csv(args["f1"])
    df2 = pd.read_csv(args["f2"])

    try:
        logger.info("Attempting to merge on columns: {}".format(args['merge_on']))
        df = df1.merge(df2, how="inner", on=args["merge_on"])

        logger.info("Saving merged data to: {}".format(args['output']))
        df.to_csv(args['output'], index=False)

    except KeyError as e:
        logger.error("{} could not be found in the DataFrame.".format(e))