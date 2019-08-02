# Scripts

This directory holds the scripts which allow automated execution of this project.

Below is a table describing each of the scripts along with their arguments if you wish to run them manually.

The root directory also includes a Makefile which further automates the pipeline. The documentation for the Makefile can be found [here](../../doc/make_docs.md)

All scripts also have optional arguments `--loggingLevel` which determines what logging messages to save, and `--loggingPath` which will set a path to save log files

|Script Name|Purpose|Required Args|Optional Args|Output|
|:-:|:-:|:-:|:-:|:-:|
|`extract_cik_script.py`|Determine all unique identifiers (CIK) from each dataset|input (.csv):  Path to data with the `cik`column (e.g. Compustat Data ) <br> <br> output (.csv): Path to desired location for the unique CIK list in .csv format|N/A|`.csv` file containing newline separated CIKs found in the dataset|
|`extract_uniq_col_script.py`|Generic version of the above script, used to extract unique tickers in the pipeline|input_file (csv):  Data with the `TICKER` column <br> <br> column_name (str): Column name to extract <br> <br> column_type (str): Column type. It accepts following values (int, str or float).<br> <br> output (.csv): Path to desired location for the unique col list in .csv format|N/A|`.csv` file containing newline separated unique values of the specified columns|
|`common_cik_script.py`|Compares the lists of previously generated CIKs to find the ones the datasets have in common|edgar (.csv): Path to unique CIK list from Edgar data <br> <br> compustat (.csv): Path to unique CIK list from Compustat data <br> <br> output (.csv): Path to desired location for the common CK list in .csv format|N/A|`.csv` file containing the newline separated CIKs which occur in both of the input datasets|
|`common_col_script.py`|Generic version of the above script, used when something other than CIK is to be compared|f1(csv): Path to input file 1 <br> <br> f1_col(str): Column from input file 1 to compare <br> <br> f2(csv):  Path to input file 2 <br> <br> f2_col(str): Column from input file 2 to compare <br> <br> output (.csv): Path to desired location for the common col list in .csv format|columnType  : Type of the column where an intersection is being determined|`.csv` file containing the newline separated values of the specified column which occur in both of the input datasets|
|`subset_data_script.py`|Subsets a dataset according to desired columns file and a valid unique identifier file|input_file (csv) : Path to original compustat data <br> <br> uid (str) : Unique identifier of firm. Examples: "cik", "tic" <br> <br> uid_type (str) : The data type of the the uid selected. Examples: "int", "str" <br> <br> column_names (str) : Path to column name file <br> <br> uid_list (str) : Path to common UID list <br> <br> output (.csv): Path to desired location for the data subset in .csv format|N/A|`.csv` file containing a subset of the input data according to the passed columns and valid UIDs|
|`create_financial_features_script.py`|Performs some feature engineering on the financial dataset to create ratios, compute volatility and perform differencing among other actions.|input (.csv) : Path to the input data which is in .csv format <br> <br> uid (str): Unique identifier for the passed .csv. Should be convertible to a string. <br> <br> output (.csv): Deisred path to save the output .csv with created features.|toDifference (.csv): Path to a .csv file containing the names of columns to perform first differencing. <br> <br> toSubtract (.json): Path to a .json file with the following schema:                      {'new_col_name": (col_to_subtract, col_being_subtracted)} <br> <br> toRatio (.json): Path to a .json file with the following schema: {'new_col_name": ("numerator_col_name", "denominator_col_name")} <br> <br> diffpct(bool): Default=True. Determines whether or not diff_col should also compute percentages. <br><br> crsp (str): Path to a file containing CRSP data. If passed, will also compute volatility|`.csv` file containing the post-engineering feature set|
|`create_label_script.py`|Creates 'up', 'down', 'flat' labels from a price series| input_file (csv) : Path to the subset of compustat data
 <br> <br> output(csv) Path to desired location for the labelled data in .csv format||`.csv` file containing the dataset with created labels|
|`extract_filings_script.py`|Extract the SEC filings from MongoDB into a Python object for manipulation in further scripts|host (str)  : Hostname of computer server that stores the database <br> <br> port (str)  : SSH port of computer server that stores the database<br><br> uid (str) : Unique identifier of firm. Examples: "cik", "tic"<br><br> uid_type (str) : The data type of the the uid selected. Examples: "int", "str"<br><br> valid_uids (str) : Path to common UID list|N/A|.pickle file containing a list of Filing() objects which hold the information from each filing.|
| `topic_modelling_script.py` | Extract topics from selected item of SEC filings | f1: Python Object containing a list of Filings <br> <br> model:  Type of topic modelling method that user want to use <br> <br> item_num:  Item from filing object that user want to perfrom topic modelling on <br> <br> topic_number:  Number of topic user wants to extract <br> <br> outputFile: Path to save the dataframe with CIK, period and topic weights of each document | stop_word_list:  Path to list of stopword <br> <br> save_model:  Option to also return the model (default is False) <br> <br> save_feature:  Option to also return feature (default is False) <br> <br> random_state:  Default=None. Fix the random state of the LDA model <br> <br> model_path: Path to save the model in pickle <br> <br> feature_path: Path to save the feature in pickle | A data frame with  CIK, Period and topic weight for each topic \n Topic Modelling (if choose to save) <br> <br> Corpus/ Text frequency (if choose to save) ||`merge_features_script.py`||||`.csv` file containing the merged dataframes|
|`keras_nn_script.py`|Build and compile a fully-connected neural network model using Keras|input_tr (.csv):  Path to CSV file containing the training data <br><br>input_test (.csv): Path to CSV file containing the test data <br><br>labels (str): Name of the label column in the training and test set. Must be the same in both.|n_layers (int): Number of hidden layers to include in the network. Dropout layers are included in number of layers. <br><br>n_neurons (list): Number of neurons in each hidden layer. Argument should be either size `n_layers`, or if `layer_types` specified, the number of dense layers. <br><br>activation (list or str): Activation functions to use at each layer. If a string is supplied, that activation will be used at each layer except for the output layer, which will always use softmax.  <br><br>layer_types (list or None): Default=None. List of strings for each layer desired. Currently, only Dropout and Dense layers are supported. If None, all layers are set to Dense. If passed, the list should be size `n_layers - 1` <br><br> dropout_rate (int): Default=0.2. Determines dropout rate for potential dropout layers. Currently only a single value is supported. <br><br>loss (str): Loss function to use when compiling the model. Will be used by the optimizer during training to determine fit <br><br> optimizer (str): Optimizer to use in training the model. <br><br> n_epochs (int): Number of epochs to train for. Currently, early stopping is not implemented, so this should be conservative at first. <br><br> desired_features (str): Path to a .csv file containing all desired features.|`.pickle` file for the model|
|`merge_feaures_script.py`|Merges two `.csv` files on shared columns. Used for combining text and numeric features into a single file.|f1(.csv): Path to the .csv containing the left DataFrame<br><br>f2(.csv): Path to the .csv containing the right DataFrame<br><br> output (.csv): Path to desired output file|merge_on (str or list of str): Default="0". Column names to merge on.Can pass multiple space separated arguments|`.csv` file containing the merged DataFrames|
|`train_model_script`|Train classical machine learning models and return the model output as well as log accuracy|input_tr (.csv)     : Path to CSV file containing the training data<br><br>input_test (.csv)   : Path to CSV file containing the test data<br><br>labels (str)        : Name of the label column in the training and test set. Must be the same in both.<br><br>model (str)         : Name of the model user want to train the data. Possible values are:<br> <br>- LR (Logistic Regression),<br>- RFC (Random Forest Classifier),<br>- KNN (K Neighbors Classifier)<br> - SVM (Support Vector Machine)|desired_features (str): Defult = None. Path to CSV file containing all features name that will be used as predictors|`.pickle` file for the model|
|`year_split_script.py`| Due to the nature of financial data, we do not want to create a train/test split randomly in the standard way. We instead want to use only information from the past in our future predictions. We do so by splitting on year. This script will be run twice, once to extract the training set and again to extract the test set.|input_file (csv) : Path to original compustat data <br><br>year_col (str) : Column name for the year in the dataset <br><br>year_type (str) : The data type of the the uid selected. Examples: "int", "str" <br><br> year_list (str) : Path to the list of desired years|N/A|`.csv` file for the splitted data|
|`lda_viz_script.py`| Script to visualize the topic using interactive pyLDAvis image for specified topic modeling option (gensim, cv_lda)|f1 (.pickle)        :  Python Object containing a list of Filings (e.g. filings_list.pickle)<br><br>model (str):  Type of topic modelling method that user want to use. Possible values are:  ["gensim", "cv_lda","tfidf_nmf"] <br><br>item_num(int):  Item from filing object that user want to perfrom topic modelling on<br><br> topic_number(int):  Number of topic user wants to extract|stop_word_list(path):  Path to list of stopword <br><br>save_model(bool) :  Option to also return the model (default is False)<br><br>save_feature(bool)  :  Option to also return feature (default is False) <br><br>random_state(int)   :  Default=None. Fix the random state of the LDA model.| outputFile(csv): Path to save the dataframe with CIK, period and topic weights of each document. <br><br>model_path(pickle): Path to save the model in pickle feature_path(pickle): Path to save the feature in pickle |