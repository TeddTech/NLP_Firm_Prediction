## Makefile

## Ted Thompson

# Run top to bottom, culminating in the final dataframe with all features.
# From here, you could choose any of the models in the final block of rules to train.
# Working [Y]
all: merge_all

# Working [Y]
required_modules:
	pip install -r requirements.txt


##-------------------------- Financial Features ------------------------------##
## Subsets the data according to desired columns & companies.
### Note: Place your data files in the /data/ directory and name them accordingly.

# Exctract unique CIK from Compustat data: Working [Y]
# Note that it uses the original files located in the /data1/wrds/ location.
data/cik_list_compustat.csv: src/scripts/extract_cik_script.py /data1/wrds/compustat_199501-201803.csv
	python src/scripts/extract_cik_script.py /data1/wrds/compustat_199501-201803.csv data/preprocessing/compustat_cik_list.csv

# Extract unique ticker info from CRSP and Compustat: Working [Y]
data/compustat_ticker_list.csv: src/scripts/extract_uniq_col_script.py /data1/wrds/compustat_199501-201803.csv
	python src/scripts/extract_uniq_col_script.py /data1/wrds/compustat_199501-201803.csv "tic" "character" data/preprocessing/compustat_ticker_list.csv

# Extracts unique tickers from CRSP data: Working [Y]
data/crsp_ticker_list.csv: src/scripts/extract_uniq_col_script.py /data1/wrds/crsp_199501-201712.csv
	python src/scripts/extract_uniq_col_script.py /data1/wrds/crsp_199501-201712.csv "TICKER" "integer" data/preprocessing/crsp_ticker_list.csv

# Compare CIKs from data sources to narrow down companies: Working [Y]
data/common_cik_list.csv: src/scripts/common_cik_script.py data/preprocessing/CIK_edgar.csv data/preprocessing/cik_list_compustat.csv
	python src/scripts/common_cik_script.py data/preprocessing/CIK_edgar.csv data/preprocessing/cik_list_compustat.csv data/preprocessing/common_cik_list.csv

# Compare Tickers from data sources to narrow down companies: Working [Y]
data/common_ticker_list.csv: src/scripts/common_col_script.py data/preprocessing/compustat_ticker_list.csv data/preprocessing/crsp_ticker_list.csv
	python src/scripts/common_col_script.py data/preprocessing/compustat_ticker_list.csv "tic" data/preprocessing/crsp_ticker_list.csv "TICKER" data/preprocessing/common_ticker_list.csv -ct=str

# Create subset of compustat data based on the above common lists: Working [Y]
data/compustat_subset.csv: src/scripts/subset_data_script.py /data1/wrds/compustat_199501-201803.csv data/preprocessing/common_cik_list.csv data/preprocessing/compustat_selected_cols.csv
	python src/scripts/subset_data_script.py /data1/wrds/compustat_199501-201803.csv cik str data/preprocessing/compustat_selected_cols.csv data/preprocessing/common_cik_list.csv data/compustat_subset.csv
	rm temp.csv

# Create subset of CRSP data based on the above common lists: Working [Y]
subset_crsp: src/scripts/subset_data_script.py /data1/wrds/crsp_199501-201712.csv data/preprocessing/common_ticker_list.csv data/preprocessing/crsp_selected_cols.csv
	python src/scripts/subset_data_script.py /data1/wrds/crsp_199501-201712.csv TICKER str data/preprocessing/crsp_selected_cols.csv data/preprocessing/common_ticker_list.csv data/crsp_subset.csv
	rm temp.csv

# Create a number of fundamental financial features and ratios: Working [Y]
create_financial_features: src/scripts/create_financial_features_script.py data/feat_eng/to_diff.csv data/feat_eng/to_sub.JSON data/feat_eng/to_ratio.json
	python -W ignore src/scripts/create_financial_features_script.py data/compustat_subset.csv cik data/compustat_processed.csv --toDifference=data/feat_eng/to_diff.csv --toSubtract=data/feat_eng/to_sub.json --toRatio=data/feat_eng/to_ratio.json --diffpct=True

# Create labels on the financial dataset, currently down/flat/up (0,1,2): Working [Y]
create_labels: src/scripts/create_label_script.py data/compustat_subset.csv data/compustat_processed.csv
	python -W ignore src/scripts/create_label_script.py data/compustat_processed.csv data/compustat_labelled.csv

##----------------------------- Text Features --------------------------------##

# Extract valid documents from MongoDB and store objects in a pickle: Working [Y]
extract_filings: src/scripts/extract_fiings_script.py data/common_cik_list.csv
	python src/scripts/extract_fiings_script.py 127.0.0.1 27017 "cik" "str" data/preprocessing/common_cik_list.csv data/filings_list.pickle

# Extract topics from Item 1 and Item 7 (Tuning can be done here by changing the items/number of topics): Working [Y]
topic_modelling: extract_filings src/scripts/topic_modelling_script.py data/filings_list.pickle
	python src/scripts/topic_modelling_script.py data/filings_list.pickle "cv_lda" 1 30 data/item_1_30_topic_features.csv
	python src/scripts/topic_modelling_script.py data/filings_list.pickle "cv_lda" 7 10 data/item_7_10_topic_features.csv

# Perform sentiment analysis on Item 1 and Item 7: Working [Y]
sentiment_analysis: extract_filings src/scripts/extract_sentiment_script.py data/filings_list.pickle
	python src/scripts/extract_sentiment_script.py data/filings_list.pickle data/sentiment_scores.csv -p item1 item7 -s item1 item7 -c item1 item7


##---------------------------- Final Preprocessing ---------------------------##
# Merge the topic features into a single file: Working [Y]
## Note that if file names above are changed, you should update the names here too
merge_topics: topic_modelling src/scripts/merge_features_script.py data/item_1_30_topic_features.csv data/item_7_10_topic_features.csv
	python merge_features_script.py data/item_1_30_topic_features.csv data/item_7_10_topic_features.csv data/topic_features.csv -m cik period


# Merge the sentiment features and the topic modelling features: Working [Y]
merge_text: merge_topics sentiment_analysis src/scripts/merge_features_script.py data/sentiment_scores
	python merge_features_script.py data/sentiment_scores data/topic_features text_features.csv -m cik period

# Merge the text features with the financial features: Working [Y]
merge_all: merge_text create_labels data/compustat_labelled.csv data/text_features.csv
	python merge_features_script.py data/compustat_labelled.csv data/topic_features.csv merged_features.csv -m cik period

# Create train-test split along year lines.
train_test_split: merge_all src/scripts/year_split_script.py data/train_years.csv data/test_years.csv data/merged_features.csv
	python src/scripts/year_split_script.py data/merged_features.csv fyear str data/tt_split/train_years.csv data/train.csv
	python src/scripts/year_split_script.py data/merged_features.csv fyear str data/tt_split/test_years.csv data/test.csv
	python src/scripts/year_split_script.py data/merged_features.csv fyear str data/tt_split/val_years.csv data/val.csv


##----------------------------- Train Models ---------------------------------##
# Train one of the specified classical machine learning models. Default is Logistic Regression
## All of the columns in the files passed to -feats can and should be changed to suit your model.
### If you do, be sure to update the required files in the rule definition above.

# Financial_only
train_fin: train_test_split src/scripts/train_model_script.py data/train.csv data/test.csv data/model_features/financial_cols.csv
	python src/scripts/train_model_script.py data/train.csv data/test.csv "label" "LR" results/fin_model_result.pickle -feats=data/model_features/financial_cols.csv

# Financial and Sentiment
train_fin_sent: train_test_split src/scripts/train_model_script.py data/train.csv data/test.csv data/model_features/financial_sentiment_cols.csv
	python src/scripts/train_model_script.py data/train.csv data/test.csv "label" "LR" results/fin_sent_model_result.pickle -feats=data/model_features/financial_sentiment_cols.csv

# Financial and Topics
train_fin_topic: train_test_split src/scripts/train_model_script.py data/train.csv data/test.csv data/model_features/financial_topic_cols.csv
	python src/scripts/train_model_script.py data/train.csv data/test.csv "label" "LR" results/fin_topic_model_result.pickle -feats=data/model_features/financial_topic_cols.csv

# Financial and all text features
train_fin_sent_topic: train_test_split src/scripts/train_model_script.py data/train.csv data/test.csv data/model_features/financial_sentiment_topic_cols.csv
		python src/scripts/train_model_script.py data/train.csv data/test.csv "label" "LR" results/fin_sent_topic_model_result.pickle -feats=data/model_features/financial_sentiment_topic_cols.csv

train_all: train_fin train_fin_sent train_fin_topic train_fin_sent_topic

# Financial_only
neural_net_fin: train_test_split src/scripts/keras_nn_script.py data/model_features/financial_cols.csv
	python keras_nn_script.py train.csv test.csv label -nl 2 -nn 50 100 -a relu sigmoid -l=categorical_crossentropy -opt=adam -n_epochs=10 -feats=data/model_features/financial_cols.csv

# Financial and Sentiment
neural_net_fin_sent: train_test_split src/scripts/keras_nn_script.py data/model_features/financial_cols.csv
	python keras_nn_script.py train.csv test.csv label -nl 2 -nn 50 100 -a relu sigmoid -l=categorical_crossentropy -opt=adam -n_epochs=10 -feats=data/model_features/financial_sentiment_cols.csv

# Financial and Topics
neural_net_fin_topic: train_test_split src/scripts/keras_nn_script.py data/model_features/financial_topic_cols.csv
	python keras_nn_script.py train.csv test.csv label -nl 2 -nn 50 100 -a relu sigmoid -l=categorical_crossentropy -opt=adam -n_epochs=10 -feats=data/model_features/financial_topic_cols.csv

# Financial and all text features
neural_net_fin_sent_topic: train_test_split src/scripts/keras_nn_script.py data/model_features/financial_sentiment_cols.csv
	python keras_nn_script.py train.csv test.csv label -nl 2 -nn 50 100 -a relu sigmoid -l=categorical_crossentropy -opt=adam -n_epochs=10 -feats=data/model_features/financial_sentiment_topic_cols.csv

neural_net_all: neural_net_fin neural_net_fin_sent neural_net_fin_topic neural_net_fin_sent_topic
