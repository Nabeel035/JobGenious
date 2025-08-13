import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from actions import search_job_description
from home_page import HomePage
from job_description import JobDescriptionPage
import data

class TestJobGenious:
    def setup_method(self):
        options = Options()
        options.add_argument("--start-maximized")
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(data.JOBGENIOUS_URL)
        time.sleep(2)


    def test_job_search_actions(self):
        # Initialize page objects
        home = HomePage(self.driver)

        # Call the login method from HomePage
        home.login(data.EMAIL, data.PASSWORD)

        #Open the Job Descriptions Page
        job_desc_page = JobDescriptionPage(self.driver)
        job_desc_page.job_list_page()
        time.sleep(3)

        #1 Search the Job from Job Descriptions List
        search_job_description(self.driver, data.SEARCH_JOB)
        time.sleep(5)

    def teardown_method(self):
        self.driver.quit()