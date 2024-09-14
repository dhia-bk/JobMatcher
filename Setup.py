import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse
from src.data_manager.config import POSTGRES_CONN_STRING 

db_config = urlparse(POSTGRES_CONN_STRING)
        self.db_params = {
            'dbname': url.path[1:],
            'user': url.username,
            'password': url.password,
            'host': url.hostname,
            'port': url.port
        }

create_scraped_jobs_table = """
CREATE TABLE IF NOT EXISTS Scraped_Jobs (
    "ID" VARCHAR(255) PRIMARY KEY, 
    "Source" VARCHAR(255), 
    "Job Title" VARCHAR(255), 
    "Company Name" VARCHAR(255), 
    "Location" TEXT, 
    "Posting Date" DATE, 
    "Description" TEXT, 
    "URL" TEXT
);
"""

create_job_recommendation_table = """
CREATE TABLE IF NOT EXISTS job_recommendation (
    job_id VARCHAR PRIMARY KEY,
    score FLOAT8,
    FOREIGN KEY (job_id) REFERENCES Scraped_Jobs("ID")
    ON DELETE CASCADE
);
"""

create_job_embeddings_table = """
CREATE TABLE IF NOT EXISTS job_embeddings (
    job_id INT PRIMARY KEY,
    job_embedding FLOAT8[]
);
"""

def create_tables():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()        
        cursor.execute(create_scraped_jobs_table)
        cursor.execute(create_job_recommendation_table)
        cursor.execute(create_job_embeddings_table)
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    create_tables()
