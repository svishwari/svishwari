"""MongoDB Connector."""

from os import getenv
from huxunifylib.database.client import DatabaseClient

# get mongo connection params
MONGO_DB_HOST = getenv("MONGO_DB_HOST")
MONGO_DB_PORT = getenv("MONGO_DB_PORT")
MONGO_DB_USERNAME = getenv("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = getenv("MONGO_DB_PASSWORD")


def get_db_client() -> DatabaseClient:
    return DatabaseClient(
        host=MONGO_DB_HOST,
        port=int(MONGO_DB_PORT) if self.config_env.get(MONGO_DB_PORT) else None,
        username=self.MONGO_DB_USERNAME,
        password=MONGO_DB_PASSWORD,
    ).connect()
