"""MongoDB Access tests."""

import logging
from share import get_mongo_client
import huxunifylib.database.constants as c

# Setup logging
logging.basicConfig(level=logging.INFO)

# Get details on MongoDB configuration.
DATABASE = get_mongo_client()

# Some defines
DATABASE_NAME = "sample_database"
COLLECTION_NAME = "sample_collection"

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
