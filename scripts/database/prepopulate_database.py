"""Purpose of this file is for populating the following database documents.
 - data sources
 - destinations (delivery platforms)
"""
# pylint: disable=too-many-lines
import logging
import os

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
from huxunifylib.database.data_management import set_constant
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
        db_c.CONFIGURATION_FIELD_NAME: "Commerce personal",
        db_c.CONFIGURATION_FIELD_ICON: "commerce_personal",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Exceed eCommerce revenue goals"
        " with personalized content creation, "
        "conversion, and experience optimization, and next best offer "
        "determination.",
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
        db_c.CONFIGURATION_FIELD_STATUS: "active",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Experience data platform",
        db_c.CONFIGURATION_FIELD_ICON: "experience_data_platform",
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
        db_c.CONFIGURATION_FIELD_STATUS: "active",
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
                db_c.CONFIGURATION_FIELD_NAME: "Home",
                db_c.CONFIGURATION_FIELD_ICON: "home",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
            },
            {
                db_c.CONFIGURATION_FIELD_NAME: "Configuration",
                db_c.CONFIGURATION_FIELD_ICON: "configuration",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
            },
            {
                db_c.CONFIGURATION_FIELD_NAME: "Data Management",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
                db_c.CONFIGURATION_FIELD_CHILDREN: [
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Data Sources",
                        db_c.CONFIGURATION_FIELD_ICON: "datasource",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Identity Resolution",
                        db_c.CONFIGURATION_FIELD_ICON: "identity-resolution",
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
                        db_c.CONFIGURATION_FIELD_ICON: "models",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    }
                ],
            },
            {
                db_c.CONFIGURATION_FIELD_NAME: "Orchestration",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
                db_c.CONFIGURATION_FIELD_CHILDREN: [
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Destinations",
                        db_c.CONFIGURATION_FIELD_ICON: "multiple_map_pins",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Segment Playground",
                        db_c.CONFIGURATION_FIELD_ICON: "playground",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Audiences",
                        db_c.CONFIGURATION_FIELD_ICON: "audiences",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Engagements",
                        db_c.CONFIGURATION_FIELD_ICON: "speaker_up",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                ],
            },
            {
                db_c.CONFIGURATION_FIELD_NAME: "Insights",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
                db_c.CONFIGURATION_FIELD_CHILDREN: [
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Customers",
                        db_c.CONFIGURATION_FIELD_ICON: "customer-profiles",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "HX TrustID",
                        db_c.CONFIGURATION_FIELD_ICON: "hx-trustid",
                        db_c.CONFIGURATION_FIELD_SUPERSCRIPT: "TM",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Email Deliverability",
                        db_c.CONFIGURATION_FIELD_ICON: "email_deliverability",
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


# RBAC Matrix
rbac_matrix = {
    "constant": "rbac_matrix",
    "value": {
        "components": {
            "alerts": {
                "label": "Alerts",
                "actions": [
                    {
                        "type": "get_all",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_one",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "delete",
                        "admin": True,
                        "editor": False,
                        "viewer": False,
                    },
                ],
            },
            "destinations": {
                "label": "Destinations",
                "actions": [
                    {
                        "type": "get_constants",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "validate",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_all",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_data_extensions",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "create_data_extensions",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "set_authentication_credentials",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "get_one",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "request_unsupported_destination",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "create_one",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "delete",
                        "admin": True,
                        "editor": False,
                        "viewer": False,
                    },
                ],
            },
            "audience": {
                "label": "Audience",
                "actions": [
                    {
                        "type": "get_rules",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "create_lookalike",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "edit_lookalike",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "get_all",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "create",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "get_insights",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_countries",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_states",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_cities",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "download",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "get_one",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "update_one",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "delete_one",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                ],
            },
            "user": {
                "label": "User",
                "actions": [
                    {
                        "type": "contact_us",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_profile",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_all",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "update_one",
                        "admin": True,
                        "editor": False,
                        "viewer": False,
                    },
                    {
                        "type": "create_favorite",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "delete_favorite",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                ],
            },
            "data_source": {
                "label": "Data Source",
                "actions": [
                    {
                        "type": "get_all",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "request_new",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "delete_one",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "request_existing",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "get_datafeeds",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_one",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "update_list_of_data_sources",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                ],
            },
            "engagements": {
                "label": "Engagements",
                "actions": [
                    {
                        "type": "get_all",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "create_one",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "get_ad_metrics",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_email_metrics",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "download_email_metrics",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "add_destination_to_engagement",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "remove_destination_from_engagement",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "add_audience_to_engagement",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "remove_audience_from_engagement",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "get_one",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "update_one",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "delete_one",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                ],
            },
            "models": {
                "label": "Models",
                "actions": [
                    {
                        "type": "get_all",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "request_one",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "get_features",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_versions_history",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_overview",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_top_features",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_drift",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_lift",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                ],
            },
            "campaigns": {
                "label": "Campaigns",
                "actions": [
                    {
                        "type": "get_list_of_campaigns",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "update_campaign_for_engagement",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "get_campaign_mappings",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                ],
            },
            "delivery": {
                "label": "Delivery",
                "actions": [
                    {
                        "type": "schedule_delivery",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "delete_delivery",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "deliver",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "deliver_audience",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "deliver_engagement",
                        "admin": True,
                        "editor": True,
                        "viewer": False,
                    },
                    {
                        "type": "get_engagement_history",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_audience_history",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                ],
            },
            "customers": {
                "label": "Customers",
                "actions": [
                    {
                        "type": "country_insights",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "revenue_insights",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "state_insights",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "city_insights",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "total_customer_insights",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "demographic_insights",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "customer_data_overview",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "list_of_customers",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "events_for_customer",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_customer_profile",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "filtered_customer_data_overview",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                ],
            },
            "idr": {
                "label": "IDR",
                "actions": [
                    {
                        "type": "matching_trends",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "get_single_datafeed",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "data_feeds",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "idr_overview",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                ],
            },
            "trustid": {
                "label": "Trust ID",
                "actions": [
                    {
                        "type": "trustid_overview",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "trustid_comparison",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "trustid_attributes",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "trustid_add_segment",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                    {
                        "type": "trustid_user_filters",
                        "admin": True,
                        "editor": True,
                        "viewer": True,
                    },
                ],
            },
        }
    },
}


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
    if db_c.USER_COLLECTION in collections_to_drop:
        collections_to_drop.remove(db_c.USER_COLLECTION)

    # do not drop destination collection if it exists
    if db_c.DELIVERY_PLATFORM_COLLECTION in collections_to_drop:
        collections_to_drop.remove(db_c.DELIVERY_PLATFORM_COLLECTION)

    # if drop all collections is false, do not drop the restricted collections
    # pylint: disable=eval-used
    if not eval(os.environ.get("DROP_ALL_COLLECTIONS", default="False")):
        collections_to_drop = [
            x
            for x in collections_to_drop
            if x not in db_c.RESTRICTED_COLLECTIONS
        ]

    for collection in collections_to_drop:
        database[db_c.DATA_MANAGEMENT_DATABASE][collection].drop()
        logging.info("Dropped the %s collection.", collection)


def create_empty_collections(
    database: MongoClient, collection_names: list
) -> None:
    """Create empty collections

    Args:
        database (MongoClient): MongoDB Client
        collection_names (list): List of collection names to create
    """
    for collection_name in collection_names:
        database[db_c.DATA_MANAGEMENT_DATABASE].create_collection(collection_name)
        logging.info("Empty collection %s created.", collection_name)


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


def insert_constants(database: MongoClient, constants: list) -> None:
    """Insert data into constants collection.

    Args:
        database (MongoClient): MongoDB Client.
        constants (List): List of constants.
    """

    logging.info("Pre-populating constants.")

    for constant in constants:
        result_id = set_constant(
            database,
            constant[db_c.CONSTANT_NAME],
            constant[db_c.CONSTANT_VALUE],
        )
        logging.info(
            "Added %s, %s.",
            constant[db_c.CONSTANT_NAME],
            result_id,
        )

    logging.info("Pre-populate constants complete.")


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
    insert_constants(db_client, [rbac_matrix])
    collections_to_create = [
        db_c.LOOKALIKE_AUDIENCE_COLLECTION,
        db_c.DELIVERY_JOBS_COLLECTION,
    ]
    create_empty_collections(db_client, collections_to_create)
    logging.info("Pre-populate database procedure complete.")
