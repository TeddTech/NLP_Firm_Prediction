# Lab Diary

Observation selected: 500 randomly selected companies

Feature selected: "atq", "ceqq", "dlttq", "niy"

| Date   | Experiment                | Result          | Hyper          | Note               |
| ------ | ------------------------- | --------------- | -------------- | ------------------ |
| 5/1/18 | Logistic Regression       | TR = 42;TS = 41 | C = 0.1        | use Score function |
| 5/1/18 | Random Forest             | TR= 97;TS=40    | Base model     | use Score function |
| 5/2/18 | Support Vector Classifier | TR= 95;TS=42    | Base model     | use Score function |
| 5/2/18 | K Nearest Neighbor        | TR= 60;TS=39    | Base model     | use Score function |
| 5/2/18 | Support Vector Classifier | TR= 98;TS=42    | C = 100        | Accuracy           |
| 5/2/18 | 1 hidden layer NN         | TR= 31;TS=33    | Base model     | Accuracy           |
| 5/2/18 | Neural Network            | TR= 41;TS=43    | max_iter = 10k | accuracy           |
| 5/2/18 | NN                        | TR= 43;TS=46    | max_iter = 50k | Accuracy           |
|        |                           |                 |                |                    |



- Use the same way to calculate score function

### Making differencing between those features above

Observation selected: 500 randomly selected companies

Feature selected: "delta_pct_atq", "delta_pct_ceqq", "delta_pct_dlttq", "delta_pct_niy"

| Date   | Experiment                | Result       | Hyper                                    | Note     |
| ------ | ------------------------- | ------------ | ---------------------------------------- | -------- |
| 5/2/18 | K Nearest Neighbor        | TR= 61;TS=44 | Base model                               | Accuracy |
| 5/2/18 | Logistic Regression       | TR= 40;TS=41 | C = 0.01,multi_class= 'multinomial',solver ='sag' | Accuracy |
| 5/2/18 | Random Forest             | TR= 98;TS=41 | Base model                               | Accuracy |
| 5/2/18 | Support Vector Classifier | TR= 57;TS=42 | C = 100                                  | Accuracy |
| 5/2/18 | Neural Network            | TR= 44;TS=42 | max_iter = 50k                           | accuracy |
|        |                           |              |                                          |          |



--> This is probably all it can learn from these features.

### New set of features, randomly selecting 500 companies:
['delta_pct_revty', 'delta_pct_cogsy', 'delta_pct_xrdy', 'delta_pct_xsgay', 'delta_pct_xopry', 'delta_pct_xinty', 'delta_pct_piy', 'delta_pct_txty' 'delta_pct_niy', 'delta_pct_dlttq', 'delta_pct_invtq', 'gpmgn', 'opmgn', 'npmgn', 'pe', 'd_to_ebitda', 'gpft', 'ebitda', 'fyearq', 'cik']

| Date   | Experiment                | Result                   | Hyper                                    | Note     |
| ------ | ------------------------- | ------------------------ | ---------------------------------------- | -------- |
| 5/8/18 | K Nearest Neighbor        | TR= 61.111;TS=48.1481    | Base model                               | Accuracy |
| 5/8/18 | Logistic Regression       | TR= 59.2593;TS=55.5556   | C = 0.01,multi_class= 'multinomial',solver ='sag' | Accuracy |
| 5/8/18 | Random Forest             | TR= 98.1481;TS=59.2593   | Base model                               | Accuracy |
| 5/8/18 | Support Vector Classifier | TR= 100;TS=55.5556       | C = 100                                  | Accuracy |
| 5/2/18 | Neural Network            | TR= 33.333333;TS=37.0370 | max_iter = 50k                           | accuracy |
|        |                           |                          |                                          |          |


### Same set of features as above, with companies selected according to `np.random.seed(1234)``
| Date   | Experiment                | Result                 | Hyper                                    | Note     |
| ------ | ------------------------- | ---------------------- | ---------------------------------------- | -------- |
| 5/8/18 | K Nearest Neighbor        | TR= 61.125;TS=39.5000  | Base model                               | Accuracy |
| 5/8/18 | Logistic Regression       | TR= 51.125;TS=51.5000  | C = 0.01,multi_class= 'multinomial',solver ='sag' | Accuracy |
| 5/8/18 | Random Forest             | TR= 99.000;TS=45.500   | Base model                               | Accuracy |
| 5/8/18 | Support Vector Classifier | TR= 100;TS=51.0000     | C = 100                                  | Accuracy |
| 5/2/18 | Neural Network            | TR= 51.2500;TS=52.0000 | max_iter = 50k                           | accuracy |



## Topic extraction exploration

| Date    | Experiment                               | Hyper                                    | Result                                   |
| ------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| 5/14/18 | Using gensim.lda to extract topic        | n_topic = 28, n_filing = 500, stopword = eng + exclude numbers | topics are overlaping                    |
| 5/15/18 | Using gensim.lda to extract topic        | n_topic = 10, n_filing = 500, stopword = eng + exclude numbers | topics are less overlapping but words distribution are bad. |
| 5/17/18 | CountVectorizer + LatentDirichletAnalysis | n_topic = 10, n_filing = 1000, stopword = eng, max_df = 0.8, min_df = 2 | Topics looks better with related words, but there are still many topics share same words. |
| 5/17/18 | CountVectorizer + LatentDirichletAnalysis | n_topic = 10, n_filing = 1000, stopword = eng, max_df = 0.5, min_df = 5 | Topics looks much better with related words, within topics but different between topics |
| 5/17/18 | TfidfVectorizer + NMF model (Frobenius norm) | n_filing = 1000, stopword = eng, max_df = 0.95, min_df = 2; NMF(n_components=10, random_state=1,alpha=.1, l1_ratio=.5) | The result are similar to the one above. Topics are better and different from each other. Topic 0 and 2 are not good. |
| 5/17/18 | TfidfVectorizer + NMF model (generalized Kullback-Leibler divergence) | n_filing = 1000, stopword = eng, max_df = 0.95, min_df = 2; NMF(n_components=10, random_state=1,beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,l1_ratio=.5) | Result not good with lots of non-related words within topics. |
| 5/17/18 | TfidfVectorizer + NMF model (generalized Kullback-Leibler divergence) | n_filing = 1000, stopword = eng, max_df = 0.5, min_df = 5; NMF(n_components=10, random_state=1,beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,l1_ratio=.5) | Result is still not good with lots of non-related words within topics. |
|         |                                          |                                          |                                          |
|         |                                          |                                          |                                          |

