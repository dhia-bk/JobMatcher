import os
import time
from datetime import datetime

from tenacity import retry, wait_fixed, stop_after_attempt

from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.job_scraper.config import LinkedIn_Config
from src.job_scraper.utils import save_DATA_to_JSON, wait_for_page_load


Linfig = LinkedIn_Config()

class LinkedInScraper:
    
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.email = Linfig.mail
        self.password = Linfig.password
        self.chrome_options = Options()
        self.chrome_options.add_argument("--log-level=3")

    def run_scraper(self):
        try:
            self.driver.get(Linfig.main_url)
            wait_for_page_load(driver = self.driver)
            self.handle_login()
            WebDriverWait(self.driver, 300).until(EC.url_contains(Linfig.feed_url))
            job_ids = self.scrape()
            save_DATA_to_JSON(job_details = job_ids, file_path = os.path.join('data', f'{datetime.now().strftime("%Y-%m-%d")}.json'))
        finally:
            self.driver.close()
            
    def scrape(self):
        DATA = [] 
        jobs_url = Linfig.ML_url
        self.driver.get(jobs_url)
        DATA.extend(self.scrape_page())
        while True :
            button, has_next = self.look_for_next_page_button()
            if not has_next:
                break
            self.go_next_page(button)
            DATA.extend(self.scrape_page())
        return DATA
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def look_for_next_page_button(self):
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, Linfig.next_button_selector)
            return next_button, True
        except NoSuchElementException:
            return None, False
        
    def go_next_page(self, next_button):
        if next_button:
            try:
                next_button.click()
                return True
            except WebDriverException:
                return False
        return False        

    def handle_login(self):
        self.driver.get(Linfig.login_url)
        try:
            self.enter_credentials()
            self.submit_login_form()
        except NoSuchElementException:
            print("Could not log in to LinkedIn. Please check your credentials.")

    def enter_credentials(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.email)
            self.driver.find_element(By.ID, "password").send_keys(self.password)
        except TimeoutException:
            print("Login form not found. Aborting login.")

    def submit_login_form(self):
        try:
            login_button = self.driver.find_element(By.XPATH, Linfig.login_button_selector)
            login_button.click()
        except NoSuchElementException:
            print("Login button not found. Please verify the page structure.")

    def scrape_page(self):
        DATA_Page = []
        _ = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, Linfig.page_is_loaded_selector)))
        list_of_jobs = self.driver.find_element(By.CLASS_NAME, Linfig.jobs_selector)
        job_items = list_of_jobs.find_elements(By.TAG_NAME, "li")
        for li in job_items:
            try:
                li = self.driver.find_element(By.CSS_SELECTOR, f'li[data-occludable-job-id="{li.get_attribute("data-occludable-job-id")}"]')
                id = li.get_attribute("data-occludable-job-id")
                if id:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", li)
                    li.click()
                    time.sleep(2)
                    try:
                        job_details = self.scrape_job(id)
                        DATA_Page.append(job_details)
                    except Exception as e:
                            continue
            except Exception:
                continue

        return DATA_Page
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def scrape_job(self, id):
        try:
            summary_div = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "job-details"))).text.strip()
            company_name = self.driver.find_element(By.CSS_SELECTOR, Linfig.company_name_selector).text.strip()
            location = self.driver.find_element(By.CSS_SELECTOR, Linfig.location_selector).text.strip()
            if company_name not in Linfig.blacklisted_companies and location not in Linfig.blacklisted_countries:
                base_url = Linfig.job_url
                job_link = f"{base_url}{id}"
                job_details = {"URL": job_link, "Source": "LinkedIn", "Posted Date": datetime.now().strftime("%Y-%m-%d"),}
                job_title = self.driver.find_element(By.CSS_SELECTOR, Linfig.job_title_selector).text.strip()
            
                job_type = self.driver.find_element(By.CSS_SELECTOR, Linfig.job_type_selector).text.strip()
                job_details.update({
                                    "Job Title": job_title,
                                    "Company Name": company_name,
                                    "Location": location,
                                    "Summary": summary_div,
                                    "Job Type": job_type
                                })
                return job_details
            else:
                pass
        except Exception:
            raise