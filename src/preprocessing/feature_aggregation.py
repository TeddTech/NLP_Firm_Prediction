import re
import time
import numpy as np
import pandas as pd
import datetime as dt
from tqdm import tqdm, trange
from src.preprocessing import diff_col


def topics(df, corpus, lda):  # Tested [Y]
    """
    Creates the topic columns

    Args
        df (pd.DataFrame):
        corpus (dict): corpus of all documents
        lda : a fitted LDA model

    Return
        df with a column called vol added
    """

    for i in range(len(lda.get_topics())):
        if logger:
            logger.info("Computing Topic_{}...".format(i))
        topic_feature = list()
        topic = 'topic_'+str(i)
        for j in range(len(lda.get_document_topics(corpus))):
            if logger:
                logger.info("Computing document_{}...".format(j))
            topic_feature.append(lda.get_document_topics(corpus)[j][i][1])

        topic_feature = pd.Series(topic_feature)
        df[topic] = topic_feature

    return df
