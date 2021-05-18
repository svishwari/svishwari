"""
purpose of this file is for populating the following database documents
 - data sources
 - destinations (delivery platforms)
"""
import logging
import huxunifylib.database.constants as c
from huxunifylib.database.cdp_data_source_management import create_data_source
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
)
from share import get_mongo_client

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Initiate Data Base client
DB_CLIENT = get_mongo_client()

# Data Sources List
DATA_SOURCES = [
    {
        c.DATA_SOURCE_NAME: "Bluecore",
        c.STATUS: "Active",
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "NetSuite",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Aqfer",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Facebook",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Salesforce Marketing Cloud",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Adobe Experience",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mailchimp",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon Advertising",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon S3",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Aol",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Apache Hive",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Azure",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "GA360",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Ads",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Gmail",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Analytics",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "IBM DB2",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "InsightIQ",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Jira",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mandrill",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Maria DB",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Medallia",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Microsoft Azure SQL",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Qualtrics",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Tableau",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Twilio",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
]

# Delivery Platforms List
DELIVERY_PLATFORMS = [
    {
        c.DELIVERY_PLATFORM_NAME: "Salesforce Marketing Cloud",
        c.STATUS: "Active",
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Facebook",
        c.STATUS: "Active",
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Google Ads",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Amazon Advertising",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Adobe Experience",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Twilio",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "SAP",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Qualtrics",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Litmus",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Fullstory",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "QuantumMetric",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Medallia",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Mailchimp",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
]

# Inserting Data Sources into Data Sources Collection
logging.info("Prepopulate data sources.")
inserted_ids = []
for i, data_source in enumerate(DATA_SOURCES):
    result_id = create_data_source(DB_CLIENT, category="", **data_source)[c.ID]
    logging.info("Added %s, %s.", data_source[c.DATA_SOURCE_NAME], result_id)
logging.info("Prepopulate data sources complete.")


# Insertion of Delivery Platforms Collection
logging.info("Prepopulate destinations.")
inserted_ids = []
for i, delivery_platform in enumerate(DELIVERY_PLATFORMS):
    result_id = set_delivery_platform(
        DB_CLIENT,
        delivery_platform_type=delivery_platform[c.DELIVERY_PLATFORM_NAME],
        **delivery_platform,
    )[c.ID]
    logging.info(
        "Added %s, %s.", delivery_platform[c.DELIVERY_PLATFORM_NAME], result_id
    )
logging.info("Prepopulate destinations complete.")

logging.info("Prepopulate complete.")
