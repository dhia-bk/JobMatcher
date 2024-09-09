import asyncpg
import pandas as pd
from urllib.parse import urlparse


class PostgresManager:
    def __init__(self, conn_string):
        url = urlparse(conn_string)
        self.db_params = {
            'dbname': url.path[1:],
            'user': url.username,
            'password': url.password,
            'host': url.hostname,
            'port': url.port
        }
        self.conn = None
        
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self):
        try:
            self.conn = await asyncpg.connect(
                user=self.db_params['user'],
                password=self.db_params['password'],
                database=self.db_params['dbname'],
                host=self.db_params['host'],
                port=self.db_params['port']
            )
            print("Connected to the database.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    async def execute_query(self, query, params=None):
        try:
            async with self.conn.transaction():
                await self.conn.execute(query, *params if params else [])
            print("Query executed successfully.")
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    async def fetch_data(self, query, params=None):
        try:
            rows = await self.conn.fetch(query, *params if params else [])
            return rows
        except Exception as e:
            print(f"Error fetching data: {e}")
            raise

    async def fetch_data_as_dataframe(self, query, params=None):
        try:
            rows = await self.fetch_data(query, params)
            df = pd.DataFrame(rows, columns=[desc.name for desc in self.conn.get_fields(query)])
            return df
        except Exception as e:
            print(f"Error loading data into DataFrame: {e}")
            raise

    async def insert_dataframe(self, table, data: pd.DataFrame):
        try:
            async with self.conn.transaction():
                columns = ', '.join([f'"{col}"' for col in data.columns])
                values = ', '.join([f"${i+1}" for i in range(len(data.columns))])
                insert_query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
                for row in data.itertuples(index=False, name=None):
                    await self.conn.execute(insert_query, *row)
            print(f"Inserted {len(data)} rows into {table}.")
        except Exception as e:
            print(f"Error inserting data: {e}")
            raise

    async def close(self):
        try:
            await self.conn.close()
            print("Database connection closed.")
        except Exception as e:
            print(f"Error closing the connection: {e}")
            raise