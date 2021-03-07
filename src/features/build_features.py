
import sklearn.feature_extraction.text 
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from sklearn.pipeline import Pipeline

from src.data.DBConnection import DBConnection
from src.data.make_dataset import preprocess_pipeline

import time 
from numpy import round
from pathlib import Path
import scipy
import pickle

import logging


def load_saved_features(date="2021-03-07"):
    """Function used to grab the saved features and pipe

    date : str
        YYYY-MM-DD format. Used to grad to correct features and pipeline file in the processed dir.
    """
    logger = logging.getLogger(__name__)
    
    proj_path = Path(__file__).resolve().parents[2]
    processed_path = proj_path / "data" / "processed"

    logger.info("Loading features and pipe from /data/processed/")

    features = scipy.sparse.load_npz(str(processed_path / f"features_{date}.npz"))
    pipe_path = str(processed_path / f"pipe_{date}.pkl")
    with open(pipe_path, 'rb') as file:
        pipe = pickle.load(file)

    return features, pipe



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
    return features, pipe