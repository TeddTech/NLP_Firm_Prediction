"""
        Find common elements of two given files

        Sample usage from terminal:
            python common_col_script.py CIK_edgar.csv "CIK" cik_list_compustat.csv
            "cik" common_cik_list.csv --columnType="int"

            python common_col_script.py crsp_ticker_list.csv "TICKER" compustat_ticker_list.csv
            "tic" common_ticker_list.csv --columnType="str"

        Args:
            f1(csv): Path to input file 1
            f1_col(str): Column from input file 1 to compare
            f2(csv):  Path to input file 2
            f2_col(str): Column from input file 2 to compare
            columnType(str): Column type. It accepts following values (int, str or float).
            loggingLevel (int): Default=3. 1-5 scale determining the logging messages to save.
                                5 is only CRITICAL, 1 is all messages
            loggingPath (dir): Default=logs/{script_name}_{unix_time}.log
                               Path to the desired location to store logs
        Returns:
            outputFile(csv): list of common elements in specified column() of file1 and file2
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
    parser.add_argument("f1", help="Input File 1 Path", type=str)
    parser.add_argument("f1_col", help="Column to compare from Input file 1", type=str)
    parser.add_argument("f2", help="Input File 1 Path", type=str)
    parser.add_argument("f2_col", help="Column to compare from Input file 1", type=str)
    parser.add_argument('output', help="Path to desired output location", type=str)

    # Optional Args
    parser.add_argument("-ct", "--columnType", help="Desired output format", default="int",
                        choices=['int', 'str', 'float'])
    parser.add_argument("-ll", "--loggingLevel", help="Level of logging desired",
                        type=str, default=3)
    parser.add_argument("-lp", "--loggingPath", help="Path for desired log file",
                        type=str, default="logs/common_col_script_{}.log".format(round(time.time())))

    # Parse arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parseArguments().__dict__
    logger = logging_wrapper(args["loggingLevel"], args["loggingPath"])

    logger.info("Reading in data")
    file1 = pd.read_csv(args["f1"], low_memory=False)
    file2 = pd.read_csv(args["f2"], low_memory=False)

    c = set(file1[args["f1_col"]])
    e = set(file2[args["f2_col"]])
    match = e & c
    match = list(match)

    logger.info("Found matching elements between columns {} and {}".format(args["f1_col"], args["f2_col"]))

    if args["columnType"] == "int":
        # Converts to string because otherwise it will save as a float for some reason.
        pd.DataFrame(data=match, columns=[args["f1_col"]]).astype(int).astype(str).to_csv(args["output"], index=False)
    else:
        pd.DataFrame(data=match, columns=[args["f1_col"]]).to_csv(args["output"], index=False)

    logger.info("Saving to {}".format(args["output"]))
