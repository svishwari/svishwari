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
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_BLUECORE,
        c.CATEGORY: c.CATEGORY_ECOMMERCE,
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ADDED: True,
    },
    {
        c.DATA_SOURCE_NAME: "NetSuite",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_NETSUITE,
        c.CATEGORY: c.CATEGORY_CRM,
        c.STATUS: c.PENDING,
        c.ENABLED: True,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Aqfer",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AQFER,
        c.CATEGORY: c.CATEGORY_MARKETING,
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ADDED: True,
    },
    {
        c.DATA_SOURCE_NAME: "Rest API",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_REST_API,
        c.CATEGORY: c.CATEGORY_API,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "OData",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_ODATA,
        c.CATEGORY: c.CATEGORY_API,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Apache Hive",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_APACHE_HIVE,
        c.CATEGORY: c.CATEGORY_BIG_DATA,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Apache Spark",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_APACHE_SPARK,
        c.CATEGORY: c.CATEGORY_BIG_DATA,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Microsoft Dynamics",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MICROSOFT_DYNAMICS,
        c.CATEGORY: c.CATEGORY_CRM,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Oracle",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_ORACLE_CRM,
        c.CATEGORY: c.CATEGORY_CRM,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Salesforce",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_SALESFORCE,
        c.CATEGORY: c.CATEGORY_CRM,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "SAP",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_SAP,
        c.CATEGORY: c.CATEGORY_CRM,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "ServiceNow",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_SERVICE_NOW,
        c.CATEGORY: c.CATEGORY_CUSTOMER_SERVICE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Zendesk",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_ZENDESK,
        c.CATEGORY: c.CATEGORY_CUSTOMER_SERVICE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Dropbox",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_DROPBOX,
        c.CATEGORY: c.CATEGORY_DATA_FILE_STORAGE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Microsoft Sharepoint",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MICROSOFT_SHAREPOINT,
        c.CATEGORY: c.CATEGORY_DATA_FILE_STORAGE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "SFTP",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_SFTP,
        c.CATEGORY: c.CATEGORY_DATA_FILE_STORAGE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Windows Fileshare",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_WINDOWS_FILESHARE,
        c.CATEGORY: c.CATEGORY_DATA_FILE_STORAGE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon Aurora",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AMAZON_AURORA,
        c.CATEGORY: c.CATEGORY_DATABASES,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google BigQuery",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_BIG_QUERY,
        c.CATEGORY: c.CATEGORY_DATABASES,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "IBM DB2",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_IBMDB2,
        c.CATEGORY: c.CATEGORY_DATABASES,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Maria DB",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MARIADB,
        c.CATEGORY: c.CATEGORY_DATABASES,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Microsoft Azure SQL DB",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AZURESQL,
        c.CATEGORY: c.CATEGORY_DATABASES,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mongo DB",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MONGODB,
        c.CATEGORY: c.CATEGORY_DATABASES,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "My SQL",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MYSQL,
        c.CATEGORY: c.CATEGORY_DATABASES,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Oracle DB",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_ORACLE_DB,
        c.CATEGORY: c.CATEGORY_DATABASES,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Tableau",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_TABLEAU,
        c.CATEGORY: c.CATEGORY_DATA_VISUALIZATION,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Analytics",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_GOOGLE_ANALYTICS,
        c.CATEGORY: c.CATEGORY_INTERNET,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "HTTP",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_HTTP,
        c.CATEGORY: c.CATEGORY_INTERNET,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Microsoft Bing",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_BING,
        c.CATEGORY: c.CATEGORY_INTERNET,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amplitude",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AMPLITUDE,
        c.CATEGORY: c.CATEGORY_MARKETING,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Ads",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_GOOGLEADS,
        c.CATEGORY: c.CATEGORY_MARKETING,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Hubspot",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_HUBSPOT,
        c.CATEGORY: c.CATEGORY_MARKETING,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mailchimp",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MAILCHIMP,
        c.CATEGORY: c.CATEGORY_MARKETING,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Marketo",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MARKETO,
        c.CATEGORY: c.CATEGORY_MARKETING,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Microsoft Advertising",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MICROSOFT_ADS,
        c.CATEGORY: c.CATEGORY_MARKETING,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Salesforce Marketing Cloud",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_SFMC,
        c.CATEGORY: c.CATEGORY_MARKETING,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon S3",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AMAZONS3,
        c.CATEGORY: c.CATEGORY_OBJECT_STORAGE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Azure Blob Storage",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AZUREBLOB,
        c.CATEGORY: c.CATEGORY_OBJECT_STORAGE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Cloud Storage",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_GOOGLE_CLOUD_STORAGE,
        c.CATEGORY: c.CATEGORY_OBJECT_STORAGE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Google Sheets",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_GOOGLE_SHEETS,
        c.CATEGORY: c.CATEGORY_FILES,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Microsoft Excel",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MICROSOFT_EXCEL,
        c.CATEGORY: c.CATEGORY_FILES,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "PayPal",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_PAYPAL,
        c.CATEGORY: c.CATEGORY_FINANCE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Quickbooks Online",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_QUICKBOOKS,
        c.CATEGORY: c.CATEGORY_FINANCE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Square",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_SQUARE,
        c.CATEGORY: c.CATEGORY_FINANCE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Stripe",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_STRIPE,
        c.CATEGORY: c.CATEGORY_FINANCE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "AOL",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AOL,
        c.CATEGORY: c.CATEGORY_PRODUCTIVITY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Gmail",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_GMAIL,
        c.CATEGORY: c.CATEGORY_PRODUCTIVITY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Insight IQ",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_INSIGHTIQ,
        c.CATEGORY: c.CATEGORY_PRODUCTIVITY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Jira",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_JIRA,
        c.CATEGORY: c.CATEGORY_PRODUCTIVITY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Mandrill",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MANDRILL,
        c.CATEGORY: c.CATEGORY_PRODUCTIVITY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Medallia",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_MEDALLIA,
        c.CATEGORY: c.CATEGORY_PRODUCTIVITY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Outlook",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_OUTLOOK,
        c.CATEGORY: c.CATEGORY_PRODUCTIVITY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Qualtrics",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_QUALTRICS,
        c.CATEGORY: c.CATEGORY_PRODUCTIVITY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "SendGrid by Twilio",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_SENDGRID,
        c.CATEGORY: c.CATEGORY_PRODUCTIVITY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "SurveyMonkey",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_SURVEY_MONKEY,
        c.CATEGORY: c.CATEGORY_PRODUCTIVITY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Twilio",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_TWILIO,
        c.CATEGORY: c.CATEGORY_PRODUCTIVITY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Yahoo",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_YAHOO,
        c.CATEGORY: c.CATEGORY_PRODUCTIVITY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Facebook",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_FACEBOOK,
        c.CATEGORY: c.CATEGORY_SOCIAL_MEDIA,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Instagram",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_INSTAGRAM,
        c.CATEGORY: c.CATEGORY_SOCIAL_MEDIA,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "LinkedIn",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_LINKEDIN,
        c.CATEGORY: c.CATEGORY_SOCIAL_MEDIA,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Snapchat",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_SNAPCHAT,
        c.CATEGORY: c.CATEGORY_SOCIAL_MEDIA,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Twitter",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_TWITTER,
        c.CATEGORY: c.CATEGORY_SOCIAL_MEDIA,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "YouTube",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_YOUTUBE,
        c.CATEGORY: c.CATEGORY_SOCIAL_MEDIA,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Adobe Experience",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_ADOBE,
        c.CATEGORY: c.CATEGORY_MARKETING,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
    },
    {
        c.DATA_SOURCE_NAME: "Amazon Advertising",
        c.DATA_SOURCE_TYPE: c.DATA_SOURCE_PLATFORM_AMAZONADS,
        c.CATEGORY: c.CATEGORY_MARKETING,
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
        c.CATEGORY: c.MARKETING,
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Facebook",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_FACEBOOK,
        c.CATEGORY: c.ADVERTISING,
        c.STATUS: c.ACTIVE,
        c.ENABLED: True,
        c.ADDED: False,
        c.IS_AD_PLATFORM: True,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Google Ads",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_GOOGLE,
        c.CATEGORY: c.ADVERTISING,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: True,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Amazon Advertising",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_AMAZON,
        c.CATEGORY: c.ADVERTISING,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: True,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Adobe Experience",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_ADOBE,
        c.CATEGORY: c.MARKETING,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Sendgrid by Twilio",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_SENDGRID,
        c.CATEGORY: c.MARKETING,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "SAP",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_SAP,
        c.CATEGORY: c.COMMERCE,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Qualtrics",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_QUALTRICS,
        c.CATEGORY: c.SURVEY,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Fullstory",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_FULLSTORY,
        c.CATEGORY: c.ANALYTICS,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "QuantumMetric",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_QUANTUMMETRIC,
        c.CATEGORY: c.ANALYTICS,
        c.STATUS: c.PENDING,
        c.ENABLED: False,
        c.ADDED: False,
        c.IS_AD_PLATFORM: False,
    },
    {
        c.DELIVERY_PLATFORM_NAME: "Medallia",
        c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_MEDALLIA,
        c.CATEGORY: c.SURVEY,
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
        logging.info(
            "Added %s, %s.", data_source[c.DATA_SOURCE_NAME], result_id
        )
    logging.info("Prepopulate data sources complete.")


def insert_delivery_platforms(
    database: MongoClient, delivery_platforms: list
) -> None:
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
