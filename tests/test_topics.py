import pytest
import pandas as pd
import numpy as np
import pickle
from sklearn.externals import joblib
from src.preprocessing.label_feature_eng import sum_ytd, annualize

texts = joblib.load('data/test_texts.pkl')
# with open("data/test_texts.pkl", "rb") as fp:
#     texts = pickle.load(fp)

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in tqdm(texts)]

df = pd.DataFrame()
corp = pd.Series(corpus)
corp = pd.DataFrame(corp)

class TestClass:

    def test_topics_corpus(self):
        assert all([corp.iloc[i,:][0] == corpus[i] for i in range(corp.shape[0])]), \
            "Error, value from topics() was not as expected"
