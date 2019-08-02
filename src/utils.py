import json
import logging
import numpy as np
import pandas as pd


def format_dates(date, from_sep="/", to_sep="-"):  # Tested [N]
    """ Utility function to use within a pandas apply to get dates in a consistent format"""
    nums = date.split(from_sep)
    return to_sep.join(nums)


def dict2json(to_json, output):  # Tested [N]
    """
    Wrapper for `json` package to easily turn python dictionaries into JSON files on disk.

    Used to create files to pass to the create_features_script for computing ratios and subtractions.

    Args:
        to_json (dict): Dictionary to serialize into JSON
        output (str): Path to save the output JSON file

    Returns:
        (bool) True if saving to JSON was successful, False otherwise.
    """
    try:
        with open(output, 'w') as f:
            json.dump(to_json, f)
        return True

    except Exception as e:
        print(e)
        return False


def logging_wrapper(level, path):
    # Determine desired logging level
    level = int(str(level) + "0")

    # Create a logging instance
    logger = logging.getLogger()
    logger.setLevel(level)

    # Setup logging file
    logger_handler = logging.FileHandler(path)
    logger_handler.setLevel(level)

    # Formatting:
    logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # Put them together
    logger_handler.setFormatter(logger_formatter)

    logger.addHandler(logger_handler)
    logger.info("Logging successfully configured!")

    return logger


def leading_zeros(df, df_col='cik'):   # Tested [Y]
    """
    Creates leading zeros infront of cik so that the length of the ciks are 10

    Args:
        df (pd.DataFrame): Dataframe that has a column needed to add leading zeros
        df_col (str): Column from the dataframe that need to be changed.

    Return
        df with leading zeros infront of the cik
    """

    L = list()
    for i in df[df_col]:
        i = str(int(i))
        while len(i) < 10:
            i = "0" + i
        L.append(i)

    dat = pd.DataFrame(L)

    return dat


def softmax_mse(y_true, softmax_pred):
    """
    Takes in softmax predictions and onehot true labels, computes MSE.
    """
    return np.mean((y_true - softmax_pred)**2)

def cross_entropy(targets, predictions, epsilon=1e-12):
   """
   Computes cross entropy between targets (encoded as one-hot vectors) and predictions.

   Args: 
        targets (N, k) ndarray      : The targets of prediction
        predictions (N, k) ndarray  : The predictions

   Returns: Scalar
   """

   predictions = np.clip(predictions, epsilon, 1. - epsilon)

   N = predictions.shape[0]

   ce = -np.sum(np.sum(targets*np.log(predictions+1e-9)))/N

   return ce