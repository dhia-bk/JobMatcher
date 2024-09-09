import os
import json
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def save_DATA_to_JSON(file_path: str, job_details: list) -> None:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)        
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
            existing_data.extend(job_details)
        else:
            existing_data = job_details        
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        elapsed_time = datetime.now() - start_time
        minutes, seconds = divmod(elapsed_time.total_seconds(), 60)
        print(f"Elapsed time: {int(minutes)} minutes and {int(seconds)} seconds")
        return result
    return wrapper

def wait_for_page_load(driver, timeout=60):
    try:
        WebDriverWait(driver, timeout).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    except TimeoutException:
        print("Page load timed out.")