import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from share import get_mongo_client
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Initate Data Base client
DB_CLIENT = get_mongo_client()

# Data Sources List
DATA_SOURCES = [
    {
        c.DATA_SOURCE_NAME: "Bluecore",
        c.JOB_STATUS: "Active",
        c.ENABLED: True,
        c.ADDED: False,  # newone
    },
    {
        c.DATA_SOURCE_NAME: "NetSuite",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Aqfer",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Facebook",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Salesforce Marketing Cloud",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Adobe Experience",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mailchimp",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon Advertising",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon S3",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Aol",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Apache Hive",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Azure",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "GA360",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Ads",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Gmail",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Analytics",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "IBM DB2",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "InsightIQ",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Jira",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mandrill",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Maria DB",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Medallia",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Microsoft Azure SQL",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Qualtrics",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Tableau",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Twilio",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
]

# Inserting Data Sources into Data Sources Collection

sources_collection = DB_CLIENT[c.DATA_MANAGEMENT_DATABASE][
    c.CDP_DATA_SOURCES_COLLECTION
]
sources_collection.insert_many(DATA_SOURCES)
inserted_sources = [source_data[c.DATA_SOURCE_NAME] for source_data in DATA_SOURCES]
logging.info("Added %d data source(s) to %s", len(inserted_sources), sources_collection)

# Destinations List
DELIVERY_PLATFORMS = [
    {
        c.DELIVERY_PLATFORM_NAME: "Salesforce Marketing Cloud",
        c.JOB_STATUS: "Active",
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Facebook",
        c.JOB_STATUS: "Active",
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Google Ads",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Amazon Advertising",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Adobe Experience",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Twilio",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "SAP",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Qualtrics",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Litmus",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Fullstory",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "QuantumMetric",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Medallia",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Mailchimp",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        c.ADDED: False,
    },
]

# Insertion of Delivery Platforms Collection
destinations_collection = DB_CLIENT[c.DATA_MANAGEMENT_DATABASE][
    c.DELIVERY_PLATFORM_COLLECTION
]
destinations_collection.insert_many(DELIVERY_PLATFORMS)
inserted_destinations = [
    destination_data[c.DELIVERY_PLATFORM_NAME] for destination_data in DATA_SOURCES
]
logging.info(
    "Added %d delivery platforms(s) to %s",
    len(inserted_destinations),
    destinations_collection,
)
