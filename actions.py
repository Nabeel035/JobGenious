import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data
from conftest import driver


def search_job_description(driver, search_text):
    wait = WebDriverWait(driver, 5)
    search_text = data.SEARCH_JOB
    search_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search job descriptions...']"))
    )
    search_input.clear()
    search_input.send_keys(search_text)
    time.sleep(3)

def click_filter_button(driver):
    wait = WebDriverWait(driver, 10)
    filter_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Filter']"))
    )
    filter_btn.click()

def clear_search(driver):
    driver.refresh()
    time.sleep(2)  # wait for page to reload

def select_status_option(driver, status_option):
    if not status_option:
        # No status option provided, skip selection and keep default
        print("No status option provided, skipping status filter selection.")
        return

    wait = WebDriverWait(driver, 10)

    # Click the "Status" dropdown inside the filter panel
    status_dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[text()='All Statuses']]")
    ))
    status_dropdown.click()
    time.sleep(2)

    # Now click the parent div of the span with the status text
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//div[span[text()='{status_option}']]")
    ))
    option.click()


def select_company_option(driver, company_name):
    if not company_name:
        print("No company name provided, skipping company filter selection.")
        return

    wait = WebDriverWait(driver, 10)

    # Click the "Company" dropdown inside the filter panel
    company_dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[text()='All Companies']]")
    ))
    company_dropdown.click()
    time.sleep(2)

    # Now click the parent div of the span with the company name text
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//div[span[text()='{company_name}']]")
    ))
    option.click()


def select_sort_by_option(driver, option_text):
    if not option_text:
        print("No sort option provided, skipping sort selection.")
        return

    wait = WebDriverWait(driver, 10)

    # Click the "Sort By" dropdown inside the filter panel (default text assumed "Newest First")
    sort_dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[text()='Newest First']]")
    ))
    sort_dropdown.click()
    time.sleep(2)

    # Now click the parent div of the span with the sort option text
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//div[span[text()='{option_text}']]")
    ))
    option.click()

JOB_ACTIONS = {
    "All Jobs": ["View", "Edit", "Publish", "Share via Email", "Duplicate", "Archive", "Delete"],
    "Active": ["View", "Edit", "Post to Job Boards", "Pause", "Mark as filled", "Share via Email", "Duplicate", "Archive"],
    "Draft": ["View", "Edit", "Publish", "Share via Email", "Duplicate", "Archive", "Delete"],
    "Paused": ["View", "Edit", "Resume", "Share via Email", "Duplicate", "Archive"],
    "Filled": ["View", "Reopen", "Share via Email", "Duplicate", "Archive"],
    "Archived": ["View", "Share via Email", "Duplicate"]
}

def perform_job_action(driver, job_row_element, job_status, action_name, timeout=10):
    """
    Given the WebDriver, a job row element (the container for a specific job),
    job status string, and the desired action name, this function clicks the ellipsis
    button for that job, waits for the menu, and selects the specified action.

    Args:
        driver: Selenium WebDriver instance
        job_row_element: Selenium WebElement representing the job row/container
        job_status (str): Status of the job, must be one of keys in JOB_ACTIONS
        action_name (str): The action to perform, must be allowed for the job_status
        timeout (int): Max seconds to wait for elements

    Raises:
        ValueError if job_status or action_name is invalid
        TimeoutException if elements are not found/clickable
    """
    wait = WebDriverWait(driver, timeout)

    # Validate inputs
    if job_status not in JOB_ACTIONS:
        raise ValueError(f"Invalid job status '{job_status}'. Must be one of {list(JOB_ACTIONS.keys())}")
    if action_name not in JOB_ACTIONS[job_status]:
        raise ValueError(f"Action '{action_name}' not allowed for status '{job_status}'. Allowed: {JOB_ACTIONS[job_status]}")

    # 1. Find and click the ellipsis (more options) button inside this job row
    more_options_button = wait.until(
        EC.element_to_be_clickable(job_row_element.find_element(By.CSS_SELECTOR, "button[aria-haspopup='menu']"))
    )
    more_options_button.click()

    # 2. Wait for the menu to appear — assume it appears as a visible container near this button
    # For example, a popup menu with role='menu' or similar (adjust selector as needed)
    menu = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='menu'], ul[role='menu']"))
    )

    # 3. Find the menu option by visible text matching action_name inside the menu
    # This assumes menu options have role='menuitem' or are clickable spans/divs with text
    action_option = wait.until(
        EC.element_to_be_clickable(menu.find_element(By.XPATH, f".//*[normalize-space(text())='{action_name}']"))
    )

    # 4. Click the action
    action_option.click()

    # Optional small wait for action to process (adjust or remove as needed)
    time.sleep(1)