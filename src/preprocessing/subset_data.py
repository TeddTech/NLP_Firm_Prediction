import pandas as pd
import numpy as np


def subset_cols(input_file, uid, column_names,
                output_file=None, logger=None):  # Tested [Y]
    """
    Utility Function to subset data columns to select a number of features.

    Args:
        input_file (str)  : Path from the current working directory to the input file.
                            The input file's first row should be column names.
        uid (str or int)  : Column name of a unique identifier
        column_names (str): Path from the current working directory to a .csv file
                            containing all column names to keep. One column name
                            should be on each line.
        output_file (str): Path from the current working directory to the location to
                           save the output
        logger (Logger): Logger object from the Logging package which has already been configured.
                         If None, no logging is performed.

    Returns:
        pd.DataFrame of the subset of data. It will also save the file in a .csv format to the specified location.
    """
    # Read in the column names to keep.
    with open(column_names, "r") as f:
        column_names = f.read()
    column_names = column_names.split("\n")

    if logger:
        logger.info("Keeping columns: {}".format(column_names))

    data = pd.read_csv(input_file, low_memory=False)

    if logger:
        logger.info("Data successfully read in")

    # Make sure that none of the uids are null. These would be unusable.
    data = data[data[uid].isnull() == False]
    # Create a new DataFrame containing only the desired columns
    data = pd.DataFrame(data=data, columns=column_names)

    if logger:
        logger.info("Removed unnecessary columns")

    # Save the file to a .csv in the desired location.
    if output_file is not None:

        if logger:
            logger.info("Saving data to: {}".format(output_file))

        data.to_csv(output_file, index=False)

    return data


def subset_rows(input_file, uid, valid_uids,
                output_file=None, uid_type="str", logger=None):  # Tested [Y]
    """
    Utility Function to subset data rows according to a unique identifier column.

    Args:
        input_file (str) : Path from the current working directory to the input file.
        uid (str or int) : Column name of the unique identifier
        uid_type (str)   : Default="str". The type of data contained in the uid column.
                           Possible entries are: "str", "int", "float"
        valid_uids (str) : Path from the current working directory to a .csv file
                           containing all valid values for the unique identifier.
                           One UID should be on each line, and the first line should contain
                           the name of the UID column.
        output_file (str): Path from the current working directory to the location to
                           save the output
        logger (Logger): Logger object from the Logging package which has already been configured.
                         If None, no logging is performed.

    Returns:
        pd.DataFrame of the subset of data. It will also save the file in a .csv format to the specified location.

    """
    # Read in and tidy the valid UIDs file.
    with open(valid_uids, 'r') as f:
        valid_uids = f.read()

    # Currently this also drops the last row as a result of how Pandas saves .csvs
    valid_uids = valid_uids.split("\n")[1:-1]  # Drop the first row which is just the UID name.

    if logger:
        logger.info("Keeping {} UIDs".format(len(valid_uids)))

    # Ensure that valid uids are the correct type so that comparisons make sense.
    if uid_type == "int":  # Branch A
        valid_uids = [int(i) for i in valid_uids]
    elif uid_type == "float":  # Branch B
        valid_uids = [float(i) for i in valid_uids]

    data = pd.read_csv(input_file, low_memory=False)

    if logger:
        logger.info("Data successfully read in")

    # Make sure that none of the uids are null. These would be unusable.
    data = data[data[uid].isnull() == False]  # Any test should have at least ONE NaN to hit this line.
    # Select only rows whose uid is in the list of valid uids
    data = data[data[uid].isin(valid_uids)]

    if logger:
        logger.info("Removed invalid UIDs")

    # Save the file to a csv if specified
    if output_file is not None:

        if logger:
            logger.info("Saving data to: {}".format(output_file))

        data.to_csv(output_file, index=False)
    # Return the subset data so this function can be used in a notebook if necessary.
    return data

def filter_nan(df, thresh=0.8, output_file=None, logger=None):
    """
    Filter's out nan and inf values in a given data set

    Args:
        input_file (str) : A pd.DataFrame.
        thresh (float) : Percentage of non-NA values required for columns in the dataset. Columns that do not meet this requirment will be droped.
        output_file (str): Path from the current working directory to the location to save the output

    Returns:
        pd.DataFrame of the filterd data. It will also save the file in a .csv format to the specified location.
    """
    if logger:
        logger.info("Reading in data")

    if logger:
        logger.info("Dataframe has {} observations".format(df.shape[0]))
        logger.info("Data successfully read in\nBeginning filtering")

    logger.info("Dropping columns that contain all nan")
    df = df.replace([np.inf, -np.inf], np.nan).dropna(axis=1, how="all")
    logger.info("Dropping rows where label column values are nan")
    df = df[np.isnan(df.label)==False]
    logger.info("Dropping columns below threshold of nans")
    df = df.dropna(axis=1, thresh=int(round(df.shape[0]*thresh)))
    logger.info("Dropping rows that contain nan's")
    df.dropna(inplace=True)

    if logger:
        logger.info("Successfully removed nan's")
        logger.info("Dataframe has {} observations".format(df.shape[0]))

    # Save the file to a csv if specified
    if output_file is not None:

        if logger:
            logger.info("Saving data to: {}".format(output_file))

        df.to_csv(output_file, index=False)
    # Return the filtered data so this function can be used in a notebook if necessary.
    return df
