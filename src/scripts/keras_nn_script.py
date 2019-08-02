import sys
import time
import pickle
import argparse
import numpy as np
import pandas as pd

from src.models import build_keras
from keras.utils import to_categorical
from src.utils import logging_wrapper, softmax_mse

"""
Building and fitting Keras Feed-Forward Network.
Sample usage from terminal:
    python keras_nn_script.py train.csv test.csv label -nl 2 -nn 50 100 -a relu sigmoid
                              -l categorical_crossentropy -opt adam

Required Args:
    input_tr (.csv):  Path to CSV file containing the training data
    input_test (.csv): Path to CSV file containing the test data
    labels (str): Name of the label column in the training and test set. Must be the same in both.

Optional Args:
    n_layers (int): Number of hidden layers to include in the network.
                    Dropout layers are included in number of layers.
    n_neurons (list): Number of neurons in each hidden layer.
                      Argument should be either size `n_layers`, or if `layer_types` specified,
                      the number of dense layers.
    activation (list or str): Activation functions to use at each layer.
                              If a string is supplied, that activation will be used at each layer
                              except for the output layer, which will always use softmax.
    layer_types (list or None): Default=None. List of strings for each layer desired.
                                Currently, only Dropout and Dense layers are supported.
                                If None, all layers are set to Dense.
                                If passed, the list should be size `n_layers - 1`
    dropout_rate (int): Default=0.2. Determines dropout rate for potential dropout layers.
                        Currently only a single value is supported.
    loss (str): Loss function to use when compiling the model.
                Will be used by the optimizer during training to determine fit
    optimizer (str): Optimizer to use in training the model.
    n_epochs (int): Number of epochs to train for. Currently, early stopping is not implemented,
                    so this should be conservative at first
                    
    desired_features (str): Path to a .csv file containing all desired features.
    loggingLevel (int): Default=3. 1-5 scale determining the logging messages to save.
                                5 is only CRITICAL, 1 is all messages
    loggingPath (str): Default=logs/{script_name}_{unix_time}.log
                       Path to the desired location to store logs


Returns:
    output (.pickle): Path to desired location to pickle the Keras model.
"""


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required Args
    parser.add_argument("input_tr", help="Training Input File Path", type=str)
    parser.add_argument("input_test", help="Test Input File Path", type=str)
    parser.add_argument("labels", help="Name of the column where labels are contained", type=str)
    parser.add_argument("output", help="Output File Path", type=str,default="keras_nn_{}.pickle".format(time.time()))

    # Optional Args
    parser.add_argument("-feats", "--desired_features",
                        help="Path to a list of columns from the datasets to use as predictors.",
                        type=str, default=None)
    parser.add_argument("-nl", "--n_layers", help="Number of hidden layers to include in the neural net",
                        type=int, default=1)
    parser.add_argument("-nn", "--n_neurons", help="Number of neurons for each hidden layer in the network. "
                                                   "Should have `n_layers` arguments",
                        nargs="*", type=int, default=[20])
    parser.add_argument("-a", "--activation", help="Activation functions for the network."
                                                   "Should have either `n_layers` arguments if you wish to specify"
                                                   "different functions for different layers, or one argument for a "
                                                   "single activation",
                        nargs="*", type=str, default="relu")
    parser.add_argument("-lt", "--layer_types", help="Types of layers to use in the network. "
                                                     "Currently only Dense and Dropout are supported",
                        nargs="*", type=str, default=["dense"])
    parser.add_argument("-dr", "--dropout_rate", help="Rate of dropout if layer_types is specified.",
                        type=float, default=0.2)
    parser.add_argument("-l", "--loss", help="Loss function to use",
                        type=str, default="categorical_crossentropy")
    parser.add_argument("-opt", "--optimizer", help="Optimization algorithm to use. Passed to model.compile()",
                        type=str, default="adam")
    parser.add_argument("-e", "--n_epochs", help="Number of epochs to train for. Passed to model.fit()",
                        type=int, default=5)
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

    # Check inputs:
    if len(args['activation']) not in [1, args['n_layers'], sum([i.lower == "dense" for i in args['layer_types']])]:
        logger.error("The length of the activations argument is not valid. Should be either 1, `n_layers`, "
                     "or a number of arguments equal to the number of dense layers.")
        raise ValueError("The number of activations passed is not valid. Should be either 1, `n_layers`, "
                         "or a number of arguments equal to the number of dense layers")

    if len(args["n_neurons"]) not in [args['n_layers'], sum([i.lower == "dense" for i in args['layer_types']])]:
        logger.error("Number of neurons is not the correct size. Should have `n_layers` arguments "
                     "or a number of arguments equal to the number of dense layers")
        raise ValueError("Number of neurons is not the correct size. Should have `n_layers` arguments or "
                         "a number of arguments equal to the number of dense layers")

    if len(args['layer_types']) != args['n_layers'] - 1:
        logger.error("Layer types is not correct. Does not conform to the number of layers desired, the length of"
                     "this argument should be `n_layers` - 1")
        raise ValueError("Layer types is not correct. Does not conform to the number of layers desired, the length of"
                         "this argument should be `n_layers` - 1, as the first layer is always dense.")

    if args['desired_features']:  # Determine the desired features if necessary.
        with open(args['desired_features'], 'r') as f:
            feats = f.read().split("\n")[:-1]

    # Read in and format training data:
    data = pd.read_csv(args['input_tr'])
    if len([i for i in feats if i in data.columns]) != len(feats):
        logger.error("One or more of {} were not found. Dataframe columns are: {}.".format(feats, data.columns))
        raise KeyError("Some desired columns were not found in the data, please check your files and try again.")

    n_cats = len(data[args['labels']].unique())
    labels = data[args['labels']].astype(np.int64).as_matrix()
    one_hot_labels = to_categorical(labels, n_cats)  # Labels must be categorical for keras
    if not args['desired_features']:
        data.drop(args['labels'], inplace=True)
        data = data.as_matrix()
    else:
        data = data[feats]
        data = data.as_matrix()

    # Read in and format test data
    test_data = pd.read_csv(args['input_test'])
    test_labels = test_data[args['labels']].astype(np.int64).as_matrix()
    if not args['desired_features']:
        test_data.drop(args['labels'], inplace=True)
        test_data = test_data.as_matrix()
    else:
        test_data = test_data[feats]
        test_data = test_data.as_matrix()
    one_hot_test = to_categorical(test_labels, n_cats)

    # Build and compile Keras model
    model = build_keras(n_layers=args['n_layers'], n_neurons=args['n_neurons'], activation=args['activation'],
                        layer_types=args['layer_types'], dropout_rate=args['dropout_rate'],
                        n_feats=data.shape[1], n_cats=n_cats, logger=logger)

    model.summary()
    # Fit model and compute predictions
    model.fit(data, one_hot_labels, epochs=args['n_epochs'])
    y_preds = model.predict(test_data)

    # Log and print MSE to stdout
    logger.info("Test MSE is: {}".format(softmax_mse(one_hot_test, y_preds)))
    print("Test MSE is: {}".format(softmax_mse(one_hot_test, y_preds)))

    if args['output']:
        with open(args["output"], 'wb') as handle:
            pickle.dump(model, handle)
