# -*- coding: utf-8 -*-
import string
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer 
from nltk import pos_tag
import nltk

import logging
from pathlib import Path

def __init__():
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')


def tokenize(text):
    """Tokenize a string of text.

    Process:
    1. removes next line.
    2. makes all lower case.
    3. removes punctuation.
    4. remove stop words.

    Parameters
    ----------
    text : str
        full text string, no preprocessing yet

    Returns
    -------
    words : list of str
        list of words
    """
    clean_text = text.replace("\n", " ")
    clean_text = clean_text.lower()
    words = ["".join(c for c in s if c not in string.punctuation) for s in clean_text.split(" ")]
    words = [w for w in words if w is not ""]
    words = [w for w in words if w not in stopwords.words("english")]
    return words

def wordnet_tags(tag): 
    """Returns WordNetLemmatizer compatible tags
    """   
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
 
def lematize(words):
    """Lematizes words (need to be preprocessed first)

    Parameters
    ----------
    words : list of str

    Returns
    -------
    list of str
    """
    lemmatizer = WordNetLemmatizer()
    doc = [lemmatizer.lemmatize(x[0], wordnet_tags(x[1])) for x in pos_tag(words)]
    return ' '.join(doc)

def preprocess_pipeline(text):
    """Preprocessing pipeline for string of text.

    Parameters
    ----------
    text : str

    Returns
    -------
    lemmed_words : list of str
        list of cleaned, tokenized, and lemmatized words
    """
    words = tokenize(text)
    lemmed_words = lematize(words)
    return lemmed_words

def main():
    pass


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    main()
