# visualizing stop words:
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

def fdist_words(words):
    """Make word frequency plot

    Parameters
    ---------
    words : list of str
        list of words in text

    Returns 
    -------
    fig : matplotlib.pyplot.Figure
    """
    fdist = FreqDist(words)
    fig = plt.figure()
    fdist.plot(25)
    return fig