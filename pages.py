import pytest
from pages.home_page import HomePage

class TestJobGenious:
    def test_get_started_button_redirects_to_signup(self, driver):
        page = HomePage(driver)
        page.load("https://www.gojobgenius.com/")
        page.click_get_started()
        assert "signup" in driver.current_url.lower()
