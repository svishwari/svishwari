"""This script creates indexes in the database.

   Note: The bash script set_mongo_db_tunnel.sh need to be run prior
   to running this script to setup port forwarding.

   The following environment variables are needed to run the script:

   MONGO_DB_HOST: The name of the host (local host if port forwarding is done).
   MONGO_DB_PORT: The port on the host (local host if port forwarding is done).
   MONGO_DB_USERNAME: The database username (should have write permission).
   MONGO_DB_PASSWORD: The password of the database.
"""

import logging
from typing import List

from pymongo import ASCENDING, MongoClient
import huxunifylib.database.constants as db_c
from database.share import get_mongo_client


# Setup logging
logging.basicConfig(level=logging.INFO)


# Set the list of indexes; each element is a tuple (database name,
# collection name, and list of field/order pairs to be indexed)
index_constants = [
    (
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.CONSTANTS_COLLECTION,
        [(db_c.CONSTANT_NAME, ASCENDING)],
    ),
    (
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.INGESTION_JOBS_COLLECTION,
        [(db_c.DATA_SOURCE_ID, ASCENDING)],
    ),
    (
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.INGESTED_DATA_COLLECTION,
        [(db_c.JOB_ID, ASCENDING)],
    ),
    (
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.INGESTED_DATA_STATS_COLLECTION,
        [(db_c.JOB_ID, ASCENDING)],
    ),
    (
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.AUDIENCES_COLLECTION,
        [(db_c.JOB_ID, ASCENDING)],
    ),
    (
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.AUDIENCE_INSIGHTS_COLLECTION,
        [(db_c.AUDIENCE_ID, ASCENDING)],
    ),
    (
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.DELIVERY_JOBS_COLLECTION,
        [
            (db_c.AUDIENCE_ID, ASCENDING),
            (db_c.DELIVERY_PLATFORM_ID, ASCENDING),
        ],
    ),
    (
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.PERFORMANCE_METRICS_COLLECTION,
        [(db_c.DELIVERY_JOB_ID, ASCENDING)],
    ),
    (
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.USER_COLLECTION,
        [(db_c.OKTA_ID, ASCENDING)],
    ),
    (
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.CAMPAIGN_ACTIVITY_COLLECTION,
        [(db_c.DELIVERY_JOB_ID, ASCENDING)],
    ),
]


def set_indexes(database: MongoClient, index_list: List) -> None:
    """Method to set indexes from list.

    Args:
        database (MongoClient): MongoDB Client.
        index_list (list): List of Indexes.
    """

    for item in index_list:
        database_name = item[0]
        collection_name = item[1]
        index_name = item[2]

        collection = database[database_name][collection_name]

        logging.info(
            "Creating an index with settings <%s> in collection <%s>...",
            index_name,
            collection.full_name,
        )

        collection.create_index(index_name)


def add_unique_compound_index(database: MongoClient) -> None:
    """Method to add unique Compound index.

    Args:
        database (MongoClient): MongoDB Client.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.INGESTED_DATA_COLLECTION
    ]

    field_str = f"{db_c.INGESTED_DATA}.{db_c.S_TYPE_CUSTOMER_ID}"
    collection.create_index(
        [(field_str, ASCENDING), (db_c.JOB_ID, ASCENDING)],
        unique=True,
    )

    logging.info(
        "Creating a unique compound index <(%s, %s)> in collection <%s>...",
        field_str,
        db_c.JOB_ID,
        collection.full_name,
    )

    logging.info("Done with creating indexes!")


if __name__ == "__main__":
    # Set up the database client
    db_client = get_mongo_client()

    # Get database
    DM_DB = db_client[db_c.DATA_MANAGEMENT_DATABASE]

    set_indexes(db_client, index_constants)
    add_unique_compound_index(db_client)
