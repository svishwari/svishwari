# pylint: disable=too-many-lines
"""This module contains connector defines."""
import os
import random
from collections import namedtuple

from huxunifylib.database import constants as db_c

TEST_MODE = "pytest"
DEVELOPMENT_MODE = "development"
PRODUCTION_MODE = "production"
FLASK_ENV = "FLASK_ENV"
TEST_AUTH_OVERRIDE = "TEST_AUTH_OVERRIDE"
SSM_INIT_LOAD_DELIMITER = "||"
HOST = "host"
PORT = "port"
USER = "user"
USERNAME = "username"
PASSWORD = "password"
SSL_CERT_PATH = "ssl_cert_path"
AWS_REGION = "AWS_REGION"
AWS_S3_BUCKET_CONST = "S3_DATASET_BUCKET"
MONGO_DB_HOST = "MONGO_DB_HOST"
MONGO_DB_PORT = "MONGO_DB_PORT"
MONGO_DB_USERNAME = "MONGO_DB_USERNAME"
MONGO_DB_PASSWORD = "MONGO_DB_PASSWORD"
OKTA_CLIENT_ID = "OKTA_CLIENT_ID"
OKTA_ISSUER = "OKTA_ISSUER"
RETURN_EMPTY_AUDIENCE_FILE = "RETURN_EMPTY_AUDIENCE_FILE"
JSON_SORT_KEYS_CONST = "JSON_SORT_KEYS"
CDP_SERVICE = "CDP_SERVICE"
CDP_CONNECTION_SERVICE = "CDP_CONNECTION_SERVICE"
TECTON_API_KEY = "TECTON_API_KEY"
TECTON_API = "TECTON_API"
MOCK_TECTON = "MOCK_TECTON"
AUDIENCE_ROUTER_JOB_ROLE_ARN_CONST = "AUDIENCE-ROUTER-JOB-ROLE-ARN"
AUDIENCE_ROUTER_EXECUTION_ROLE_ARN_CONST = "AUDIENCE-ROUTER-EXECUTION-ROLE-ARN"
AUDIENCE_ROUTER_IMAGE_CONST = "AUDIENCE-ROUTER-IMAGE"
AUDIENCE_ROUTER_JOB_QUEUE_CONST = "AUDIENCE-ROUTER-JOB-QUEUE"
CDPR_EVENT_CONST = "CDPR-EVENT"
FLDR_EVENT_CONST = "FLDR-EVENT"
DISABLE_DELIVERIES = "DISABLE_DELIVERIES"
DISABLE_DELIVERY_MSG = "Deliveries are disabled."
SALES_FORECASTING = "Sales forecasting"

# ORCH ROUTER PARAMS FOR OKTA
UNIFIED_OKTA_REDIRECT_URI = "unified_okta_redirect_uri"
UNIFIED_OKTA_TEST_USER_NAME = "unified_okta_test_user_name"
UNIFIED_OKTA_TEST_USER_PW = "unified_okta_test_user_pw"

# JIRA
JIRA_PROJECT_KEY = "JIRA_PROJECT_KEY"
JIRA_SERVER = "JIRA_SERVER"
JIRA_API_KEY = "JIRA_API_KEY"
ISSUE_TYPE = "issue_type"
KEY = "key"
TASK = "Task"
TICKET_TYPE_BUG = "Bug"

# general defines
ID = "id"
NAME = "name"
LABEL = "label"
OWNER = "owner"
STATUS = "status"
BODY = "body"
TYPE = "type"
ROLE = "role"
DESCRIPTION = "description"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
EMAIL = "email"
PHONE = "phone"
AGE = "age"
GENDER = "gender"
CATEGORY = "category"
ADDRESS = "address"
CITY = "city"
STATE = "state"
ZIP = "zip"
ZIP_CODE = "zip_code"
COOKIE = "cookie"
PROP = "prop"
ICON = "icon"
CREATED_BY = "created_by"
MATCH_CONFIDENCE = "match_confidence"
DELIVERIES = "deliveries"
DEFAULT_AUDIENCE_DELIVERY_COUNT = 2
OVERVIEW = "overview"
DATE_RANGE = "date_range"
HUX_ID = "hux_id"
REDACT_FIELD = "redact"
LIMIT = "limit"
CREATE_TIME = "create_time"
CONTACT_EMAIL = "contact_email"
CLIENT_REQUEST = "client_request"
CLIENT_ACCOUNT = "client_account"
USE_CASE = "use_case"
FIELD_TYPE = "field_type"
INTERVAL = "interval"

QUERY_PARAMETER_BATCH_SIZE = "batch_size"
QUERY_PARAMETER_BATCH_NUMBER = "batch_number"
QUERY_PARAMETER_SORT_ORDER = "sort_order"
QUERY_PARAMETER_NOTIFICATION_TYPES = "notification_types"
QUERY_PARAMETER_NOTIFICATION_CATEGORY = "category"
QUERY_PARAMETER_USERS = "users"

HEALTH_CHECK_ENDPOINT = "/health-check"
HEALTH_CHECK = "healthcheck"

TOTAL_RECORDS = "total_records"
MATCH_RATE = "match_rate"
MATCH_RATES = "match_rates"
TOTAL = "total"
TOTAL_UNIQUE_IDS = "total_unique_ids"
TOTAL_UNKNOWN_IDS = "total_unknown_ids"
TOTAL_KNOWN_IDS = "total_known_ids"
TOTAL_INDIVIDUAL_IDS = "total_individual_ids"
TOTAL_HOUSEHOLD_IDS = "total_household_ids"
TOTAL_ADDRESS_IDS = "total_address_ids"
TOTAL_ANONYMOUS_IDS = "total_anonymous_ids"
UPDATED = "updated"
TOTAL_CUSTOMERS = "total_customers"
NEW_CUSTOMERS_ADDED = "new_customers_added"
CUSTOMERS_LEFT = "customers_left"
TOTAL_COUNTRIES = "total_countries"
TOTAL_COUNT = "total_count"
TOTAL_STATES = "total_us_states"
TOTAL_CITIES = "total_cities"
COUNTRIES = "countries"
STATES = "states"
CITIES = "cities"
MIN_AGE = "min_age"
MAX_AGE = "max_age"
AVERAGE_AGE = "avg_age"
GENDER_WOMEN = "gender_women"
GENDER_MEN = "gender_men"
GENDER_OTHER = "gender_other"
GENDER_WOMEN_COUNT = "gender_women_count"
GENDER_MEN_COUNT = "gender_men_count"
GENDER_OTHER_COUNT = "gender_other_count"
GENDERS = [GENDER_WOMEN, GENDER_MEN, GENDER_OTHER]
MIN_LTV_PREDICTED = "min_ltv_predicted"
MAX_LTV_PREDICTED = "max_ltv_predicted"
MIN_LTV_ACTUAL = "min_ltv_actual"
MAX_LTV_ACTUAL = "max_ltv_actual"
AVG_LTV = "avg_ltv"
MIN_LTV = "min_ltv"
MAX_LTV = "max_ltv"
COUNTRY = "country"
CONTACT_PREFERENCES = "contact_preferences"
IDENTITY_RESOLUTION = "identity_resolution"
POPULATION_PERCENTAGE = "population_percentage"
PERCENTAGE = "percentage"
CO_OCCURRENCES = "cooccurrences"
IDENTIFIER = "identifier"
INCOME = "income"
COUNT = "count"
AVG_SPENT_WOMEN = "avg_spent_women"
AVG_SPENT_MEN = "avg_spent_men"
AVG_SPENT_OTHER = "avg_spent_other"
REVENUE = "revenue"
YEAR = "year"
MONTH = "month"
MINUTE = "minute"
HOUR = "hour"
PERIOD = "period"
DAY_OF_WEEK = "day_of_week"
MONTHLY_PERIOD_ITEMS = "monthly_period_items"
DAY_OF_MONTH = "day_of_month"
DAILY = "Daily"
MONTHLY = "Monthly"
WEEKLY = "Weekly"
EVERY = "every"
AM = "AM"
PM = "PM"
PERIODICIY = "periodicity"
MONTHLY_PERIOD_LIST = ["Day", "First", "Second", "Third", "Fourth", "Last"]
DAY_LIST = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
DAY_OF_MONTH_NAME_LIST = [
    "Day",
    "Weekend",
    "Weekend day",
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]
DAY_OF_MONTH_LIST = [str(x) for x in range(1, 32)] + DAY_OF_MONTH_NAME_LIST
AUTOMATED_DELIVERY_MINUTE_CRON = "*/15"
SCHEDULE = "schedule"
SCHEDULE_CRON = "schedule_cron"
NEXT_DELIVERY = "next_delivery"
DIGITAL_ADVERTISING = "digital_advertising"
# TODO: Remove State Names once it connected with CDM
STATE_NAMES = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District of Columbia",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
    "PR": "Puerto Rico",
}
STATE_LABEL = "state_label"
COUNTRIES_LIST = {"US": "United States"}
COUNTRY_LABEL = "country_label"
DEMOGRAPHIC = "demo"
DATE = "date"
RECORDED = "recorded"
DIFFERENCE_COUNT = "diff_count"
EXCLUDE = "exclude"

# AWS defines
AWS_MODULE_NAME = "huxunify.api.data_connectors.aws"
AWS_SSM_NAME = "ssm"
AWS_EVENTS_NAME = "events"
AWS_BATCH_NAME = "batch"
AWS_S3_NAME = "s3"
AWS_SSM_PARAM_NOT_FOUND_ERROR_MESSAGE = "Required parameter(s) not found."

AWS_BUCKET = "Bucket"
AWS_TARGET_ID = "Id"
AWS_TARGET_ARN = "Arn"
AWS_TARGET_ROLE_ARN = "RoleArn"
AWS_TARGET_BATCH_PARAMS = "BatchParameters"

REQUIRED = "required"
DELIVERY_SCHEDULE = "delivery_schedule"
START_DATE = "start_date"
END_DATE = "end_date"
ENABLED = "enabled"
DISABLED = "disabled"
SIZE = "size"
IS_ADDED = "is_added"
DAY = "day"
WEEK = "week"
REQUESTED = "requested"

STATUS_NOT_DELIVERED = "Not Delivered"
STATUS_DELIVERED = "Delivered"
STATUS_DELIVERING = "Delivering"
STATUS_DELIVERY_PAUSED = "Delivery Paused"
STATUS_ACTIVE = "Active"
STATUS_INACTIVE = "Inactive"
STATUS_DISABLED = "Disabled"
STATUS_DRAFT = "Draft"
STATUS_PENDING = "Pending"
STATUS_REQUESTED = "Requested"
STATUS_ERROR = "Error"
STATUS_PAUSED = "Paused"
STATUS_STOPPED = "Stopped"

# used for weighting the rollup status for engagement deliveries
# 0 being the highest.
WEIGHT = "weight"
STATUS_WEIGHTS = {
    STATUS_ACTIVE: 11,
    STATUS_DELIVERED: 10,
    STATUS_NOT_DELIVERED: 9,
    STATUS_DELIVERING: 8,
    STATUS_DELIVERY_PAUSED: 7,
    STATUS_INACTIVE: 5,
    STATUS_DRAFT: 4,
    STATUS_PENDING: 3,
    db_c.STATUS_IN_PROGRESS: 3,
    STATUS_PAUSED: 2,
    STATUS_STOPPED: 1,
    STATUS_ERROR: 0,
    db_c.STATUS_FAILED: 0,
}
# Download Audience Fields
DOWNLOAD_TYPE = "download_type"
GOOGLE_ADS = "google_ads"
AMAZON_ADS = "amazon_ads"
GENERIC_ADS = "generic_ads"
GOOGLE_ADS_DEFAULT_COLUMNS = [
    "Zip",
    "Country",
    "First Name",
    "Phone",
    "Last Name",
    "Email",
]
AMAZON_ADS_DEFAULT_COLUMNS = [
    "zip",
    "first_name",
    "phone",
    "last_name",
    "state",
    "address",
    "email",
]
GENERIC_ADS_DEFAULT_COLUMNS = [
    "hux_id",
    "address",
    "address_hashed",
    "city_hashed",
    "country_code_hashed",
    "date_of_birth_day_hashed",
    "date_of_birth_month_hashed",
    "date_of_birth_year_hashed",
    "email_address",
    "email_address_hashed",
    "email_preference",
    "first_name",
    "first_name_hashed",
    "first_name_initial_hashed",
    "gender_hashed",
    "last_name",
    "last_name_hashed",
    "mobile_device_id",
    "phone_number_digits_only_hashed",
    "postal_code_hashed",
    "state_or_province_hashed",
]

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
SFMC_PERFORMANCE_METRICS_DATA_EXTENSIONS = "perf_data_extensions"
SFMC_PERFORMANCE_METRICS_DATA_EXTENSION = "performance_metrics_data_extension"
SFMC_CAMPAIGN_ACTIVITY_DATA_EXTENSION = "campaign_activity_data_extension"
SFMC_DATA_EXTENSION_NAME = "Name"
SFMC_CUSTOMER_KEY = "CustomerKey"

# Sendgrid connector defines
SENDGRID_AUTH_TOKEN = "sendgrid_auth_token"

# Qualtrics connector defines
QUALTRICS_API_TOKEN = "qualtrics_api_token"
QUALTRICS_DATA_CENTER = "qualtrics_data_center"
QUALTRICS_OWNER_ID = "qualtrics_owner_id"
QUALTRICS_DIRECTORY_ID = "qualtrics_directory_id"

# google ads connector defines
GOOGLE_DEVELOPER_TOKEN = "google_developer_token"
GOOGLE_REFRESH_TOKEN = "google_refresh_token"
GOOGLE_CLIENT_CUSTOMER_ID = "google_client_customer_id"
GOOGLE_CLIENT_ID = "google_client_id"
GOOGLE_CLIENT_SECRET = "google_client_secret"

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
    db_c.DELIVERY_PLATFORM_SENDGRID: {
        SENDGRID_AUTH_TOKEN: {
            NAME: "Auth Token",
            TYPE: "password",
            REQUIRED: True,
            DESCRIPTION: None,
        },
    },
    db_c.DELIVERY_PLATFORM_QUALTRICS: {
        QUALTRICS_API_TOKEN: {
            NAME: "Auth Token",
            TYPE: "password",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        QUALTRICS_DATA_CENTER: {
            NAME: "Data Center",
            TYPE: "text",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        QUALTRICS_OWNER_ID: {
            NAME: "Owner ID",
            TYPE: "text",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        QUALTRICS_DIRECTORY_ID: {
            NAME: "Directory ID",
            TYPE: "text",
            REQUIRED: True,
            DESCRIPTION: None,
        },
    },
    GOOGLE_ADS: {
        GOOGLE_DEVELOPER_TOKEN: {
            NAME: "Developer Token",
            TYPE: "password",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        GOOGLE_REFRESH_TOKEN: {
            NAME: "Refresh Token",
            TYPE: "password",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        GOOGLE_CLIENT_CUSTOMER_ID: {
            NAME: "Client Customer ID",
            TYPE: "text",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        GOOGLE_CLIENT_ID: {
            NAME: "Client ID",
            TYPE: "password",
            REQUIRED: True,
            DESCRIPTION: None,
        },
        GOOGLE_CLIENT_SECRET: {
            NAME: "Client Secret",
            TYPE: "password",
            REQUIRED: True,
            DESCRIPTION: None,
        },
    },
}

# DESTINATION Secret Mapping
MONGO = "mongo"
DESTINATION_SECRETS = {
    db_c.DELIVERY_PLATFORM_FACEBOOK: {
        MONGO: [
            FACEBOOK_AD_ACCOUNT_ID,
            FACEBOOK_APP_ID,
        ],
        AWS_SSM_NAME: [FACEBOOK_ACCESS_TOKEN, FACEBOOK_APP_SECRET],
    },
    db_c.DELIVERY_PLATFORM_SFMC: {
        MONGO: [
            SFMC_CLIENT_ID,
            SFMC_AUTH_BASE_URI,
            SFMC_ACCOUNT_ID,
            SFMC_SOAP_BASE_URI,
            SFMC_REST_BASE_URI,
        ],
        AWS_SSM_NAME: [SFMC_CLIENT_SECRET],
    },
    db_c.DELIVERY_PLATFORM_SENDGRID: {
        MONGO: [],
        AWS_SSM_NAME: [SENDGRID_AUTH_TOKEN],
    },
    db_c.DELIVERY_PLATFORM_QUALTRICS: {
        MONGO: [
            QUALTRICS_DIRECTORY_ID,
            QUALTRICS_DATA_CENTER,
            QUALTRICS_OWNER_ID,
        ],
        AWS_SSM_NAME: [QUALTRICS_API_TOKEN],
    },
    db_c.DELIVERY_PLATFORM_GOOGLE: {
        MONGO: [GOOGLE_CLIENT_CUSTOMER_ID],
        AWS_SSM_NAME: [
            GOOGLE_DEVELOPER_TOKEN,
            GOOGLE_CLIENT_SECRET,
            GOOGLE_REFRESH_TOKEN,
            GOOGLE_CLIENT_ID,
        ],
    },
}

ONLY_ADDED = "only_added"
DELETE_DATASOURCES_SUCCESS = "Successfully deleted data source(s) - {}."

# error messages
CANNOT_DELETE_DATASOURCES = "Error deleting data source(s) - {}."
INVALID_DESTINATION_AUTH = "Invalid authentication details entered."
AUTH401_ERROR_MESSAGE = "Access token is missing or invalid."
BSON_INVALID_ID = (
    lambda invalid_id: f"'{invalid_id}' is not a valid ObjectId, it must be a "
    f"12-byte input or a 24-character hex string"
)
MESSAGE = "message"
FAILED_DEPENDENCY_CONNECTION_ERROR_MESSAGE = (
    "Failed connecting to dependent API."
)
FAILED_DEPENDENCY_ERROR_MESSAGE = (
    "Failed to obtain data from dependent API endpoint."
)
EMPTY_RESPONSE_DEPENDENCY_ERROR_MESSAGE = (
    "Returned empty object from dependent API endpoint."
)

EMPTY_OBJECT_ERROR_MESSAGE = "Data not provided."
DUPLICATE_NAME = "Name already exists."
SFMC_CONFIGURATION_MISSING = "SFMC data extension config object missing."
PERFORMANCE_METRIC_DE_NOT_ASSIGNED = (
    "Performance metrics data extension not assigned."
)
CAMPAIGN_ACTIVITY_DE_NOT_ASSIGNED = (
    "Campaign activity data extension not assigned."
)
SAME_PERFORMANCE_CAMPAIGN_ERROR = (
    "Performance metric and Campaign activity cannot be same"
)
INVALID_AUTH_DETAILS = "Invalid authentication details."
INVALID_AUTH_HEADER = "Authorization header is invalid."
INVALID_AUTH = "You are not authorized to visit this page."
INVALID_BATCH_PARAMS = "Invalid Batch Number or Batch Size"

AUDIENCE_NOT_FOUND = "Audience not found."
SOURCE_AUDIENCE_NOT_FOUND = "Source Audience not found."
DESTINATION_NOT_FOUND = "Destination not found."
NOTIFICATION_NOT_FOUND = "Notification not found."
ENGAGEMENT_NOT_FOUND = "Engagement not found."
DESTINATION_NOT_SUPPORTED = "Destination is not supported."
SUCCESSFUL_DELIVERY_JOB_NOT_FOUND = "No successful delivery job found"
ZERO_AUDIENCE_SIZE = "Sum of Audience(s) is zero"
ENGAGEMENT_NO_AUDIENCES = "Engagement has no audiences."
AUDIENCE_NOT_ATTACHED_TO_ENGAGEMENT = (
    "Audience not attached to the engagement."
)
DESTINATION_NOT_ATTACHED_ENGAGEMENT_AUDIENCE = (
    "Destination not attached to the engagement audience."
)
DELIVERY_JOBS_NOT_FOUND_TO_MAP = "No delivery jobs found to map."
USER_NOT_FOUND = "User not found."

# Destination API fields
DESTINATIONS_TAG = "destinations"
DESTINATIONS_ENDPOINT = "/destinations"
DESTINATION_ID = "destination_id"
DESTINATION = "destination"
DESTINATIONS = "destinations"
DESTINATION_IDS = "destination_ids"
DESTINATION_TYPE = "type"
DELIVERY_PLATFORM_TYPE = "delivery_platform_type"
DESTINATION_NAME = "name"
DESTINATION_CAMPAIGN_COUNT = "campaign_count"
LATEST_DELIVERY = "latest_delivery"
CONNECTION_STATUS = "connection_status"
AUTHENTICATION = "authentication"
AUTHENTICATION_DETAILS = "authentication_details"
DESTINATION_REFRESH = "refresh_all"
DESTINATION_AUTHENTICATION_SUCCESS = "Destination authentication successful."
DESTINATION_AUTHENTICATION_FAILED = "Destination authentication failed."
DESTINATION_CONNECTION_FAILED = "Destination connection failed."
INVALID_STATUS = "Invalid status value."
INVALID_COMPONENT_NAME = "Invalid component name."
DATA_EXTENSIONS = "data-extensions"
DATA_EXTENSION = "data_extension"
DATA_EXTENSION_ID = "data_extension_id"
DATA_EXTENSION_NOT_SUPPORTED = "Data extension not supported"
GENERIC_DESTINATION = "generic_destination"
DESTINATIONS_CATEGORIES = "destinations_categories"
DESTINATION_AUDIENCES = "destination_audiences"

# Engagement fields
ENGAGEMENT = "engagement"
ENGAGEMENT_ID = "engagement_id"
ENGAGEMENT_IDS = "engagement_ids"
ENGAGEMENT_ENDPOINT = "/engagements"
ENGAGEMENT_TAG = "engagements"
DELIVERY_TAG = "delivery"
DELIVER = "deliver"
DELIVERY_HISTORY = "delivery-history"
CAMPAIGNS = "campaigns"
AD_SET_ID = "ad_set_id"
AD_SET_NAME = "ad_set_name"
DELIVERY_JOB_ID = "delivery_job_id"
AUDIENCE_PERFORMANCE = "audience-performance"
AUDIENCE_PERFORMANCE_LABEL = "audience_performance"
DISPLAY_ADS = "display-ads"
IS_AD_PLATFORM = "is_ad_platform"
MY_ENGAGEMENTS = "my_engagements"

DISPLAY_ADS_METRICS = [
    "spend",
    "reach",
    "impressions",
    "conversions",
    "clicks",
    "frequency",
    "cost_per_thousand_impressions",
    "click_through_rate",
    "cost_per_action",
    "cost_per_click",
    "engagement_rate",
]
EMAIL_METRICS = [
    "sent",
    "hard_bounces",
    "hard_bounces_rate",
    "delivered",
    "delivered_rate",
    "open",
    "open_rate",
    "clicks",
    "conversions",
    "click_to_open_rate",
    "unique_clicks",
    "unique_opens",
    "unsubscribe",
    "unsubscribe_rate",
]
SUMMARY = "summary"
DELIVERED = "delivered"
UNSUBSCRIBE = "unsubscribe"
UNCATEGORIZED = "uncategorized"
SPEND = "spend"
ENGAGEMENT_ID_PARAMS = [
    {
        "name": ENGAGEMENT_ID,
        "description": "Engagement ID.",
        "type": "string",
        "in": "path",
        "required": True,
        "example": "60b8d6d7d3cf80b4edcd890b",
    }
]
# CDP Data Source Constants
CDP_DATA_SOURCE_DESCRIPTION = "CDP data source body"
CDP_DATA_SOURCE_CATEGORY_MAP = {
    db_c.DATA_SOURCE_PLATFORM_ODATA: db_c.CATEGORY_API,
    db_c.DATA_SOURCE_PLATFORM_REST_API: db_c.CATEGORY_API,
    db_c.DATA_SOURCE_PLATFORM_APACHE_HIVE: db_c.CATEGORY_BIG_DATA,
    db_c.DATA_SOURCE_PLATFORM_APACHE_SPARK: db_c.CATEGORY_BIG_DATA,
    db_c.DATA_SOURCE_PLATFORM_MICROSOFT_DYNAMICS: db_c.CATEGORY_CRM,
    db_c.DATA_SOURCE_PLATFORM_NETSUITE: db_c.CATEGORY_CRM,
    db_c.DATA_SOURCE_PLATFORM_ORACLE_CRM: db_c.CATEGORY_CRM,
    db_c.DATA_SOURCE_PLATFORM_SALESFORCE: db_c.CATEGORY_CRM,
    db_c.DATA_SOURCE_PLATFORM_SAP: db_c.CATEGORY_CRM,
    db_c.DATA_SOURCE_PLATFORM_SERVICE_NOW: db_c.CATEGORY_CUSTOMER_SERVICE,
    db_c.DATA_SOURCE_PLATFORM_ZENDESK: db_c.CATEGORY_CUSTOMER_SERVICE,
    db_c.DATA_SOURCE_PLATFORM_DROPBOX: db_c.CATEGORY_DATA_FILE_STORAGE,
    db_c.DATA_SOURCE_PLATFORM_MICROSOFT_SHAREPOINT: db_c.CATEGORY_DATA_FILE_STORAGE,
    db_c.DATA_SOURCE_PLATFORM_SFTP: db_c.CATEGORY_DATA_FILE_STORAGE,
    db_c.DATA_SOURCE_PLATFORM_WINDOWS_FILESHARE: db_c.CATEGORY_DATA_FILE_STORAGE,
    db_c.DATA_SOURCE_PLATFORM_AMAZON_AURORA: db_c.CATEGORY_DATABASES,
    db_c.DATA_SOURCE_PLATFORM_BIG_QUERY: db_c.CATEGORY_DATABASES,
    db_c.DATA_SOURCE_PLATFORM_IBMDB2: db_c.CATEGORY_DATABASES,
    db_c.DATA_SOURCE_PLATFORM_MARIADB: db_c.CATEGORY_DATABASES,
    db_c.DATA_SOURCE_PLATFORM_AZURESQL: db_c.CATEGORY_DATABASES,
    db_c.DATA_SOURCE_PLATFORM_MONGODB: db_c.CATEGORY_DATABASES,
    db_c.DATA_SOURCE_PLATFORM_MYSQL: db_c.CATEGORY_DATABASES,
    db_c.DATA_SOURCE_PLATFORM_ORACLE_DB: db_c.CATEGORY_DATABASES,
    db_c.DATA_SOURCE_PLATFORM_TABLEAU: db_c.CATEGORY_DATA_VISUALIZATION,
    db_c.DATA_SOURCE_PLATFORM_BLUECORE: db_c.CATEGORY_ECOMMERCE,
    db_c.DATA_SOURCE_PLATFORM_SHOPIFY: db_c.CATEGORY_ECOMMERCE,
    db_c.DATA_SOURCE_PLATFORM_GOOGLE_ANALYTICS: db_c.CATEGORY_INTERNET,
    db_c.DATA_SOURCE_PLATFORM_GA360: db_c.CATEGORY_INTERNET,
    db_c.DATA_SOURCE_PLATFORM_HTTP: db_c.CATEGORY_INTERNET,
    db_c.DATA_SOURCE_PLATFORM_BING: db_c.CATEGORY_INTERNET,
    db_c.DATA_SOURCE_PLATFORM_AMPLITUDE: db_c.CATEGORY_MARKETING,
    db_c.DATA_SOURCE_PLATFORM_AQFER: db_c.CATEGORY_MARKETING,
    db_c.DATA_SOURCE_PLATFORM_GOOGLEADS: db_c.CATEGORY_MARKETING,
    db_c.DATA_SOURCE_PLATFORM_AMAZONADS: db_c.CATEGORY_MARKETING,
    db_c.DATA_SOURCE_PLATFORM_ADOBE: db_c.CATEGORY_MARKETING,
    db_c.DATA_SOURCE_PLATFORM_HUBSPOT: db_c.CATEGORY_MARKETING,
    db_c.DATA_SOURCE_PLATFORM_MAILCHIMP: db_c.CATEGORY_MARKETING,
    db_c.DATA_SOURCE_PLATFORM_MARKETO: db_c.CATEGORY_MARKETING,
    db_c.DATA_SOURCE_PLATFORM_MICROSOFT_ADS: db_c.CATEGORY_MARKETING,
    db_c.DATA_SOURCE_PLATFORM_SFMC: db_c.CATEGORY_MARKETING,
    db_c.DATA_SOURCE_PLATFORM_AMAZONS3: db_c.CATEGORY_OBJECT_STORAGE,
    db_c.DATA_SOURCE_PLATFORM_AZUREBLOB: db_c.CATEGORY_OBJECT_STORAGE,
    db_c.DATA_SOURCE_PLATFORM_GOOGLE_CLOUD_STORAGE: db_c.CATEGORY_OBJECT_STORAGE,
    db_c.DATA_SOURCE_PLATFORM_GOOGLE_SHEETS: db_c.CATEGORY_FILES,
    db_c.DATA_SOURCE_PLATFORM_MICROSOFT_EXCEL: db_c.CATEGORY_FILES,
    db_c.DATA_SOURCE_PLATFORM_PAYPAL: db_c.CATEGORY_FINANCE,
    db_c.DATA_SOURCE_PLATFORM_QUICKBOOKS: db_c.CATEGORY_FINANCE,
    db_c.DATA_SOURCE_PLATFORM_SQUARE: db_c.CATEGORY_FINANCE,
    db_c.DATA_SOURCE_PLATFORM_STRIPE: db_c.CATEGORY_FINANCE,
    db_c.DATA_SOURCE_PLATFORM_AOL: db_c.CATEGORY_PRODUCTIVITY,
    db_c.DATA_SOURCE_PLATFORM_GMAIL: db_c.CATEGORY_PRODUCTIVITY,
    db_c.DATA_SOURCE_PLATFORM_INSIGHTIQ: db_c.CATEGORY_PRODUCTIVITY,
    db_c.DATA_SOURCE_PLATFORM_JIRA: db_c.CATEGORY_PRODUCTIVITY,
    db_c.DATA_SOURCE_PLATFORM_MANDRILL: db_c.CATEGORY_PRODUCTIVITY,
    db_c.DATA_SOURCE_PLATFORM_MEDALLIA: db_c.CATEGORY_PRODUCTIVITY,
    db_c.DATA_SOURCE_PLATFORM_OUTLOOK: db_c.CATEGORY_PRODUCTIVITY,
    db_c.DATA_SOURCE_PLATFORM_QUALTRICS: db_c.CATEGORY_PRODUCTIVITY,
    db_c.DATA_SOURCE_PLATFORM_SENDGRID: db_c.CATEGORY_PRODUCTIVITY,
    db_c.DATA_SOURCE_PLATFORM_SURVEY_MONKEY: db_c.CATEGORY_PRODUCTIVITY,
    db_c.DATA_SOURCE_PLATFORM_TWILIO: db_c.CATEGORY_PRODUCTIVITY,
    db_c.DATA_SOURCE_PLATFORM_YAHOO: db_c.CATEGORY_PRODUCTIVITY,
    db_c.DATA_SOURCE_PLATFORM_FACEBOOK: db_c.CATEGORY_SOCIAL_MEDIA,
    db_c.DATA_SOURCE_PLATFORM_INSTAGRAM: db_c.CATEGORY_SOCIAL_MEDIA,
    db_c.DATA_SOURCE_PLATFORM_LINKEDIN: db_c.CATEGORY_SOCIAL_MEDIA,
    db_c.DATA_SOURCE_PLATFORM_SNAPCHAT: db_c.CATEGORY_SOCIAL_MEDIA,
    db_c.DATA_SOURCE_PLATFORM_TWITTER: db_c.CATEGORY_SOCIAL_MEDIA,
    db_c.DATA_SOURCE_PLATFORM_YOUTUBE: db_c.CATEGORY_SOCIAL_MEDIA,
}

CDP_DATA_SOURCE_CATEGORIES = list(set(CDP_DATA_SOURCE_CATEGORY_MAP.values()))
ACTION_ACTIVATED = "activated"
ACTION_REQUESTED = "requested"
ACTION_REMOVED = "removed"

# Authentication API fields
AUTHORIZATION = "Authorization"
AUTHENTICATION_TOKEN = "token"
AUTHENTICATION_ACCESS_TOKEN = "access_token"
AUTHENTICATION_TOKEN_TYPE_HINT = "token_type_hint"
OKTA_TEST_USER_NAME = "OKTA_TEST_USER_NAME"
OKTA_TEST_USER_PW = "OKTA_TEST_USER_PW"
OKTA_REDIRECT_URI = "OKTA_REDIRECT_URI"
OKTA_USER_ID = "user_id"
OKTA_UID = "uid"
OKTA_ID_SUB = "sub"

# define access levels for RBAC
AccessLevel = namedtuple(
    "AccessLevel", db_c.USER_ROLE, defaults=(db_c.USER_ROLE_VIEWER,)
)
ADMIN_LEVEL = AccessLevel(db_c.USER_ROLE_ADMIN)
EDITOR_LEVEL = AccessLevel(db_c.USER_ROLE_EDITOR)
VIEWER_LEVEL = AccessLevel(db_c.USER_ROLE_VIEWER)
USER_ROLE_ALL = [ADMIN_LEVEL, EDITOR_LEVEL, VIEWER_LEVEL]

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
AUDIENCE_FILTERS_EQUALS = "equals"
AUDIENCE_FILTER_CITY = "City"
INSIGHTS = "insights"
AUDIENCE_FILTER_FIELD = "field"
AUDIENCE_FILTER_TYPE = "type"
AUDIENCE_FILTER_VALUE = "value"
AUDIENCE_LAST_DELIVERED = "last_delivered"
AUDIENCE_LAST_DELIVERY = "last_delivery"
AUDIENCE_ENGAGEMENTS = "engagements"
AUDIENCE_SIZE_PERCENTAGE = "audience_size_percentage"
AUDIENCE_STANDALONE_DELIVERIES = "standalone_deliveries"
AUDIENCE_ROUTER_STUB_TEST = "AUDIENCE_ROUTER_STUB_TEST"
AUDIENCE_ROUTER_CERT_PATH = "../rds-combined-ca-bundle.pem"
AUDIENCE_ROUTER_MONGO_PASSWORD_FROM = "unifieddb_rw"
LOOKALIKE_AUDIENCES = "lookalike_audiences"
LOOKALIKE_AUDIENCES_ENDPOINT = "/lookalike-audiences"
LOOKALIKEABLE = "lookalikeable"
IS_LOOKALIKE = "is_lookalike"
LOOKALIKE = "lookalike"
LOOKALIKE_SOURCE_EXISTS = "source_exists"
WORKED_BY = "worked_by"
ATTRIBUTE = "attribute"

PARAM_STORE_PREFIX = "unified"
PARAMETER_STORE_ERROR_MSG = (
    "An error occurred while attempting to"
    " store secrets in the parameter store."
)

# users
USER_TAG = "user"
USER_NAME = "user_name"
DISPLAY_NAME = "display_name"
USER_PHONE_NUMBER = "phone_number"
USER_ACCESS_LEVEL = "access_level"
USER_PII_ACCESS = "pii_access"
USER_DESCRIPTION = "USER API"
USER_ENDPOINT = "/users"
FAVORITE = "favorite"
FAVORITES = "favorites"
PROFILE = "profile"
CONTACT_US = "contact-us"

# Models
# TODO: Remove relevant constants from here once integrated with Tecton API
MODELS_TAG = "model"
MODEL = "model"
MODELS = "models"
MODELS_ENDPOINT = "/models"
MODELS_VERSION_HISTORY = "version-history"
MODEL_NAME = "model_name"
MODEL_TYPE = "model_type"
MODEL_ID = "model_id"
MODEL_SHAP_DATA = "shap_data"
MODEL_ONE_SHAP_DATA = [
    "dow-pe_u_dow-count",
    "duration_days-order-min",
    "dow-u_wd-weekday",
    "dow-pe_u_wd-weekday",
    "1to2y-quantity-cnt",
    "1to2y-data_source-transactions",
    "1to2y-price-max",
    "1to2y-price-sum",
    "1to2y-price-avg",
    "1to2y-price-cnt",
    "1to2y-positive-order",
    "1to2y-type-transaction",
    "1to2y-quantity-max",
    "1to2y-quantity-sum",
    "1to2y-quantity-avg",
    "dow-pe_u_dow-thursday",
    "dow-u_dow-thursday",
    "8to12m-data_source-transactions",
    "8to12m-price-max",
    "8to12m-price-sum",
]
MODEL_TWO_SHAP_DATA = [
    "8to12m-price-min",
    "8to12m-price-avg",
    "8to12m-price-cnt",
    "8to12m-type-transaction",
    "8to12m-positive-order",
    "8to12m-quantity-max",
    "8to12m-quantity-sum",
    "8to12m-quantity-avg",
    "dow-pe_u_dow-tuesday",
    "dow-u_dow-tuesday",
    "1to2y-description-red",
    "dow-u_dow-wednesday",
    "dow-pe_u_dow-wednesday",
    "4m-quantity-cnt",
    "4m-price-avg",
    "4m-price-sum",
    "4m-price-max",
    "4m-price-cnt",
    "4m-price-min",
    "1to2y-description-set",
]
MODEL_ID_PARAMS = [
    {
        "name": MODEL_ID,
        "description": "Model id",
        "type": "string",
        "in": "path",
        "required": True,
        "example": "1",
    }
]
MODEL_STATUS_MAPPING = {
    "success": STATUS_ACTIVE,
    "pending": STATUS_PENDING,
    "active": STATUS_ACTIVE,
}

PURCHASE = "purchase"
LTV = "ltv"
RMSE = "rmse"
AUC = "auc"
RECALL = "recall"
CURRENT_VERSION = "current_version"
PRECISION = "precision"
PERFORMANCE_METRIC = "performance_metric"
FEATURE_IMPORTANCE = "feature-importance"
SCORE = "score"

FEATURES = "features"
JOIN_KEYS = "joinKeys"
RESULTS = "results"
LATEST_VERSION = "latest_version"
VERSION = "version"
FULCRUM_DATE = "fulcrum_date"
LAST_TRAINED = "last_trained"
LOOKBACK_WINDOW = "lookback_window"
PREDICTION_WINDOW = "prediction_window"
PAST_VERSION_COUNT = "past_version_count"
FEATURE_SERVICE = "feature_service"
DATA_SOURCE = "data_source"
POPULARITY = "popularity"
BUCKET = "bucket"
PREDICTED_VALUE = "predicted_value"
ACTUAL_VALUE = "actual_value"
PROFILE_COUNT = "profile_count"
PREDICTED_RATE = "predicted_rate"
ACTUAL_RATE = "actual_rate"
PREDICTED_LIFT = "predicted_lift"
ACTUAL_LIFT = "actual_lift"
PROFILE_SIZE_PERCENT = "profile_size_percent"
RUN_DATE = "run_date"
DRIFT = "drift"
REGRESSION_MODELS = [LTV]
CLASSIFICATION_MODELS = [UNSUBSCRIBE, PURCHASE]

# CDP DATA SOURCES
CDP_DATA_SOURCES_TAG = "data sources"
CDP_DATA_SOURCES_ENDPOINT = "/data-sources"
CDP_DATA_SOURCE_IDS = "data_source_ids"
CDP_DATA_SOURCE_TYPE = "datasource_type"

# Customers
CUSTOMERS_ENDPOINT = "/customers"
CUSTOMERS_TAG = "customers"
CUSTOMERS_INSIGHTS = "customers-insights"
GEOGRAPHICAL = "geo"
CUSTOMERS_API_HEADER_KEY = "x-api-key"
CUSTOMERS_DEFAULT_BATCH_SIZE = 1000
CUSTOMER_COUNT = "customer_count"
OPT_IN = "Opt-In"
OPT_OUT = "Opt-Out"
PREFERENCE_EMAIL = "preference_email"
PREFERENCE_PUSH = "preference_push"
PREFERENCE_SMS = "preference_sms"
PREFERENCE_IN_APP = "preference_in_app"

MAX_WORKERS_THREAD_POOL = os.cpu_count() * 1 + 1

# Demographic
CITIES_DEFAULT_BATCH_SIZE = 100

# Notifications
NOTIFICATIONS_TAG = "notifications"
NOTIFICATION_ID = "notification_id"
NOTIFICATIONS_ENDPOINT = "/notifications"
NOTIFICATION_STREAM_TIME_SECONDS = 60

NOTIFICATION_CATEGORIES = [
    ENGAGEMENT_TAG,
    DELIVERY_TAG,
    ORCHESTRATION_TAG,
    DESTINATIONS_TAG,
    CDP_DATA_SOURCES_TAG,
    CUSTOMERS_TAG,
    MODELS,
]
# AWS BATCH
BATCH_SIZE = "batch_size"

# TODO HUS-363 remove once we can pass empty filters to CDP.
CUSTOMER_OVERVIEW_DEFAULT_FILTER = {
    "filters": [
        {
            "section_aggregator": "ALL",
            "section_filters": [
                {"field": "country", "type": "equals", "value": "US"}
            ],
        }
    ]
}

# IDR Fields
IDR_TAG = "idr"
IDR_ENDPOINT = "/idr"
DATA_FEEDS = "data_feeds"
TIMESTAMP = "timestamp"
STITCHED = "stitched"
PINNING = "pinning"

# IDR Matching Trends
MATCHING_TRENDS = "matching-trends"

KNOWN_IDS = "known_ids"
UNIQUE_HUX_IDS = "unique_hux_ids"
ANONYMOUS_IDS = "anonymous_ids"

# IDR Data feeds
DATAFEED_ID = "datafeed_id"
DATAFEED_DATA_SOURCE_TYPE = "datasource_name"
DATAFEED_DATA_SOURCE_NAME = "datasource_label"
DATAFEED_NEW_IDS_COUNT = "new_ids_generated"
DATAFEED_RECORDS_PROCESSED_COUNT = "total_rec_processed"
PINNING_TIMESTAMP = "pinning_timestamp"
STITCHED_TIMESTAMP = "stitched_timestamp"

# customer event fields
CUSTOMER_TOTAL_DAILY_EVENT_COUNT = "total_event_count"
CUSTOMER_DAILY_EVENT_WISE_COUNT = "event_type_counts"
ABANDONED_CART_EVENT = "abandoned_cart"
CUSTOMER_LOGIN_EVENT = "customer_login"
VIEWED_CART_EVENT = "viewed_cart"
VIEWED_CHECKOUT_EVENT = "viewed_checkout"
VIEWED_SALE_ITEM_EVENT = "viewed_sale_item"
TRAIT_COMPUTED_EVENT = "trait_computed"
ITEM_PURCHASED_EVENT = "item_purchased"
TRAIT = "trait"
SALE = "sale"
VIEW_CONTENT = "view_content"
PRODUCT_SEARCH = "product_search"
ABANDONED_CARTS = "abandoned_carts"
TRAITS_ANALYZED = "traits_analysed"
SALES_MADE = "sales_made"
CONTENT_VIEWED = "content_viewed"
PRODUCTS_SEARCHED = "products_searched"
PURCHASES_MADE = "purchases_made"
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

# Alerts Fields
DEFAULT_BATCH_SIZE = 5
DEFAULT_BATCH_NUMBER = 1

NOTIFICATION_TYPE = "notification_type"
NOTIFICATION_ID = "notification_id"

# health check prometheus metric constants
MONGO_CONNECTION_HEALTH = "mongo_connection_health"
TECTON_CONNECTION_HEALTH = "tecton_connection_health"
OKTA_CONNECTION_HEALTH = "okta_connection_health"
AWS_SSM_CONNECTION_HEALTH = "aws_ssm_connection_health"
AWS_BATCH_CONNECTION_HEALTH = "aws_batch_connection_health"
AWS_S3_CONNECTION_HEALTH = "aws_s3_connection_health"
AWS_EVENTS_CONNECTION_HEALTH = "aws_events_connection_health"
CDM_API_CONNECTION_HEALTH = "cdm_api_connection_health"
CDM_CONNECTION_SERVICE_CONNECTION_HEALTH = (
    "cdm_connection_service_connection_health"
)

# CDM API constants
CDM_CONNECTIONS_ENDPOINT = "connections"
CDM_IDENTITY_ENDPOINT = "identity"
DATASOURCES = "datasources"
DATAFEEDS = "datafeeds"

PROPENSITY_TO_PURCHASE_FEATURES_RESPONSE_STUB = [
    {
        ID: 3,
        VERSION: "22.8.32",
        NAME: random.choice(
            [
                f"4w-ORDTDOL-cnt-{i}",
                f"profile-NSTOREDIST-sum-{i}",
                f"2m-ITEMNO-94508948346-{i}",
                f"2w-ORDAMT-max-{i}",
                f"1to2y-COGS-sum-{i}",
                f"1to2y-ITEMQTY-avg-{i}",
                f"2m-ORDTDOL-cnt-{i}",
                f"dow-pe_u_dow-pe_count-{i}",
                f"duration_days-item-min-{i}",
                f"2m-COGS-cnt-{i}",
            ]
        ),
        FEATURE_SERVICE: PURCHASE,
        DATA_SOURCE: random.choice(
            ["Buyers", "Retail", "Promotion", "Email", "Ecommerce"]
        ),
        CREATED_BY: random.choice(["Susan Miller", "Jack Miller"]),
        STATUS: random.choice(
            [
                STATUS_PENDING,
                STATUS_ACTIVE,
                STATUS_STOPPED,
            ]
        ),
        POPULARITY: random.randint(1, 3),
        SCORE: round(random.uniform(0.5, 2.9), 4),
    }
    for i in range(50)
]

PROPENSITY_TO_PURCHASE_MODEL_OVERVIEW_STUB = {
    MODEL_NAME: "Propensity to Purchase",
    PERFORMANCE_METRIC: {
        RMSE: -1,
        AUC: 0.82,
        PRECISION: 0.81,
        RECALL: 0.59,
        CURRENT_VERSION: "22.8.32",
    },
    DESCRIPTION: "Predicts the propensity of a customer to make a purchase "
    "after receiving an email.",
    MODEL_TYPE: "purchase",
}

# Connections Data feeds Constants
PROCESSED_AT = "processed_at"
RECORDS_PROCESSED = "records_processed"
RECORDS_RECEIVED = "records_received"
THIRTY_DAYS_AVG = "thirty_days_avg"
RECORDS_PROCESSED_PERCENTAGE = "records_processed_percentage"

DEFAULT_DATE_FORMAT = "%Y-%m-%d"

MODELS_STUB = [
    {
        CATEGORY: "Email",
        TYPE: "Classification",
        NAME: "Propensity to Open",
        DESCRIPTION: " Propensity for a customer to open an email.",
        ID: "5df65e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Email",
        TYPE: "Classification",
        NAME: "Propensity to Click",
        DESCRIPTION: "Propensity for a customer to click "
        "on a link in an email.",
        ID: "aa789e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Email",
        TYPE: "Unknown",
        NAME: "Email Content Optimization",
        DESCRIPTION: "Alter email content to optimize "
        "email campaign performance.",
        ID: "99e45e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Trust ID",
        TYPE: "Classification",
        NAME: "Capability Propensity",
        DESCRIPTION: "Propensity for a customer to have positive,"
        " negative, or neutral capability score.",
        ID: "bc123e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Trust ID",
        TYPE: "Classification",
        NAME: "Trust Propensity",
        DESCRIPTION: "Propensity for a customer to have positive,"
        " negative, or neutral trust score.",
        ID: "a15d8e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Trust ID",
        TYPE: "Classification",
        NAME: "Humanity Propensity",
        DESCRIPTION: "Propensity for a customer to have positive,"
        " negative, or neutral humanity score.",
        ID: "bd732e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Trust ID",
        TYPE: "Classification",
        NAME: "Reliability Propensity",
        DESCRIPTION: "Propensity for a customer to have positive,"
        " negative, or neutral reliability score.",
        ID: "99d12e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Trust ID",
        TYPE: "Classification",
        NAME: "Transparency Propensity",
        DESCRIPTION: "Propensity for a customer to have positive,"
        " negative, or neutral transparency score.",
        ID: "bed54e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Retention",
        TYPE: "Classification",
        NAME: "Churn",
        DESCRIPTION: "Propensity for a customer to leave a service "
        "over a defined time range.",
        ID: "11d54e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Sales forecasting",
        TYPE: "Regression",
        NAME: "Predicted Sales Per Customer",
        DESCRIPTION: "Predicting sales for a customer over a "
        "defined time range.",
        ID: "bba67e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Sales forecasting",
        TYPE: "Regression",
        NAME: "Predicted Sales Per Store",
        DESCRIPTION: "Predicting sales for a store over a "
        "defined time range.",
        ID: "a45b7e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Web",
        TYPE: "Classification",
        NAME: "Propensity to Purchase Product Category",
        DESCRIPTION: "Propensity for a customer to make a web purchase"
        " in a particular product category.",
        ID: "88ee4e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Web",
        TYPE: "Classification",
        NAME: "Propensity to Visit Product Category",
        DESCRIPTION: "Propensity for a customer to make a web visit"
        " in a particular product category.",
        ID: "aab41e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Web",
        TYPE: "Classification",
        NAME: "Propensity to Visit Website",
        DESCRIPTION: "Propensity for a customer to visit a website.",
        ID: "99a78e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
    {
        CATEGORY: "Uncategorized",
        TYPE: "Classification",
        NAME: "Segmentation",
        DESCRIPTION: "Segment a set of customers.",
        ID: "99a78e0bd7edaad4c36bec4a3682f02d36441fe1",
        STATUS: STATUS_PENDING,
    },
]

# Configurations
CONFIGURATIONS_TAG = "configurations"
CONFIGURATION_ID = "configuration_id"
CONFIGURATIONS_ENDPOINT = "/configurations"

# Histogram data stub.
VALUES = "values"
# TODO Remove once we have data from CDP
AUDIENCE_RULES_HISTOGRAM_DATA = {
    MODEL: {
        "propensity_to_unsubscribe": {
            "name": "Propensity to unsubscribe",
            "type": "range",
            "min": 0.0,
            "max": 1.0,
            "steps": 0.05,
            "values": [
                (0.024946739301654024, 11427),
                (0.07496427927927932, 11322),
                (0.12516851755300673, 11508),
                (0.17490722222222196, 11340),
                (0.22475237305041784, 11028),
                (0.27479887395267527, 10861),
                (0.32463341819221986, 10488),
                (0.3748012142488386, 9685),
                (0.424857603462838, 9472),
                (0.4748600344076149, 8719),
                (0.5247584942372063, 8069),
                (0.5748950945245762, 7141),
                (0.6248180486698927, 6616),
                (0.6742800016897607, 5918),
                (0.7240552640642912, 5226),
                (0.7748771045863732, 4666),
                (0.8245333194000475, 4067),
                (0.8741182097701148, 3480),
                (0.9238849161073824, 2980),
                (0.9741102931596075, 2456),
            ],
        },
        "ltv_predicted": {
            "name": "Predicted lifetime value",
            "type": "range",
            "min": 0,
            "max": 998.80,
            "steps": 20,
            "values": [
                (25.01266121420892, 20466),
                (74.90030921605447, 19708),
                (124.93400516206559, 18727),
                (174.636775834374, 17618),
                (224.50257155855883, 15540),
                (274.4192853530467, 14035),
                (324.5557537562226, 11650),
                (374.0836229319332, 9608),
                (424.08129865033845, 7676),
                (474.0542931632165, 6035),
                (523.573803219089, 4610),
                (573.6697460367739, 3535),
                (623.295952316871, 2430),
                (674.0507447610822, 1737),
                (722.9281163886425, 1127),
                (773.0364963285016, 828),
                (823.8157326407769, 515),
                (872.0919142507652, 327),
                (922.9545223902437, 205),
                (975.5857619444447, 108),
            ],
        },
        "propensity_to_purchase": {
            "name": "Propensity to purchase",
            "type": "range",
            "min": 0.0,
            "max": 1.0,
            "steps": 0.05,
            "values": [
                (0.02537854973094943, 11522),
                (0.07478697708351197, 11651),
                (0.1248279331496129, 11249),
                (0.1747714344852409, 11112),
                (0.2249300773782431, 10985),
                (0.2748524565641576, 10763),
                (0.32492868003913766, 10220),
                (0.3745931779533858, 9997),
                (0.42461185061435747, 9278),
                (0.4747488547963946, 8767),
                (0.5245381213163091, 8144),
                (0.5748252185124849, 7368),
                (0.6245615267403664, 6694),
                (0.6745955099966098, 5902),
                (0.7241630427350405, 5265),
                (0.7744812744022826, 4559),
                (0.824692568267536, 3977),
                (0.8744300917431203, 3379),
                (0.9241139159001297, 3044),
                (0.9740590406189552, 2585),
            ],
        },
    },
    "age": {
        "name": "Age",
        "type": "range",
        "min": 18,
        "max": 79,
        "steps": 5,
        "values": [
            (18, 15129),
            (23, 17236),
            (28, 20589),
            (33, 22001),
            (38, 21161),
            (43, 18317),
            (48, 14023),
            (53, 9740),
            (58, 5893),
            (63, 3299),
            (68, 1557),
            (73, 731),
            (78, 65),
        ],
    },
}
