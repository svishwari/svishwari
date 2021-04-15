"""This script creates indexes in the database.

   Note: The bash script set_mongo_db_tunnel.sh need to be run prior
   to running this script to setup port forwarding.

   The following environment variables are needed to run the script:

   MONGO_DB_HOST: The name of the host (local host if port forwarding is done).
   MONGO_DB_PORT: The port on the host (local host if port forwarding is done).
   MONGO_DB_USERNAME: The database username (should have write permission).
   MONGO_DB_PASSWORD: The password of the database.
"""

import os
import logging

from pymongo import ASCENDING

import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient

# Get details on MongoDB configuration.
HOST = os.environ.get("MONGO_DB_HOST")
PORT = (
    int(os.environ["MONGO_DB_PORT"]) if "MONGO_DB_PORT" in os.environ else None
)
USERNAME = os.environ.get("MONGO_DB_USERNAME")
PASSWORD = os.environ.get("MONGO_DB_PASSWORD")

# Set the list of indexes; each element is a tuple (database name,
# collection name, and list of field/order pairs to be indexed)
INDEX_LIST = [
    (
        c.DATA_MANAGEMENT_DATABASE,
        c.CONSTANTS_COLLECTION,
        [(c.CONSTANT_NAME, ASCENDING)],
    ),
    (
        c.DATA_MANAGEMENT_DATABASE,
        c.INGESTION_JOBS_COLLECTION,
        [(c.DATA_SOURCE_ID, ASCENDING)],
    ),
    (
        c.DATA_MANAGEMENT_DATABASE,
        c.INGESTED_DATA_COLLECTION,
        [(c.JOB_ID, ASCENDING)],
    ),
    (
        c.DATA_MANAGEMENT_DATABASE,
        c.INGESTED_DATA_STATS_COLLECTION,
        [(c.JOB_ID, ASCENDING)],
    ),
    (
        c.DATA_MANAGEMENT_DATABASE,
        c.AUDIENCES_COLLECTION,
        [(c.JOB_ID, ASCENDING)],
    ),
    (
        c.DATA_MANAGEMENT_DATABASE,
        c.AUDIENCE_INSIGHTS_COLLECTION,
        [(c.AUDIENCE_ID, ASCENDING)],
    ),
    (
        c.DATA_MANAGEMENT_DATABASE,
        c.DELIVERY_JOBS_COLLECTION,
        [(c.AUDIENCE_ID, ASCENDING), (c.DELIVERY_PLATFORM_ID, ASCENDING)],
    ),
    (
        c.DATA_MANAGEMENT_DATABASE,
        c.PERFORMANCE_METRICS_COLLECTION,
        [(c.DELIVERY_JOB_ID, ASCENDING)],
    ),
]

# Setup logging
logging.basicConfig(level=logging.INFO)

# Set up the database client
DB_CLIENT = DatabaseClient(HOST, PORT, USERNAME, PASSWORD).connect()

# Get database
DM_DB = DB_CLIENT[c.DATA_MANAGEMENT_DATABASE]

# Loop through the list and set the indexes
for item in INDEX_LIST:

    database_name = item[0]
    collection_name = item[1]
    index_list = item[2]

    collection = DB_CLIENT[database_name][collection_name]

    logging.info(
        "Creating an index with settings <%s> in collection <%s>...",
        index_list,
        collection.full_name,
    )

    collection.create_index(index_list)

# Add a unique compound index for customer ID
collection = DB_CLIENT[c.DATA_MANAGEMENT_DATABASE][c.INGESTED_DATA_COLLECTION]

field_str = "%s.%s" % (c.INGESTED_DATA, c.S_TYPE_CUSTOMER_ID)
collection.create_index(
    [(field_str, ASCENDING), (c.JOB_ID, ASCENDING)],
    unique=True,
)

logging.info(
    "Creating an unique compound index <(%s, %s)> in collection <%s>...",
    field_str,
    c.JOB_ID,
    collection.full_name,
)


logging.info("Done with creating indexes!")
