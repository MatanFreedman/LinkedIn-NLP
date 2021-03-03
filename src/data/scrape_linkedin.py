import os
from dotenv import load_dotenv, find_dotenv
import logging
import pickle
from pathlib import Path

from src.data.DBConnection import DBConnection 
from src.data.LinkedInBot import LinkedInBot

def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, path):
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             driver.add_cookie(cookie)

def run(bot, keywords, location):
    logging.info("Begin linkedin keyword search")
    bot.search_linkedin(keywords = keywords, location = location)
    bot.wait()
    # scrape pages,only do first 8 pages since after that the data isn't 
    # well suited for me anyways:  
    for page in range(2, 9):
        # get the jobs list items to scroll through:
        jobs = bot.get_job_page_list_items()
        for job in jobs:
            bot.scroll_to(job)
            [position, company, location] = job.text.split('\n')[:3]
            details = bot.driver.find_element_by_id("job-details").text

            # send to DB:
            data = (position, company, location, details)
            if not db.is_duplicate(data):
                db.insert_position(data)
                # just to view in cmd window:
                logging.info(f"Added to DB: {position}, {company}, {location}")
            else:
                logging.info(f"Duplicate entry found: {position}, {company}, {location}")

        # go to next page:
        bot.driver.find_element_by_xpath(f"//button[@aria-label='Page {page}']").click()
        logging.info(f"Going to page {page}")
        bot.wait()

    logging.info("Duplicate entries exceeded")

def main():
    load_dotenv(find_dotenv())
    db = DBConnection()

    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    data_dir = Path(__file__).resolve().parents[0]

    bot = LinkedInBot(useProxy=False)

    if os.path.exists(str(data_dir) + "/cookies.txt"):
        bot.driver.get("https://www.linkedin.com/")
        bot.load_cookie( str(data_dir) + "/cookies.txt")
        bot.driver.get("https://www.linkedin.com/")
    else:
        EMAIL = os.getenv("EMAIL")
        PASSWORD = os.getenv("PASSWORD")
        bot.login(
            email=EMAIL,
            password=PASSWORD
        )
        bot.save_cookie(str(data_dir) + "/cookies.txt")
    
    for keywords in ["Data Scientist", "Data Analyst"]:
        bot.run(keywords, "Canada", db)

    save_cookie(bot.driver, str(data_dir) + "/cookies.txt")
    bot.close_session()

if __name__ == "__main__":
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
