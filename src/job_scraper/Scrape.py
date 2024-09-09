import concurrent.futures
from linkedin_scraper import LinkedInScraper
from GlassDoor_Scraper import GlassDoor_Scraper
from Indeed_Scraper import IndeedInScraper
from utils import time_it

def run_scraper(scraper_class):
    scraper = scraper_class()
    scraper.run_scraper()

@time_it
def Scrape():
    scrapers = [GlassDoor_Scraper, LinkedInScraper, IndeedInScraper]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_scraper, scraper) for scraper in scrapers]  
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception:
                pass    
    print('Done scraping')

Scrape()