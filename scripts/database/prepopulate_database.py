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
from pymongo import MongoClient

from scripts.database.share import get_mongo_client

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Data Sources List
data_sources_constants = [
    {
        c.DATA_SOURCE_NAME: "Bluecore",
        c.DATA_SOURCE_TYPE: "bluecore",
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ADDED: True,
    },
    {
        c.DATA_SOURCE_NAME: "NetSuite",
        c.DATA_SOURCE_TYPE: "netsuite",
        c.STATUS: c.PENDING,
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Aqfer",
        c.DATA_SOURCE_TYPE: "aqfer",
        c.STATUS: c.PENDING,
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Facebook",
        c.DATA_SOURCE_TYPE: "facebook",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Salesforce Marketing Cloud",
        c.DATA_SOURCE_TYPE: "salesforce",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Adobe Experience",
        c.DATA_SOURCE_TYPE: "adobe-experience",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mailchimp",
        c.DATA_SOURCE_TYPE: "mailchimp",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon Advertising",
        c.DATA_SOURCE_TYPE: "amazon-advertising",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon S3",
        c.DATA_SOURCE_TYPE: "amazon-s3",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Aol",
        c.DATA_SOURCE_TYPE: "aol",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Apache Hive",
        c.DATA_SOURCE_TYPE: "apache-hive",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Azure",
        c.DATA_SOURCE_TYPE: "azure-blob",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "GA360",
        c.DATA_SOURCE_TYPE: "GA360",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Ads",
        c.DATA_SOURCE_TYPE: "google-ads",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Gmail",
        c.DATA_SOURCE_TYPE: "gmail",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Analytics",
        c.DATA_SOURCE_TYPE: "google-analytics",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "IBM DB2",
        c.DATA_SOURCE_TYPE: "IBMDB2",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "InsightIQ",
        c.DATA_SOURCE_TYPE: "insightIQ",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Jira",
        c.DATA_SOURCE_TYPE: "jira",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mandrill",
        c.DATA_SOURCE_TYPE: "mandrill",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Maria DB",
        c.DATA_SOURCE_TYPE: "mariaDB",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Medallia",
        c.DATA_SOURCE_TYPE: "medallia",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Microsoft Azure SQL",
        c.DATA_SOURCE_TYPE: "microsoftAzureSQL",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Qualtrics",
        c.DATA_SOURCE_TYPE: "qualtrics",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Tableau",
        c.DATA_SOURCE_TYPE: "tableau",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Twilio",
        c.DATA_SOURCE_TYPE: "twilio",
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
]

# Delivery Platforms List
delivery_platforms_constants = [
    {
        c.DELIVERY_PLATFORM_NAME: "Salesforce Marketing Cloud",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_SFMC,
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Facebook",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_FACEBOOK,
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Google Ads",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_GOOGLE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Amazon Advertising",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_AMAZON,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Adobe Experience",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_ADOBE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Twilio",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_TWILIO,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "SAP",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_SAP,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Qualtrics",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_QUALTRICS,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Litmus",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_LITMUS,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Fullstory",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_FULLSTORY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "QuantumMetric",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_QUANTUMMETRIC,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Medallia",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_MEDALLIA,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Mailchimp",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_MAILCHIMP,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
]


def drop_collections(database: MongoClient) -> None:
    """
    Drop collections for writing.
    Args:
        database(MongoClient):Database Client

    Returns:
        None
    """

    collections = [
        c.CDP_DATA_SOURCES_COLLECTION,
        c.DELIVERY_PLATFORM_COLLECTION,
    ]
    for collection in collections:
        database[c.DATA_MANAGEMENT_DATABASE][collection].drop()


def insert_data_sources(database: MongoClient, data_sources: list) -> None:
    """
        Inserting Data Sources into Data Sources Collection
    Args:
        database (MongoClient): MongoDB Client
        data_sources (List): List of Data Sources Object

    Returns:
        None
    """

    logging.info("Prepopulate data sources.")

    for data_source in data_sources:
        result_id = create_data_source(
            database,
            data_source[c.DATA_SOURCE_NAME],
            category="",
            added=data_source[c.ADDED],
            enabled=data_source[c.ENABLED],
            source_type=data_source[c.DATA_SOURCE_TYPE],
            status=data_source[c.STATUS],
        )[c.ID]
        logging.info(
            "Added %s, %s.", data_source[c.DATA_SOURCE_NAME], result_id
        )
    logging.info("Prepopulate data sources complete.")


def insert_delivery_platforms(
    database: MongoClient, delivery_platforms: list
) -> None:
    """
        Insertion of Delivery Platforms Collection

    Args:
        database (MongoClient): MongoDB Client
        delivery_platforms (List): List of Delivery Platform Objects

    Returns:

    """

    logging.info("Prepopulate destinations.")

    for delivery_platform in delivery_platforms:
        if (
            delivery_platform[c.DELIVERY_PLATFORM_TYPE]
            in c.SUPPORTED_DELIVERY_PLATFORMS
        ):
            result_id = set_delivery_platform(
                database,
                **delivery_platform,
            )[c.ID]
            logging.info(
                "Added %s, %s.",
                delivery_platform[c.DELIVERY_PLATFORM_NAME],
                result_id,
            )
    logging.info("Prepopulate destinations complete.")


if __name__ == "__main__":
    # Initiate Data Base client
    db_client = get_mongo_client()

    drop_collections(db_client)
    insert_data_sources(db_client, data_sources_constants)
    insert_delivery_platforms(db_client, delivery_platforms_constants)
    logging.info("Prepopulate complete.")
