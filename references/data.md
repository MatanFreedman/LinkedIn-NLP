# Data
The source data is all pulled from LinkedIn using LinkedInBot and the scrape_linkedin.py script. 

The linkedin_data.db file contains the data in data/raw:

TABLE: positions
COLUMNS
-------
id TEXT       : identifier
position TEXT : LinkedIn position title
company TEXT  : Company hiring 
location TEXT : Location of position
details TEX   : Entire details section of job listing
date TEXT     : date of insertion to DB


You can use the DBConnection class in src/data to create and communicate with the DB. 