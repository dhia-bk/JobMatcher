import re
from urllib.parse import urlparse
import pandas as pd
from typing import List, Dict
from bson import ObjectId
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class DataProcessor:

    def __init__(self) -> None:
        self.processed_jobs_cache = {}

    async def _process_job(self, job: Dict, fields_mapping: Dict[str, str], split_info: bool = False) -> Dict:
        try:
            job_id = str(job.get("_id")) if isinstance(job.get("_id"), ObjectId) else job.get("_id")
            job_title = job.get(fields_mapping['Job Title'], '').strip()
            company_name = job.get(fields_mapping['Company Name'], '').strip()
            location = job.get(fields_mapping['Location'], '').strip()
            key = (job_title, company_name)
            if key in self.processed_jobs_cache:
                self.processed_jobs_cache[key]['Location'] += f" / {location}"
                return None  

            processed_job = {
                'ID': job_id,
                'Source': job.get("Source"),
                'Job Title': job_title,
                'Company Name': company_name,
                'Location': location,
                'Posting Date': pd.to_datetime(job.get("Posted Date"), errors='coerce'),
                'Description': job.get(fields_mapping['Description'], ''),
                'URL': job.get("URL")
            }

            if split_info:
                info_lines = job.get(fields_mapping['Company Name'], '').split('\n')
                processed_job['Company Name'] = info_lines[0].strip() if len(info_lines) > 0 else ''
                processed_job['Location'] = info_lines[3].strip() if len(info_lines) > 3 else ''
                if fields_mapping['Description'] == 'Info':
                    processed_job['Description'] = ' '.join(info_lines[5: info_lines.index("Show more")]) if "Show more" in info_lines else ''

            self.processed_jobs_cache[key] = processed_job
            return processed_job
        except Exception as e:
            return None

    async def clean_data(self, mongo_data: List[Dict], fields_mapping: Dict[str, str], split_info: bool = False) -> pd.DataFrame:
        self.processed_jobs_cache = {}  
        cleaned_data = [
            processed_job for job in mongo_data 
            if (processed_job := await self._process_job(job, fields_mapping, split_info)) is not None
        ]
        return pd.DataFrame(cleaned_data)

    async def clean_linkedin(self, linkedin_mongo: List[Dict]) -> pd.DataFrame:           
        fields_mapping = {
            'Job Title': 'Job Title', 
            'Company Name': 'Company Name',
            'Location': 'Location',
            'Description': 'Summary'
        }
        linkedin_cleaned = await self.clean_data(linkedin_mongo, fields_mapping)
        self.validate_data(linkedin_cleaned)
        return linkedin_cleaned 

    async def clean_indeed(self, indeed_mongo: List[Dict]) -> pd.DataFrame:
        fields_mapping = {
            'Job Title': 'Info', 
            'Company Name': 'Info',
            'Location': 'Remote',
            'Description': 'Description'
        }
        return await self.clean_data(indeed_mongo, fields_mapping)

    async def clean_glassdoor(self, glassdoor_mongo: List[Dict]) -> pd.DataFrame:
        fields_mapping = {
            'Job Title': 'Job Title', 
            'Company Name': 'Info',
            'Location': 'Info',
            'Description': 'Info'
        }
        return await self.clean_data(glassdoor_mongo, fields_mapping, split_info=True)

    @staticmethod
    def validate_data(df: pd.DataFrame) -> pd.DataFrame:
        validation_errors = []
        
        for column in ['ID', 'Source', 'Job Title', 'Company Name', 'Location', 'Posting Date', 'Description', 'URL']:
            if column not in df.columns:
                validation_errors.append(f"Missing required column: {column}")
                continue
            if df[column].isnull().any():
                validation_errors.append(f"Missing values in column: {column}")

        if 'Posting Date' in df.columns:
            invalid_dates = df[~df['Posting Date'].apply(lambda x: isinstance(x, pd.Timestamp))]
            if not invalid_dates.empty:
                validation_errors.append("Invalid date format in 'Posting Date' column")

        if 'URL' in df.columns:
            invalid_urls = df[~df['URL'].apply(lambda x: bool(urlparse(x).scheme))]
            if not invalid_urls.empty:
                validation_errors.append("Invalid URLs in 'URL' column")

        if 'ID' in df.columns:
            duplicate_ids = df[df.duplicated('ID')]
            if not duplicate_ids.empty:
                validation_errors.append("Duplicate job IDs found")

        if validation_errors:
            print("Validation Errors:")
            for error in validation_errors:
                print(f"- {error}")
        else:
            print("Data validation passed.")

        return df

    @staticmethod
    def clean_text(text: str, for_bm25: bool = False) -> str:
        if for_bm25:
            text = re.sub(r'[^\w\s,.?!\'"]+', '', text)
        else:
            text = re.sub(r'[^\w\s,.?!\'"-]+', '', text)
        text = text.replace('\n', ' ').lower()
        if for_bm25:
            tokens = word_tokenize(text)
            stop_words = set(stopwords.words('english'))
            tokens = [word for word in tokens if word not in stop_words]
            cleaned_text = ' '.join(tokens)
        else:
            cleaned_text = re.sub(r'\s+', ' ', text).strip()
        return cleaned_text