## Sauder School of Business - Capstone Project Proposal
Ted Thompson

### 1.1 Problem Statement

The UBC Sauder School of Business group has a large database from the U.S. Securities and Exchange Commission (SEC) fillings, Wharton financial fundamental data, and stock price history. In this project, we seek to build a framework to leverage SEC filings for obtaining industry intelligence. Specifically, we are given two prediction problems: classification of firm survival and predicting firm performance.



### 1.2 The Data

###### SEC Filings
* Raw data includes: 11.7 M filings, 532K entities (American firms and investors) in 24K cities

* 164K parsed [10-K](https://en.wikipedia.org/wiki/Form_10-K)  filings in MongoDB
* More than 14,000 of these companies have multiple (>3) filings in the period.
* Includes information about the company itself such as sector, as well as discussion by management about risks in the coming year, legal proceedings, and executive compensation among other things. [SEC 10-K Item Descriptions](https://www.sec.gov/fast-answers/answersreada10khtm.html)

###### CRSP Data
* The stock prices data comes from the [Center for Research in Security Prices](https://en.wikipedia.org/wiki/Center_for_Research_in_Security_Prices).
* 64 features of daily frequency with time range from January 1995 to December 2017

###### Compustat Data
* Time range from January 1995 to March 2018
* 645 features contain information from financial statements on a yearly and quarterly basis.

##### Difficulties posed by the data

- Several huge databases stored in different places
  - Need to create workflows to combine these and incorporate all data into our models
- Data of different frequencies (daily, monthly, quarterly, annually)
  - Determine the frequency of predictions we would like to make

### 1.3 Final Data Product

#### Scientific Objectives


From the available data, it will be more challenging to predict firm survival due to inadequate information on bankruptcy. Our group decided to start with the second proposed problem: prediction of firm performance using stock prices as a proxy. To begin with, we will specify this as a discrete problem, classifying whether a firms stock price will go up, go down, or remain flat relative to the previous period. At first, using EDA along with our domain knowledge, we expect to narrow down the number of features and observations used. From there, we will construct features based on the textual data from SEC filings and financial fundamental data to use in our predictive models.


#### Deliverables

The final data product will consist of three main points:

1. a data pipeline making our analysis reproducible
2. a set of features extracted from the text data we've been given
3. a written report documenting our findings throughout the project


The data pipeline will be made up of multiple components: cleaning and tidying the data, performing the feature extraction from SEC filings, integrating these features with our data from Wharton Research Data Services, fitting and evaluating our models.


The set of features extracted from the text will form part of the pipeline. In addition, we will provide scripts to allow these techniques to be performed on additional inputs in the future so that they can be used in future research.

Finally, if time permits we will consider the idea of creating a visual dashboard using [Plotly Dash](https://dash.plot.ly/gallery) to explore some patterns in our features.  We believe that when using abstract methods such as deep learning, this dashboard will help interpretation easier and visualizing useful clusters in our extracted features will help to communicate their usefulness.

### 1.4 Data Science Techniques

##### Feature and Model Selection
- Using exploratory data analysis (EDA) to find any multicollinearity in order to exclude features that are highly correlated to other features.
- Basic models to cluster the data such as [`kmeans`](https://en.wikipedia.org/wiki/K-means_clustering).
- Domain knowledge to make educated choices on selecting which financial metrics to include as features.

##### NLP


* Topic Analysis
  - We will use [LDA](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) to try and model the topics found in each of the items from the SEC filings.

* [Sentiment Analysis](https://en.wikipedia.org/wiki/Sentiment_analysis)
  - We will fit a Logistic Regression model and extract the distribution of coefficients to detect positive or negative sentiments from the text data.
  - We feel that sentiment on items relating to risks faced by a company or performance over the last year may be useful to determine how management feels about the company's prospects moving forward.

* Embeddings:
  -[Word2Vec](https://en.wikipedia.org/wiki/Word2vec)/[GloVe](https://www.aclweb.org/anthology/D14-1162)/[FastText](https://fasttext.cc/) vectors to give contextual information to words.

  - Use these word embeddings to form item embeddings summarizing each of the 'items' in a 10-K filing. We can then compare these embedded vectors between firms.

##### Classification/Regression

* Combining selected financial metrics and features derived from the NLP techniques above, we can use some basic regression to start with, then moving forward more complicated models such as [random forests](https://en.wikipedia.org/wiki/Random_forest), or neural networks.


### 1.5 Timeline and Evaluation

##### Milestone 1: April 25th - May 2nd
- Start cleaning data and building pipeline
- Baseline predictions using selected Wharton data

##### Milestone 2: May 2nd - May 9th
- Begin to extract features from SEC filings by implementing LDA for Topic Modeling
- Second iteration of model: Adding SEC data and using NLP

##### Milestone 3:  May 9th - May 18th
- Third iteration of model: Improving upon current model using insights gained from previous milestones

- Extract more features from SEC filings using sentiment analysis

- If we decide do a Dashboard, start working on it at some point within this milestone.

##### Milestone 4: May 18th - May 26th
- Fourth iteration of model: Improving upon current model using insights gained from previous milestones
- Extract more features from SEC Filings using word/Item embeddings

##### Milestone 5: May 26th - June 4th
- Final presentation
- Final report
