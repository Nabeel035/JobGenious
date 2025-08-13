import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from actions import perform_job_action
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


    def test_create_job_actions(self):
        # Initialize page objects
        home = HomePage(self.driver)
        # Call the login method from HomePage
        home.login(data.EMAIL, data.PASSWORD)
        #Open the Job Descriptions Page
        job_desc_page = JobDescriptionPage(self.driver)
        job_desc_page.job_list_page()
        time.sleep(3)

        # Example: assuming you have located a job row element and know its status
        job_row = self.driver.find_element(By.CSS_SELECTOR, "div.job-row[data-job-id='123']")  # Example selector
        status = "Active"
        action = "Pause"

        perform_job_action(self.driver, job_row, status, action)
