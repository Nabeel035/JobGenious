import time


from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data
from form_fields import FormFields
from data import WORK_ARRANGEMENT


class JobDescriptionPage:
    def __init__(self, driver):
        self.driver = driver
        self.form_field = FormFields(driver)  # Initialize helper class
        self.wait = WebDriverWait(driver, 10)
        self.wait = WebDriverWait(driver, 10)

    # Locators
    CREATE_JOB_BUTTON = (By.XPATH, "//button[contains(., 'Create Job Description')]")
    NEW_JOB_BUTTON = (By.XPATH, "//button[contains(., 'New Job Description')]")
    JOB_LIST_ITEMS = (By.CSS_SELECTOR, "table tbody tr")  # Adjust if job list uses different HTML
    JOB_TITLE_FIELD = (By.NAME, "job_title")
    #WORK_ARRANGEMENT_FIELD = (By.XPATH, f"//div[@role='option'][normalize-space()='{WORK_ARRANGEMENT}']")
    WORK_LOCATION_FIELD = (By.NAME, "work_location")
    EMPLOYMENT_TYPE_FIELD = (By.NAME, "employment_type")
    EXPERIENCE_LEVEL_FIELD = (By.NAME, "experience_level")
    SALARY_RANGE_FIELD = (By.NAME, "salary_range")
    ADDITIONAL_DETAILS_FIELD = (By.NAME, "additional_details")
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Generate Job Description']")



    def close_toast_popup(self):
        try:
            toast_close = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'toast-close')]"))
            )
            toast_close.click()
            print("✅ Toast popup closed.")
        except:
            print("ℹ️ No toast popup found.")

    def job_already_exists(self):
        """
        Checks if job description table or any job row exists.
        Returns True if jobs found, otherwise False.
        """
        try:
            self.driver.find_element(By.XPATH, "//table//tr[td]")
            return True
        except:
            return False

    def open_job_list_page(self):
        try:
            job_list_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Job Description"))
            )
            job_list_link.click()
            print("✅ Navigated to Job Description list page.")
        except:
            print("❌ Unable to open Job Description list page.")
            raise

    def click_new_job_button(self):
        try:
            # Match on the visible text only, not the SVG
            new_job_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[normalize-space(text())='New Job Description']")
                )
            )
            new_job_btn.click()
            print("✅ Clicked 'New Job Description' button.")
        except TimeoutException:
            print("❌ Unable to click 'New Job Description' button.")
            raise

    def click_create_job_button_dashboard(self):
        try:
            create_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Create Job Description')]")
                )
            )
            create_btn.click()
            print("✅ Clicked 'Create Job Description' on dashboard.")
        except:
            print("❌ Unable to click 'Create Job Description' button.")
            raise

    def fill_job_description_form(self):
        driver = self.driver  # Make sure we're using the actual WebDriver instance

        try:
            # 1. Check if jobs already exist
            try:
                existing_jobs = driver.find_elements(By.XPATH, "//table//tr")
                if len(existing_jobs) > 1:  # Assuming first row is table header
                    print("ℹ️ Existing jobs found — opening New Job Description form.")
                    # Navigate to job description page
                    job_desc_link = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Job Description')]"))
                    )
                    job_desc_link.click()
            except Exception:
                print("ℹ️ No existing jobs found.")

            # 2. Click on "+ New Job Description" button
            new_job_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'New Job Description')]"))
            )
            new_job_btn.click()
            print("✅ Clicked 'New Job Description' button.")

            # 3. Wait for the dialog header "Create New Job Description" to appear
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[text()='Create New Job Description']"))
            )
            print("✅ 'Create New Job Description' dialog opened.")

            # 4. Fill job title
            self.form_field.select_job_title()
            time.sleep(2)

            # 5. Select or Create Company
            self.form_field.select_or_create_company(data.HIRING_COMPANY)
            time.sleep(2)

            # 5. Select Work Arrangement/Type
            self.form_field.select_work_arrangement(data.WORK_ARRANGEMENT)
            time.sleep(2)

            # Split WORK_LOCATION into main and qualifier parts (e.g. "Remote - Anywhere" and "Global")
            location_parts = data.WORK_LOCATION.rsplit(" ", 1)
            location_main = location_parts[0]  # e.g. "Remote - Anywhere"
            location_qualifier = location_parts[1] if len(location_parts) > 1 else ""  # e.g. "Global"

            # Call the method from FormFields with work arrangement and location parts
            self.form_field.select_work_location(data.WORK_ARRANGEMENT, location_main, location_qualifier)
            time.sleep(2)

            # Suppose data.WORK_LOCATION = "Remote - Anywhere Global"
            # Split into main and qualifier parts
            location_parts = data.WORK_LOCATION.rsplit(" ", 1)
            location_main = location_parts[0]
            location_qualifier = location_parts[1] if len(location_parts) > 1 else ""

            # 6. Select Work Location
            self.form_field.select_work_location(data.WORK_ARRANGEMENT, location_main, location_qualifier)
            time.sleep(2)

            self.driver.find_element(By.NAME, "employment_type").send_keys(data.EMPLOYMENT_TYPE)
            self.driver.find_element(By.NAME, "experience_level").send_keys(data.EXPERIENCE_LEVEL)
            self.driver.find_element(By.NAME, "salary_range").send_keys(data.SALARY_RANGE)
            self.driver.find_element(By.NAME, "additional_details").send_keys(data.ADDITIONAL_DETAILS)

            # Submit
            self.driver.find_element(*self.SUBMIT_BUTTON).click()
            print("[INFO] Job description created successfully.")

        except Exception as e:
            print(f"❌ Error filling job description form: {e}")
            raise

    def create_job_description(self):
        self.close_toast_popup()

        try:
            if self.job_already_exists():
                print("ℹ️ Job already exists.")
                self.open_job_list_page()
                self.click_new_job_button()
            else:
                print("ℹ️ No existing jobs found.")
                self.click_create_job_button_dashboard()

            self.fill_job_description_form()
        except Exception as e:
            print(f"❌ Error creating job description: {e}")
            raise



