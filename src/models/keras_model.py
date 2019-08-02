import numpy as np
from keras.models import Sequential
from keras.layers import BatchNormalization
from keras.layers.core import Dense, Dropout


def build_keras(n_layers, n_neurons, activation, n_feats, n_cats,
                layer_types=None, dropout_rate=0.2,
                loss="categorical_crossentropy", optimizer='adam', logger=None):  # Tested [N]
    """
    Builds and compiles a fully-connected neural network model using Keras

    Args:
        n_layers (int): Number of hidden layers to include in the network.
                        Dropout layers are included in number of layers.
        n_neurons (list): Number of neurons in each hidden layer.
                          Argument should be either size `n_layers`, or if `layer_types` specified,
                          the number of dense layers.
        activation (list or str): Activation functions to use at each layer.
                                   If a string is supplied, that activation will be used at each layer
                                   except for the output layer, which will always use softmax.
        n_feats (int): Number of features in the input data. Required to set input_shape
        n_cats (int): Number of categories in the target labels. Required to set output layer.
        layer_types(list): Default=None. List of strings for each layer desired.
                           Currently, only Dropout and Dense layers are supported.
                           If None, all layers are set to Dense.
                           If passed, the list should be size `n_layers - 1`
        dropout_rate (int): Default=0.2. Determines dropout rate for potential dropout layers.
                            Currently only a single value is supported.
        loss (str): Loss function to use when compiling the model.
                    Will be used by the optimizer during training to determine fit
        optimizer (str): Optimizer to use in training the model.
        logger (Logger): Logger object from the Logging package which has already been configured.
                         If None, no logging is performed.

    Returns:
        (keras.model) Compiled model containing the desired Dense layers.
                      After this, just needs to be fit with training/test data
    """

    model = Sequential()
    model.add(BatchNormalization())
    model.add(Dense(n_neurons[0], activation=activation[0], input_shape=(n_feats, )))
    if logger:
        logger.info("Added the first hidden layer with "
                    "{} neurons, and a(n) {} activation function. There are {} input neurons".format(n_neurons[0],
                                                                                                     activation[0],
                                                                                                     n_feats))
    if not layer_types:  # If only dense layers are desired
        for i in range(1, n_layers):  # Adds each of the desired layers
            if len(activation) == 1:
                act = activation[0]
            else:  # Allows for different activations to be specified at different layers
                act = activation[i]

            model.add(Dense(n_neurons[i], activation=act))

            if logger:
                logger.info("Added dense layer with {} neurons and a(n) {} activation function".format(n_neurons[i],
                                                                                                       activation))
    else:
        dense_counter = 0  # For determining how many neurons in this dense layer
        for i in range(1, n_layers):
            if len(activation) == 1:
                act = activation[0]
            else:  # Allows for different activations to be specified at different layers
                act = activation[dense_counter]

            if layer_types[i - 1] == "dense":
                model.add(Dense(n_neurons[dense_counter], activation=act))
                if logger:
                    logger.info("Layer {} is a dense layer "
                                "with {} neurons and a(n) {} activation function".format(i,
                                                                                         n_neurons[i],
                                                                                         act))
                dense_counter += 1
            elif layer_types[i - 1] == "dropout":
                model.add(Dropout(dropout_rate))

    model.add(Dense(n_cats, activation='softmax'))  # Final output layer with n_cats output neurons

    if logger:
        logger.info("Added the output layer with {} output neurons using a softmax activation".format(n_cats))

    model.compile(loss=loss, optimizer=optimizer)

    if logger:
        logger.info("Model successfully compiled")

    return model
