"""Since Windows does not have an easily compatible "make" command I am just going to
execute the processes here
"""
import os 
import logging

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)

# create dataset:
logging.info("Run src\data\scrape_linkedin.py")
from src.data import scrape_linkedin
scrape_linkedin.main()
logging.info("Finished scraping LinkedIn data.")

