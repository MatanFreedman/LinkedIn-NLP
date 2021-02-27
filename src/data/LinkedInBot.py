from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
import os 

class LinkedInBot:
    def __init__(self, verbose=True, useProxy=False, delay=5):
        self.verbose=verbose
        self.delay=delay

        bot_dir = Path(__file__).resolve().parents[0]
        driver_path = str(bot_dir) + "\\geckodriver.exe"

        self.proxy = self.create_proxy() if useProxy else None
        self.driver = webdriver.Firefox(executable_path=driver_path, proxy=self.proxy)


    def login(self, email, password):
        """Go to linkedin and login"""

        # go to linkedin:
        self.driver.maximize_window()
        self.driver.get('https://www.linkedin.com/login')
        
        if self.verbose: print("Logging in...")
        time.sleep(3)
        login_email = self.driver.find_element_by_name('session_key')
        login_email.send_keys(email)
        # enter linkedin:
        login_pass = self.driver.find_element_by_name('session_password')
        login_pass.send_keys(password)
        login_pass.send_keys(Keys.RETURN)
        time.sleep(6)


    def close_session(self):
        """This function closes the actual session"""
        print('End of the session!')
        self.driver.close()


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
        print("Using proxy: ", myProxy)
        return proxy


    def go_to_job_page(self):
        """ Go to job section and search using keywords and locations """
        if self.verbose: print("Navigation to Jobs page...")
        # go to Jobs
        self.wait_for_element_ready(By.LINK_TEXT, 'Jobs')
        jobs_link = self.driver.find_element_by_link_text('Jobs')
        jobs_link.click()
        time.sleep(self.delay)


    def wait_for_element_ready(self, by, text):
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((by, text)))
        except TimeoutException:
            pass


    def search_linkedin(self, keywords, location):
        """Enter keywords into search bar
        """
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
        if self.verbose: print("Keyword search successful...")
        time.sleep(self.delay)


    def get_job_page_list_items(self):
        """Gets the sidebar items that are in view
        
        Returns: list of Selenium web elements
        """
        list_items = self.driver.find_elements_by_class_name("occludable-update")
        return list_items


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


    def wait(self, t_delay=None):
        """Just easier to build this in here.
        Parameters
        ----------
        t_delay [optional] : int
            seconds to wait.
        """
        delay = self.delay if t_delay == None else t_delay
        time.sleep(delay)

if __name__ == "__main__":
    bot = LinkedInBot(useProxy=False)

    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    bot.login(
        email=EMAIL,
        password=PASSWORD
    )
    bot.go_to_job_page()
    bot.search_linkedin(keywords = "Data Analyst", location = "Canada")
    bot.wait()