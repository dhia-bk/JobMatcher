import asyncio
from data_manager.MongoManager import MongoManager
from data_manager.PostgresManager import PostgresManager
from data_manager.DataProcessor import DataProcessor
import os
from datetime import datetime

MONGO_URI = "mongodb+srv://dhia_braiek:FVJTdjEFTdkVyHXo@machinelearningjobs.qqhbz.mongodb.net/?retryWrites=true&w=majority&appName=MachineLearningJobs"

POSTGRES_CONN_STRING = "postgresql://Ml_Jobs_owner:T96qkisZEFIJ@ep-purple-fire-a2n3tg6x.eu-central-1.aws.neon.tech/Ml_Jobs?sslmode=require"

SCRAPE_DATA_PATH = './data/'  

POSTGRES_TABLE = 'Scraped_Jobs'

async def run_pipeline():
    mongo_manager = MongoManager(MONGO_URI)
    postgres_manager = PostgresManager(POSTGRES_CONN_STRING)
    data_processor = DataProcessor()

    mongo_manager.ping_connection()
    linkedin_data = await mongo_manager.get_todays_jobs_from('LinkedIn')
    print("got data from mongo")
    linkedin_cleaned_df = await data_processor.clean_linkedin(linkedin_data)  
    print(linkedin_cleaned_df.columns)

    print("Step 4: Saving cleaned data to àPostgreSQL...")
    await postgres_manager.connect()
    try:
        await postgres_manager.insert_dataframe(POSTGRES_TABLE, linkedin_cleaned_df)
    except Exception as e:
        print(f"Error inserting data: {e}")
    
    await postgres_manager.close()
    print("Pipeline execution completed.")

if __name__ == '__main__':
    asyncio.run(run_pipeline())