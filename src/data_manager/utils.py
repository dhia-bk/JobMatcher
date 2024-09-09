import asyncio
from datetime import datetime
import json
import os
from MongoManager import MongoManager  
from DataProcessor import DataProcessor
# from data_manager.PostgresManager import PostgresManager


conn_string = "postgresql://Ml_Jobs_owner:T96qkisZEFIJ@ep-purple-fire-a2n3tg6x.eu-central-1.aws.neon.tech/Ml_Jobs?sslmode=require"


# po = PostgresManager(conn_string)
da = DataProcessor()

mongo_uri = "mongodb+srv://dhia_braiek:FVJTdjEFTdkVyHXo@machinelearningjobs.qqhbz.mongodb.net/?retryWrites=true&w=majority&appName=MachineLearningJobs"

db_name = 'MLjobs'
collection_name = 'MLjobs'

# Initialize MongoManager
mongo_manager = MongoManager(uri=mongo_uri, db_name=db_name, collection_name=collection_name)

mongo_manager.save_data_to_mongo(r"data\2024-09-08.json")
# async def main():
#     connected = await mongo_manager.ping_connection()
#     if connected:
#         print("Successfully connected to MongoDB.")
#     else:
#         print("Failed to connect to MongoDB.")
#         return

#     # await mongo_manager.save_data_to_mongo(file_path)
#     print("Retrieving today's jobs from LinkedIn...")
#     linkedin_jobs = await mongo_manager.get_todays_jobs_from('LinkedIn', collection_name)
#     if linkedin_jobs:
#         print(f"Retrieved {len(linkedin_jobs)} jobs from LinkedIn.")
#     else:
#         print("No jobs found from LinkedIn today.")


#     # Close MongoDB connection
#     closed = await mongo_manager.close_connection()
#     if closed:
#         print("Successfully closed the connection to MongoDB.")
#     else:
#         print("Failed to close the connection to MongoDB.")

#     cleaned_lin = da.clean_indeed(linkedin_jobs)
#     print("cleaned data")
#     # Rename columns to match PostgreSQL expected names
#     cleaned_lin.rename(columns={
#     'Job Title': 'Job_Title',
#     'Company Name': 'Company_Name',
#     'Posting Date': 'Posting_Date'
# }, inplace=True)


#     conn = po._connect()

#     print("adding to postgress")

#     po.add_jobs(cleaned_lin, conn)
#     print('done!')

# if __name__ == "__main__":
#     asyncio.run(main())