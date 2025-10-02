import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
import data
from form_fields import FormFields

class AddApplication:
    def __init__(self, driver):
        self.driver = driver
        self.form_field = FormFields(driver)  # Initialize helper class
        self.wait = WebDriverWait(driver, 10)

    def close_toast_popup(self):
        try:
            toast_close = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'toast-close')]"))
            )
            toast_close.click()
            time.sleep(2)
            print("✅ Toast popup closed.")
        except:
            print("ℹ️ No toast popup found.")

    def create_add_aaplication(self):
        pass