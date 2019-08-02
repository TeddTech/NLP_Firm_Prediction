import re
import time
import numpy as np
import pandas as pd
import datetime as dt
from tqdm import tqdm, trange


def label_performance(delta_s, cutoff=0.1):  # Tested [Y]

    """
    Takes the change of a given performance metric and outputs a label; up, down or flat.

    Args:
        delta_s (float): The change in performance metric from the previous period.
        cutoff (float): Default=0.1. Value to use to determine whether a performance metric is no longer 'flat'

    Returns:
        (str) 1,2 or 3 where 1 is down, 2 is flat and 3 is up.
    """
    # May want to switch labels to; ('up'=1, 'flat'=0, 'down'=-1)
    if delta_s > cutoff:  # Branch A
        return 2
    elif abs(delta_s) > cutoff:  # Branch B
        return 0
    else:  # Branch C
        return 1


def diff_col(df,  col_name, uid='cik', diffpct=True, logger=None):  # Tested [N]

    """
    Differences in each year within a specified column in a DataFrame, with the option of adding a percentage change as well.

    Args:
        df (pd.DataFrame): DataFrame to perform differencing on.
        col_name (str or int): Name of the column to difference.
        uid (str or int): Default="cik". Unique identifier of groupings in the data.
                          Used to determine masking for nonsensical values.
        diffpct (bool): Default=True. If True include a column of the percentage change of the feature as well

    Returns:
        pd.DataFrame with delta_* column added.
    """
    # Creates diff column
    df['delta_{}'.format(col_name)] = df[col_name].diff()

    # Inputs NA in the diff column for the rows that switch over to different firms
    diff_mask = df[uid] != df[uid].shift(1)
    df['delta_{}'.format(col_name)][diff_mask] = np.nan

    # Creates delta_pct_* column
    if diffpct:  # Branch A
        df['delta_pct_{}'.format(col_name)] = df['delta_{}'.format(col_name)] / df[col_name].shift(1)
        df['delta_pct_{}'.format(col_name)][diff_mask] = np.nan
        df = df[np.isfinite(df["delta_pct_{}".format(col_name)])]
        return df

    df = df[np.isfinite(df["delta_{}".format(col_name)])]
    return df  # Branch B


def annualize(df, period_label='fqtr', period_val=4):  # Tested [Y]

    """
    Select only a subset of a DataFrame which has a particular value in a selected column.
    Used for selecting only 4th quarter observations from Compustat in Sauder's 2018 Capstone Project

    Args:
        df (pd.DataFrame): DataFrame containing observations to be subset.
        period_label (str or int): Default="fqtr". Label of a dataframe column to use for annualizing data
        period_val (str or int): Default=4. Value of the column to select by

    Returns:
        pd.DataFrame with only observations specified by period_val in period_label's column.
    """
    # Only select observations of firms final quarter of their fiscal year
    out = df[df[period_label] == period_val]
    return out


def diff_label(df, uid='cik', p='prccq', cutoff=0.1, diffpct=True):  # Tested [Y]

    """
    Creates a diff column for a given dataframe where the diff column is the difference in perfromace metric (p) of the current period and pervious period.
    And creates a label column by comparing the change of a given perfromace metric (p) and outputs a label; up, down or flat.

    Args:
        df (pd.DataFrame): DataFrame of selected features and observation.
        uid (str) : Default="cik". Unique identifier of a firm.
        p (str) : Default="prccq". Performance indicator of a firm.
        cutoff (float): Default=0.1. Value of cutoff for the label_performance() function
        diffpct (bool) : Default=True. If True create a column for the percentage change as well.

    Returns:
        pd.DataFrame : With performance differences and label columns added.
    """
    df1 = df[np.isfinite(df[p])]  # Drop all line that column p has NA

    # Creates diff column
    df1['diff'] = df1[p].diff()

    # Inputs NA in the diff column for the rows that switch over to different firms
    diff_mask = df1[uid] != df1[uid].shift(1)
    df1['diff'][diff_mask] = np.nan
    

    # Creates diffpct column
    if diffpct:  # Branch A
        df1['diffpct'] = df1['diff']/df1[p].shift(1)
        df1['diffpct'][diff_mask] = np.nan
        df1['label'] = df1['diffpct'].apply(label_performance, args=(cutoff,))
        df1['label'] = df1['label'].shift(-1)
        label_mask = df1[uid] != df1[uid].shift(-1)
        df1['label'][label_mask] = np.nan
        # Drops the last year for each company, where no label would exist.
        df = df1.dropna(axis=0, how='any', subset=['label'])
        # Drops the first year for each company
        df = df1.dropna(axis=0, how='any', subset=['diff'])
        return df

    # Creates label column
    df1['label'] = df1['diff'].apply(label_performance, args=(cutoff,))
    df1['label'] = df1['label'].shift(-1)
    label_mask = df1[uid] != df1[uid].shift(-1)
    df1['label'][label_mask] = np.nan

    # Drops the first year for each company
    df = df1.dropna(axis=0, how='any', subset=['diff'])
    # Drops the last year for each company, where no label would exist.
    df = df1.dropna(axis=0, how='any', subset=['label'])
    return df


def bi_col(df, thresh, df_col='xrdy', greater=True):       # Tested [Y]
    """
    This function turns a numeric feature to a binary one based on a given threshold.

    Args
        df (pd.DataFrame): Dataframe containing the columns to turn into binary features.
        df_col (str): Name of the column to transform
        thresh (float): Threshold value to use for determining output
        greater (bool): Default=True. Determines which side of the threshold will be set to True in the binary feature.
                        If True, then values larger than the threshold will be True, and vice versa.

    Return
        (pd.DataFrame) The initial dataframe entered with the column specified changed to a binary values
    """
    if thresh:  # Branch A
        df[df[df_col] > thresh] = np.NaN
        df = np.isnan(df[df_col])
        if greater:  # Branch B
            return df
        else:  # Branch C
            df = df.replace({True: False, False: True})
            return df

    df = np.isnan(df[df_col])
    df = df.replace({True: False, False: True})
    return df


def ratio_col(df, df_cols):                  # Tested [Y]
    """
    This function computes the ratio between two columns and returns a Dataframe containing the ratio as a column.

    Args
        df (pd.DataFrame): Dataframe containing the columns to compute a ratio.
        df_cols (tuple): A tuple containing the names of columns in the Dataframe to use in computing the ratio.
                         Format is (<numerator>, <denominator>)
    Return
        (pd.Series) The inital dataframe entered with addition columns for the ratio of the two columns specified in the df_cols argument
    """

    df[df_cols[0]] = df[df_cols[0]].div(df[df_cols[1]].values, axis=0)
    return df[df_cols[0]]


def mrk_cap(df, col, list_cols):             # Tested [Y]
    df[list_cols] = df[list_cols].div(df[col].values,axis=0)
    return df


def sub_col(df, df_cols):                    # Tested [Y]
    """
    This function takes the difference between two columns.

    Args
        df (pd.DataFrame):
        df_cols (tuple): A tuple containing the names of columns in the dataframe to subtract from each other.
                         Format is (<subtract_from>, <being_subtracted>)
    Return
        (pd.DataFrame) A Dataframe with one column which is the difference between the two columns passed.
    """

    df = df[[df_cols[1], df_cols[0]]]
    df = df.diff(axis=1)
    df = df.drop(df_cols[1], 1)
    return df


def vol(df1, df2, logger=None):  # Tested [Y]
    """
    Computes the volatility of a given firm for each year

    Args
        df1 : CRSP dataframe
        df2 : Compustat dataframe

    Return
        df with a column called vol added
    """
    df1 = pd.read_csv(df1)
    df1 = df1.sort_values(['TICKER','date'])
    df1 = df1.rename(columns = {'date':'datadate', 'TICKER':'tic'})
    logger.info('Performing diff_col')
    df = diff_col(df=df1, col_name='PRC', uid='tic', diffpct=True)

    temp = df.groupby(['tic'])
    temp = temp.rolling(window=252, min_periods=252, center=False).std()  # temp = pd.rolling_std(temp,252,252)
    temp = temp.reset_index([0], drop=True)  # temp = pd.merge(df.drop(columns=['delta_pct_PRC']), temp[['delta_pct_PRC', 'tic', 'datadate']], how='inner', on=['tic', 'datadate'])

    df['vol'] = temp.delta_pct_PRC

    df = df.sort_values(['tic', 'datadate'])

    for i in trange(1,253):
        mask = df['tic'] != df['tic'].shift(i)
        df['vol'][mask] = np.nan

    df = pd.merge(df2, df[['vol', 'tic', 'datadate']], how='inner', on=['tic', 'datadate'])

    return df


def sum_ytd(df, df_col, uid='cik', date='fyearq'):  # Tested [N]
    """
    This function takes the cumlative sum of a column in a given dataframe within a give group.

    Args
        df (pd.DataFrame):
        df_col (str): The name of column in the dataframe to be summed
        uid (str): The name of a unique identifier column in df to group by. Ex. 'cik', 'tic'
        date (str): The name of a date column in the df to group by. Ex 'fyearq', 'datacqtr', 'datadate', 'fqtr'
    Return
        (pd.DataFrame) A dataframe with one column which is the sum year to date of the df_col within a given group.
    """

    dftemp = df[[uid, date, df_col]]

    df = df[df_col[:-1] + "Y"] = dftemp.groupby([uid, date]).cumsum(0)

    return df
