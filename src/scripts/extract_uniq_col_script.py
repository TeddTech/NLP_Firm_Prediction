"""
        Unique Value Extractor from a given CSV

        Sample usage from terminal:
            `python extract_uniq_col_script.py compustat_199501-201803.csv "tic" "character" compustat_ticker_list.csv`
            `python extract_uniq_col_script.py crsp_199501-201712.csv "TICKER" "integer" crsp_ticker_list.csv`

        Args:
            input_file (csv):  Data with the `TICKER` column
            column_name (str): Column name to extract
            column_type (str): Column type. It accepts following values (int, str or float).
            loggingLevel (int): Default=3. 1-5 scale determining the logging messages to save.
                                5 is only CRITICAL, 1 is all messages
            loggingPath (dir): Default=logs/{script_name}_{unix_time}.log
                               Path to the desired location to store logs

        Returns:
            output_file(csv): Extracted column as a csv
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
    parser.add_argument("col_name", help="Column to extract", type=str)
    parser.add_argument("col_type", help="Type of column ot extract", type=str)
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

    logger.info("Reading in data from:{}".format(args["input"]))
    data = pd.read_csv(args["input"], low_memory=False)

    # drop NA cik values:
    data = data[data[args["col_name"]].isnull() == False]

    # unique ticker list:
    ticker_list = data[args["col_name"]].unique()

    logger.info("Saving data to: {}".format(args["output"]))
    if args["col_type"] == "int":
        pd.DataFrame(data=ticker_list, columns=[args["col_name"]]).astype(int).astype(str).to_csv(args["output"], index=False)
    else:
        pd.DataFrame(data=ticker_list, columns=[args["col_name"]]).to_csv(args["output"], index=False)

