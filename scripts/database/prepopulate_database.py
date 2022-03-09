"""Purpose of this file is for populating the following database documents.
 - data sources
 - destinations (delivery platforms)
"""
# pylint: disable=too-many-lines
import logging
import os
from distutils.util import strtobool

import huxunifylib.database.constants as db_c
from huxunifylib.database.cdp_data_source_management import create_data_source
from huxunifylib.database.data.data_sources import DATA_SOURCES_LIST
from huxunifylib.database.data.delivery_platforms import DELIVERY_PLATFORM_LIST
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
    get_delivery_platform_by_type,
)
from huxunifylib.database.collection_management import (
    create_document,
)
from pymongo import MongoClient

from database.share import get_mongo_client

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Models List
models_list = [
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_EMAIL,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Propensity to Unsubscribe",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to unsubscribe"
        " from an email marketing list.",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_EMAIL,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Propensity to Open",
        db_c.MODEL_DESCRIPTION: " Propensity for a customer to open an email.",
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
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_WEB,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Propensity to Visit Website",
        db_c.MODEL_DESCRIPTION: "Propensity for a customer to visit a website.",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: db_c.MODEL_CATEGORY_UNCATEGORIZED,
        db_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
        db_c.NAME: "Segmentation",
        db_c.MODEL_DESCRIPTION: "Segment a set of customers.",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: "Retention",
        db_c.TYPE: "churn",
        db_c.NAME: "Propensity to churn",
        db_c.MODEL_DESCRIPTION: "Propensity of a customer to "
        "churn in a future time window.",
        db_c.VERSION: "21.11.22",
        db_c.FULCRUM: "2021-11-22",
        db_c.LOOKBACK_DAYS: 120,
        db_c.PREDICTION_DAYS: 30,
        db_c.OWNER: "decisioning",
        db_c.OWNER_EMAIL: "huxdecisiong",
        db_c.DATE_TRAINED: "2021-11-22",
        db_c.STATUS: db_c.PENDING,
        db_c.ADDED: False,
        db_c.ENABLED: True,
    },
    {
        db_c.CATEGORY: "Retention",
        db_c.TYPE: "Purchase",
        db_c.NAME: "Propensity to purchase",
        db_c.MODEL_DESCRIPTION: "Propensity of a customer making a "
        "purchase in a future time window.",
        db_c.VERSION: "21.10.7",
        db_c.FULCRUM: "2021-10-07",
        db_c.LOOKBACK_DAYS: 90,
        db_c.PREDICTION_DAYS: 14,
        db_c.OWNER: "decisioning",
        db_c.OWNER_EMAIL: "huxdecisiong",
        db_c.DATE_TRAINED: "2021-10-07",
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
        db_c.CONFIGURATION_FIELD_ICON: "email_deliverability",
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
    {
        db_c.CONFIGURATION_FIELD_NAME: "Navigation Settings",
        db_c.CONFIGURATION_FIELD_TYPE: "navigation_settings",
        db_c.CONFIGURATION_FIELD_SETTINGS: [
            {
                db_c.CONFIGURATION_FIELD_NAME: "Data Management",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
                db_c.CONFIGURATION_FIELD_CHILDREN: [
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Data Sources",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Identity Resolution",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                ],
            },
            {
                db_c.CONFIGURATION_FIELD_NAME: "Decisioning",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
                db_c.CONFIGURATION_FIELD_CHILDREN: [
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Models",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    }
                ],
            },
            {
                db_c.CONFIGURATION_FIELD_NAME: "Customer Insights",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
                db_c.CONFIGURATION_FIELD_CHILDREN: [
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "All Customers",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Segment Playground",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                ],
            },
            {
                db_c.CONFIGURATION_FIELD_NAME: "Orchestration",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
                db_c.CONFIGURATION_FIELD_CHILDREN: [
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Destinations",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Audiences",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Engagements",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                ],
            },
        ],
    },
]

# Client Projects List
client_projects_list = [
    {
        db_c.NAME: "Monamie",
        db_c.TYPE: "monamie",
        db_c.DESCRIPTION: "Monamie Project",
        db_c.URL: "https://localhost/monamie",
        db_c.ICON: "default.ico",
        db_c.ACCESS_LEVEL: "viewer",
    },
    {
        db_c.NAME: "Creatiff Inc.",
        db_c.TYPE: "creatiff-inc",
        db_c.DESCRIPTION: "Creatiff Inc. Project",
        db_c.URL: "https://localhost/creatiff",
        db_c.ICON: "default.ico",
        db_c.ACCESS_LEVEL: "editor",
    },
    {
        db_c.NAME: ".am",
        db_c.TYPE: "dot-am",
        db_c.DESCRIPTION: ".am Project",
        db_c.URL: "https://localhost/am",
        db_c.ICON: "default.ico",
        db_c.ACCESS_LEVEL: "admin",
    },
]

# Applications List
applications_constants = [
    {
        db_c.NAME: "Apache Airflow",
        db_c.CATEGORY: "Data Processing",
        db_c.TYPE: "apache-airflow",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Docker",
        db_c.CATEGORY: "Data Processing",
        db_c.TYPE: "docker",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Kubernetes",
        db_c.CATEGORY: "Data Processing",
        db_c.TYPE: "kubernetes",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Matillion",
        db_c.CATEGORY: "Data Processing",
        db_c.TYPE: "matillion",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "MongoDB",
        db_c.CATEGORY: "Data Storage",
        db_c.TYPE: "mongodb",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Snowflake",
        db_c.CATEGORY: "Data Storage",
        db_c.TYPE: "snowflake",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Algorithmia",
        db_c.CATEGORY: "Modeling",
        db_c.TYPE: "algorithmia",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Binderhub",
        db_c.CATEGORY: "Modeling",
        db_c.TYPE: "binderhub",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Kubeflow",
        db_c.CATEGORY: "Modeling",
        db_c.TYPE: "kubeflow",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Jupyterhub",
        db_c.CATEGORY: "Modeling",
        db_c.TYPE: "jupyterhub",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Tecton",
        db_c.CATEGORY: "Modelling",
        db_c.TYPE: "tecton",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Grafana",
        db_c.CATEGORY: "Monitoring",
        db_c.TYPE: "grafana",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Prometheus",
        db_c.CATEGORY: "Monitoring",
        db_c.TYPE: "prometheus",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Medallia",
        db_c.CATEGORY: "Reporting",
        db_c.TYPE: "medallia",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Microsoft Power BI",
        db_c.CATEGORY: "Reporting",
        db_c.TYPE: "microsoft-power-bi",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Salesforce Datorama",
        db_c.CATEGORY: "Reporting",
        db_c.TYPE: "salesforce-datorama",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "SparkPost",
        db_c.CATEGORY: "Reporting",
        db_c.TYPE: "sparkpost",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
    {
        db_c.NAME: "Tableau",
        db_c.CATEGORY: "Reporting",
        db_c.TYPE: "tableau",
        db_c.ICON: "default.ico",
        db_c.ENABLED: True,
    },
]


def drop_collections(database: MongoClient) -> None:
    """Drop collections for writing.

    Args:
        database (MongoClient): Database Client.
    """

    logging.info("Dropping collections.")

    collections_to_drop = database[
        db_c.DATA_MANAGEMENT_DATABASE
    ].list_collection_names()

    # do not drop user collection if it exists
    collections_to_drop.remove(db_c.USER_COLLECTION)

    # if drop all collections is false, do not drop the restricted collections
    if not strtobool(os.environ.get("DROP_ALL_COLLECTIONS", default="False")):
        collections_to_drop = [
            x
            for x in collections_to_drop
            if x not in db_c.RESTRICTED_COLLECTIONS
        ]

    for collection in collections_to_drop:
        database[db_c.DATA_MANAGEMENT_DATABASE][collection].drop()
        logging.info("Dropped the %s collection.", collection)


def insert_data_sources(database: MongoClient, data_sources: list) -> None:
    """Inserting Data Sources into Data Sources Collection.

    Args:
        database (MongoClient): MongoDB Client.
        data_sources (List): List of Data Sources Object.
    """

    logging.info("Pre-populating data sources.")

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
    logging.info("Pre-populate data sources complete.")


def insert_delivery_platforms(
    database: MongoClient, delivery_platforms: list
) -> None:
    """Insertion of Delivery Platforms Collection.

    Args:
        database (MongoClient): MongoDB Client.
        delivery_platforms (List): List of Delivery Platform Objects.
    """

    logging.info("Pre-populating destinations.")

    for delivery_platform in delivery_platforms:
        if (
            delivery_platform[db_c.DELIVERY_PLATFORM_TYPE]
            in db_c.SUPPORTED_DELIVERY_PLATFORMS
        ):
            existing_delivery_platform = get_delivery_platform_by_type(
                database, delivery_platform[db_c.DELIVERY_PLATFORM_TYPE]
            )
            # add delivery platform only if it does not exist
            if not existing_delivery_platform:
                result_id = set_delivery_platform(
                    database,
                    **delivery_platform,
                )[db_c.ID]
                logging.info(
                    "Added %s, %s.",
                    delivery_platform[db_c.DELIVERY_PLATFORM_NAME],
                    result_id,
                )
            else:
                logging.info(
                    "%s with id %s already exists.",
                    delivery_platform[db_c.DELIVERY_PLATFORM_NAME],
                    existing_delivery_platform[db_c.ID],
                )
    logging.info("Pre-populate destinations complete.")


def insert_configurations(database: MongoClient, configurations: list) -> None:
    """Insert data into configurations Collection.

    Args:
        database (MongoClient): MongoDB Client.
        configurations (List): List of Configuration Objects.
    """

    logging.info("Pre-populating configurations.")

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
    logging.info("Pre-populated configurations.")


def insert_models(database: MongoClient, models: list) -> None:
    """Insert data into models collection

    Args:
        database (MongoClient): MongoDB Client.
        models (List): List of Model Objects.
    """
    logging.info("Pre-populating models.")

    for model in models:
        model_id = create_document(database, db_c.MODELS_COLLECTION, model)
        logging.info("Added %s, %s.", model[db_c.NAME], model_id)

    logging.info("Pre-populate models complete.")


def insert_client_projects(
    database: MongoClient, client_projects: list
) -> None:
    """Insert data into client_projects collection.

    Args:
        database (MongoClient): MongoDB Client.
        client_projects (List): List of client project objects.
    """

    logging.info("Pre-populating client projects.")

    for client_project in client_projects:
        result_id = create_document(
            database,
            db_c.CLIENT_PROJECTS_COLLECTION,
            client_project,
        )[db_c.ID]

        logging.info(
            "Added %s, %s.",
            client_project[db_c.NAME],
            result_id,
        )

    logging.info("Pre-populated client projects.")


def insert_applications(database: MongoClient, applications: list) -> None:
    """Insert data into applications collection.

    Args:
        database (MongoClient): MongoDB Client.
        applications (List): List of application objects.
    """

    logging.info("Pre-populating applications.")

    for application in applications:
        result_id = create_document(
            database,
            db_c.APPLICATIONS_COLLECTION,
            application,
        )[db_c.ID]

        logging.info(
            "Added %s, %s.",
            application[db_c.NAME],
            result_id,
        )

    logging.info("Pre-populate applications complete.")


if __name__ == "__main__":
    # Initiate Data Base client
    db_client = get_mongo_client()
    drop_collections(db_client)
    insert_data_sources(db_client, DATA_SOURCES_LIST)
    insert_delivery_platforms(db_client, DELIVERY_PLATFORM_LIST)
    insert_configurations(db_client, configurations_constants)
    insert_models(db_client, models_list)
    insert_client_projects(db_client, client_projects_list)
    insert_applications(db_client, applications_constants)
    logging.info("Pre-populate database procedure complete.")
