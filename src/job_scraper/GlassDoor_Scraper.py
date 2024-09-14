import os 
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

from src.job_scraper.config import GlassDoor_Config
from src.job_scraper.utils import save_DATA_to_JSON


glassfig = GlassDoor_Config()

class GlassDoor_Scraper():

    def __init__(self) -> None:
        chrome_options = Options()
        self.driver =driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def run_scraper(self):
        DATA = self.scrape()
        save_DATA_to_JSON(job_details = DATA, file_path = os.path.join('data', f'{datetime.now().strftime("%Y-%m-%d")}.json'))

    def scrape(self):
        try:
            self.driver.get(glassfig.ML_url)
            WebDriverWait(self.driver, 3000).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app-navigation")))
            self.click_show_more_button()
            data = self.get_jobs_DATA()
            return data
        finally:
            self.driver.close()

    def click_show_more_button(self):
        while True:
            self.close_pop_up()  
            button, exists = self.locate_show_more_button()
            if not exists:
                break
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                button.click()
                self.close_pop_up() 
            except Exception:
                pass

    def locate_show_more_button(self):
        try:
            button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='load-more']")))
            if isinstance(button, list):
                button = button[0]
            print('found button')
            return button , True
        except Exception as e:
            print('button not found')
            return None, False
        
    def get_jobs_DATA(self):
        DATA = []
        jobs_list = self.driver.find_elements(By.XPATH, "/html/body/div[3]/div[1]/div[4]/div[2]/div[1]/div[2]/ul/li")
        for job in jobs_list:
            try:
                time.sleep(5)
                self.close_pop_up()
                self.driver.execute_script("arguments[0].scrollIntoView(true);", job)
                job.click()
                time.sleep(5)
                DATA.append(self.scrape_job(job))
            except Exception as e:
                pass
        return DATA
        
   
    def scrape_job(self, job):
        try:
            job_title = job.find_element(By.CLASS_NAME,"JobCard_jobTitle___7I6y").text
            
            url = job.find_element(By.CLASS_NAME,"JobCard_jobTitle___7I6y").get_attribute("href")
            try:    
                info = self.driver.find_element(By.CSS_SELECTOR,"#app-navigation > div.PageContainer_pageContainer__CVcfg.Page_fullHeight__QlatA > div.TwoColumnLayout_container___jk7P.TwoColumnLayout_selected__MnOqq.TwoColumnLayout_serp__pCNV6 > div.TwoColumnLayout_columnRight__GRvqO.TwoColumnLayout_selected__MnOqq > div > div.JobDetails_jobDetailsContainer__y9P3L").text
            except Exception:
                print("problem"*5,"location"*5)
            job_details = {"URL": url, 
                               "Source": "GlassDoor", 
                               "Posted Date": datetime.now().strftime("%Y-%m-%d"), 
                               "Job Title" : job_title,
                               "Info" : info}
            return job_details
        except Exception as e:    
            return None

    def close_pop_up(self):
        try:
            element = WebDriverWait(self.driver, 0.5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog'].Modal"))
            )
            close_button = element.find_element(By.CLASS_NAME, 'CloseButton')
            close_button.click()
        except Exception as e:
            pass

        try:
            WebDriverWait(self.driver, 0.5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "modal_Modal__wyPlr"))
            )
            close_button = WebDriverWait(self.driver, 0.5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='job-alert-modal-close']"))
            )
            close_button.click()
        except Exception:
            pass