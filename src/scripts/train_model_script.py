"""
Training the model
Sample usage from terminal:
    python train_model_script.py train.csv test.csv "label" "LR" results/model_result.pickle -feats=features.csv
Required Args:
    input_tr (.csv)     : Path to CSV file containing the training data
    input_test (.csv)   : Path to CSV file containing the test data
    labels (str)        : Name of the label column in the training and test set. Must be the same in both.
    model (str)         : Name of the model user want to train the data.
                            Possible values are:
                            - LR (Logistic Regression),
                            - RFC (Random Forest Classifier),
                            - KNN (K Neighbors Classifier)
                            - SVM (Support Vector Machine)

Optional Args:
    desired_features (str): Defult = None,
                          Path to CSV file containing all features name that will be used as predictors

    loggingLevel (int)  : Default = 3. 1-5 scale determining the logging messages to save.
                          5 is only CRITICAL, 1 is all messages
    loggingPath (str)   : Default = logs/{script_name}_{unix_time}.log
                          Path to the desired location to store logs

Returns:
    output (.pickle)    : Path to desired location to pickle the model.
"""

import time
import pickle
import argparse
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer
from src.utils import cross_entropy, logging_wrapper
from sklearn.model_selection import train_test_split

# model
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.ensemble import RandomForestClassifier as RFC

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required Args
    parser.add_argument("input_tr", help="Training Input File Path", type=str)
    parser.add_argument("input_test", help="Test Input File Path", type=str)
    parser.add_argument("labels", help="Name of the column where labels are contained", type=str)
    parser.add_argument("model", help="Model to train the data", type=str, choices=["LR", "RFC", "KNN", "SVM"])
    parser.add_argument("output", help="Output File Path", type=str)

    # Optional Args
    parser.add_argument("-feats", "--desired_features",
                        help="Path to a list of columns from the datasets to use as predictors.",
                        type=str, default=None)
    parser.add_argument("-ll", "--loggingLevel", help="Level of logging desired",
                        type=str, default=3)
    parser.add_argument("-lp", "--loggingPath", help="Path for desired log file",
                        type=str, default="logs/keras_nn_script_{}.log".format(round(time.time())))

    # Parse arguments
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parseArguments().__dict__
    logger = logging_wrapper(args['loggingLevel'], args['loggingPath'])

    logger.info("Read in and format training data...")
    print("Read in and format training data...")

    data = pd.read_csv(args['input_tr'])

    if args['desired_features']:
        logger.info("Determine the desired features if necessary...")
        print("Determine the desired features if necessary...")

        with open(args['desired_features'], 'r') as f:
            feats = f.read().split("\n")[:-1]
    else:
        feats = data.columns

    if len([i for i in feats if i in data.columns]) != len(feats):
        logger.error("The following columns were not found in the dataframe {}. Dataframe columns are: {}.".format([i for i in feats if i not in data.columns], data.columns))
        raise KeyError("Some desired columns were not found in the data, please check your files and try again.")

    labels = pd.get_dummies(data[args['labels']])

    if not args['desired_features']:
        data.drop(args['labels'], inplace=True)
        data = data.as_matrix()
    else:
        data = data[feats]
        data = data.as_matrix()

    logger.info("Finished read in and format training data...")
    print("Finished read in and format training data...")

    logger.info("Read in and format test data...")
    print("Read in and format test data...")
    test_data = pd.read_csv(args['input_test'])
    test_labels = pd.get_dummies(test_data[args['labels']])

    if not args['desired_features']:
        test_data.drop(args['labels'], inplace=True)
        test_data = test_data.as_matrix()
    else:
        test_data = test_data[feats]
        test_data = test_data.as_matrix()

    logger.info("Finished read in and format test data...")
    print("Finished read in and format test data...")

    logger.info("Instantiate Pipeline object...")
    print("Instantiate Pipeline object...")

    if args["model"] == "LR":
        pl = Pipeline([
                ('imputer', Imputer()), # Imputer is used in case there are missing values in one of the predictors
                ("clf", OneVsRestClassifier(LogisticRegression()))
            ])
    elif args["model"] == "RFC":
        pl = Pipeline([
                ('imputer', Imputer()), # Imputer is used in case there are missing values in one of the predictors
                ("clf", OneVsRestClassifier(RFC()))
            ])
    elif args["model"] == "KNN":
        pl = Pipeline([
                ('imputer', Imputer()), # Imputer is used in case there are missing values in one of the predictors
                ("clf", OneVsRestClassifier(KNN()))
            ])
    elif args["model"] == "SVM":
        pl = Pipeline([
                ('imputer', Imputer()), # Imputer is used in case there are missing values in one of the predictors
                ("clf", OneVsRestClassifier(SVC()))
            ])
    else:
        logger.error("Model input is not within options.")
        raise KeyError("Model input is not within options of 'LR', 'RFC', 'KNN' or 'SVM', please try again.")

    logger.info("Fit the pipeline to the training data...")
    print("Fit the pipeline to the training data...")
    pl.fit(data, labels)

    logger.info("Compute and print accuracy...")
    print("Compute and print accuracy...")
    train_pred = pl.predict(data)
    accuracy = cross_entropy(labels, train_pred)

    # Log and print cross entropy
    logger.info("Train accuracy is: {}".format(accuracy))
    print("Train Accuracy is: {}".format(accuracy))

    softmax_pred = pl.predict(test_data)
    accuracy = cross_entropy(test_labels, softmax_pred)

    # Log and print cross entropy
    logger.info("Test accuracy is: {}".format(accuracy))
    print("Test Accuracy is: {}".format(accuracy))

    logger.info("Save the model as a pickle")
    print("Save the model as a pickle")
    with open(args["output"], 'wb') as handle:
        pickle.dump(pl, handle)
