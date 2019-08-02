# Source folder

April 2018

This folder contains all the source code

### **Structure of this folder**

```
├── model        				<- Store all functions to perform modelling
│   │
│   ├── extract_sentiment.py			
│   ├── extract_topic.py     
│   ├── keras_model.py
│   └── prototype_model.py
│
│
├── Preprocessing     			<- Store all functions to perform preprocessing steps
│   │
│   ├── financial_cols.csv
│   ├── financial_sentiment_cols.csv
│   ├── financial_sentiment_topic_cols.csv     
│   ├── financial_topic_cols.csv
│   ├── vol_financial_cols.csv
│   ├── vol_financial_sentiment_cols.csv
│   ├── vol_financial_sentiment_topic_cols.csv
│   ├── vol_financial_topic_cols.csv
│   ├── sentiment_cols.csv
│   ├── sentiment_topic_cols.csv            
│   └── topic_cols.csv
│
├── Scripts   				  <- Store all scripts to run on the server
│   │
│   ├── test_years.csv
│   ├── train_years.csv
│   └── val_year.csv
│
├── fillings_count_sql_query     <- Query wrote to obtain information from SQL database
├── structures.py            	<-Define Filing object and function filing_to_mongo
└── utils.py           		    <- Store all utilities functions




```

### Links to files in this folder

|Folder|Description|Files|
| :---:|  :---:    |:---:|
|Models| Store all functions to perform modelling|[extract_sentiment.py](models\extract_sentiment.py) <br> [extract_topic.py](models\extract_topic.py) <br> [keras_model.py](models\keras_model.py) <br> [prototype_model.py](models\prototype_model.py)  |
|Preprocessing| Store all functions to perform preprocessing steps | [feature_aggregation.py](preprocessing\feature_aggregation.py) <br> [label_feature_eng.py](preprocessing\label_feature_eng.py) <br> [subset_data.py](preprocessing\subset_data.py) <br> [text_extract.py](preprocessing\text_extract.py) |
|Scripts| Store all scripts to run on the server | [common_cik_script.py](scripts\common_cik_script.py) <br> [common_col_script](scripts\common_col_script.py) <br> [create_financial_features_script](scripts\create_financial_features_script.py) <br> [create_label_script](scripts\create_label_script.py) <br> [extract_cik_script](scripts\extract_cik_script.py) <br> [extract_filings_script](scripts\extract_filings_script.py) <br> [extract_sentiment_script](scripts\extract_sentiment_script.py) <br> [extract_uniq_col_script](scripts\extract_uniq_col_script.py) <br> [keras_nn_script](scripts\keras_nn_script.py) <br> [merge_features_script](scripts\merge_features_script.py) <br> [subset_data_script](scripts\subset_data_script.py) <br>  [topic_modelling_script](scripts\topic_modelling_script.py) <br> [train_model_script](scripts\train_model_script.py)|
|[fillings_count_sql_query](fillings_count_sql_query.md)|Query wrote to obtain information from SQL database| |
|[structures.py](structures.py)|Define Filing object and function filing_to_mongo| |
|[utils.py](structures.py)|Store all utilities functions| |
