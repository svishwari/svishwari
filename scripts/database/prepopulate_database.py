"""Purpose of this file is for populating the following database documents
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

from database.share import get_mongo_client

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Data Sources List
data_sources_constants = [
    {
        c.DATA_SOURCE_NAME: "Bluecore",
        c.DATA_SOURCE_TYPE: c.CDP_DATA_SOURCE_BLUECORE,
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ADDED: True,
    },
    {
        c.DATA_SOURCE_NAME: "NetSuite",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_NETSUITE,
        c.STATUS: c.PENDING,
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Aqfer",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AQFER,
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ADDED: True,
    },
    {
        c.DATA_SOURCE_NAME: "Facebook",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_FACEBOOK,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Salesforce Marketing Cloud",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_SFMC,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Adobe Experience",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_ADOBE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mailchimp",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MAILCHIMP,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon Advertising",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AMAZONADS,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon S3",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AMAZONS3,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Aol",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AOL,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Apache Hive",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_APACHE_HIVE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Azure",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AZUREBLOB,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "GA360",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_GA360,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Ads",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_GOOGLEADS,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Gmail",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_GMAIL,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Analytics",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_GOOGLE_ANALYTICS,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "IBM DB2",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_IBMDB2,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "InsightIQ",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_INSIGHTIQ,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Jira",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_JIRA,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mandrill",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MANDRILL,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Maria DB",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MARIADB,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Medallia",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MEDALLIA,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Microsoft Azure SQL",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AZURESQL,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Qualtrics",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_QUALTRICS,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Tableau",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_TABLEAU,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Sendgrid by Twilio",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_SENDGRID,
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
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Facebook",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_FACEBOOK,
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ADDED: False,
        c.IS_AD_PLATFORM: True,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Google Ads",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_GOOGLE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: True,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Amazon Advertising",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_AMAZON,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: True,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Adobe Experience",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_ADOBE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Sendgrid by Twilio",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_SENDGRID,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "SAP",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_SAP,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Qualtrics",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_QUALTRICS,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Litmus",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_LITMUS,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Fullstory",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_FULLSTORY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "QuantumMetric",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_QUANTUMMETRIC,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Medallia",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_MEDALLIA,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Mailchimp",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_MAILCHIMP,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
]


def drop_collections(database: MongoClient) -> None:
    """Drop collections for writing.

    Args:
        database (MongoClient): Database Client.
    """

    collections = [
        c.CDP_DATA_SOURCES_COLLECTION,
        c.DELIVERY_PLATFORM_COLLECTION,
    ]
    for collection in collections:
        database[c.DATA_MANAGEMENT_DATABASE][collection].drop()


def insert_data_sources(database: MongoClient, data_sources: list) -> None:
    """Inserting Data Sources into Data Sources Collection.

    Args:
        database (MongoClient): MongoDB Client.
        data_sources (List): List of Data Sources Object.
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
        logging.info("Added %s, %s.", data_source[c.DATA_SOURCE_NAME], result_id)
    logging.info("Prepopulate data sources complete.")


def insert_delivery_platforms(database: MongoClient, delivery_platforms: list) -> None:
    """Insertion of Delivery Platforms Collection.

    Args:
        database (MongoClient): MongoDB Client.
        delivery_platforms (List): List of Delivery Platform Objects.
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
