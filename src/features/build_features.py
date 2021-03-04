
import sklearn.feature_extraction.text 
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from sklearn.pipeline import Pipeline

from src.data.DBConnection import DBConnection
from src.data.make_dataset import preprocess_pipeline

import time 
from numpy import round

import logging

def bag_of_words_tfid_norm():
    """Builds main featureset using the preprocessing pipeline, TF-IDF vectorizer + TF-IDF transformer
    to normalize dataset.
    """
    logger = logging.getLogger(__name__)
    logger.info("Building TF-IDF vector + normalizing")

    # start timer:
    t0 = time.time()

    # initialize DB connection:
    db = DBConnection()

    # get iterator for "positons" info
    sql = """SELECT details FROM positions;"""
    corpus = db.cur.execute(sql)

    # create pipeline:
    tfidf_vec = Pipeline([('tfid_vec', TfidfVectorizer(tokenizer=None, preprocessor=preprocess_pipeline))])
    tfidf = Pipeline([('tfid', TfidfTransformer())])
    pipe = Pipeline([
        ('tfidf_vec', tfidf_vec),
        ('tfidf', tfidf)
    ])

    # fit pipeline:
    features = pipe.fit_transform(corpus)

    # print time:
    logger.info(f"Feature building took {round(time.time() - t0, 2)} seconds")
    return features