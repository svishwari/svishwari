# pylint: disable=too-many-lines
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
from pymongo import MongoClient

from database.share import get_mongo_client

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Configurations List
configurations_constants = [
    {
        db_c.CONFIGURATION_FIELD_NAME: "Data Management",
        db_c.CONFIGURATION_FIELD_ICON: "uncategorised",
        db_c.CONFIGURATION_FIELD_TYPE: "module",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Monitor data quality "
        "throughout ingestion and create a peristent"
        " identifier and profile for every consumer.",
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
        " consumer insights.",
        db_c.CONFIGURATION_FIELD_STATUS: "active",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Consumer Insights",
        db_c.CONFIGURATION_FIELD_ICON: "uncategorised",
        db_c.CONFIGURATION_FIELD_TYPE: "module",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "A 360 degree view of "
        "each consumer, understanding not only their needs and "
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
        " experience for existing and new consumers.",
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
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Brings voice of the consumer "
        "to make improvements to your consumer "
        "experience at an individual and macro level.",
        db_c.CONFIGURATION_FIELD_STATUS: "pending",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "InSightIQ",
        db_c.CONFIGURATION_FIELD_ICON: "insight_iq",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Enrich your consumer profiles"
        " with our collection of third party data to "
        "have a deeper understanding of your consumers.",
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
        db_c.CONFIGURATION_FIELD_NAME: "HX Trust ID",
        db_c.CONFIGURATION_FIELD_ICON: "trust_id",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Enables brands to gain "
        "visibility, monitor and  engage with their consumers "
        "based on AI – generated experienced based metrics.",
        db_c.CONFIGURATION_FIELD_STATUS: "active",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_ROADMAP: False,
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Search.AI",
        db_c.CONFIGURATION_FIELD_ICON: "search_ai",
        db_c.CONFIGURATION_FIELD_TYPE: "business_solution",
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Leverages search data to"
        " optimize the creation, placement, and timing of online "
        "content to increase consumer acquisition.",
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
        db_c.CONFIGURATION_FIELD_NAME:"Error Alerts",
        db_c.CONFIGURATION_FIELD_TYPE:"error_alerts",
        db_c.CONFIGURATION_FIELD_MODULES:{
            db_c.DESTINATIONS: False,
            db_c.MODELS: False,
            db_c.DATASOURCES: False
        }
    },
    {
        db_c.CONFIGURATION_FIELD_NAME: "Navigation Settings",
        db_c.CONFIGURATION_FIELD_TYPE: "navigation_settings",
        db_c.CONFIGURATION_FIELD_SETTINGS: [
            {
                db_c.CONFIGURATION_FIELD_NAME: "Home",
                db_c.CONFIGURATION_FIELD_LABEL: "Home",
                db_c.CONFIGURATION_FIELD_ICON: "home",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
            },
            {
                db_c.CONFIGURATION_FIELD_NAME: "Configuration",
                db_c.CONFIGURATION_FIELD_LABEL: "Configuration",
                db_c.CONFIGURATION_FIELD_ICON: "configuration",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
            },
            {
                db_c.CONFIGURATION_FIELD_NAME: "Data Management",
                db_c.CONFIGURATION_FIELD_LABEL: "Data Management",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
                db_c.CONFIGURATION_FIELD_CHILDREN: [
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Data Sources",
                        db_c.CONFIGURATION_FIELD_LABEL: "Data Sources",
                        db_c.CONFIGURATION_FIELD_ICON: "datasource",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Identity Resolution",
                        db_c.CONFIGURATION_FIELD_LABEL: "Identity Resolution",
                        db_c.CONFIGURATION_FIELD_ICON: "identity-resolution",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                ],
            },
            {
                db_c.CONFIGURATION_FIELD_NAME: "Decisioning",
                db_c.CONFIGURATION_FIELD_LABEL: "Decisioning",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
                db_c.CONFIGURATION_FIELD_CHILDREN: [
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Models",
                        db_c.CONFIGURATION_FIELD_LABEL: "Models",
                        db_c.CONFIGURATION_FIELD_ICON: "models",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    }
                ],
            },
            {
                db_c.CONFIGURATION_FIELD_NAME: "Orchestration",
                db_c.CONFIGURATION_FIELD_LABEL: "Orchestration",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
                db_c.CONFIGURATION_FIELD_CHILDREN: [
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Destinations",
                        db_c.CONFIGURATION_FIELD_LABEL: "Destinations",
                        db_c.CONFIGURATION_FIELD_ICON: "multiple_map_pins",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Segment Playground",
                        db_c.CONFIGURATION_FIELD_LABEL: "Segment Playground",
                        db_c.CONFIGURATION_FIELD_ICON: "playground",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Audiences",
                        db_c.CONFIGURATION_FIELD_LABEL: "Audiences",
                        db_c.CONFIGURATION_FIELD_ICON: "audiences",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Engagements",
                        db_c.CONFIGURATION_FIELD_LABEL: "Engagements",
                        db_c.CONFIGURATION_FIELD_ICON: "speaker_up",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                ],
            },
            {
                db_c.CONFIGURATION_FIELD_NAME: "Insights",
                db_c.CONFIGURATION_FIELD_LABEL: "Insights",
                db_c.CONFIGURATION_FIELD_ENABLED: True,
                db_c.CONFIGURATION_FIELD_CHILDREN: [
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Customers",
                        db_c.CONFIGURATION_FIELD_LABEL: "Customers",
                        db_c.CONFIGURATION_FIELD_ICON: "customer-profiles",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "HX TrustID",
                        db_c.CONFIGURATION_FIELD_LABEL: "HX TrustID",
                        db_c.CONFIGURATION_FIELD_ICON: "hx-trustid",
                        db_c.CONFIGURATION_FIELD_SUPERSCRIPT: "TM",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                    {
                        db_c.CONFIGURATION_FIELD_NAME: "Email Deliverability",
                        db_c.CONFIGURATION_FIELD_LABEL: "Email Deliverability",
                        db_c.CONFIGURATION_FIELD_ICON: "email_deliverability",
                        db_c.CONFIGURATION_FIELD_ENABLED: True,
                    },
                ],
            },
        ],
    },
    # RBAC Matrix constant
    {
        db_c.CONFIGURATION_FIELD_NAME: "RBAC Matrix",
        db_c.CONFIGURATION_FIELD_TYPE: db_c.CONFIGURATION_TYPE_RBAC_MATRIX,
        db_c.CONFIGURATION_FIELD_DESCRIPTION: "Role Based Access Control Matrix",
        db_c.CONFIGURATION_FIELD_ENABLED: True,
        db_c.CONFIGURATION_FIELD_SETTINGS: {
            db_c.COMPONENTS: {
                db_c.CLIENT_CONFIG: {
                    db_c.CONFIGURATION_FIELD_LABEL: "Client Settings",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "client_settings",
                            db_c.USER_ROLE_ADMIN: False,
                            db_c.USER_ROLE_EDITOR: False,
                            db_c.USER_ROLE_VIEWER: False,
                        }
                    ],
                },
                db_c.ALERTS: {
                    db_c.CONFIGURATION_FIELD_LABEL: "Alerts",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "get_all",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "delete",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: False,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                    ],
                },
                db_c.DESTINATIONS: {
                    db_c.CONFIGURATION_FIELD_LABEL: "Destinations",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "get_constants",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "validate",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_all",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_data_extensions",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "create_data_extensions",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "set_authentication_credentials",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "get_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "request_unsupported_destination",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "create_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "delete",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: False,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                    ],
                },
                db_c.AUDIENCE: {
                    db_c.CONFIGURATION_FIELD_LABEL: "Audience",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "get_rules",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "create_lookalike",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "edit_lookalike",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "get_all",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "create",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "get_insights",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_countries",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_states",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_cities",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "download",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "get_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "update_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "delete_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                    ],
                },
                db_c.USER: {
                    db_c.CONFIGURATION_FIELD_LABEL: "User",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "contact_us",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_profile",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_all",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "update_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: False,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "create_favorite",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "delete_favorite",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                    ],
                },
                db_c.DATA_SOURCE: {
                    db_c.CONFIGURATION_FIELD_LABEL: "Data Source",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "get_all",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "request_new",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "delete_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "request_existing",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "get_datafeeds",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "update_list_of_data_sources",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                    ],
                },
                db_c.ENGAGEMENTS: {
                    db_c.CONFIGURATION_FIELD_LABEL: "Engagements",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "get_all",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "create_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "get_ad_metrics",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_email_metrics",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "download_email_metrics",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "add_destination_to_engagement",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "remove_destination_from_engagement",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "add_audience_to_engagement",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "remove_audience_from_engagement",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "get_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "update_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "delete_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                    ],
                },
                db_c.MODELS: {
                    db_c.CONFIGURATION_FIELD_LABEL: "Models",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "get_all",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "request_one",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "get_features",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_versions_history",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_overview",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_top_features",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_drift",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_lift",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                    ],
                },
                db_c.CAMPAIGNS: {
                    db_c.CONFIGURATION_FIELD_LABEL: "Campaigns",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "get_list_of_campaigns",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "update_campaign_for_engagement",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "get_campaign_mappings",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                    ],
                },
                db_c.DELIVERY: {
                    db_c.CONFIGURATION_FIELD_LABEL: "Delivery",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "schedule_delivery",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "delete_delivery",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "deliver",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "deliver_audience",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "deliver_engagement",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: False,
                        },
                        {
                            db_c.TYPE: "get_engagement_history",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_audience_history",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                    ],
                },
                db_c.CUSTOMERS: {
                    db_c.CONFIGURATION_FIELD_LABEL: "Customers",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "country_insights",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "revenue_insights",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "state_insights",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "city_insights",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "total_customer_insights",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "demographic_insights",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "customer_data_overview",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "list_of_customers",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "events_for_customer",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_customer_profile",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "filtered_customer_data_overview",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                    ],
                },
                db_c.IDR: {
                    db_c.CONFIGURATION_FIELD_LABEL: "IDR",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "matching_trends",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "get_single_datafeed",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "data_feeds",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "idr_overview",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                    ],
                },
                db_c.TRUST_ID: {
                    db_c.CONFIGURATION_FIELD_LABEL: "Trust ID",
                    db_c.ACTIONS: [
                        {
                            db_c.TYPE: "trustid_overview",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "trustid_comparison",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "trustid_attributes",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "trustid_add_segment",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                        {
                            db_c.TYPE: "trustid_user_filters",
                            db_c.USER_ROLE_ADMIN: True,
                            db_c.USER_ROLE_EDITOR: True,
                            db_c.USER_ROLE_VIEWER: True,
                        },
                    ],
                },
            }
        },
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
        db_c.ACCESS_LEVEL: db_c.USER_ROLE_VIEWER,
    },
    {
        db_c.NAME: "Creatiff Inc.",
        db_c.TYPE: "creatiff-inc",
        db_c.DESCRIPTION: "Creatiff Inc. Project",
        db_c.URL: "https://localhost/creatiff",
        db_c.ICON: "default.ico",
        db_c.ACCESS_LEVEL: db_c.USER_ROLE_EDITOR,
    },
    {
        db_c.NAME: ".am",
        db_c.TYPE: "dot-am",
        db_c.DESCRIPTION: ".am Project",
        db_c.URL: "https://localhost/am",
        db_c.ICON: "default.ico",
        db_c.ACCESS_LEVEL: db_c.USER_ROLE_ADMIN,
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

empty_collections_to_create = [
    db_c.AUDIENCE_CUSTOMERS_COLLECTION,
    db_c.AUDIENCE_INSIGHTS_COLLECTION,
    db_c.AUDIENCES_COLLECTION,
    db_c.AUDIENCE_AUDIT_COLLECTION,
    db_c.CACHE_COLLECTION,
    db_c.CAMPAIGN_ACTIVITY_COLLECTION,
    db_c.DELIVERABILITY_METRICS_COLLECTION,
    db_c.DELIVERY_JOBS_COLLECTION,
    db_c.ENGAGEMENTS_COLLECTION,
    db_c.INGESTED_DATA_COLLECTION,
    db_c.INGESTED_DATA_STATS_COLLECTION,
    db_c.INGESTION_JOBS_COLLECTION,
    db_c.LOOKALIKE_AUDIENCE_COLLECTION,
    db_c.NOTIFICATIONS_COLLECTION,
    db_c.PERFORMANCE_METRICS_COLLECTION,
    db_c.SURVEY_METRICS_COLLECTION,
    db_c.USER_COLLECTION,
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
    mongo_client: MongoClient, collection_names: list
) -> None:
    """Create empty collections.

    Args:
        mongo_client (MongoClient): MongoDB Client.
        collection_names (list): List of collection names to create.
    """

    database = mongo_client[db_c.DATA_MANAGEMENT_DATABASE]

    # get the list of collection names currently present in DB
    db_collection_names = database.list_collection_names()

    for collection_name in collection_names:
        # create a new empty collection only if the collection does not already
        # exist in db
        if collection_name not in db_collection_names:
            database.create_collection(collection_name)
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
    insert_client_projects(db_client, client_projects_list)
    insert_applications(db_client, applications_constants)
    # create required empty collection for all the other collections
    create_empty_collections(db_client, empty_collections_to_create)
    logging.info("Pre-populate database procedure complete.")
