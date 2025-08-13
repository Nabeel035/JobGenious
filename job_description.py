import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
import data
from form_fields import FormFields


class JobDescriptionPage:
    def __init__(self, driver):
        self.driver = driver
        self.form_field = FormFields(driver)  # Initialize helper class
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
            job_title = data.JOB_TITLE  # from data.py

            # Check for duplicates
            existing_titles = [
                row.text.strip()
                for row in driver.find_elements(By.XPATH, "//table//tr/td[1]")  # Assuming first column is job title
            ]

            if job_title in existing_titles:
                print(f"⚠️ Job title '{job_title}' already exists!")
                job_title = f"{job_title} duplicate."
                print(f"ℹ️ Updated title to '{job_title}'.")

            # Pass the final title into your form field selection
            self.form_field.select_job_title(job_title)
            time.sleep(2)

            # 5. Select or Create Company
            self.form_field.select_or_create_company(data.HIRING_COMPANY)
            time.sleep(2)

            # 5. Select Work Arrangement/Type
            self.form_field.select_work_arrangement(data.WORK_ARRANGEMENT)
            time.sleep(2)


            # 6. Select Work Location
            self.form_field.select_work_location(data.WORK_LOCATION)
            time.sleep(2)

            #7 - Select the Job Type
            self.form_field.select_employment_type(data.EMPLOYMENT_TYPE)
            time.sleep(3)

            #8 - Select the Experience
            self.form_field.select_experience_level(data.EXPERIENCE_LEVEL)
            time.sleep(3)

            #9 - Select the Salary Range
            self.form_field.enter_salary_range(data.SALARY_RANGE)
            time.sleep(3)

            #10 - Additional Details
            self.form_field.fill_additional_details(data.ADDITIONAL_DETAILS)
            time.sleep(3)

            # Submit
            self.driver.find_element(*self.SUBMIT_BUTTON).click()
            print("[INFO] Job description created successfully.")

            # Wait for page/job description to load before clicking Download
            download_button = WebDriverWait(driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Download']"))
            )
            download_button.click()
            print("✅ Download button clicked successfully")

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

    def job_list_page(self):
        # Wait for the Job Descriptions link to be clickable
        job_list_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/job-descriptions']"))
        )
        job_list_link.click()

        # Optional: Wait for the job descriptions page to load (adjust locator)
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Job Descriptions')]"))
        )


