Using LinkedIn Job Descriptions to Build an LDA Topic Model Algorithm
======================================================================

Purpose 
-------
The purpose of this project was to build a topic model using data scraped from LinkedIn's jobs section.


Method
------
This project involved collecting data from LinkedIn, cleaning and preprocessing the data, and creating unsupervised topic labels using a Latent Dirichlet Analysis (LDA) model. 

I built my own scraper (see src/data/LinkedInBot.py) using Selenium and ran it every few days until I had around 6 GBs of data. I wanted to create a dataset that was imbalanced and also had a mix of similarities between topics to simulate a real world problem. To create the dataset I used search key words like: Data Scientist, Data Analyst, Accountant, Finance, Civil Engineer, and Restaurant. I made the dataset heavily imbalanced by running the scraper many more times with the Data Scientist and Data Analyst key words. I saved the data using a SQLite database in the "data" folder. The code used to run the bot is in the project root directory named "Makefile.py", and was used to collect 1274 unique job postings.

I cleaned the data by looping through each document and removing: linebreaks ("\n"), emails, links, phone numbers, social media handles, and all french documents. I preprocessed the documents by: removing punctuation, removing stopwords, removing low- and high- frequency words, creating bi- and tri-grams, lemmatizing the text, and finally converting the corpus into a term-frequency-inverse document frequency (TF-IDF) matrix. I continually iterated over these preprocessing steps while modelling to improve the topic results, for example by adjusting the frequency filtering thresholds and the bi- and tri-gram thresolds.

Next I experimented with different NLP algorithms to discover topics within the dataset. After experimenting with sklearn and gensim models, I found that the gensim methods were the fastest and easiest to use. I used Gensim's coherence score to evaluate each model throughout the modelling stage. To optimize the topic results I played with parameters such as: number of topics, number of passes over corpus, and iterations of each document, as well as the mentioned preprocessing steps and parameters.


Results
-------
My final LDA model had a coherence score of 0.544 and had 5 topics which were similar to the keywords I used to build the dataset. The topics were:
1. Accountant
2. Data Analyst (Product or Client)
3. Civil Engineer
4. Data Scientist (more ML/AI and SWE)
5. Restaurant Job

The keywords for these descriptions are shown below. 

#### Table 1: Top-10 terms for each topic in the LDA model.
![Topic Terms](https://github.com/MatanFreedman/LinkedIn-NLP/blob/master/notebooks/topic-modelling/topic_terms.PNG)

The topic frequencies (shown below) shows that number of Data Analyst postings far exceeded those of any other topic. I was expecting a similar number of Data Scientist postings, however there could be a few reasons for this. Some Data Scientist search results may actually be for Data Analyst-type jobs, and whoever posted them is using the wrong label (e.g., an inexperienced hiring manager or recruiter). The model could also be misclassifying some Data Scientist jobs as Data Analyst jobs since the language between the two descriptions is likely very similar. LinkedIn may also be showing me jobs that it recommends regardless of the keywords searched, therefore they may be recommending me more Data Analyst jobs even when my bot searched "Data Scientist".

![Topic Frequencies](https://github.com/MatanFreedman/LinkedIn-NLP/blob/master/notebooks/topic-modelling/topic_frequencies.png)
#### Figure 1: Topic frequencies in corpus.

We can also see how similar the topics are by using a python LDA visualization library (pyLDAvis) that displays the topics as points in PCA space (using PC1 and PC2), and the size of each point representing the frequency of the topic in the dataset. The pyLDAvis results are shown below. 

![pyLDAvis](https://github.com/MatanFreedman/LinkedIn-NLP/blob/master/notebooks/topic-modelling/pyldavis.PNG)
#### Figure 2: Topic similarity and frequency. The topics are represented as points in 2D (PCA) space, so points that are closer together are similar, and points that are further apart are less similar. The size of each point corresponds to the relative frequency of that topic in the corpus. 

You can see that Topic 2 (Data Analyst) and Topic 4 (Data Scientist) are closely related which makes sense. Topic 2 is much larger than the other topics due to the imbalancedness of the dataset or model error (these two topics may be too similar to distinguish). Topic 1 (Accountant) and Topic 3 (Civil Engineer) are also closely related, which is a bit surprising but it might make sense since both jobs likely involve budgets, reporting, and excel skills. Finally, Topic 5 (Restaurant) is small and far away from all the other topics, which makes sense since it is not at all related to the other job industries.  


Conclusions
-----------
The LDA model created the expected topics: Data Scientist, Data Analyst, Accountant, Civil Engineer, and Restaurant Employee. The model was able to handle the largely imbalanced dataset (many more records of Data Analyst and Data Scientist), however the model identified many more Data Analyst positions over Data Scientist positions. This may be due to model error, job poster, or by the LinkedIn recommendation algorithm overriding the search words. Further work would be to look into the Data Analyst and Data Scientist imbalance, as well as to compare the accuracy of the topics to the classified texts.
<br><br><br><br>

How To Set Up Project
==================================
To build project:
1. `python -m venv venv`
2. `venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. Create a .env file with LinkedIn EMAIL and PASSWORD like:<Br>
    EMAIL="your@email.com"<br>
    PASSWORD="your_password"
5. Scrape data: `python Makefile.py`


Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │

