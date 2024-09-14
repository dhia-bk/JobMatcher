import time
from datetime import datetime
import concurrent.futures
import os 

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from contextlib import closing

from src.job_scraper.config import Indeed_Config
from src.job_scraper.utils import save_DATA_to_JSON


Infig = Indeed_Config()

class IndeedInScraper:
    
    def __init__(self):
        pass

    def run_scraper(self):
        all_jobs = self.scrape_all_jobs()
        save_DATA_to_JSON(job_details = all_jobs, file_path = os.path.join('data', f'{datetime.now().strftime("%Y-%m-%d")}.json')) 

    def scrape_all_jobs(self):
        nbr_of_jobs = self.get_nbr_of_jobs()
        base_url = Infig.ML_url
        page_urls = self.get_page_urls(base_url, nbr_of_jobs)
        all_jobs = []
        time.sleep(3)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.scrape_page, url): url for url in page_urls}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    page_jobs = future.result()
                    all_jobs.extend(page_jobs)
                except Exception as e:
                    print(f"Error scraping page {url}: {e}") 
        return all_jobs
    
    def get_nbr_of_jobs(self):
        driver = driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        with closing(driver):
            try:
                driver.get(Infig.ML_url)
                nbr = driver.find_element(By.CSS_SELECTOR, "#jobsearch-JapanPage > div > div.css-hyhnne.e37uo190 > div > div.css-pprl14.eu4oa1w0 > div.jobsearch-JobCountAndSortPane.css-lrjfwh.eu4oa1w0 > div > div > div.jobsearch-JobCountAndSortPane-jobCount.css-13jafh6.eu4oa1w0").text
                nbr = int(nbr.replace('jobs', "").strip())
                driver.close()
                return nbr 
            except Exception as e:
                print("ERROR Extracting the number of job listings\n check the CSS SELECTOR (nbr_selector) IN THE CONFIG FILE")    
        
    def get_page_urls(self, base_url, nbr_of_jobs):
        page_urls = []
        if nbr_of_jobs <= 10:
            page_urls.append(base_url)
        else:
            pages = (nbr_of_jobs // 10) + (1 if nbr_of_jobs % 10 != 0 else 0)
            for page in range(pages):
                page_url = f"{base_url}?start={page * 10}"
                page_urls.append(page_url)
        return page_urls

    def scrape_page(self, url):
        try:
            driver = driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            page_data = []
            driver.get(url)
            jobs_div = driver.find_element(By.CSS_SELECTOR, Infig.jobs_div_selector)
            joblist = jobs_div.find_element(By.TAG_NAME,"ul")
            jobs = joblist.find_elements(By.TAG_NAME, "li")
            for job in jobs:
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", job)
                    job.click()
                    time.sleep(5)
                    job_details = self.scrape_job(job, driver)
                    page_data.append(job_details)
                except Exception:
                    pass
        finally:
            driver.close()
            return page_data  
     
    def scrape_job(self, job, driver):
        try:
            jobTitle_companyName_Place = job.find_elements(By.TAG_NAME, "table")[0].text
            url = job.find_element(By.TAG_NAME, "a").get_attribute("href")
            description = driver.find_element(By.ID, "jobDescriptionText").text
            job_details = {"URL": url, 
                           "Source": "Indeed", 
                           "Posted Date": datetime.now().strftime("%Y-%m-%d"),
                           "Info" : jobTitle_companyName_Place,
                           "Description" : description
                           }
            return job_details
        except Exception:
            return None