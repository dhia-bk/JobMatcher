import os
import json
from datetime import datetime
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi


class MongoManager:
    
    """
    A class to manage MongoDB operations asynchronously.
    
    Attributes:
        uri (str): MongoDB URI for connecting to the database.
        db_name (str): Name of the database to use.
        collection_name (str): Default collection name to use.
    """

    def __init__(self, uri: str, db_name: str = 'MLjobs', collection_name: str = 'MLjobs') -> None:
        self.uri = uri
        self.client = AsyncIOMotorClient(self.uri, server_api=ServerApi('1'))
        self.db_name = db_name
        self.collection_name = collection_name
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        return None

    def __enter__(self):
        self.client = AsyncIOMotorClient(self.uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        return self

    def __exit__(self):
        if self.client:
            self.client.close()

    def ping_connection(self) -> bool:
        try:
            self.client.admin.command('ping')
            return True
        except PyMongoError as e:
            print(f"Failed to ping the connection: {e}")
            return False

    def save_data_to_mongo(self, file_path: str, collection_name: Optional[str] = None) -> bool:
        if not os.path.exists(file_path) or not file_path.endswith('.json'):
            print(f"File path {file_path} is invalid or not a JSON file.")
            return False
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                data = [job for job in data if job is not None]

            if not data:
                print("No valid data to insert.")
                return False

            collection = self.db[collection_name] if collection_name else self.collection
            try:
                if collection.insert_many(data):
                    # os.remove(file_path)
                    return True
                return False
            except Exception as e:
                print(e)
        except (PyMongoError, json.JSONDecodeError, OSError) as e:
            print(f"Failed to save data to MongoDB: {e}")
            return False

    async def get_todays_jobs_from(self, source: str, collection_name: Optional[str] = None) -> List[dict]:
        try:
            query = {
                'Posted Date': datetime.now().strftime("%Y-%m-%d"),
                'Source': source
            }
            collection = self.db[collection_name] if collection_name else self.collection
            matching_jobs = await collection.find(query).to_list(length=None)
            for job in matching_jobs:
                job['_id'] = str(job['_id'])
            return matching_jobs
        except PyMongoError as e:
            print(f"Failed to retrieve jobs: {e}")
            return []

    def close_connection(self) -> bool:
        try:
            self.client.close()
            return True
        except PyMongoError as e:
            print(f"Failed to close the connection: {e}")
            return False
        
URI = "mongodb+srv://dhia_braiek:FVJTdjEFTdkVyHXo@machinelearningjobs.qqhbz.mongodb.net/?retryWrites=true&w=majority&appName=MachineLearningJobs"