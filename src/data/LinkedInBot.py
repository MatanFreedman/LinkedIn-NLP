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

LOGGER = logging.getLogger(__name__)

class LinkedInBot:
    """Bot used to scrape LinkedIn
    """

    def __init__(self, useProxy=False, delay=5, headless=True):
        """
        Parameters
        ----------
        useProxy : bool, optional
            if user wants to use a proxy (publicly available, use w caution)
        delay : int, optional
            Sets amount of time to wait after some actions (so that LinkedIn doesn't start using captcha)

        """
        self.delay=delay
        self.proxy = self.create_proxy() if useProxy else None
        
        if headless:
            options = webdriver.firefox.options.Options()
            options.set_headless()
        else:
            options = None
            
        LOGGER.info("starting driver")
        driver_path = str(Path(__file__).resolve().parents[0]) + "\\geckodriver.exe"    
        self.driver = webdriver.Firefox(executable_path=driver_path, proxy=self.proxy, options=options)
        self.driver.maximize_window()

    def login(self, email, password):
        """Go to linkedin and login
        
        Parameters
        ----------
        email : str
        password : str
        """
        # go to linkedin:
        LOGGER.info("Logging in")
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(self.delay)

        self.driver.find_element_by_id('username').send_keys(email)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('password').send_keys(Keys.RETURN)
        time.sleep(self.delay)

    def save_cookie(self, path):
        """Saves browser cookies.
        Parameters
        ----------
        path : str
            path must exist (except for file)
        """
        LOGGER.info("Saving cookie")
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        """Loads cookies from file

        Parameters
        ----------
        path : str
            Path must exist
        """
        LOGGER.info("Loading cookies")
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def create_proxy(self):
        """Creates proxy using free-proxy-list.net
        
        Note
        ----
        Use with caution.
        """
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
        """Enter keywords into search bar.

        Parameters
        ----------
        keywords : str
        location : str
        """
        LOGGER.info("Searching jobs page")
        self.driver.get("https://www.linkedin.com/jobs/")
        # search based on keywords and location and hit enter
        self.wait_for_element_ready(By.CLASS_NAME, 'jobs-search-box__text-input')
        time.sleep(self.delay)
        search_bars = self.driver.find_elements_by_class_name('jobs-search-box__text-input')
        search_keywords = search_bars[0]
        search_keywords.send_keys(keywords)
        search_location = search_bars[3]
        search_location.send_keys(location)
        time.sleep(self.delay)
        search_location.send_keys(Keys.RETURN)
        LOGGER.info("Keyword search successful")
        time.sleep(self.delay)

    def wait(self, t_delay=None):
        """Make bot wait for t_delay seconds.
        Parameters
        ----------
        t_delay : int, optional
            seconds to wait.
        """
        delay = self.delay if t_delay == None else t_delay
        time.sleep(delay)

    def scroll_to(self, job_list_item):
        """Scroll to the list item in the column 

        Parameters
        ----------
        job_list_item : selenium element
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
        list of str : [position, company, location, details]
        """
        [position, company, location] = job.text.split('\n')[:3]
        details = self.driver.find_element_by_id("job-details").text
        return [position, company, location, details]
   
    def wait_for_element_ready(self, by, text):
        """Waits for an element to be ready

        Parameters
        ----------
        by : Selenium BY object
        text : str
        """
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((by, text)))
        except TimeoutException:
            LOGGER.debug("wait_for_element_ready TimeoutException")
            pass

    def get_job_page_list_items(self):
        """Gets the sidebar items that are in view
        
        Returns
        -------
        list of Selenium web elements
        """
        return self.driver.find_elements_by_class_name("occludable-update")

    def close_session(self):
        """Closes session
        """
        logging.info("Closing session")
        self.driver.close()

    def run(self, keywords, location, db):
        """Searchs keywords + location, then scrapes first 8 pages of LinkedIn.
        After completed, will just post message "Done Scraping".

        Parameters
        ----------
        keywords : str
        location : str
        db : DBConnection class object
            import from DBConnection.py 
        """
        LOGGER.info("Begin linkedin keyword search")
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
                    LOGGER.info(f"Added to DB: {position}, {company}, {location}")
                else:
                    LOGGER.info(f"Duplicate entry found: {position}, {company}, {location}")

            # go to next page:
            self.driver.find_element_by_xpath(f"//button[@aria-label='Page {page}']").click()
            self.wait()
        LOGGER.info("Done scraping.")

if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    from src.data.DBConnection import DBConnection
    import os 

    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    data_dir = Path(__file__).resolve().parents[0]

    load_dotenv(find_dotenv())
    db = DBConnection()
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
    

    bot.run("Data Analyst", "Canada", db)

