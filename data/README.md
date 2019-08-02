# Data folder

April 2018

MDS Capstone Project- SEC Filing Analytics for U.S. Industry Intelligence



**Faculty members:**

·      Hasan Cavusoglu ([cavusoglu@sauder.ubc.ca](mailto:cavusoglu@sauder.ubc.ca))

·      Gene Moo Lee ([gene.lee@sauder.ubc.ca](mailto:gene.lee@sauder.ubc.ca))

System administrator / graduate research assistant:

·      Victor Song ([victor.xpsong@gmail.com](mailto:victor.xpsong@gmail.com))



**Compute Server:**

·      Hostname: misr.sauder.ubc.ca

·      SSH Port: 16800

·      User accounts will be provided by individual emails



**MySQL Access via phpMyAdmin:**

·      <http://misr.sauder.ubc.ca/phpmyadmin>  

·      User accounts will be provided by individualemails



**Data Sets**

| Data                 | Description                             | Location                                 |
| -------------------- | --------------------------------------- | ---------------------------------------- |
| SEC  EDGAR meta data | File  ID, Filing type, Company ID, etc. | misr’s  MySQL (db name: edgar_mds)       |
| SEC  EDGAR raw data  | Unparsed  HTML/text files               | misr:/var/opt/mds/data/edgar_raw         |
| 10-K  parsed data    | Items  and Parts are parsed             | misr’s  MongoDB                          |
| Compustat            | Accounting/Finance  Data (licensed)     | misr:/var/opt/mds/data/wrds/compustat_199501-201803.csv |
| CSRP                 | Stock  Price Data (licensed)            | misr:/var/opt/mds/data/wrds/crsp_199501-201712.csv |



### **Structure of this folder**

```
├── preprocessing        <- Data used for subsetting
│   │
│   ├── CIK_edgar.csv			
│   ├── cik_list_compustat.csv     
│   ├── common_cik_list.csv
│   ├── common_ticker_list.csv
│   ├── compustat_selected_cols.csv
│   ├── compustat_ticker_list.csv
│   ├── crsp_selected_cols.csv        
│   └── crsp_ticker_list.csv
│
│
├── model_features       <- Data used for features in models are contain in this directory
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
├── train_test_split     <- Data used for splitting the data 
│   │
│   ├── test_years.csv
│   ├── train_years.csv
│   └── val_year.csv
│
├── tests                <- Data used for test
│   │
│   ├── 1000_filings_for_test.pickle
│   ├── data_for_test.csv      
│   ├── fillings_for_test.json
│   └── test_texts.pkl
│
├── create_financial_feat   <- Data used to create financial features
│   │
│   ├── to_bi.csv
│   ├── to_diff.csv   
│   ├── to_ratio.json
│   └── to_sub.json
```



 ### **Files in this folder**

| File name                                | Description                              |
| ---------------------------------------- | ---------------------------------------- |
| [1000_filings_for_test](1000_filings_for_test.pickle)| List of 1000 filings for test|
| [CIK_edgar](CIK_edgar.csv)               | All CIK in Edgar database                |
| [CIK_list_compustat](cik_list_compustat.csv) | CIK list inside Compustat file       |
| [common_cik_list](common_cik_list.csv)   | List of common CIK between Compustat and CRSP data |
| [common_ticker_list](common_ticker_list.csv) | List of common ticker between Compustat and CRSP data |
| [compustat_selected_cols](compustat_selected_cols.csv) | Names of all columns needed from Compustat dataset to subset |
| [compustat_ticker_list](compustat_ticker_list.csv) | Names of all ticker needed from Compustat dataset to subset |
| [crsp_selected_cols](crsp_selected_cols.csv) | Names of all columns needed from CRSP dataset to subset |
| [crsp_ticker_list](crsp_ticker_list.csv) | Names of all ticker needed from CRSP dataset |
| [data_for_test](data_for_test.csv)       | Toy data for unit test                   |
| [filings_for_test](filings_for_test.json) | Json data for test                      |
| [final_cik_list](final_cik_list.csv)     | Final CIK common list for extracting MongoDB |
| [LM_Negative](LM_Negative.csv)           | Negative financial sentiment word        |
| [LM_Positive](LM_Positive.csv)           | Positive financial sentiment words       |
| [sentiment_scores_item1_7](sentiment_scores_item1_7.csv)|Sentiment scores for item 1 and 7|
| [test_texts](test_texts.pkl)             | Data for volatility test                 |
| [Test_years](test_years.csv)             | Years for testing data                   |
| [to_bi](to_bi.csv)                       | Columns name to use `bi()` function on   |
| [to_diff](to_diff.csv)                   | Columns name to use `diff()` function on |
| [to_ratio](to_ratio.json)                | Columns name to use `ratio()` function on|
| [to_sub](to_sub.json)                    | Columns name to use `sub()` function on  |
| [train_years](train_years.csv)           | Years for training data                  |
