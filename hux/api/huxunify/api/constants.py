"""This module contains connector defines."""

from huxunifylib.database import constants as db_c

DEVELOPMENT_MODE = "development"
PRODUCTION_MODE = "production"
# general defines
ID = "id"
NAME = "name"
OWNER = "owner"
STATUS = "status"
BODY = "body"
TYPE = "type"
DESCRIPTION = "description"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
EMAIL = "email"
PHONE = "phone"
AGE = "age"
GENDER = "gender"
ADDRESS = "address"
CITY = "city"
STATE = "state"
ZIP = "zip"
CREATED_BY = "created_by"
UPDATED_BY = "updated_by"
MATCH_CONFIDENCE = "match_confidence"
DELIVERIES = "deliveries"
OVERVIEW = "overview"

HEALTH_CHECK_ENDPOINT = "/health-check"
HEALTH_CHECK = "healthcheck"

TOTAL_RECORDS = "total_records"
MATCH_RATE = "match_rate"
TOTAL_UNIQUE_IDS = "total_unique_ids"
TOTAL_UNKNOWN_IDS = "total_unknown_ids"
TOTAL_KNOWN_IDS = "total_known_ids"
TOTAL_INDIVIDUAL_IDS = "total_individual_ids"
TOTAL_HOUSEHOLD_IDS = "total_household_ids"
UPDATED = "updated"
TOTAL_CUSTOMERS = "total_customers"
COUNTRIES = "total_countries"
STATES = "total_us_states"
CITIES = "total_cities"
MIN_AGE = "min_age"
MAX_AGE = "max_age"
GENDER_WOMEN = "gender_women"
GENDER_MEN = "gender_men"
GENDER_OTHER = "gender_other"
MIN_LTV_PREDICTED = "min_ltv_predicted"
MAX_LTV_PREDICTED = "max_ltv_predicted"
MIN_LTV_ACTUAL = "min_ltv_actual"
MAX_LTV_ACTUAL = "max_ltv_actual"

# AWS defines
AWS_MODULE_NAME = "huxunify.api.data_connectors.aws"
AWS_SSM_NAME = "ssm"
AWS_BATCH_NAME = "batch"
AWS_HEALTH_TESTS = {
    AWS_SSM_NAME: ["get_parameter", {"Name": "unifieddb_host_alias"}],
    AWS_BATCH_NAME: ["cancel_job", {"jobId": "test", "reason": "test"}],
}

NAME = "name"
DESCRIPTION = "description"
TYPE = "type"
REQUIRED = "required"
DELIVERY_SCHEDULE = "delivery_schedule"
START_DATE = "start_date"
END_DATE = "end_date"
STATUS = "status"
ENABLED = "enabled"
SIZE = "size"
IS_ADDED = "is_added"

STATUS_NOT_DELIVERED = "Not Delivered"
STATUS_DELIVERED = "Delivered"
STATUS_DELIVERING = "Delivering"
STATUS_DELIVERY_PAUSED = "Delivery Paused"
STATUS_ACTIVE = "Active"
STATUS_INACTIVE = "Inactive"
STATUS_DRAFT = "Draft"
STATUS_PENDING = "Pending"
STATUS_ERROR = "Error"
STATUS_PAUSED = "Paused"
STATUS_STOPPED = "Stopped"

# Facebook connector defines
FACEBOOK_AD_ACCOUNT_ID = "facebook_ad_account_id"
FACEBOOK_APP_ID = "facebook_app_id"
FACEBOOK_APP_SECRET = "facebook_app_secret"
FACEBOOK_ACCESS_TOKEN = "facebook_access_token"

# SFMC connector defines
SFMC_CLIENT_ID = "sfmc_client_id"
SFMC_CLIENT_SECRET = "sfmc_client_secret"
SFMC_ACCOUNT_ID = "sfmc_account_id"
SFMC_AUTH_BASE_URI = "sfmc_auth_base_uri"
SFMC_REST_BASE_URI = "sfmc_rest_base_uri"
SFMC_SOAP_BASE_URI = "sfmc_soap_base_uri"
SFMC_PERFORMANCE_EXT_NAME = "sfmc_performance_ext_name"
SFMC_PERFORMANCE_EXT_VALUES = "sfmc_performance_ext_values"

OPERATION_SUCCESS = "SUCCESS"
OPERATION_FAILED = "FAILED"

DESTINATION_CONSTANTS = {
    db_c.DELIVERY_PLATFORM_FACEBOOK: {
        FACEBOOK_AD_ACCOUNT_ID: {
            NAME: "Ad Account ID",
            TYPE: "text",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        FACEBOOK_APP_ID: {
            NAME: "App ID",
            TYPE: "text",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        FACEBOOK_ACCESS_TOKEN: {
            NAME: "Access Token",
            TYPE: "password",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        FACEBOOK_APP_SECRET: {
            NAME: "App Secret",
            TYPE: "password",
            REQUIRED: True,
            DESCRIPTION: None,
        },
    },
    db_c.DELIVERY_PLATFORM_SFMC: {
        SFMC_ACCOUNT_ID: {
            NAME: "Account ID",
            TYPE: "text",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        SFMC_AUTH_BASE_URI: {
            NAME: "Auth Base URI",
            TYPE: "text",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        SFMC_CLIENT_ID: {
            NAME: "Client ID",
            TYPE: "text",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        SFMC_CLIENT_SECRET: {
            NAME: "Client Secret",
            TYPE: "password",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        SFMC_REST_BASE_URI: {
            NAME: "REST Base URI",
            TYPE: "text",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        SFMC_SOAP_BASE_URI: {
            NAME: "Soap Base URI",
            TYPE: "text",
            REQUIRED: True,
            DESCRIPTION: None,
        },
    },
}

# user preferences
PREFERENCE_KEY = "preference_key"
PREFERENCE_KEY_DESCRIPTION = "the preference key you want to store."
PREFERENCE_VALUE = "preference_value"
PREFERENCE_VALUE_DESCRIPTION = "the value of the preference."
PREFERENCE_BODY_DESCRIPTION = "Input preference body."
FAVORITE_BODY_DESCRIPTION = "Input favorite component body."

# error messages
CANNOT_DELETE_DESTINATIONS = "Error deleting destination(s)."
CANNOT_UPDATE_DESTINATIONS = "Error updating destination."
INVALID_DESTINATION_AUTH = "Invalid authentication details entered."
AUTH401_ERROR_MESSAGE = "Access token is missing or invalid."
INVALID_OBJECT_ID = "Object ID is not valid."
EMPTY_OBJECT_ERROR_MESSAGE = "Data not provided."
INVALID_DELIVERY_SCHEDULE = "Delivery schedule is not valid."
DUPLICATE_NAME = "Name already exists."

# Destination API fields
DESTINATIONS_TAG = "destinations"
DESTINATIONS_DESCRIPTION = "Destinations API"
DESTINATIONS_ENDPOINT = "/destinations"
DESTINATION_ID = "destination_id"
DESTINATION = "destination"
DESTINATIONS = "destinations"
DESTINATION_IDS = "destination_ids"
DESTINATION_TYPE = "type"
DELIVERY_PLATFORM_TYPE = "delivery_platform_type"
DESTINATION_NAME = "name"
DESTINATION_CAMPAIGN_COUNT = "campaign_count"
CONNECTION_STATUS = "connection_status"
AUTHENTICATION_DETAILS = "authentication_details"
DESTINATION_AUTHENTICATION_SUCCESS = "Destination authentication successful."
DESTINATION_AUTHENTICATION_FAILED = "Destination authentication failed."
DESTINATION_NOT_SUPPORTED = "Destination is not supported yet."
INVALID_ID = "Invalid Object ID."
INVALID_COMPONENT_NAME = "Invalid component name."
DATA_EXTENSIONS = "data-extensions"
DATA_EXTENSION = "data_extension"
DATA_EXTENSION_ID = "data_extension_id"
DATA_EXTENSION_FAILED = "Unable to retrieve destination data extension."

# Engagement fields
ENGAGEMENT_ID = "engagement_id"
ENGAGEMENT_IDS = "engagement_ids"
ENGAGEMENT_NAME = "engagement_name"
ENGAGEMENT_ENDPOINT = "/engagements"
ENGAGEMENT_TAG = "engagements"
DELIVERY_TAG = "delivery"
DELIVER = "deliver"
CAMPAIGNS = "campaigns"
CAMPAIGN_ID = "campaign_id"
DELIVERY_MOMENT = "delivery_moment"
DELIVERY_JOB_ID = "delivery_job_id"
AUDIENCE_PERFORMANCE = "audience-performance"
DISPLAY_ADS = "display-ads"

SPEND = "spend"
REACH = "reach"
IMPRESSIONS = "impressions"
CONVERSIONS = "conversions"
CLICKS = "clicks"
FREQUENCY = "frequency"
CPM = "cost_per_thousand_impressions"
CTR = "click_through_rate"
CPA = "cost_per_action"
CPC = "cost_per_click"
ENGAGEMENT_RATE = "engagement_rate"
SUMMARY = "summary"
IS_MAPPED = "is_mapped"

EMAIL = "email"
SENT = "sent"
HARD_BOUNCES = "hard_bounces"
HARD_BOUNCES_RATE = "hard_bounces_rate"
DELIVERED = "delivered"
DELIVERED_RATE = "delivered_rate"
OPEN = "open"
OPEN_RATE = "open_rate"
COTR = "click_to_open_rate"
UNIQUE_CLICKS = "unique_clicks"
UNIQUE_OPENS = "unique_opens"
UNSUBSCRIBE = "unsubscribe"
UNSUBSCRIBE_RATE = "unsubscribe_rate"

# CDP Data Source Constants
CDP_DATA_SOURCE_NAME = "name"
CDP_DATA_SOURCE_CATEGORY = "category"
CDP_DATA_SOURCE_DESCRIPTION = "CDP data source body"
CDP_DATA_SOURCE_FEED_COUNT = "feed_count"
CDP_DATA_SOURCE_ADDED = "is_added"
CDP_DATA_SOURCE_ENABLED = "is_enabled"

CDP_DATA_SOURCE_NAME_DESCRIPTION = "Name of the CDP data source"
CDP_DATA_SOURCE_CATEGORY_DESCRIPTION = "Category of the CDP data source"

# Authentication API fields
AUTHENTICATION_TAG = "authenticate"
AUTHENTICATION_DESCRIPTION = "Authentication API"
AUTHENTICATION_ENDPOINT = "/authenticate"
AUTHENTICATION_TOKEN = "access_token"
CANNOT_AUTHENTICATE_USER = "Error authenticating user."

AUTHENTICATION_TOKEN = "token"
AUTHENTICATION_ACCESS_TOKEN = "access_token"
AUTHENTICATION_TOKEN_TYPE_HINT = "token_type_hint"
AUTHENTICATION_OKTA_CLIENT_ID = "OKTA-CLIENT-ID"
AUTHENTICATION_OKTA_ISSUER = "OKTA-ISSUER"
OKTA_USER_ID = "user_id"
OKTA_ID_SUB = "sub"

# Orchestration API fields
ORCHESTRATION_ENDPOINT = "/orchestration"
AUDIENCE_ENDPOINT = "/audiences"
AUDIENCES = "audiences"
ORCHESTRATION_TAG = "orchestration"
AUDIENCE = "audience"
AUDIENCE_ID = "audience_id"
AUDIENCE_IDS = "audience_ids"
AUDIENCE_NAME = "name"
AUDIENCE_FILTERS = "filters"
AUDIENCE_SECTION_AGGREGATOR = "section_aggregator"
AUDIENCE_SECTION_FILTERS = "section_filters"
AUDIENCE_INSIGHTS = "audience_insights"
AUDIENCE_FILTER_FIELD = "field"
AUDIENCE_FILTER_TYPE = "type"
AUDIENCE_FILTER_VALUE = "value"
AUDIENCE_LAST_DELIVERED = "last_delivered"
AUDIENCE_ENGAGEMENTS = "engagements"
AUDIENCE_SIZE = "audience_size"
AUDIENCE_STATUS = "audience_status"
AUDIENCE_ROUTER_STUB_TEST = "AUDIENCE_ROUTER_STUB_TEST"
AUDIENCE_ROUTER_STUB_VALUE = "1"
AUDIENCE_ROUTER_CERT_PATH = "../rds-combined-ca-bundle.pem"
AUDIENCE_ROUTER_MONGO_PASSWORD_FROM = "unifieddb_rw"


STUB_INSIGHTS_RESPONSE = {
    TOTAL_CUSTOMERS: 121321321,
    COUNTRIES: 2,
    STATES: 28,
    CITIES: 246,
    MIN_AGE: 34,
    MAX_AGE: 100,
    GENDER_WOMEN: 0.4651031,
    GENDER_MEN: 0.481924,
    GENDER_OTHER: 0.25219,
}

PARAM_STORE_PREFIX = "unified"
PARAMETER_STORE_ERROR_MSG = (
    "An error occurred while attempting to"
    " store secrets in the parameter store."
)

# users
USER_TAG = "user"
USER_NAME = "user_name"
USER_DESCRIPTION = "USER API"
USER_ENDPOINT = "/users"

# Models
MODELS_TAG = "model"
MODELS_DESCRIPTION = "MODEL API"
MODELS_ENDPOINT = "/models"
MODEL_NAME = "model_name"
MODEL_NAME_PARAMS = [
    {
        "name": MODEL_NAME,
        "description": "Model name.",
        "type": "string",
        "in": "path",
        "required": True,
        "example": "churn",
    },
]
MODEL_LIST_PAYLOAD = {
    "params": {
        "feature_service_name": "ui_metadata_models_service",
        "join_key_map": {"model_metadata_client": "HUS"},
    }
}
FEATURES = "features"
JOIN_KEYS = "joinKeys"
RESULTS = "results"
LATEST_VERSION = "latest_version"
FULCRUM_DATE = "fulcrum_date"
LAST_TRAINED = "last_trained"
LOOKBACK_WINDOW = "lookback_window"
PREDICTION_WINDOW = "prediction_window"
PAST_VERSION_COUNT = "past_version_count"

# CDP DATA SOURCES
CDP_DATA_SOURCES_TAG = "data sources"
CDP_DATA_SOURCES_DESCRIPTION = "CDP DATA SOURCES API"
CDP_DATA_SOURCES_ENDPOINT = "/data-sources"
CDP_DATA_SOURCE_IDS = "data_source_ids"

# Customers
CUSTOMER_ID = "customer_id"
CUSTOMERS_ENDPOINT = "/customers"
CUSTOMERS_TAG = "customers"

# AWS BATCH
BATCH_SIZE = "batch_size"


# Customers API Fields
CUSTOMERS_TAG = "customers"
CUSTOMERS_ENDPOINT = "/customers"
CUSTOMERS_DESCRIPTION = "Customers API"

# TODO HUS-363 remove once we can pass empty filters to CDP.
CUSTOMER_OVERVIEW_DEFAULT_FILTER = {
    "filters": {
        "section_aggregator": "ALL",
        "section_filters": [
            {"field": "country", "type": "equals", "value": "us"}
        ],
    }
}

# IDR Fields
IDR_TAG = "idr"
IDR_ENDPOINT = "/idr"

# ERROR
INVALID_AUTH_HEADER = "Authorization header is invalid."
INVALID_AUTH = "You are not authorized to visit this page."

# FILTERING
REDACTED = "++REDACTED++"
CUSTOMER_PROFILE_REDACTED_FIELDS = [
    EMAIL,
    PHONE,
    AGE,
    GENDER,
    ADDRESS,
    CITY,
    STATE,
    ZIP,
]

MOCK_CUSTOMER_PROFILE_RESPONSE = {
    "id": "1531-2039-22",
    "first_name": "Bertie",
    "last_name": "Fox",
    "match_confidence": 0.96666666661,
    "since": "2020-02-20T20:02:02.202000Z",
    "ltv_actual": 60.22,
    "ltv_predicted": 59.55,
    "conversion_time": "2020-02-20T20:02:02.202000Z",
    "churn_rate": 5,
    "last_click": "2020-02-20T20:02:02.202000Z",
    "last_purchase": "2020-02-20T20:02:02.202000Z",
    "last_email_open": "2020-02-20T20:02:02.202000Z",
    "email": "bertiefox@mail.com",
    "phone": "(555)555-1231",
    "age": 53,
    "gender": "Female",
    "address": "4364 Pursglove Court",
    "city": "Dayton",
    "state": "Ohio",
    "zip": "45402-1317",
    "preference_email": False,
    "preference_push": False,
    "preference_sms": False,
    "preference_in_app": False,
    "identity_resolution": {
        "name": {
            "percentage": "0.26",
            "data_sources": [
                {
                    "id": "585t749997acad4bac4373b",
                    "name": "Adobe Experience",
                    "type": "adobe-experience",
                    "percentage": 0.49,
                },
                {
                    "id": "685t749997acad4bac4373b",
                    "name": "Google Analytics",
                    "type": "google-analytics",
                    "percentage": 0.51,
                },
            ],
        },
        "address": {"percentage": 0.2, "data_sources": []},
        "email": {"percentage": 0.34, "data_sources": []},
        "phone": {"percentage": 0.1, "data_sources": []},
        "cookie": {"percentage": 0.1, "data_sources": []},
    },
    "propensity_to_unsubscribe": 1,
    "propensity_to_purchase": 0,
}
