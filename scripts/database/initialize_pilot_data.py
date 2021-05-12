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
        c.DELIVERY_PLATFORM_NAME: "Bluecore",
        c.JOB_STATUS: "Active",
        c.ENABLED: True,
        "added": False,  # newone
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Netsuite",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Aqfer",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Facebook",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Salesforce Marketing Cloud",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Twilio",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Google Ads",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Tableau",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Adobe Experience",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Mailchimp",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
]

# Inserting Data Sources into Data Sources Collection

sources_collection = DB_CLIENT[c.DATA_MANAGEMENT_DATABASE][
    c.CDP_DATA_SOURCES_COLLECTION
]
sources_collection.insert_many(DATA_SOURCES)
inserted_sources = [source_data["name"] for source_data in DATA_SOURCES]
logging.info(
    "Added these data sources in the cdp_data_sources collection", inserted_sources
)

# Destinations List
DESTINATIONS = [
    {
        c.DELIVERY_PLATFORM_NAME: "Salesforce Marketing Cloud",
        c.JOB_STATUS: "Active",
        c.ENABLED: True,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Facebook",
        c.JOB_STATUS: "Active",
        c.ENABLED: True,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Google Ads",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Amazon Advertising",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Adobe Experience",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Twilio",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "SAP",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Qualtrics",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Litmus",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Fullstory",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "QuantumMetric",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Medallia",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Mailchimp",
        c.JOB_STATUS: "Pending",
        c.ENABLED: False,
        "added": False,
    },
]

# Insertion of Delivery Platforms Collection
destinations_collection = DB_CLIENT[c.DATA_MANAGEMENT_DATABASE][
    c.DELIVERY_PLATFORM_COLLECTION
]
destinations_collection.insert_many(DESTINATIONS)
inserted_destinations = [destination_data["name"] for destination_data in DATA_SOURCES]
logging.info(
    "Added these destinations in the delivery_platforms collection",
    inserted_destinations,
)
