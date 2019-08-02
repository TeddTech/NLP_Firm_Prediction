import pandas as pd
from time import time
from tqdm import trange
from gensim import corpora, models
from gensim.models.ldamodel import LdaModel
from src.preprocessing.text_extract import tokenize_item
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


def tfidf_nmf(filings_list, item_num, topic_number, stop_word_list, random_state=None, logger=None):  # Tested [N]
    """
    Create LDA model from a given list of filing object using TFIDF and NMF from scikit learn
    
    Args:
    
        filings_list(list)  : List of filing in Filing object
        item_num(int)       : Item from filing object that user want to perfrom LDA on
        topic_number(int)   : Number of topic user wants to extract
        stop_word_list(list): List of stopword
        random_state=None   : Fix the random state of the LDA model.
        logger (Logger)     : Logger object from the Logging package which has already been configured. If None, no logging
                         is performed.
    Returns:
        The Non Negative Matrix Factorization model
        TF-IDF features
        TF-IDF vectorizer
    """
    if logger:
        logger.info("Turn filing list into a dataframe...")
    
    print("Turn filing list into a dataframe...")
    temp = [i for i in filings_list]
    filing_pd = pd.DataFrame(temp)
    
    if logger:
        logger.info("Extracting tf-idf features for NMF...")
    
    print("Extracting tf-idf features for NMF...")
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                       stop_words=stop_word_list)
    t0 = time()
    tfidf = tfidf_vectorizer.fit_transform(filing_pd['item{}'.format(item_num)])
    if logger:
        logger.info("Finished extracting tf features in {}s.".format(round(time() - t0, 3)))
    print("Finished extracting tf features in {}s.\n".format(round(time() - t0, 3)))
    

    # Fit the NMF model
    if logger:
        logger.info("Fitting the NMF model (Frobenius norm) with tf-idf features, "
              "n_samples={} and n_features={}...".format(filing_pd.shape[0], filing_pd.shape[1]))
    
    print("Fitting the NMF model (Frobenius norm) with tf-idf features, "
              "n_samples={} and n_features={}...".format(filing_pd.shape[0], filing_pd.shape[1]))
    t0 = time()
    
    if random_state: # Branch A
        nmf = NMF(n_components=topic_number, random_state=random_state,
                  alpha=.1, l1_ratio=.5).fit(tfidf)
    else: # Branch B
        nmf = NMF(n_components=topic_number, alpha=.1, l1_ratio=.5).fit(tfidf)
    
    if logger:
        logger.info("Finished fitting NMF model in {}s".format(round(time() - t0, 3)))
        
    print("Finished fitting NMF model in {}s".format(round(time() - t0, 3)))
    return (nmf, tfidf, tfidf_vectorizer)
    
def cv_lda(filings_list, item_num, topic_number, stop_word_list, random_state=None, logger=None):  # Tested [N]
    """
    Create LDA model from a given list of filing object using CountVectorizer and LDA from scikit learn
    
    Args:
    
        filings_list(list)  : List of filing in Filing object
        item_num(int)       : Item from filing object that user want to perfrom LDA on
        topic_number(int)   : Number of topic user wants to extract
        stop_word_list(list): List of stopword
        random_state=None   : Fix the random state of the LDA model.
        logger (Logger)     : Logger object from the Logging package which has already been configured. If None, no logging
                             is performed.
    Returns:
        The LDA model
        TF features
        TF vectorizer
    """
    if logger:
        logger.info("Turn filing list into a dataframe...")
    print("Turn filing list into a dataframe...")
    temp = [i for i in filings_list]
    filing_pd = pd.DataFrame(temp)
    
    if logger:
        logger.info("Extracting tf features for LDA...")
    print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(max_df=0.5, min_df=5,
                                    stop_words=stop_word_list)
    t0 = time()
    tf = tf_vectorizer.fit_transform(filing_pd['item{}'.format(item_num)])
    
    if logger:
        logger.info("Finished extracting tf features in {}s.".format(round(time() - t0, 3)))
    print("Finished extracting tf features in {}s.\n".format(round(time() - t0, 3)))
    
    if logger:
        logger.info("Creating the LDA model...")
    print("Creating the LDA model...")
    if random_state: # Branch A
        lda = LatentDirichletAllocation(n_components=topic_number, max_iter=5,
                                        learning_method='online',
                                        learning_offset=50.)
    else: # Branch B
        lda = LatentDirichletAllocation(n_components=topic_number, max_iter=5,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=random_state)
    if logger:
        logger.info("Finished creating LDA model")
    print("Finished creating LDA model \n")
    
    if logger:
        logger.info("Fit the LDA model")
    t0 = time()
    lda.fit(tf)
    if logger:
        logger.info("Finished fitting LDA model in {}s.".format(round(time() - t0, 3)))
    print("Finished fitting LDA model in {}s.".format(round(time() - t0, 3)))
    return (lda, tf, tf_vectorizer)


def gensim_model(filings_list, item_num, topic_number, stop_word_list, random_state=None, logger=None):  # Tested [P]
    """
    Create LDA model from a given list of filing object using LDA model from gensim library
    
    Args:
    
        filings_list(list)  : List of filing in Filing object
        item_num(int)       : Item from filing object that user want to perfrom LDA on
        topic_number(int)   : Number of topic user wants to extract
        stop_word_list(list): List of stopword
        random_state=None   : Fix the random state of the LDA model.
        logger (Logger)     : Logger object from the Logging package which has already been configured. If None, no logging
                             is performed.
    
    Returns:
        The LDA model
        Corpus of each document in the text list
        Dictionary created from the list of document
    """
    if logger:
        logger.info("Tokenize item {} of filings list...".format(item_num))
    print("Tokenize item {} of filings list...".format(item_num))
    
    t0 = time()
    texts = list()
    for i in trange(len(filings_list)):
        texts.append(tokenize_item(filings_list[i], item_num, stop_words_list = stop_word_list))
    
    if logger:
        logger.info("Finished tokenize item {} of filings list in {}s".format(item_num, round(time() - t0, 3)))
    print("Finished tokenizing in {}s".format(round(time() - t0, 3)))
    
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    if logger:
        logger.info("Fitting the LDA model...")
    print("Fitting the LDA model...")
    
    t0 = time()    
    if random_state: # Branch A
        ldamodel = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=topic_number, minimum_probability=0,
                                            random_state=random_state)
    else: # Branch B
        ldamodel = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=topic_number, minimum_probability=0)
        
    if logger:
        logger.info("Finidhed fitting LDA model in {}s.".format(round(time() - t0, 3)))
    print("Finished fitting LDA model in {}s.".format(round(time() - t0, 3)))
    return (ldamodel, corpus, dictionary)


def topic_modelling(model, filings_list, item_num, topic_number, stop_word_list, random_state=None, logger=None):  # Tested [N]
    """
    Create topic modelling from a given list of filing object using user choice of topic modelling method
    
    Args:
    
        model(str)          : Name of topic modeling method (gensim, cv_lda, tfidf_nmf). Default is cv_lda.
        filings_list(list)  : List of filing in Filing object
        item_num(int)       : Item from filing object that user want to perfrom topic modelling on
        topic_number(int)   : Number of topic user wants to extract
        stop_word_list(list): List of stopword
        random_state=None   : Fix the random state of the topic model.
        logger (Logger)     : Logger object from the Logging package which has already been configured. If None, no logging
                             is performed.
        
    Returns:
        The topic modelling model
        If using gensim:
            Corpus of each document in the text list
            Dictionary created from the list of document
        If using scikit-learn:
            TF features
        
    """
    if model == "gensim": # Branch A
        result = gensim_model(filings_list, item_num, topic_number, stop_word_list, random_state=random_state, logger=logger)
        
    elif model == "cv_lda": # Branch B
        result = cv_lda(filings_list, item_num, topic_number, stop_word_list, random_state=random_state, logger=logger)
        
    elif model == "tfidf_nmf": # Branch C
        result = tfidf_nmf(filings_list, item_num, topic_number, stop_word_list, random_state=random_state, logger=logger)
        
    else: # Branch D
        if logger:
            logger.warning("Model input was not in accepted form")
            logger.warning("Using the default choice: CV_LDA")
        print("Model input was not in accepted form")
        print("Using the default choice: CV_LDA")
        result = cv_lda(filings_list, item_num, topic_number, stop_word_list, random_state=random_state, logger=logger)
            
    return result


def extract_topics(model, filings_list, item_num, topic_number, stop_word_list, random_state=None, save_model=False, 
                   save_feature=False, logger=None):   # Tested [P]
    """
    Extract the topics from list of tokenize list 
    
    Args:
    
        model(str)          : Name of topic modeling method (gensim, cv_lda, tfidf_nmf). Default is cv_lda.
        filings_list(list)  : List of filing in Filing object
        item_num(int)       : Item from filing object that user want to perfrom topic modelling on
        topic_number(int)   : Number of topic user wants to extract
        stop_word_list(list): List of stopword
        random_state=None   : Fix the random state of the topic model.
        save_model(bool)    : Option to also return the model (default is False)
        save_feature(bool)  : Option to also return feature (default is False)
        logger (Logger)     : Logger object from the Logging package which has already been configured. If None, no logging
                             is performed.
    
    Returns:
        A dataframe including CIK, Period and Topic number.
    
    """
    
    if logger:
        logger.info("Start modeling {} topics using item {} of the filing...".format(topic_number, item_num))
    print("Start modeling {} topics using item {} of the filing...".format(topic_number, item_num))
    
    if random_state:  # Branch A
        result = topic_modelling(model, filings_list, item_num, topic_number, stop_word_list, random_state=random_state, logger=logger)
        
    else:  # Branch B
        result = topic_modelling(model, filings_list, item_num, topic_number, stop_word_list, logger=logger)
    
    topic_model = result[0]
    feature = result[1]
    if logger:
        logger.info("Finish modelling.")
        logger.info("Start extracting topic and put in a df with CIK and Period...")
    
    print("Finish modelling.")
    
    print("Start extracting topic and put in a df with CIK and Period...")
    t0 = time()
    df = dict()
    df['cik'] = list()
    df['period'] = list()
    for i in range(topic_number):
        topic = 'topic_'+str(i)
        df[topic] = list()
        
    if model == "gensim": # Branch C
        topic_doc = topic_model.get_document_topics(feature)
        for n in range(len(topic_doc)):
            df['cik'].append(filings_list[n]["cik"])
            df['period'].append(filings_list[n]["period"])
            if logger:
                logger.info("Computing document_{}...".format(n))
            print("Computing document_{}...".format(n))
            for i in range(topic_number):
                if logger:
                    logger.info("Computing Topic_{}...".format(i))
                print("Computing Topic_{}...".format(i))
                topic = 'topic_'+str(i)
                df[topic].append(topic_doc[n][i][1])
    
    elif model == "cv_lda" or model == "tfidf_nmf":  # Branch D
        doc_topic = topic_model.transform(feature)
        for n in range(doc_topic.shape[0]):
            if logger:
                logger.info("Computing document_{}...".format(n))
            print("Computing document_{}...".format(n))
            
            df['cik'].append(filings_list[n]["cik"])
            df['period'].append(filings_list[n]["period"])
            
            for i in range(doc_topic.shape[1]):
                if logger:
                    logger.info("Computing Topic_{}...".format(i))
                print("Computing Topic_{}...".format(i))
                topic = 'topic_'+str(i)
                df[topic].append(doc_topic[n][i])
        
    else:  # Branch E
        if logger:
            logger.warning("Model input was not in accepted form")
            logger.warning("Using the default choice: CV_LDA")
        print("Model input was not in accepted form")
        print("Using the default choice: CV_LDA")
        doc_topic = topic_model.transform(feature)
        for n in range(doc_topic.shape[0]):
            if logger:
                logger.info("Computing document_{}...".format(n))
            print("Computing document_{}...".format(n))
            
            df['cik'].append(filings_list[n]["cik"])
            df['period'].append(filings_list[n]["period"])
            
            for i in range(doc_topic.shape[1]):
                if logger:
                    logger.info("Computing Topic_{}...".format(i))
                print("Computing Topic_{}...".format(i))
                topic = 'topic_'+str(i)
                df[topic].append(doc_topic[n][i])

    final_df = pd.DataFrame(df)   
    
    col_order = ["cik", "period"] + ["topic_{}".format(i) for i in range(topic_number)]
    final_df = final_df[col_order]
    
    if logger:
        logger.info("Finished extracting topic and turned into a data frame in {}s".format(round(time() - t0, 3)))
        logger.info("Save and return the result")
    print("Finished extracting topic and turned into a data frame in {}s".format(round(time() - t0, 3)))
    print("Save and return the result")
    
    if save_model == True:  
        if save_feature == True:  # Branch F
            return (final_df, topic_model, feature)
        else:  # Branch G
            return(final_df, topic_model)
    else: 
        if save_feature == True:  # Branch H
            return (final_df, feature)
        else:  # Branch I
            return final_df
        
