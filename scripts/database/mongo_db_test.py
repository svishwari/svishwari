"""MongoDB Access tests."""

import os
import logging

import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient

# Setup logging
logging.basicConfig(level=logging.INFO)

# Get database info
DATABASE_LOCAL_HOST = os.environ.get("DATABASE_LOCAL_HOST")
DATABASE_LOCAL_PORT = (
    int(os.environ["DATABASE_LOCAL_PORT"])
    if "DATABASE_LOCAL_PORT" in os.environ
    else None
)
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

# Some defines
DATABASE_NAME = "sample_database"
COLLECTION_NAME = "sample_collection"

# Connect to Document DB
CLIENT = DatabaseClient(
    DATABASE_LOCAL_HOST,
    DATABASE_LOCAL_PORT,
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
)

assert CLIENT is not None

DATABASE = CLIENT.connect()

assert DATABASE is not None

# Create a test db and cpllection
DOC_DB = DATABASE[DATABASE_NAME]

COLLECTION = DOC_DB[COLLECTION_NAME]

# Insert a document and then find it

DOC = {"test_key": "test_value"}

INSERTED_ID = COLLECTION.insert_one(DOC).inserted_id

assert INSERTED_ID is not None

if INSERTED_ID is not None:
    logging.info("Inserted %s into a test collection!", str(DOC))

COLLECTION.create_index([("test_key", 1)])

ITEM = COLLECTION.find_one({c.ID: INSERTED_ID})

assert ITEM is not None

if ITEM is not None:
    logging.info("Retrieved %s from the test collection!", str(ITEM))

assert "test_key" in ITEM
assert ITEM["test_key"] == DOC["test_key"]

logging.info("Dropping the test collection to cleanup...")

DOC_DB.drop_collection(COLLECTION_NAME)

logging.info("Done with testing document DB!")
