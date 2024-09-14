from datetime import datetime
import asyncio
import pandas as pd
from src.data_manager.MongoManager import MongoManager
from src.data_manager.PostgresManager import PostgresManager
from src.data_manager.DataProcessor import DataProcessor
from src.Job_Matcher import JobMatcher
from src.job_scraper.Scrape import Scrape

    
MONGO_URI = "....."

POSTGRES_CONN_STRING = "......."

SCRAPED_DATA_PATH = "./data/"

RESUME_PATH = "./Final - Resume.pdf"

from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text


async def main(mongo_uri: str, postgres_conn_string: str):
    Scrape()

    mongo_manager = MongoManager(uri=mongo_uri)
    mongo_manager.ping_connection()
    mongo_manager.save_data_to_mongo(rf"{SCRAPED_DATA_PATH}{datetime.now().strftime("%Y-%m-%d")}.json")
    indeed_jobs = await mongo_manager.get_todays_jobs_from("Indeed")
    linkedin_jobs = await mongo_manager.get_todays_jobs_from("LinkedIn")
    glassdoor_jobs = await mongo_manager.get_todays_jobs_from("Glassdoor")
    mongo_manager.close_connection()
    
    data_processor = DataProcessor()
    processed_indeed_jobs = await data_processor.clean_indeed(indeed_jobs)
    processed_linkedin_jobs = await data_processor.clean_linkedin(linkedin_jobs)
    processed_glassdoor_jobs = await data_processor.clean_glassdoor(glassdoor_jobs)


    descriptions = pd.concat([
    processed_indeed_jobs[['ID', 'Description']],
    processed_linkedin_jobs[['ID', 'Description']],
    processed_glassdoor_jobs[['ID', 'Description']]
    ])
    descriptions.reset_index(drop=True, inplace=True)


    async with PostgresManager(postgres_conn_string) as postgres_manager:
        await postgres_manager.connect()
        await postgres_manager.insert_dataframe('scraped_jobs', processed_indeed_jobs)
        await postgres_manager.insert_dataframe('scraped_jobs', processed_linkedin_jobs)
        await postgres_manager.insert_dataframe('scraped_jobs', processed_glassdoor_jobs)
        await postgres_manager.close()
    
    matcher = JobMatcher()
    vector_embedding_df = matcher.batch_encode(descriptions)
    resume = extract_text_from_pdf(RESUME_PATH)
    resume_encoded = matcher.encode_resume(resume)
    vector_df = matcher.vector_search(resume_encoded, vector_embedding_df)
    bm25_df = matcher.bm25_search(resume, descriptions)
    reccomendation_df = matcher.reciprocal_rank_fusion(vector_df, bm25_df)

    async with PostgresManager(postgres_conn_string) as postgres_manager:
        await postgres_manager.connect()
        await postgres_manager.insert_dataframe('job_embeddings', vector_embedding_df)
        await postgres_manager.insert_dataframe('job_recommendation', reccomendation_df)
        await postgres_manager.close()


if __name__ == "__main__":
    asyncio.run(main(MONGO_URI, POSTGRES_CONN_STRING))
