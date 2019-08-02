import pandas as pd
import numpy as np
import missingno as msno

# model selection
from sklearn.model_selection import train_test_split

from src.preprocessing import sub_col, ratio_col, diff_col, annualize, diff_label


def create_features(df, uid, to_diff=None, to_sub=None, to_div=None, diffpct=True,
                    logger=None):  # Tested [N]
    """
    Performs column differencing, subtraction of two columns, and creating ratios of two columns

    Args:
        df (pd.DataFrame): Dataframe containing the columns to operate on and create new features.
        uid (str or int) : Column name for the unique identifier in the DataFrame
        to_diff (list): Default=None. List containing rows to difference. Will add the column: `delta_<colname>`
                        If `diffpct=True`, then will also add: `delta_pct_<colname>`

        to_sub (dict): Default=None. Dictionary containing features to extract and new column names.
                       Should take the following format: {<new_col_name>: (col_to_subtract, col_being_subtracted)}

        to_div (dict): Default=None. Dictionary containing features to divide and new column names.
                       Should take the following format: {<new_col_name>: (numerator, denominator)}

        diffpct (bool): Default=True. Determines whether or not the diff_col function will also return percentages

        logger (Logger): Logger object from the Logging package which has already been configured.
                         If None, no logging is performed.
    Returns:
        (pd.DataFrame) Dataframe with the newly created columns appended to the end.
    """
    if logger:
        logger.info("To start, the DataFrame has: {} observations".format(df.shape[0]))

    df_annual = annualize(df, period_label='fqtr', period_val=4) #change if you would like more grananual observations.
    if logger:
        logger.info("Annualized dataframe has {} observations".format(df_annual.shape[0]))

    df_dummy = df_annual

    if to_diff:
        if logger:
            logger.info("Beginning differencing")
        for column in to_diff:
            try:  # Branch A
                if logger:
                    logger.info("Differencing {} with diffpct={}".format(column, diffpct))
                df = diff_col(df_dummy, column, uid=uid, diffpct=diffpct, logger=logger)
            except KeyError:  # Branch B
                if logger:
                    logger.warning("Column {} was not found in the dataframe".format(column))
                print("Column {} was not found in the dataframe".format(column))
        if logger:
            logger.info("Dataframe currently has {} rows".format(df.shape[0]))

    if to_sub:
        if logger:
            logger.info("Beginning subtraction")

        for k, v in to_sub.items():
            try:  # Branch C
                if logger:
                    logger.info("Subtracting {} from {}".format(v[0], v[1]))
                df[k] = sub_col(df, v)
            except KeyError as e:  # Branch D
                if logger:
                    logger.warning("Column {} was not found in the dataframe".format(e))
                print("Column {} was not found in the dataframe".format(e))
        if logger:
            logger.info("DataFrame currently has {} rows".format(df.shape[0]))

    if to_div:
        if logger:
            logger.info("Beginning subtraction")

        for k, v in to_div.items():
            try:  # Branch E
                if logger:
                    logger.info("Dividing {} over {}".format(v[0], v[1]))
                df[k] = ratio_col(df, v)
            except KeyError as e:  # Branch F
                if logger:
                    logger.warning("Column {} was not found in the dataframe".format(e))
                print("Column {} was not found in the dataframe".format(e))
        if logger:
            logger.info("DataFrame currently has {} rows".format(df.shape[0]))
    if logger:
        logger.info("Features successfully created")
    return df


def prototype(df, desired_cols,  model_dict,
              uid, cat_vars=None, uid_subset=None, test_size=0.2, random_state=None,
              logger=None):  # Tested [N]
    """
    Select features, create labels, subset the data and form training and testing sets before fitting models.

    Args:
        df (pd.DataFrame): DataFrame containing desired columns with which to train models.

        desired_cols (list): List of columns to keep for model training.

        cat_vars (list): Default=None. List of variables to transform to categorical within pandas before training.

        model_dict (dict): Dictionary containing model names as keys and objects as values. {<name>: <initlaized_object>}
                           Any objects with a fit and predict method will work, designed for sklearn objects though.

        uid (str or int) : Column name for the unique identifier in the DataFrame

        uid_subset (int): Default=None. Will select this many <uid>s to use for modelling.
                          If None, then the whole DataFrame is used.

        test_size (float): Default=0.2. Should be between 0 and 1. Determines the size of train_test_split

        random_state (int): Default=None. Random seed to use for splitting and fitting models.
                            If None then no random state is passed.
        logger (Logger): Logger object from the Logging package which has already been configured.
                         If None, no logging is performed.
    Returns:
        (dict) Dictionary of scores. Keys are the classifier names and the values are a list.
               Format of the dictionary is: {<classifier name>: [training accuracy, test accuracy]}
    """
    try:  # Branch A
        if logger:
            logger.info("Selecting desired columns: {}".format(desired_cols))
        df = df[desired_cols]
    except KeyError as e:  # Branch B
        if logger:
            logger.error("Some desired columns were not found: {}".format(e))
        raise KeyError("Some desired columns were not found: {}".format(e))

    if uid_subset:  # Branch C
        all_uids = df[uid]
        if random_state:
            np.random.seed(random_state) # Branch D
        random_sel_biz = np.random.choice(all_uids, uid_subset)
        df = df[df[uid].isin(random_sel_biz)]

    df = annualize(df)
    df_labelled = diff_label(df)

    if cat_vars:  # Branch E
        if logger:
            logger.info("Converting categorical variables: {}".format(cat_vars))

        for var in cat_vars:
            df_labelled[var] = df_labelled[var].astype("category")

    df_presplit = df_labelled[[col for col in df_labelled.columns if col not in ['diff', 'diffpct', 'fqtr']]]
    df_presplit = df_presplit.dropna()
    y = df_presplit['label'].as_matrix()
    features = df_presplit.drop(["label"], axis=1).as_matrix()

    scores = dict()

    if random_state:  # Branch F
        # Create training and test set
        if logger:
            logger.info("Creating train/test split")
        X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=test_size, random_state=random_state)

        # Train models, and print out accuracy.
        for classifier_name, classifier_obj in model_dict.items():
            scores[classifier_name] = list()

            if logger:
                logger.info("Fitting {}".format(classifier_name))
            try:
                classifier_obj.fit(X_train, y_train, random_state=random_state)

            except Exception as e:
                classifier_obj.fit(X_train, y_train)
                if logger:
                    logger.info("{} does not have a random state to set".format(classifier_name))

            print("  Evaluating...")
            pred_train = classifier_obj.predict(X_train)
            train_score = np.mean(pred_train == y_train)

            if logger:
                logger.info("Training accuracy for {} is {}".format(classifier_name, train_score))

            print("  Training accuracy: %f" % train_score)
            scores[classifier_name].append(train_score)
            pred_test = classifier_obj.predict(X_test)
            test_score = np.mean(pred_test == y_test)

            if logger:
                logger.info("Training accuracy for {} is {}".format(classifier_name, test_score))

            print("  Test accuracy:     %f" % test_score)
            scores[classifier_name].append(test_score)

    else:  # Branch G
        # Create training and test set
        if logger:
            logger.info("Creating train/test split")

        X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=test_size)
        # Train models, and print out accuracy.
        for classifier_name, classifier_obj in model_dict.items():
            scores[classifier_name] = list()

            if logger:
                logger.info("Fitting {}".format(classifier_name))

            classifier_obj.fit(X_train, y_train)
            print("  Evaluating...")
            pred_train = classifier_obj.predict(X_train)
            train_score = np.mean(pred_train == y_train)

            if logger:
                logger.info("Training accuracy for {} is {}".format(classifier_name, train_score))

            print("  Training accuracy: %f" % train_score)
            scores[classifier_name].append(train_score)

            pred_test = classifier_obj.predict(X_test)
            test_score = np.mean(pred_test == y_test)

            if logger:
                logger.info("Test accuracy for {} is {}".format(classifier_name, test_score))

            print("  Test accuracy:     %f" % test_score)
            scores[classifier_name].append(test_score)

    return scores
