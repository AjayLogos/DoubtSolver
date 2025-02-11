#%%
from psycopg_pool import ConnectionPool
import os
from dotenv import load_dotenv
#%%
load_dotenv()

# PostgreSQL database connection details
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")


class PostgresAdapter:
    def __init__(self) -> None:
        self.dsn = f"dbname={DATABASE_NAME} user={DATABASE_USER} password={DATABASE_PASSWORD} host={DATABASE_HOST} port={DATABASE_PORT}"
        self.connection = None

    def connect(self):
        if self.connection == None:
            self.connection = ConnectionPool(
                min_size=1,  # Minimum number of idle connections
                max_size=10,
                conninfo=self.dsn,
            )

    def get_pool_connection(self):
        if self.connection == None:
            self.connect()
        return self.connection

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

