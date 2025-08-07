import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from home_page import HomePage  # make sure this file exists and is correctly named
import data  # must have JOBGENIOUS_URL and is_url_reachable()

class TestJobGenious:
    @classmethod
    def setup_class(cls):
        # Optional: Check if URL is reachable
        if not data.is_url_reachable(data.JOBGENIOUS_URL):
            raise Exception("URL not reachable!")

        options = Options()
        options.add_argument("--start-maximized")

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get(data.JOBGENIOUS_URL)
        cls.page = HomePage(cls.driver)
        time.sleep(2)

    def test_title_contains_jobgenious(self):
        assert "JobGenius" in self.driver.title

    def test_get_started_button_redirects_to_signup(self):
        self.page.click_get_started()
        time.sleep(2)
        assert "signup" in self.driver.current_url.lower()

    @classmethod
    def teardown_class(cls):
        time.sleep(1)
        cls.driver.quit()
