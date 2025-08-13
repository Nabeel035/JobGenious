import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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


    def test_create_job(self):
        # Initialize page objects
        home = HomePage(self.driver)
        # Call the login method from HomePage
        home.login(data.EMAIL, data.PASSWORD)

        time.sleep(2)
        #logout the account
        home.logout()
        time.sleep(5)

    def teardown_method(self):
        self.driver.quit()