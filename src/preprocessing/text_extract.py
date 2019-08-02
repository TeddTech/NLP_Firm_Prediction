import re
import nltk
import gensim
import datetime
import mongoengine
import pymongo as mongo
from tqdm import tqdm, trange
from string import punctuation
from nltk.corpus import stopwords
from gensim import corpora, models
from gensim.models.ldamodel import LdaModel
from src.structures import Filing, filing_from_mongo


def replace_number(tokenized_list, logger=None):  # Tested [Y]
    """
    Replace the number in filling with a special character after tokenize. If there are several number: save only one

    Args:
        tokenized_list(list): A list of tokenized word
        logger (Logger)     : Logger object from the Logging package which has already been configured. If None, no logging
                             is performed.
                             
    Returns:
        The tokenized list that does not contain any number but instead only special character
    """
    digits = r"\d+"

    for i in range(len(tokenized_list)):
        if str(tokenized_list[i]).isdigit():  # Branch A
            tokenized_list[i] = "<#>"

        # handle digit attaches to a string
        if len(re.split(digits, tokenized_list[i])) != 1:  # Branch B
            tokenized_list[i] = re.sub('\d+', '<#>', tokenized_list[i])

        # handle digit.digit or digit,digit
        if tokenized_list[i] in ["<#>,<#>", "<#>.<#>", "<#>,<#>,<#>", "<#>."]:  # Branch C
            tokenized_list[i] = "<#>"

    return tokenized_list


def tokenize_item(filing, item_num, remove_stop_words=True,
                  remove_punctuation=True, tag_numbers=True, lower_case=True, 
                  stop_words_list=stopwords.words('english'), logger=None):  # Tested [N]
    """
    Creates a list of tokens for a single item in a Filing object given an item number.

    Args:
        filing (Filing)             : The filing from which to extract tokens.
        item_num (str or int)       : The item number to tokenize
        remove_stop_words (bool)    : Default=True. Removes stop words from nltk's standard english stopword list
        remove_punctuation (bool)   : Default=True. Removes punctuation according to string.punctuation,
                                      as well as: "--", "-", "``", "..." and "''"
        tag_numbers (bool)          : Default=True. Turns all numeric values into '<#>' to reduce the number of unique tokens
        lower_case (bool)           : Default=True. Turns all tokens in the list into lower-case
        stop_words_list (list):     : The list of stopwords that user wants to remove, default is the English stopwords.
        logger (Logger)             : Logger object from the Logging package which has already been configured. If None, no logging
                                     is performed.
                             
    Returns:
        (list) List of tokens from the specified item for the provided Filing object
    """

    if not isinstance(item_num, int) and not item_num.isdigit():
        raise ValueError("item_num={} is an invalid ")  # Branch A

    tokens = nltk.tokenize.word_tokenize(filing['item{}'.format(item_num)])

    if lower_case:  # Branch B
        tokens = [word.lower() for word in tokens]

    if tag_numbers:  # Branch C
        tokens = replace_number(tokens)

    if remove_stop_words:  # Branch D
        tokens = [word for word in tokens if word not in stop_words_list]

    if remove_punctuation:  # Branch E
        tokens = [word for word in tokens if word not in ["-", "--", "``", "''", "..."] + list(punctuation)]

    return tokens


def get_all_filings(collection, limit=None, filter=None, logger=None):  # Tested [P]
    """
    Get text data from the parsing collection from MongoDB data
    Organize and structure the data into Filing object

    Args:
        collection (mongoDB collection)  : the collection name taken from the MongoDB
        limit (int)                      : the limit number of filings we want to extract
        filter (dict)                    : JSON-like filter dictionary according to MongoDB syntax
        logger (Logger)                  : Logger object from the Logging package which has already been configured. If None, no logging
                                         is performed.
                                         
    Returns:
        (list) A list of all Filing objects, each object is one SEC filing

    """
    filings_list = list()
    # Limit the number of filings retrieved
    if limit:  # Branch A

        # Check the input
        if limit <= 0:  # Branch B
            raise ValueError("Limit must be a positive number")

        if not isinstance(limit, int):  # Branch C
            raise TypeError("Limit must be an integer")

        if filter:  # Branch C
            for item in tqdm(collection.find().limit(limit)):
                val = filing_from_mongo(item, filter, logger=logger)
                if not isinstance(val, dict):
                    filings_list.append(val)  # Iterate over each retrieved document

            return filings_list

        else:  # Branch D
            for item in tqdm(collection.find().limit(limit)):
                val = filing_from_mongo(item, logger=logger)
                if not isinstance(val, dict):
                    filings_list.append(val)

            return filings_list

    # If you don't want a limit
    else:  # Branch E
        if filter:
            for item in tqdm(collection.find()):
                val = filing_from_mongo(item, filter, logger=logger)
                if not isinstance(val, dict):
                    filings_list.append(val)
            return filings_list
        
        else:  # Branch F
            for item in tqdm(collection.find()):
                val = filing_from_mongo(item, logger=logger)
                if not isinstance(val, dict):
                    filings_list.append(val)
            return filings_list


def tokenize_filings(filings_list, item_num, remove_stop_words=True, 
                     remove_punctuation=True, tag_numbers=True, lower_case=True,
                     stop_words_list=nltk.corpus.stopwords.words('english'), logger=None):  # Tested [Y]

    """
    Tokenize the specified items of all Filing object from a list of SEC filing

    Args:

        filings_list (Filing)       : The filing from which to extract tokens.
        item_num (str or int)       : The item number to tokenize
        remove_stop_words (bool)    : Default=True. Removes stop words from nltk's standard english stopword list
        remove_punctuation (bool)   : Default=True. Removes punctuation according to string.punctuation,
                                       as well as: "--", "-", "``", "..." and "''"
        tag_numbers (bool)          : Default=True. Turns all numeric values into '<#>' to reduce the number of unique tokens
        lower_case (bool)           : Default=True. Turns all tokens in the list into lower-case
        stop_words_list (list):     : The list of stopwords that user wants to remove, default is the English stopwords.
        logger (Logger)             : Logger object from the Logging package which has already been configured. If None, no logging
                                     is performed.
                             
    Returns:
        (list) A list of tokenize items for each filing from the given list

    """

    texts = list()
    for i in trange(len(filings_list)):
        texts.append(tokenize_item(filings_list[i].__dict__, item_num, remove_stop_words=remove_stop_words,
                                   remove_punctuation=remove_punctuation, tag_numbers=tag_numbers,
                                   lower_case=lower_case, stop_words_list=stop_words_list, logger=logger))

    return texts
