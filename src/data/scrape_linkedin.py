import os
from dotenv import load_dotenv, find_dotenv

from DBConnection import DBConnection 
from LinkedInBot import LinkedInBot
load_dotenv(find_dotenv())

db = DBConnection()

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

# scrape pages:  
for page in range(2,4):
    # get the jobs list items to scroll through:
    jobs = bot.get_job_page_list_items()
    for job in jobs:
        bot.scroll_to(job)
        [position, company, location] = job.text.split('\n')[:3]
        details = bot.driver.find_element_by_id("job-details").text

        # send to DB:
        data = (position, company, location, details)
        db.insert_position(data)

        # just to view in cmd window:
        print([position, company])

    # go to next page:
    bot.driver.find_element_by_xpath(f"//button[@aria-label='Page {page}']").click()
    bot.wait()