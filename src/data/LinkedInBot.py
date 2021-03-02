from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import logging
import pickle


class LinkedInBot:
    def __init__(self, useProxy=False, delay=5):
        self.delay=delay
        self.proxy = self.create_proxy() if useProxy else None
        
        driver_path = str(Path(__file__).resolve().parents[0]) + "\\geckodriver.exe"

        logging.info("Starting driver")
        self.driver = webdriver.Firefox(executable_path=driver_path, proxy=self.proxy)

    def login(self, email, password):
        """Go to linkedin and login"""
        # go to linkedin:
        logging.info("Logging in")
        self.driver.maximize_window()
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(self.delay)

        self.driver.find_element_by_id('username').send_keys(email)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('password').send_keys(Keys.RETURN)
        time.sleep(self.delay)

    def save_cookie(self, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def create_proxy(self):
        response = requests.get('https://free-proxy-list.net')
        text = BeautifulSoup(response.content)
        table = text.tbody
        for row in table.find_all("tr"):
            elements = [e.text for e in row.find_all("td")]
            ip = elements[0]
            port = elements[1]
            https = elements[6]
            anon = elements[5]
            if https == "yes" and anon == "elite proxy":
                break
        myProxy = "{}:{}".format(ip, port)
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': myProxy,
            'ftpProxy': myProxy,
            'sslProxy': myProxy,
            'noProxy': '' # set this value as desired
            })
        logging.info("Using proxy: ", myProxy)
        return proxy

    def search_linkedin(self, keywords, location):
        """Enter keywords into search bar
        """
        logging.info("Searching jobs page")
        self.driver.get("https://www.linkedin.com/jobs/")
        # search based on keywords and location and hit enter
        self.wait_for_element_ready(By.CLASS_NAME, 'jobs-search-box__text-input')
        time.sleep(self.delay)
        search_bars = self.driver.find_elements_by_class_name('jobs-search-box__text-input')
        search_keywords = search_bars[0]
        search_keywords.send_keys(keywords)
        search_location = search_bars[2]
        search_location.send_keys(location)
        time.sleep(self.delay)
        search_location.send_keys(Keys.RETURN)
        logging.info("Keyword search successful")
        time.sleep(self.delay)

    def wait(self, t_delay=None):
        """Just easier to build this in here.
        Parameters
        ----------
        t_delay [optional] : int
            seconds to wait.
        """
        delay = self.delay if t_delay == None else t_delay
        time.sleep(delay)

    def scroll_to(self, job_list_item):
        """Just a function that will scroll to the list item in the column 
        """
        self.driver.execute_script("arguments[0].scrollIntoView();", job_list_item)
        job_list_item.click()
        time.sleep(self.delay)
 
    def get_position_data(self, job):
        """Gets the position data for a posting.

        Parameters
        ----------
        job : Selenium webelement

        Returns
        -------
        list of strings : [position, company, location, details]
        """
        [position, company, location] = job.text.split('\n')[:3]
        details = self.driver.find_element_by_id("job-details").text
        return [position, company, location, details]
   
    def wait_for_element_ready(self, by, text):
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((by, text)))
        except TimeoutException:
            logging.debug("wait_for_element_ready TimeoutException")
            pass

    def get_job_page_list_items(self):
        """Gets the sidebar items that are in view
        
        Returns: list of Selenium web elements
        """
        return self.driver.find_elements_by_class_name("occludable-update")

    def close_session(self):
        """This function closes the actual session"""
        logging.info("Closing session")
        self.driver.close()

    def run(self, keywords, location, db):
        """Searchs keywords + location, then scrapes first 8 pages of LinkedIn.
        After completed, will just post message "Done Scraping".

        Parameters
        ----------
        keywords : string
        location : string
        db : DBConnection class object
            In DBConnection.py 
        """
        logging.info("Begin linkedin keyword search")
        self.search_linkedin(keywords, location)
        self.wait()

        # scrape pages,only do first 8 pages since after that the data isn't 
        # well suited for me anyways:  
        for page in range(2, 9):
            # get the jobs list items to scroll through:
            jobs = self.driver.find_elements_by_class_name("occludable-update")
            for job in jobs:
                self.scroll_to(job)
                [position, company, location, details] = self.get_position_data(job)

                # send to DB:
                data = (position, company, location, details)
                if not db.is_duplicate(data):
                    db.insert_position(data)

                    # just to view in cmd window:
                    logging.info(f"Added to DB: {position}, {company}, {location}")
                else:
                    logging.info(f"Duplicate entry found: {position}, {company}, {location}")

            # go to next page:
            self.driver.find_element_by_xpath(f"//button[@aria-label='Page {page}']").click()
            self.wait()
        logging.info("Done scraping.")

if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    import os 

    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    load_dotenv(find_dotenv())
    bot = LinkedInBot(useProxy=False)
    bot.login(
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD")
    )
