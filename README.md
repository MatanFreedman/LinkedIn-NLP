Using LinkedIn Job Descriptions to Build an LDA Topic Model Algorithm
======================================================================

Purpose 
-------
Build a topic model using data scraped from LinkedIn's jobs section.

Method
------
This project involved collecting data from LinkedIn, cleaning and preprocessing the data, and creating topics using a Latent Dirichlet Analysis (LDA) model. 

I built my own scraper (see src/data/LinkedInBot.py) using Selenium and ran it every few days until I had enough data. I wanted to create a dataset that was imbalanced and also had a mix of similarities between topics to simulate a real world problem. To create the dataset I used search key words like: Data Scientist, Data Analyst, Accountant, Finance, Civil Engineer, and Restaurant. I made the dataset heavily imbalanced by running the scraper many more times with the Data Scientist and Data Analyst key words. I saved the data using a SQLite database in the "data" folder. The code used to run the bot is in the project root directory named "Makefile.py", and was used to collect 1274 unique job postings (around 6 GB).

I cleaned the data by looping through each document and removing: linebreaks ("\n"), emails, links, phone numbers, social media handles, and all french documents. I preprocessed the documents by: removing punctuation, removing stopwords, removing low- and high- frequency words, creating bi- and tri-grams, lemmatizing the text, and finally converting the corpus into a term-frequency-inverse document frequency (TF-IDF) matrix. I continually iterated over these preprocessing steps while modelling to improve the topic results, for example adjusting the frequency filtering thresholds and the bi- and tri-gram thresolds.

Next I experimented with different NLP algorithms to discover topics within the dataset. After experimenting with sklearn and gensim models, I found that the gensim methods were the fastest and easiest to use. I used Gensim's coherence model to evaluate each model throughout this stage. To optimize the topic results I played with parameters such as: number of topics, number of passes over corpus, and iterations of each document, as well as the mentioned preprocessing steps/parameters.

Results
-------
My final LDA model had a coherence score of 0.544 and had 5 topics which were similar to the keywords I used to build the dataset. The topics were:
1. Accountant
2. Data Analyst (Product or Client)
3. Civil Engineer
4. Data Scientist (more ML/AI and SWE)
5. Restaurant Job

The keywords for these descriptions are shown below. 

![Topic Terms](https://github.com/MatanFreedman/LinkedIn-NLP/blob/master/notebooks/topic-modelling/topic_terms.PNG)

The topic distribution (shown below) shows that Data Analyst postings far exceed that of any other topic. I was expecting a similar amount of Data Scientist topics however there could be a few reasons for this. Some Data Scientist postings could actually be for Data Analyst-type job descriptions, and whoever posted them is using the wrong label. The model could also be miss-classifying these jobs since the language between the two descriptions is likely very similar. 

![Topic Frequencies](https://github.com/MatanFreedman/LinkedIn-NLP/blob/master/notebooks/topic-modelling/topic_frequencies.PNG)

Conclusions
-----------
The LDA

How to Use
==================================
To build project:
1. `python -m venv venv`
2. `venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. Create a .env file with LinkedIn EMAIL and PASSWORD like:<Br>
    EMAIL="your@email.com"<br>
    PASSWORD="your_password"
5. Scrape data: `python Makefile.py`

<br><br><br>

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

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
<p><small><a href="https://medium.com/@rrfd/cookiecutter-data-science-organize-your-projects-atom-and-jupyter-2be7862f487e">Good explanation for how to use this template here </a></small></p>
