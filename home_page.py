import time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def click_login_button(self):
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Log In']"))
        ).click()


    def enter_email(self, email):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        ).send_keys(email)

    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        ).send_keys(password)

    def click_Signin_button(self):
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(., 'Sign in')]"))
        ).click()

    def login(self, email, password):  # ✅ Correct
        self.click_login_button()
        self.enter_email(email)
        self.enter_password(password)
        time.sleep(1)
        self.click_Signin_button()
        time.sleep(3)

    def logout(self):
        wait = WebDriverWait(self.driver, 10)
        try:
            logout_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Logout']"))
            )
            logout_button.click()
            print("✅ Successfully logged out")
        except TimeoutException:
            print("⚠ Logout button not found or not clickable")


