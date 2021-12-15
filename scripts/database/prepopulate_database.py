"""Purpose of this file is for populating the following database documents
 - data sources
 - destinations (delivery platforms)
"""
# pylint: disable=too-many-lines
import logging
import huxunifylib.database.constants as db_c
from huxunifylib.database.cdp_data_source_management import create_data_source
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
)
from huxunifylib.database.collection_management import (
    create_document,
)
from pymongo import MongoClient

from database.share import get_mongo_client

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Data Sources List
data_sources_constants = [
    {
        db_c.DATA_SOURCE_NAME: "Bluecore",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_BLUECORE,
        db_c.CATEGORY: db_c.CATEGORY_ECOMMERCE,
        db_c.STATUS: db_c.ACTIVE,
        db_c.ENABLED: True,
        db_c.ADDED: True,
    },
    {
        db_c.DATA_SOURCE_NAME: "NetSuite",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_NETSUITE,
        db_c.CATEGORY: db_c.CATEGORY_CRM,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: True,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Aqfer",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_AQFER,
        db_c.CATEGORY: db_c.CATEGORY_MARKETING,
        db_c.STATUS: db_c.ACTIVE,
        db_c.ENABLED: True,
        db_c.ADDED: True,
    },
    {
        db_c.DATA_SOURCE_NAME: "Rest API",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_REST_API,
        db_c.CATEGORY: db_c.CATEGORY_API,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "OData",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_ODATA,
        db_c.CATEGORY: db_c.CATEGORY_API,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Apache Hive",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_APACHE_HIVE,
        db_c.CATEGORY: db_c.CATEGORY_BIG_DATA,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Apache Spark",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_APACHE_SPARK,
        db_c.CATEGORY: db_c.CATEGORY_BIG_DATA,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Microsoft Dynamics",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_MICROSOFT_DYNAMICS,
        db_c.CATEGORY: db_c.CATEGORY_CRM,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Oracle",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_ORACLE_CRM,
        db_c.CATEGORY: db_c.CATEGORY_CRM,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Salesforce",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_SALESFORCE,
        db_c.CATEGORY: db_c.CATEGORY_CRM,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "SAP",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_SAP,
        db_c.CATEGORY: db_c.CATEGORY_CRM,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "ServiceNow",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_SERVICE_NOW,
        db_c.CATEGORY: db_c.CATEGORY_CUSTOMER_SERVICE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Zendesk",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_ZENDESK,
        db_c.CATEGORY: db_c.CATEGORY_CUSTOMER_SERVICE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Dropbox",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_DROPBOX,
        db_c.CATEGORY: db_c.CATEGORY_DATA_FILE_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Microsoft Sharepoint",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_MICROSOFT_SHAREPOINT,
        db_c.CATEGORY: db_c.CATEGORY_DATA_FILE_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "SFTP",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_SFTP,
        db_c.CATEGORY: db_c.CATEGORY_DATA_FILE_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Windows Fileshare",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_WINDOWS_FILESHARE,
        db_c.CATEGORY: db_c.CATEGORY_DATA_FILE_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Amazon Aurora",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_AMAZON_AURORA,
        db_c.CATEGORY: db_c.CATEGORY_DATABASES,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Google BigQuery",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_BIG_QUERY,
        db_c.CATEGORY: db_c.CATEGORY_DATABASES,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "IBM DB2",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_IBMDB2,
        db_c.CATEGORY: db_c.CATEGORY_DATABASES,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Maria DB",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_MARIADB,
        db_c.CATEGORY: db_c.CATEGORY_DATABASES,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Microsoft Azure SQL DB",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_AZURESQL,
        db_c.CATEGORY: db_c.CATEGORY_DATABASES,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Mongo DB",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_MONGODB,
        db_c.CATEGORY: db_c.CATEGORY_DATABASES,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "My SQL",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_MYSQL,
        db_c.CATEGORY: db_c.CATEGORY_DATABASES,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Oracle DB",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_ORACLE_DB,
        db_c.CATEGORY: db_c.CATEGORY_DATABASES,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Tableau",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_TABLEAU,
        db_c.CATEGORY: db_c.CATEGORY_DATA_VISUALIZATION,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Google Analytics",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_GOOGLE_ANALYTICS,
        db_c.CATEGORY: db_c.CATEGORY_INTERNET,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "HTTP",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_HTTP,
        db_c.CATEGORY: db_c.CATEGORY_INTERNET,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Microsoft Bing",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_BING,
        db_c.CATEGORY: db_c.CATEGORY_INTERNET,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Amplitude",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_AMPLITUDE,
        db_c.CATEGORY: db_c.CATEGORY_MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Google Ads",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_GOOGLEADS,
        db_c.CATEGORY: db_c.CATEGORY_MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Hubspot",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_HUBSPOT,
        db_c.CATEGORY: db_c.CATEGORY_MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Mailchimp",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_MAILCHIMP,
        db_c.CATEGORY: db_c.CATEGORY_MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Marketo",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_MARKETO,
        db_c.CATEGORY: db_c.CATEGORY_MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Microsoft Advertising",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_MICROSOFT_ADS,
        db_c.CATEGORY: db_c.CATEGORY_MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Salesforce Marketing Cloud",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_SFMC,
        db_c.CATEGORY: db_c.CATEGORY_MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Amazon S3",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_AMAZONS3,
        db_c.CATEGORY: db_c.CATEGORY_OBJECT_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Azure Blob Storage",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_AZUREBLOB,
        db_c.CATEGORY: db_c.CATEGORY_OBJECT_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Google Cloud Storage",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_GOOGLE_CLOUD_STORAGE,
        db_c.CATEGORY: db_c.CATEGORY_OBJECT_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Google Sheets",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_GOOGLE_SHEETS,
        db_c.CATEGORY: db_c.CATEGORY_FILES,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Microsoft Excel",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_MICROSOFT_EXCEL,
        db_c.CATEGORY: db_c.CATEGORY_FILES,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "PayPal",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_PAYPAL,
        db_c.CATEGORY: db_c.CATEGORY_FINANCE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Quickbooks Online",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_QUICKBOOKS,
        db_c.CATEGORY: db_c.CATEGORY_FINANCE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Square",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_SQUARE,
        db_c.CATEGORY: db_c.CATEGORY_FINANCE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Stripe",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_STRIPE,
        db_c.CATEGORY: db_c.CATEGORY_FINANCE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "AOL",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_AOL,
        db_c.CATEGORY: db_c.CATEGORY_PRODUCTIVITY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Gmail",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_GMAIL,
        db_c.CATEGORY: db_c.CATEGORY_PRODUCTIVITY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Insight IQ",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_INSIGHTIQ,
        db_c.CATEGORY: db_c.CATEGORY_PRODUCTIVITY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Jira",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_JIRA,
        db_c.CATEGORY: db_c.CATEGORY_PRODUCTIVITY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Mandrill",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_MANDRILL,
        db_c.CATEGORY: db_c.CATEGORY_PRODUCTIVITY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Medallia",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_MEDALLIA,
        db_c.CATEGORY: db_c.CATEGORY_PRODUCTIVITY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Outlook",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_OUTLOOK,
        db_c.CATEGORY: db_c.CATEGORY_PRODUCTIVITY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Qualtrics",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_QUALTRICS,
        db_c.CATEGORY: db_c.CATEGORY_PRODUCTIVITY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "SendGrid by Twilio",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_SENDGRID,
        db_c.CATEGORY: db_c.CATEGORY_PRODUCTIVITY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "SurveyMonkey",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_SURVEY_MONKEY,
        db_c.CATEGORY: db_c.CATEGORY_PRODUCTIVITY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Twilio",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_TWILIO,
        db_c.CATEGORY: db_c.CATEGORY_PRODUCTIVITY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Yahoo",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_YAHOO,
        db_c.CATEGORY: db_c.CATEGORY_PRODUCTIVITY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Facebook",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_FACEBOOK,
        db_c.CATEGORY: db_c.CATEGORY_SOCIAL_MEDIA,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Instagram",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_INSTAGRAM,
        db_c.CATEGORY: db_c.CATEGORY_SOCIAL_MEDIA,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "LinkedIn",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_LINKEDIN,
        db_c.CATEGORY: db_c.CATEGORY_SOCIAL_MEDIA,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Snapchat",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_SNAPCHAT,
        db_c.CATEGORY: db_c.CATEGORY_SOCIAL_MEDIA,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Twitter",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_TWITTER,
        db_c.CATEGORY: db_c.CATEGORY_SOCIAL_MEDIA,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "YouTube",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_YOUTUBE,
        db_c.CATEGORY: db_c.CATEGORY_SOCIAL_MEDIA,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Adobe Experience",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_ADOBE,
        db_c.CATEGORY: db_c.CATEGORY_MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
    {
        db_c.DATA_SOURCE_NAME: "Amazon Advertising",
        db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_AMAZONADS,
        db_c.CATEGORY: db_c.CATEGORY_MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
    },
]

# Delivery Platforms List
delivery_platforms_constants = [
    {
        db_c.DELIVERY_PLATFORM_NAME: "Facebook",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_FACEBOOK,
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.ACTIVE,
        db_c.ENABLED: True,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Google Ads",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_GOOGLE,
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Salesforce Marketing Cloud",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SFMC,
        db_c.CATEGORY: db_c.MARKETING,
        db_c.STATUS: db_c.ACTIVE,
        db_c.ENABLED: True,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Sendgrid by Twilio",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SENDGRID,
        db_c.CATEGORY: db_c.MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Qualtrics",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_QUALTRICS,
        db_c.CATEGORY: db_c.SURVEY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Amazon Advertising",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_AMAZON,
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Liveramp",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_LIVERAMP,
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Pinterest",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_PINTEREST,
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "TheTradeDesk",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_THE_TRADEDESK,
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Twitter",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_TWITTER,
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Google DV360",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_GOOGLE_DV360,
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Fullstory",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_FULLSTORY,
        db_c.CATEGORY: db_c.ANALYTICS,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "QuantumMetric",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_QUANTUMMETRIC,
        db_c.CATEGORY: db_c.ANALYTICS,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Salesforce Commerce Cloud",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SFCC,
        db_c.CATEGORY: db_c.COMMERCE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "SAP",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SAP,
        db_c.CATEGORY: db_c.COMMERCE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Adobe Campaign",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_ADOBE_CAMPAIGN,
        db_c.CATEGORY: db_c.MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Adobe Experience Platform",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_ADOBE,
        db_c.CATEGORY: db_c.MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Salesforce CDP",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SALESFORCE_CDP,
        db_c.CATEGORY: db_c.MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Salesforce Datorama",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SALESFORCE_DATORAMA,
        db_c.CATEGORY: db_c.CATEGORY_REPORTING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Tableau",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_TABLEAU,
        db_c.CATEGORY: db_c.CATEGORY_REPORTING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "AWS S3",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_AMAZONS3,
        db_c.CATEGORY: db_c.CATEGORY_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Azure Blob",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_AZUREBLOB,
        db_c.CATEGORY: db_c.CATEGORY_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Google Cloud Stoorage",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_GOOGLE_CLOUD_STORAGE,
        db_c.CATEGORY: db_c.CATEGORY_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "SFTP",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SFTP,
        db_c.CATEGORY: db_c.CATEGORY_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Medallia",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_MEDALLIA,
        db_c.CATEGORY: db_c.SURVEY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
]

# Models List
models_list = [
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_EMAIL,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Propensity to Unsubscribe",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to unsubscribe"
        " from an email marketing list.",
        db_c.MODEL_ID: "a54d7e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_EMAIL,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Propensity to Open",
        db_c.MODEL_DESCRIPTION: " Propensity for a customer to open an email.",
        db_c.MODEL_ID: "5df65e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_EMAIL,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Propensity to Click",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to click "
        "on a link in an email.",
        db_c.MODEL_ID: "aa789e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_EMAIL,
        db_c.TYPE: db_c.MODEL_TYPE_UNKNOWN,
        db_c.NAME: "Email Content Optimization",
        db_c.MODEL_DESCRIPTION: "Alter email content to optimize "
        "email campaign performance.",
        db_c.MODEL_ID: "99e45e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_SALES_FORECASTING,
        db_c.TYPE: db_c.MODEL_TYPE_REGRESSION,
        db_c.NAME: "Customer Lifetime Value",
        db_c.MODEL_DESCRIPTION: "Predicting the lifetime value of a "
        "customer over a defined time range.",
        db_c.MODEL_ID: "cc768e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_SALES_FORECASTING,
        db_c.TYPE: db_c.MODEL_TYPE_REGRESSION,
        db_c.NAME: "Predicted Sales Per Customer",
        db_c.MODEL_DESCRIPTION: "Predicting sales for a customer over a "
        "defined time range.",
        db_c.MODEL_ID: "bba67e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_SALES_FORECASTING,
        db_c.TYPE: db_c.MODEL_TYPE_REGRESSION,
        db_c.NAME: "Predicted Sales Per Store",
        db_c.MODEL_DESCRIPTION: "Predicting sales for a store over a "
        "defined time range.",
        db_c.MODEL_ID: "a45b7e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_TRUST_ID,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Capability Propensity",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to have positive,"
        " negative, or neutral capability score.",
        db_c.MODEL_ID: "bc123e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_TRUST_ID,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Trust Propensity",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to have positive,"
        " negative, or neutral trust score.",
        db_c.MODEL_ID: "a15d8e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_TRUST_ID,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Humanity Propensity",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to have positive,"
        " negative, or neutral humanity score.",
        db_c.MODEL_ID: "bd732e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_TRUST_ID,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Reliability Propensity",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to have positive,"
        " negative, or neutral reliability score.",
        db_c.MODEL_ID: "99d12e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_TRUST_ID,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Transparency Propensity",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to have positive,"
        " negative, or neutral transparency score.",
        db_c.MODEL_ID: "bed54e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_RETENTION,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Churn",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to leave a service "
        "over a defined time range.",
        db_c.MODEL_ID: "11d54e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_WEB,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Propensity to Purchase Product Category",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to make a web purchase"
        " in a particular product category.",
        db_c.MODEL_ID: "88ee4e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_WEB,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Propensity to Visit Product Category",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to make a web visit"
        " in a particular product category.",
        db_c.MODEL_ID: "aab41e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_WEB,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Propensity to Visit Website",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to visit a website.",
        db_c.MODEL_ID: "99a78e0bd7edaad4c36bec4a3682f02d36441fe1",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_UNCATEGORIZED,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Segmentation",
        db_c.MODEL_DESCRIPTION: "Segment a set of customers.",
        db_c.MODEL_ID: "d7480a81b3c84fd696e43c18e31a481a",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
]

# Configurations List
configurations_constants = [
    {
        db_c.CONFIGURATION_FIELD_NAME: "Data Management",
        db_c.CONFIGURATION_FIELD_ICON: "uncategorised",
        db_c.CONFIGURATION_FIELD_TYPE: "module",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Monitor data quality "
        "throughout ingestion and create a peristent"
        " identifier and profile for every customer",
        db_c.CONFIGURATION_FIELD_STATUS: "active",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Decisioning",
        db_c.CONFIGURATION_FIELD_ICON: "uncategorised",
        db_c.CONFIGURATION_FIELD_TYPE: "module",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Track performance of "
        "decisioning models and reveal actionable"
        " customer insights.",
        db_c.CONFIGURATION_FIELD_STATUS: "active",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Customer Insights",
        db_c.CONFIGURATION_FIELD_ICON: "uncategorised",
        db_c.CONFIGURATION_FIELD_TYPE: "module",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "A 360 degree view of "
        "each customer, understanding not only their needs and "
        "preferences, but also the person behind the data.",
        db_c.CONFIGURATION_FIELD_STATUS: "active",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Orchestration",
        db_c.CONFIGURATION_FIELD_ICON: "uncategorised",
        db_c.CONFIGURATION_FIELD_TYPE: "module",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Seamlessly route audiences to"
        " an activation channel of choice to deliver a personalized"
        " experience for existing and new customers.",
        db_c.CONFIGURATION_FIELD_STATUS: "active",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Content",
        db_c.CONFIGURATION_FIELD_ICON: "uncategorised",
        db_c.CONFIGURATION_FIELD_TYPE: "module",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Content allows you to present"
        " visitors with unique experiences tailored to their needs.",
        db_c.CONFIGURATION_FIELD_STATUS: "pending",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Measurement",
        db_c.CONFIGURATION_FIELD_ICON: "uncategorised",
        db_c.CONFIGURATION_FIELD_TYPE: "module",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Find out why your audiences"
        " think what they think, behave as they "
        "behave and feel what they feel.",
        db_c.CONFIGURATION_FIELD_STATUS: "pending",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Commerce personal",
        db_c.CONFIGURATION_FIELD_ICON: "commerce_personal",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Lorem ipsum dolor sit amet, "
        "consectetur adipiscing elit ut aliquam.",
        db_c.CONFIGURATION_FIELD_STATUS: "pending",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Digital Giant",
        db_c.CONFIGURATION_FIELD_ICON: "digital_advertising",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Lorem ipsum dolor sit amet, "
        "consectetur adipiscing elit ut aliquam.",
        db_c.CONFIGURATION_FIELD_STATUS: "pending",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Email deliverability",
        db_c.CONFIGURATION_FIELD_ICON: "email_deliverabilit",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Ensure emails land in the right "
        "inbox by providing insights on all aspects of a "
        "successful marketing strategy from beginning to end.",
        db_c.CONFIGURATION_FIELD_STATUS: "pending",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Experience data platform",
        db_c.CONFIGURATION_FIELD_ICON: "datamgmg.ico",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Brings voice of the customer "
        "to make improvements to your customer "
        "experience at an individual and macro level.",
        db_c.CONFIGURATION_FIELD_STATUS: "pending",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Insight IQ",
        db_c.CONFIGURATION_FIELD_ICON: "insight_iq",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Enrich your customer profiles"
        " with this collections of data sources at"
        " the individual level enabling an enhanced customer experience.",
        db_c.CONFIGURATION_FIELD_STATUS: "pending",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Intelligent marketing",
        db_c.CONFIGURATION_FIELD_ICON: "intelligent_marketing",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "These capabilities were folded "
        "into the segmentation engine, as was Hux Audience.",
        db_c.CONFIGURATION_FIELD_STATUS: "pending",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Trust ID",
        db_c.CONFIGURATION_FIELD_ICON: "trust_id",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Enables brands to gain "
        "visibility, monitor and  engage with their customers "
        "based on AI – generated experienced based metrics.",
        db_c.CONFIGURATION_FIELD_STATUS: "pending",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Search AI",
        db_c.CONFIGURATION_FIELD_ICON: "search_ai",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Leverages search data to"
        " optimize the creation, placement, and timing of online "
        "content to increase customer acquisition.",
        db_c.CONFIGURATION_FIELD_STATUS: "pending",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Cognitive spark",
        db_c.CONFIGURATION_FIELD_ICON: "cognitive_spark",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "A modular cloud-based product"
        " designed to enable brands and portfolios "
        "to make AI powered decisions at scale.",
        db_c.CONFIGURATION_FIELD_STATUS: "pending",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
]


def drop_collections(database: MongoClient) -> None:
    """Drop collections for writing.

    Args:
        database (MongoClient): Database Client.
    """

    collections = [
        db_c.CDP_DATA_SOURCES_COLLECTION,
        db_c.DELIVERY_PLATFORM_COLLECTION,
        db_c.MODELS_COLLECTION,
        db_c.CONFIGURATIONS_COLLECTION,
    ]
    for collection in collections:
        database[db_c.DATA_MANAGEMENT_DATABASE][collection].drop()


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
            data_source[db_c.DATA_SOURCE_NAME],
            category="",
            added=data_source[db_c.ADDED],
            enabled=data_source[db_c.ENABLED],
            source_type=data_source[db_c.DATA_SOURCE_TYPE],
            status=data_source[db_c.STATUS],
        )[db_c.ID]
        logging.info(
            "Added %s, %s.", data_source[db_c.DATA_SOURCE_NAME], result_id
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
            delivery_platform[db_c.DELIVERY_PLATFORM_TYPE]
            in db_c.SUPPORTED_DELIVERY_PLATFORMS
        ):
            result_id = set_delivery_platform(
                database,
                **delivery_platform,
            )[db_c.ID]
            logging.info(
                "Added %s, %s.",
                delivery_platform[db_c.DELIVERY_PLATFORM_NAME],
                result_id,
            )
    logging.info("Prepopulate destinations complete.")


def insert_configurations(database: MongoClient, configurations: list) -> None:
    """Insert data into configurations Collection.

    Args:
        database (MongoClient): MongoDB Client.
        configurations (List): List of Configuration Objects.
    """

    logging.info("Prepopulate configurations.")

    for configuration in configurations:
        result_id = create_document(
            database,
            db_c.CONFIGURATIONS_COLLECTION,
            configuration,
        )[db_c.ID]
        logging.info(
            "Added %s, %s.",
            configuration[db_c.NAME],
            result_id,
        )
    logging.info("Prepopulated configurations.")


def insert_models(database: MongoClient, models: list) -> None:
    """Insert data into models collection

    Args:
        database (MongoClient): MongoDB Client.
        models (List): List of Model Objects.
    """
    logging.info("Prepopulate models.")

    for model in models:
        model_id = create_document(database, db_c.MODELS_COLLECTION, model)[
            db_c.ID
        ]
        logging.info("Added %s, %s.", model[db_c.NAME], model_id)

    logging.info("Prepopulate models complete.")


if __name__ == "__main__":
    # Initiate Data Base client
    db_client = get_mongo_client()
    drop_collections(db_client)
    insert_data_sources(db_client, data_sources_constants)
    insert_delivery_platforms(db_client, delivery_platforms_constants)
    insert_configurations(db_client, configurations_constants)
    insert_models(db_client, models_list)
    logging.info("Prepopulate complete.")
