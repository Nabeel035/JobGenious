import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from home_page import HomePage
import data  # your data.py file

class TestJobGenious:
    def setup_method(self):
        options = Options()
        options.add_argument("--start-maximized")
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://www.gojobgenius.com/")
        time.sleep(2)

    def test_login_button_click(self):
        home = HomePage(self.driver)
        home.click_login_button()
        home.enter_email(data.EMAIL)
        home.enter_password(data.PASSWORD)
        time.sleep(2)
        home.click_Signin_button()
        time.sleep(5)  # Optional: Replace with assertion

    def teardown_method(self):
        self.driver.quit()
