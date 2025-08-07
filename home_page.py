from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.get_started_button = (By.XPATH, "//button[text()='Get Started']")

    def load(self, url):
        self.driver.get(url)

    def click_get_started(self):
        # Wait until the button is visible and clickable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.get_started_button)
        ).click()
