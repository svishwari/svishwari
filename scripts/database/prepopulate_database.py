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
        c.DATA_SOURCE_TYPE: "bluecore",
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "NetSuite",
        c.DATA_SOURCE_TYPE: "netsuite",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Aqfer",
        c.DATA_SOURCE_TYPE: "aqfer",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Facebook",
        c.DATA_SOURCE_TYPE: "facebook",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Salesforce Marketing Cloud",
        c.DATA_SOURCE_TYPE: "sfmc",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Adobe Experience",
        c.DATA_SOURCE_TYPE: "adobe",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mailchimp",
        c.DATA_SOURCE_TYPE: "mailchimp",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon Advertising",
        c.DATA_SOURCE_TYPE: "amazonadv",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon S3",
        c.DATA_SOURCE_TYPE: "amazons3",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Aol",
        c.DATA_SOURCE_TYPE: "aol",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Apache Hive",
        c.DATA_SOURCE_TYPE: "apache",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Azure",
        c.DATA_SOURCE_TYPE: "azure",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "GA360",
        c.DATA_SOURCE_TYPE: "ga360",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Ads",
        c.DATA_SOURCE_TYPE: "googleads",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Gmail",
        c.DATA_SOURCE_TYPE: "gmail",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Analytics",
        c.DATA_SOURCE_TYPE: "googleanalytics",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "IBM DB2",
        c.DATA_SOURCE_TYPE: "ibmdb2",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "InsightIQ",
        c.DATA_SOURCE_TYPE: "insightiq",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Jira",
        c.DATA_SOURCE_TYPE: "jira",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mandrill",
        c.DATA_SOURCE_TYPE: "mandrill",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Maria DB",
        c.DATA_SOURCE_TYPE: "mariadb",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Medallia",
        c.DATA_SOURCE_TYPE: "medallia",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Microsoft Azure SQL",
        c.DATA_SOURCE_TYPE: "azuresql",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Qualtrics",
        c.DATA_SOURCE_TYPE: "qualtrics",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Tableau",
        c.DATA_SOURCE_TYPE: "tableau",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Twilio",
        c.DATA_SOURCE_TYPE: "twilio",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
]

# Delivery Platforms List
DELIVERY_PLATFORMS = [
    {
        c.DELIVERY_PLATFORM_NAME: "Salesforce Marketing Cloud",
        c.DELIVERY_PLATFORM_TYPE: "sfmc",
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Facebook",
        c.DELIVERY_PLATFORM_TYPE: "facebook",
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Google Ads",
        c.DELIVERY_PLATFORM_TYPE: "googleads",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Amazon Advertising",
        c.DELIVERY_PLATFORM_TYPE: "amazonadv",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Adobe Experience",
        c.DELIVERY_PLATFORM_TYPE: "adobe",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Twilio",
        c.DELIVERY_PLATFORM_TYPE: "twilio",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "SAP",
        c.DELIVERY_PLATFORM_TYPE: "sap",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Qualtrics",
        c.DELIVERY_PLATFORM_TYPE: "qualtrics",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Litmus",
        c.DELIVERY_PLATFORM_TYPE: "litmus",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Fullstory",
        c.DELIVERY_PLATFORM_TYPE: "fullstory",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "QuantumMetric",
        c.DELIVERY_PLATFORM_TYPE: "quantummetric",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Medallia",
        c.DELIVERY_PLATFORM_TYPE: "medallia",
        c.STATUS: c.COMING_SOON,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Mailchimp",
        c.DELIVERY_PLATFORM_TYPE: "mailchimp",
        c.STATUS: c.COMING_SOON,
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
