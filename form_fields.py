import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import data


class FormFields:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)


    #def select_job_title(self):
        #job_title_field = WebDriverWait(self.driver, 10).until(
         #   EC.presence_of_element_located((By.NAME, "title"))
       # )
        #job_title_field.clear()
        #time.sleep(3)
        #job_title_field.send_keys(data.JOB_TITLE)
        #print(f"✅ Job title filled: {data.JOB_TITLE}")

    def select_job_title(self, title=None):
        """
        Selects or fills in the job title field.
        If `title` is not provided, uses JOB_TITLE from data.py.
        """
        job_title_value = title if title else data.JOB_TITLE

        job_title_field = self.driver.find_element(By.NAME, "title")
        job_title_field.clear()
        job_title_field.send_keys(job_title_value)

    def select_or_create_company(self, company_name):
        wait = WebDriverWait(self.driver, 5)

        # Open dropdown
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Company hiring for this position')]"))
        ).click()

        # Type company name
        search_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Search companies...']")))
        search_input.clear()
        search_input.send_keys(company_name)

        # Match nested <span>
        company_locator = (
            By.XPATH,
            f"//div[@role='option']//*[normalize-space(text())='{company_name}']"
        )

        try:
            wait.until(EC.visibility_of_element_located(company_locator))
            wait.until(EC.element_to_be_clickable(company_locator)).click()
            print(f"✅ Selected existing company: {company_name}")
        except TimeoutException:
            print(f"⚠ Company '{company_name}' not found, creating new one...")
            use_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//button[contains(., 'Use \"{company_name}\"')]")
            ))
            use_button.click()
            print(f"✅ Created and selected new company: {company_name}")

    def select_work_arrangement(self, arrangement):
        valid_options = ["Remote", "On-site", "Hybrid"]
        if arrangement not in valid_options:
            raise ValueError(f"Invalid Work Arrangement: {arrangement}")

        wait = WebDriverWait(self.driver, 15)

        # Wait until label is visible - signals form ready
        wait.until(EC.visibility_of_element_located((
            By.XPATH, "//label[contains(text(),'Work Arrangement')]"
        )))

        # Find the dropdown button relative to label inside same div
        dropdown_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//label[contains(text(),'Work Arrangement')]/parent::div//button[@role='combobox']"
        )))
        dropdown_btn.click()
        time.sleep(3)

        # Wait for dropdown options to appear
        wait.until(EC.presence_of_all_elements_located((
            By.XPATH,
            "//div[@role='option']"
        )))

        # Click desired option
        option = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            f"//div[@role='option' and normalize-space()='{arrangement}']"
        )))
        option.click()

        print(f"✅ Selected work arrangement: {arrangement}")

    def select_work_location(self, location_name):
        """
        Safely select the work location from the dropdown.
        """
        try:
            wait = WebDriverWait(self.driver, 10)

            # 1. Open the Work Location dropdown
            dropdown = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//label[contains(., 'Work Location')]/following-sibling::div")
            ))
            dropdown.click()
            time.sleep(3)
            print(f"✅ Opened Work Location dropdown for: {location_name}")

            # 2. Wait for and click the desired location
            option = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                f"//div[@class='flex items-center justify-between w-full']//span[normalize-space()='{location_name}']"
            )))
            option.click()
            print(f"✅ Selected work location: {location_name}")

            # Scroll to Employment Type label so it's visible before selection
            employment_label = wait.until(EC.presence_of_element_located((
                By.XPATH, "//label[normalize-space()='Employment Type']"
            )))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                       employment_label)
            print("📜 Scrolled to Employment Type section.")

        except TimeoutException:
            print(f"❌ Timeout: Could not find or select work location '{location_name}'")
            raise
        except Exception as e:
            print(f"❌ Error selecting work location '{location_name}': {e}")
            raise


    def select_employment_type(self, option_text):
        wait = WebDriverWait(self.driver, 10)

        valid_options = [
            "Full-time",
            "Part-time",
            "Contract",
            "Freelance",
            "Internship"
        ]

        if option_text not in valid_options:
            raise ValueError(f"Invalid Employment Type: '{option_text}'. Valid: {valid_options}")

        dropdown_btn_xpath = "//label[normalize-space()='Employment Type']/following-sibling::button"
        dropdown_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_btn_xpath)))
        dropdown_btn.click()
        time.sleep(3)

        option_xpath = f"//body//div[@role='option' and normalize-space()='{option_text}']"
        option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option.click()

        print(f"✅ Selected Employment Type: {option_text}")

    def select_experience_level(self, level):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        valid_options = ["Entry Level", "Mid Level", "Senior Level", "Lead Level", "Executive Level"]  # adjust to actual site values
        if level not in valid_options:
            raise ValueError(f"Invalid Experience Level: {level}")

        # Step 1: Click the combobox
        dropdown_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//label[normalize-space()='Experience Level']/following-sibling::button"
        )))
        dropdown_btn.click()
        time.sleep(3)

        # Step 2: Wait for and click the matching option (Radix portals may put it in body)
        option_xpath = f"//body//div[@role='option' and normalize-space()='{level}']"
        option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option.click()

        print(f"✅ Selected Experience Level: {level}")

    def enter_salary_range(self, salary_text):
        wait = WebDriverWait(self.driver, 10)

        print(f"💰 Requested salary range: {salary_text}")

        if not salary_text.strip():
            print("⚠️ Salary range is empty — skipping input.")
            return

        salary_input_xpath = "//input[@id='salaryRange']"
        salary_input = wait.until(EC.element_to_be_clickable((By.XPATH, salary_input_xpath)))

        # Clear any existing value before typing
        salary_input.clear()
        salary_input.send_keys(salary_text)

        print(f"✅ Entered salary range: {salary_text}")

    def fill_additional_details(self, details_text):
        wait = WebDriverWait(self.driver, 10)

        # Locate the textarea
        textarea = wait.until(EC.presence_of_element_located((By.ID, "description")))

        # Scroll into view so it's visible
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", textarea)

        # Clear any pre-filled text
        textarea.clear()

        # Enter the provided details
        textarea.send_keys(details_text)

        print(f"📝 Additional Details filled with: {details_text}")


