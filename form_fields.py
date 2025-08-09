from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import data


class FormFields:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def select_job_title(self):
        job_title_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "title"))
        )
        job_title_field.clear()
        job_title_field.send_keys(data.JOB_TITLE)
        print(f"✅ Job title filled: {data.JOB_TITLE}")

    def select_or_create_company(self, company_name):
        wait = WebDriverWait(self.driver, 5)

        # 1️⃣ Open the "Hiring Company" dropdown
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Company hiring for this position')]"))
        ).click()

        # 2️⃣ Wait for search input to appear and type the company name
        search_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Search companies...']")
        ))
        search_input.clear()
        search_input.send_keys(company_name)

        try:
            # 3️⃣ If the company exists in the list, click it
            existing_company = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(@class,'company-option') and text()='{company_name}']"))
            )
            existing_company.click()
            print(f"Selected existing company: {company_name}")

        except:
            # 4️⃣ Otherwise, click the "Use 'Company_Name'" button to create it
            use_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//button[contains(., 'Use \"{company_name}\"')]"))
            )
            use_button.click()
            print(f"Created and selected new company: {company_name}")

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

    def select_option_by_parts(self, main_text, qualifier_text=""):
        """
        Generic method to select dropdown option where label is split into main and qualifier parts.
        qualifier_text is optional.
        """

        # Wait for options container and click dropdown if needed (adjust locator as needed)
        # Assuming dropdown is already open when this method is called
        # If not, you can add logic to click the dropdown before calling this method

        if qualifier_text:
            option_xpath = (
                f"//div[@role='option' and "
                f".//span[normalize-space()='{main_text}'] and "
                f".//div[contains(@class, 'rounded-full') and normalize-space()='{qualifier_text}']]"
            )
        else:
            option_xpath = (
                f"//div[@role='option' and .//span[normalize-space()='{main_text}']]"
            )

        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option.click()
        print(f"✅ Selected option: '{main_text}' '{qualifier_text}'")

    def select_work_location(self, work_arrangement, location_main, location_qualifier=""):
            """
            Select Work Location based on dependent Work Arrangement.
            """

            valid_options_map = {
                "Remote": [
                    ("Remote - Anywhere", "Global"),
                    ("Remote - US Only", ""),
                    ("Remote - North America", ""),
                    ("Remote - EST Timezone", ""),
                    ("Remote - CST Timezone", ""),
                    ("Remote - MST Timezone", ""),
                    ("Remote - PST Timezone", ""),
                ],
                "On-site": [
                    ("New York, NY", ""),
                    ("Los Angeles, CA", ""),
                    ("Chicago, IL", ""),
                    ("Houston, TX", ""),
                    ("Phoenix, AZ", ""),
                    ("Philadelphia, PA", ""),
                    ("San Antonio, TX", ""),
                ],
                "Hybrid": [
                    ("Remote - Anywhere", "Global"),
                    ("New York, NY", ""),
                    ("Los Angeles, CA", ""),
                    ("Chicago, IL", ""),
                    ("Houston, TX", ""),
                    ("Phoenix, AZ", ""),
                    ("Philadelphia, PA", ""),
                    ("San Antonio, TX", ""),
                ]
            }

            if work_arrangement not in valid_options_map:
                raise ValueError(f"Unknown work arrangement: {work_arrangement}")

            valid_locations = valid_options_map[work_arrangement]

            if (location_main, location_qualifier) not in valid_locations:
                raise ValueError(
                    f"Invalid Work Location '{location_main} {location_qualifier}'. Expected one of {valid_locations}")

            wait = WebDriverWait(self.driver, 15)

            # Wait for Work Location label to ensure dropdown is ready
            wait.until(EC.visibility_of_element_located((
                By.XPATH, "//label[contains(text(),'Work Location')]"
            )))

            # Open the dropdown
            dropdown_btn = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//label[contains(text(),'Work Location')]/parent::div//button[@role='combobox']"
            )))
            dropdown_btn.click()

            # Wait for all options to appear
            wait.until(EC.presence_of_all_elements_located((
                By.XPATH, "//div[@role='option']"
            )))

            # Build XPath for option ignoring SVG and matching visible text exactly
            # The text node will be inside a div child ignoring the SVG sibling
            if location_qualifier:
                # Match main text inside a div plus qualifier inside sibling div (like "Global")
                xpath_option = (
                    f"//div[@role='option' and .//div[normalize-space(text())='{location_main}'] "
                    f"and .//div[contains(text(),'{location_qualifier}')]]"
                )
            else:
                # Match the visible text ignoring SVG inside a div
                xpath_option = (
                    f"//div[@role='option' and .//div[normalize-space(text())='{location_main}']]"
                )

            option = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                xpath_option
            )))
            option.click()

            print(f"✅ Selected work location: {location_main} {location_qualifier}".strip())