# pylint: disable=too-many-lines
"""This module contains connector defines."""
import os
import random
import datetime
from collections import namedtuple

from huxunifylib.database import constants as db_c

TEST_MODE = "pytest"
DEVELOPMENT_MODE = "development"
PRODUCTION_MODE = "production"
API_SPEC = "apispec_1.json"
FLASK_ENV = "FLASK_ENV"
TEST_AUTH_OVERRIDE = "TEST_AUTH_OVERRIDE"
HOST = "host"
PORT = "port"
USER = "user"
USERNAME = "username"
PASSWORD = "password"
CONNECTION_STRING = "connection_string"
SSL_FLAG = "ssl_flag"
SSL_CERT_PATH = "ssl_cert_path"
SSL_CERT_FILE_NAME = "SSL_CERT_FILE_NAME"
TLS_CERT_KEY = "tls_cert_key_file"
TLS_CERT_KEY_FILE_NAME = "TLS_CERT_KEY_FILE_NAME"
TLS_CA_CERT_KEY = "tls_ca_cert_key_file"
TLS_CA_CERT_KEY_FILE_NAME = "TLS_CA_CERT_KEY_FILE_NAME"
MONGO_DB_HOST = "MONGO_DB_HOST"
MONGO_DB_PORT = "MONGO_DB_PORT"
MONGO_DB_USERNAME = "MONGO_DB_USERNAME"
MONGO_DB_PASSWORD = "MONGO_DB_PASSWORD"
MONGO_CONNECTION_STRING = "MONGO_CONNECTION_STRING"
MONGO_DB_USE_SSL = "MONGO_DB_USE_SSL"
OKTA_CLIENT_ID = "OKTA_CLIENT_ID"
OKTA_ISSUER = "OKTA_ISSUER"
OKTA_REDIRECT_URI = "OKTA_REDIRECT_URI"
OKTA_TEST_USER_NAME = "OKTA_TEST_USER_NAME"
OKTA_TEST_USER_PW = "OKTA_TEST_USER_PW"
RETURN_EMPTY_AUDIENCE_FILE = "RETURN_EMPTY_AUDIENCE_FILE"
JSON_SORT_KEYS_CONST = "JSON_SORT_KEYS"
CDP_SERVICE = "CDP_SERVICE"
CDP_CONNECTION_SERVICE = "CDP_CONNECTION_SERVICE"
DECISIONING_URL = "DECISIONING_URL"
DISABLE_DELIVERIES = "DISABLE_DELIVERIES"
DISABLE_SCHEDULED_DELIVERIES = "DISABLE_SCHEDULED_DELIVERIES"
DISABLE_DELIVERY_MSG = "Deliveries are disabled."
DEFAULT_NEW_USER_PROJECT_NAME = "DEFAULT_NEW_USER_PROJECT_NAME"
DEFAULT_OKTA_GROUP_NAME = "DEFAULT_OKTA_GROUP_NAME"
DEFAULT_OKTA_APP = "DEFAULT_OKTA_APP"
ENVIRONMENT_NAME = "ENVIRONMENT_NAME"
FORM_PAYLOAD = "form_payload"
FORM_FILENAME = "form_filename"
FILE_OBJ = "file_obj"

# PLEASE NOTE - these are only here because DEN API
# is only available in a couple environments.
STAGING_ENV = "STG1"
LILDEV_ENV = "LILDEV"
LPZDEV_ENV = "LPZDEV"
HUSDEV2_ENV = "HUSDEV2"

# AWS constants
AWS_REGION = "AWS_REGION"
AWS_S3_BUCKET_CONST = "S3_DATASET_BUCKET"

AUDIENCE_ROUTER_JOB_ROLE_ARN_CONST = "AUDIENCE-ROUTER-JOB-ROLE-ARN"
AUDIENCE_ROUTER_EXECUTION_ROLE_ARN_CONST = "AUDIENCE-ROUTER-EXECUTION-ROLE-ARN"
AUDIENCE_ROUTER_IMAGE_CONST = "AUDIENCE-ROUTER-IMAGE"
AUDIENCE_ROUTER_CERT_PATH = "../rds-combined-ca-bundle.pem"
AUDIENCE_ROUTER_MONGO_PASSWORD_FROM = "unifieddb_rw"

CLOUD_PROVIDER = "CLOUD_PROVIDER"

# Azure constants
AZURE_BATCH_ACCOUNT_NAME = "AZURE_BATCH_ACCOUNT_NAME"
AZURE_BATCH_ACCOUNT_KEY = "AZURE_BATCH_ACCOUNT_KEY"
AZURE_BATCH_ACCOUNT_URL = "AZURE_BATCH_ACCOUNT_URL"
AZURE_STORAGE_ACCOUNT_NAME = "AZURE_STORAGE_ACCOUNT_NAME"
AZURE_STORAGE_ACCOUNT_KEY = "AZURE_STORAGE_ACCOUNT_KEY"
AZURE_STORAGE_CONNECTION_STRING = "AZURE_STORAGE_CONNECTION_STRING"
AZURE_STORAGE_CONTAINER_NAME = "AZURE_STORAGE_CONTAINER_NAME"
AZURE_STORAGE_BLOB_NAME = "AZURE_STORAGE_BLOB_NAME"
AZURE_KEY_VAULT_NAME = "AZURE_KEY_VAULT_NAME"
AZURE_TENANT_ID = "AZURE_TENANT_ID"
AZURE_CLIENT_ID = "AZURE_CLIENT_ID"
AZURE_CLIENT_SECRET = "AZURE_CLIENT_SECRET"
AZURE = "azure"

# ORCH ROUTER PARAMS FOR OKTA
UNIFIED_OKTA_REDIRECT_URI = "unified_okta_redirect_uri"
UNIFIED_OKTA_TEST_USER_NAME = "unified_okta_test_user_name"
UNIFIED_OKTA_TEST_USER_PW = "unified_okta_test_user_pw"

# JIRA
JIRA_PROJECT_KEY = "JIRA_PROJECT_KEY"
JIRA_USER_EMAIL = "JIRA_USER_EMAIL"
JIRA_SERVER = "JIRA_SERVER"
JIRA_API_KEY = "JIRA_API_KEY"
ISSUE_TYPE = "issue_type"
KEY = "key"
COMPONENT = "component"
TASK = "Task"
TICKET_TYPE_BUG = "Bug"

# general defines
ID = "id"
NAME = "name"
LABEL = "label"
OWNER = "owner"
STATUS = "status"
SUB_STATUS = "sub_status"
RUN_DURATION = "run_duration"
BODY = "body"
TYPE = "type"
ROLE = "role"
DESCRIPTION = "description"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
EMAIL = "email"
PUSH = "push"
IN_APP = "in_app"
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
URL = "url"
CREATED = "created"
ISSUES = "issues"
FIELDS = "fields"
STATUSES = "statuses"
INPUT_FILE = "input_file"
UNIQUE_ID = "unique_id"
TEXT = "text"
EVENTS = "events"
ENDPOINT = "endpoint"
RACE_ETHNICITY = "race_ethnicity"

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
DESTINATION_CHECK_CRON = "*/15"
DELIVERY_JOB_CRON = "0 * * * *"
TRUST_ID_CRON = "0 0 ? * *"
SCHEDULE = "schedule"
SCHEDULE_CRON = "schedule_cron"
NEXT_DELIVERY = "next_delivery"
UNSET = "unset"
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
AWS_S3_NAME = "s3"
AWS_SSM_PARAM_NOT_FOUND_ERROR_MESSAGE = "Required parameter(s) not found."
AWS_BUCKET = "Bucket"

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
STATUS_SUCCESS = "Success"
STATUS_COMPLETE = "Complete"
STATUS_INCOMPLETE = "Incomplete"
STATUS_RUNNING = "Running"
STATUS_FAILED = "Failed"
STATUS_CANCELLED = "Canceled"
STATUS_IN_PROGRESS = "In Progress"
STATUS_PARTIAL_SUCCESS_PROGRESS = "Partial Success - In Progress"
STATUS_WAITING = "Waiting"
STATUS_PARTIAL_SUCCESS_WAITING = "Partial Success - Waiting"
STATUS_PARTIAL_SUCCESS = "Partial Success"

STATUS_MAPPING = {
    db_c.STATUS_IN_PROGRESS: STATUS_DELIVERING,
    db_c.AUDIENCE_STATUS_DELIVERING: STATUS_DELIVERING,
    db_c.STATUS_SUCCEEDED: STATUS_DELIVERED,
    db_c.AUDIENCE_STATUS_DELIVERED: STATUS_DELIVERED,
    db_c.STATUS_FAILED: STATUS_ERROR,
    db_c.AUDIENCE_STATUS_ERROR: STATUS_ERROR,
    db_c.AUDIENCE_STATUS_PAUSED: STATUS_DELIVERY_PAUSED,
    db_c.AUDIENCE_STATUS_NOT_DELIVERED: STATUS_NOT_DELIVERED,
}

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
DOWNLOAD_TYPES = "download_types"
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
FACEBOOK_AD_ACCOUNT_ID = "facebook-ad-account-id"
FACEBOOK_APP_ID = "facebook-app-id"
FACEBOOK_APP_SECRET = "facebook-app-secret"
FACEBOOK_ACCESS_TOKEN = "facebook-access-token"

# SFMC connector defines
SFMC_CLIENT_ID = "sfmc-client-id"
SFMC_CLIENT_SECRET = "sfmc-client-secret"
SFMC_ACCOUNT_ID = "sfmc-account-id"
SFMC_AUTH_BASE_URI = "sfmc-auth-base-uri"
SFMC_REST_BASE_URI = "sfmc-rest-base-uri"
SFMC_SOAP_BASE_URI = "sfmc-soap-base-uri"
SFMC_PERFORMANCE_METRICS_DATA_EXTENSIONS = "perf_data_extensions"
SFMC_PERFORMANCE_METRICS_DATA_EXTENSION = "performance_metrics_data_extension"
SFMC_CAMPAIGN_ACTIVITY_DATA_EXTENSION = "campaign_activity_data_extension"
SFMC_DATA_EXTENSION_NAME = "Name"
SFMC_CUSTOMER_KEY = "CustomerKey"

# Sendgrid connector defines
SENDGRID_AUTH_TOKEN = "sendgrid-auth-token"

# Qualtrics connector defines
QUALTRICS_API_TOKEN = "qualtrics-api_token"
QUALTRICS_DATA_CENTER = "qualtrics-data-center"
QUALTRICS_OWNER_ID = "qualtrics-owner-id"
QUALTRICS_DIRECTORY_ID = "qualtrics-directory-id"

# google ads connector defines
GOOGLE_DEVELOPER_TOKEN = "google-developer-token"
GOOGLE_REFRESH_TOKEN = "google-refresh-token"
GOOGLE_CLIENT_CUSTOMER_ID = "google-client-customer-id"
GOOGLE_CLIENT_ID = "google-client-id"
GOOGLE_CLIENT_SECRET = "google-client-secret"

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
DESTINATION_SECRETS = {
    db_c.DELIVERY_PLATFORM_FACEBOOK: [
        FACEBOOK_AD_ACCOUNT_ID,
        FACEBOOK_APP_ID,
        FACEBOOK_ACCESS_TOKEN,
        FACEBOOK_APP_SECRET,
    ],
    db_c.DELIVERY_PLATFORM_SFMC: [
        SFMC_CLIENT_ID,
        SFMC_AUTH_BASE_URI,
        SFMC_ACCOUNT_ID,
        SFMC_SOAP_BASE_URI,
        SFMC_REST_BASE_URI,
        SFMC_CLIENT_SECRET,
    ],
    db_c.DELIVERY_PLATFORM_SENDGRID: [SENDGRID_AUTH_TOKEN],
    db_c.DELIVERY_PLATFORM_QUALTRICS: [
        QUALTRICS_DIRECTORY_ID,
        QUALTRICS_DATA_CENTER,
        QUALTRICS_OWNER_ID,
        QUALTRICS_API_TOKEN,
    ],
    db_c.DELIVERY_PLATFORM_GOOGLE: [
        GOOGLE_CLIENT_CUSTOMER_ID,
        GOOGLE_DEVELOPER_TOKEN,
        GOOGLE_CLIENT_SECRET,
        GOOGLE_REFRESH_TOKEN,
        GOOGLE_CLIENT_ID,
    ],
}

ONLY_ADDED = "only_added"
DELETE_DATASOURCES_SUCCESS = "Successfully deleted data source(s) - {}."

# error messages
ERROR_ALERTS = "error_alerts"
MODULES = "modules"
CANNOT_DELETE_DATASOURCES = "Error deleting data source(s) - {}."
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
DESTINATION_ALREADY_PRESENT = "Destination already present."
DESTINATION_AUTHENTICATION_INVALID = (
    "Failed to update the authentication details of the destination."
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
INVALID_COMPONENT_NAME = "Invalid component name."
DATA_EXTENSIONS = "data-extensions"
DATA_EXTENSION = "data_extension"
DATA_EXTENSION_ID = "data_extension_id"
DATA_EXTENSION_NOT_SUPPORTED = "Data extension not supported"
GENERIC_DESTINATION = "generic_destination"
DESTINATION_CATEGORIES = "destination_categories"
DESTINATION_AUDIENCES = "destination_audiences"
DELIVERY_PLATFORM_LINK = "delivery_platform_link"
DELIVERY_PLATFORM_NAME = "delivery_platform_name"
EMPTY_USER_APPLICATION_RESPONSE = "No applications found for user."

# Map db status values to api status values
DESTINATION_STATUS_MAPPING = {
    db_c.STATUS_SUCCEEDED: STATUS_ACTIVE,
    db_c.STATUS_PENDING: STATUS_PENDING,
    db_c.STATUS_FAILED: STATUS_ERROR,
    db_c.STATUS_REQUESTED: STATUS_REQUESTED,
}

# Engagement fields
ENGAGEMENT = "engagement"
ENGAGEMENT_ID = "engagement_id"
ENGAGEMENT_IDS = "engagement_ids"
ENGAGEMENT_ENDPOINT = "/engagements"
ENGAGEMENT_TAG = "engagements"
DELIVERY_TAG = "delivery"
DELIVER = "deliver"
DELIVERY_HISTORY = "delivery-history"
PENDING_JOBS = "pending-jobs"
ORCH_INTEGRATION_TEST_CPDR = "orch_integration_test_cpdr"
ORCH_INTEGRATION_TEST_FLDR = "orch_integration_test_fldr"
ORCH_INTEGRATION_TEST_DR = "orch_integration_test_dr"
ORCH_INTEGRATION_TEST_MCA = "orch_integration_test_mca"

TRIGGERS_TAG = "triggers"
CAMPAIGNS = "campaigns"
AD_SET_ID = "ad_set_id"
AD_SET_NAME = "ad_set_name"
DELIVERY_JOB_ID = "delivery_job_id"
AUDIENCE_PERFORMANCE = "audience-performance"
AUDIENCE_PERFORMANCE_LABEL = "audience_performance"
AUDIENCE_DELIVERY_SCHEDULE = "audience_delivery_schedule"
DISPLAY_ADS = "display-ads"
IS_AD_PLATFORM = "is_ad_platform"
MY_ENGAGEMENTS = "my_engagements"
ENGAGEMENTS_DEFAULT_BATCH_SIZE = 0

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
HXTRUSTID_LEVEL = AccessLevel(db_c.USER_ROLE_TRUSTID)

USER_ROLE_ALL = [ADMIN_LEVEL, EDITOR_LEVEL, VIEWER_LEVEL]
COMMON_USER_ROLE = [ADMIN_LEVEL, EDITOR_LEVEL, VIEWER_LEVEL, HXTRUSTID_LEVEL]
TRUST_ID_ROLE_ALL = [HXTRUSTID_LEVEL, ADMIN_LEVEL]

USER_DISPLAY_ROLES = {
    db_c.USER_ROLE_ADMIN: "Admin",
    db_c.USER_ROLE_EDITOR: "Edit",
    db_c.USER_ROLE_VIEWER: "View-Only",
    db_c.USER_ROLE_TRUSTID: "TrustId",
}

# Orchestration API fields
ORCHESTRATION_ENDPOINT = "/orchestration"
AUDIENCE_ENDPOINT = "/audiences"
AUDIENCES = "audiences"
ORCHESTRATION_TAG = "orchestration"
DECISIONING = "decisioning"
AUDIENCE = "audience"
AUDIENCE_UPLOAD = "audience_upload"
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
AUDIENCE_FILTER_RANGE = "range"
AUDIENCE_FILTER_DELTA_TYPE = "delta_type"
AUDIENCE_FILTER_NOT_RANGE = "not_range"
AUDIENCE_FILTER_CONTACT_PREFERENCE = "contact_preference"
AUDIENCE_FILTER_PREFERENCE_EMAIL = "preference_email"
AUDIENCE_FILTER_PREFERENCE_SMS = "preference_sms"
AUDIENCE_FILTER_PREFERENCE_PUSH = "preference_push"
AUDIENCE_FILTER_PREFERENCE_IN_APP = "preference_in_app"
AUDIENCE_FILTER_CONTACT_PREFERENCES_UNIFIED = [EMAIL, TEXT, PUSH, IN_APP]
AUDIENCE_FILTER_CONTACT_PREFERENCES_CDM = [
    AUDIENCE_FILTER_PREFERENCE_EMAIL,
    AUDIENCE_FILTER_PREFERENCE_SMS,
    AUDIENCE_FILTER_PREFERENCE_PUSH,
    AUDIENCE_FILTER_PREFERENCE_IN_APP,
]
AUDIENCE_FILTER_CONTACT_PREFERENCES_CDP_MAP = {
    EMAIL: AUDIENCE_FILTER_PREFERENCE_EMAIL,
    TEXT: AUDIENCE_FILTER_PREFERENCE_SMS,
    PUSH: AUDIENCE_FILTER_PREFERENCE_PUSH,
    IN_APP: AUDIENCE_FILTER_PREFERENCE_IN_APP,
}
AUDIENCE_LAST_DELIVERED = "last_delivered"
AUDIENCE_LAST_DELIVERY = "last_delivery"
AUDIENCE_ENGAGEMENTS = "engagements"
AUDIENCE_SIZE_PERCENTAGE = "audience_size_percentage"
AUDIENCE_STANDALONE_DELIVERIES = "standalone_deliveries"
LOOKALIKE_AUDIENCES = "lookalike_audiences"
LOOKALIKE_AUDIENCES_ENDPOINT = "/lookalike-audiences"
LOOKALIKEABLE = "lookalikeable"
IS_LOOKALIKE = "is_lookalike"
LOOKALIKE = "lookalike"
LOOKALIKE_SOURCE_EXISTS = "source_exists"
WORKED_BY = "worked_by"
ATTRIBUTE = "attribute"
TRUST_ID_ATTRIBUTES = "attributes"
AUDIENCES_DEFAULT_BATCH_SIZE = 0
TAGS = "tags"
INDUSTRY_TAG = "industry_tag"
CONTACT_PREFERENCE_ATTRIBUTE = "contact_preference_attribute"

PARAM_STORE_PREFIX = "unified"
SECRET_STORAGE_ERROR_MSG = (
    "An error occurred while attempting to"
    " store secrets in the cloud secret storage."
)

AUDIENCE_RULES_DAYS = "days"
AUDIENCE_RULES_WEEKS = "weeks"
AUDIENCE_RULES_MONTHS = "months"
AUDIENCE_RULES_YEARS = "years"
ALLOWED_AUDIENCE_TIMEDELTA_TYPES = [
    AUDIENCE_RULES_DAYS,
    AUDIENCE_RULES_WEEKS,
    AUDIENCE_RULES_MONTHS,
    AUDIENCE_RULES_YEARS,
]

# users
USER_TAG = "user"
USERS = "users"
USER_NAME = "user_name"
DISPLAY_NAME = "display_name"
IS_USER_NEW = "is_user_new"
SHOW_LATEST_RELEASE_NOTES = "show_latest_release_notes"
LINK_LATEST_RELEASE_NOTES = "link_latest_release_notes"
USER_PHONE_NUMBER = "phone_number"
USER_EMAIL_ADDRESS = "email_address"
USER_ACCESS_LEVEL = "access_level"
USER_PII_ACCESS = "pii_access"
USER_DEMO_MODE = "demo_mode"
USER_ENDPOINT = "/users"
FAVORITE = "favorite"
FAVORITES = "favorites"
PROFILE = "profile"
CONTACT_US = "contact-us"
RESET = "reset"
RBAC_MATRIX = "rbac_matrix"
INDUSTRY = "industry"
TARGET = "target"
RELEASE_VERSION_LATEST = "RELEASE_VERSION_LATEST"
RELEASE_NOTES_LATEST = "RELEASE_NOTES_LATEST"

# Models
MODELS_TAG = "model"
MODEL = "model"
MODELS = "models"
MODELS_ENDPOINT = "/models"
MODELS_VERSION_HISTORY = "version-history"
MODEL_NAME = "model_name"
MODEL_TYPE = "model_type"
MODEL_METADATA = "model_metadata"
BINARY = "binary"
FEATURE = "feature"
VERSION_NUMBER = "version_number"
FEATURE_DESCRIPTION = "feature_description"
PREDICTED = "predicted"
ACTUAL = "actual"
PROFILES = "profiles"
SIZE_PROFILE = "size_profile"
RATE_PREDICTED = "rate_predicted"
LIFT = "lift"
LIFT_PREDICTED = "lift_predicted"
LIFT_ACTUAL = "lift_actual"
RATE_ACTUAL = "rate_actual"
MODEL_ID = "model_id"
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
LATEST_VERSION = "latest_version"
VERSION = "version"
FULCRUM_DATE = "fulcrum_date"
LAST_TRAINED = "last_trained"
TRAINED_DATE = "trained_date"
LOOKBACK_WINDOW = "lookback_window"
PREDICTION_WINDOW = "prediction_window"
PAST_VERSION_COUNT = "past_version_count"
DATA_SOURCE = "data_source"
FEATURE_TYPE = "feature_type"
MEAN = "mean"
MIN = "min"
MAX = "max"
LCUV = "lcuv"
MCUV = "mcuv"
UNIQUE_VALUES = "unique_value"
RECORDS_NOT_NULL = "records_not_null"
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

# CDP DATA SOURCES
CDP_DATA_SOURCES_TAG = "data sources"
CDP_DATA_SOURCES_ENDPOINT = "/data-sources"
CDP_DATA_SOURCE_IDS = "data_source_ids"
CDP_DATA_SOURCE_TYPE = "datasource_type"
DATAFEED_NAME = "datafeed_name"
PROCESSED_START_DATE = "processed_start_dt"
PROCESSED_END_DATE = "processed_end_dt"
DATA_SOURCES = "data_sources"

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
NOTIFICATION_EMAIL_RECIPIENTS = "recipients"
NOTIFICATION_EMAIL_ALERT_CATEGORY = "alert_category"
NOTIFICATION_EMAIL_ALERT_TYPE = "alert_type"
NOTIFICATION_EMAIL_ALERT_DESCRIPTION = "alert_description"

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
IDR_INSIGHTS = "idr_insights"
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
VIEWED_CHECKOUT_EVENT = "viewed_checkout"
TRAIT = "trait"
SALE = "sale"
VIEW_CONTENT = "view_content"
PRODUCT_SEARCH = "product_search"
ABANDONED_CART = "abandoned_cart"
PRODUCT_SEARCHED = "product_searched"
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
    FIRST_NAME,
    LAST_NAME,
]

# Alerts Fields
DEFAULT_BATCH_SIZE = 5
DEFAULT_BATCH_NUMBER = 1

NOTIFICATION_TYPE = "notification_type"

# CDM API constants
CDM_CONNECTIONS_ENDPOINT = "connections"
CDM_IDENTITY_ENDPOINT = "identity"
DATASOURCES = "datasources"
DATA_MANAGEMENT = "data_management"
DATAFEEDS = "datafeeds"

# Connections Data feeds Constants
PROCESSED_AT = "processed_at"
RECORDS_PROCESSED = "records_processed"
RECORDS_RECEIVED = "records_received"
THIRTY_DAYS_AVG = "thirty_days_avg"
RECORDS_PROCESSED_PERCENTAGE = "records_processed_percentage"
VALUE = "value"
FLAG_INDICATOR = "flag_indicator"
DATA_FILES = "data_files"

DEFAULT_DATE_FORMAT = "%Y-%m-%d"

# Configurations
CONFIGURATIONS_TAG = "configurations"
CONFIGURATIONS_ENDPOINT = "/configurations"
SETTINGS = "settings"
NAVIGATION_CHILDREN = "children"
SAMPLE_NAVIGATION_SETTINGS = {
    db_c.CONFIGURATION_FIELD_SETTINGS: [
        {
            db_c.CONFIGURATION_FIELD_NAME: "Data Management",
            db_c.CONFIGURATION_FIELD_LABEL: "Data Management",
            db_c.CONFIGURATION_FIELD_ENABLED: True,
            db_c.CONFIGURATION_FIELD_CHILDREN: [
                {
                    db_c.CONFIGURATION_FIELD_NAME: "Data Sources",
                    db_c.CONFIGURATION_FIELD_LABEL: "Data Sources",
                    db_c.CONFIGURATION_FIELD_ENABLED: True,
                },
                {
                    db_c.CONFIGURATION_FIELD_NAME: "Identity Resolution",
                    db_c.CONFIGURATION_FIELD_LABEL: "Identity Resolution",
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
                    db_c.CONFIGURATION_FIELD_ENABLED: True,
                }
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
                    db_c.CONFIGURATION_FIELD_ENABLED: True,
                },
                {
                    db_c.CONFIGURATION_FIELD_NAME: "Email Deliverability",
                    db_c.CONFIGURATION_FIELD_LABEL: "Email Deliverability",
                    db_c.CONFIGURATION_FIELD_ENABLED: True,
                },
            ],
        },
    ]
}
SAMPLE_RBAC_MATRIX_SETTINGS = {
    db_c.CONFIGURATION_FIELD_SETTINGS: {
        db_c.COMPONENTS: {
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
            }
        }
    }
}

# Applications
APPLICATIONS_TAG = "applications"
APPLICATION_ID = "application_id"
APPLICATIONS_ENDPOINT = "/applications"

# Client Projects
CLIENT_PROJECTS_TAG = "client-projects"
CLIENT_PROJECT_ID = "client_project_id"
CLIENT_PROJECTS_ENDPOINT = "/client-projects"
CLIENT_ENDPOINT = "/client"

# Histogram data stub.
VALUES = "values"
VALUE_FROM = "value_from"
VALUE_TO = "value_to"
HISTOGRAM_GROUP_SIZE = 10

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
        "min": 0,
        "max": 120,
        "steps": 1,
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

REASON_FOR_REQUEST = "reason_for_request"
NEW_USER_REQUEST_PREFIX = "[NEW USER REQUEST]"
REQUEST_NEW_USER = "request_new_user"
REQUESTED_BY = "requested_by"
USER_PREFERENCES = "preferences"
ALERTS = "alerts"

RESOURCE_OWNER = "resource_owner"
ALLOWED_RESOURCES_FOR_ABAC = [AUDIENCE, ENGAGEMENT]

REQUESTED_USERS = "requested_users"
# Jira States.
STATE_IN_PROGRESS = "In Progress"
STATE_TO_DO = "To Do"
STATE_IN_REVIEW = "In Review"
STATE_DONE = "Done"

MODEL_PIPELINE_PERFORMANCE_STUB = {
    "training": {
        "frequency": "Weekly",
        "last_run": datetime.datetime.now() - datetime.timedelta(days=1),
        "most_recent_run_duration": "00:22:45",
        "total_runs": 15,
        "run_duration": [
            {
                "status": "Success",
                "timestamp": datetime.datetime.now()
                - datetime.timedelta(days=x),
                "duration": "12m 41s",
                "label": f"{x} run of last 10",
            }
            for x in range(0, 10)
        ],
    },
    "scoring": {
        "frequency": "Weekly",
        "last_run": datetime.datetime.now() - datetime.timedelta(days=1),
        "most_recent_run_duration": "00:22:45",
        "total_runs": 10,
        "run_duration": [
            {
                "status": "Success",
                "timestamp": datetime.datetime.now()
                - datetime.timedelta(days=x),
                "duration": "12m 41s",
                "label": f"{x} run of last 10",
            }
            for x in range(0, random.randrange(10))
        ],
    },
}

# Deliverability Constants
EMAIL_DELIVERABILITY_ENDPOINT = "email_deliverability"
MEASUREMENT_TAG = "measurement"
OPEN_RATE = "open_rate"
DELIVERED_COUNT = "delivered_count"
OVERALL_INBOX_RATE = "overall_inbox_rate"
SENDING_DOMAINS_OVERVIEW = "sending_domains_overview"
DELIVERED_OPEN_RATE_OVERVIEW = "delivered_open_rate_overview"
DOMAIN_NAME = "domain_name"
SENT = "sent"
BOUNCE_RATE = "bounce_rate"
CLICK_RATE = "click_rate"
DELIVERED_RATE = "delivered_rate"
UNSUBSCRIBE_RATE = "unsubscribe_rate"
COMPLAINTS_RATE = "complaints_rate"
DELIVERABILITY_METRICS = "deliverability_metrics"

CAMPAIGN_ID = "campaign_id"
UNSUBSCRIBES = "unsubscribes"
COMPLAINTS = "complaints"
SOFT_BOUNCES = "soft_bounces"
BOUNCES = "bounces"
HARD_BOUNCES = "hard_bounces"
OPENS = "opens"
CLICKS = "clicks"
FILL_EMPTY_DATES = "fill_empty_dates"
# TODO Remove once email deliverability data is available.

DOMAIN_1 = "domain_1"

ALLOWED_EMAIL_DOMAIN_NAMES = [DOMAIN_1]
SENDING_DOMAINS_OVERVIEW_STUB = [
    {
        DOMAIN_NAME: DOMAIN_1,
        SENT: 554,
        BOUNCE_RATE: 0.14,
        OPEN_RATE: 0.91,
        CLICK_RATE: 0.85,
    }
]

ALERT_SAMPLE_RESPONSE = {
    ALERTS: {
        DATA_MANAGEMENT: {
            DATA_SOURCES: {
                db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                db_c.NOTIFICATION_TYPE_SUCCESS: False,
                db_c.NOTIFICATION_TYPE_CRITICAL: False,
            },
        },
        DECISIONING: {
            MODELS: {
                db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                db_c.NOTIFICATION_TYPE_SUCCESS: False,
                db_c.NOTIFICATION_TYPE_CRITICAL: False,
            },
        },
        ORCHESTRATION_TAG: {
            DESTINATIONS: {
                db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                db_c.NOTIFICATION_TYPE_SUCCESS: False,
                db_c.NOTIFICATION_TYPE_CRITICAL: False,
            },
            AUDIENCE_ENGAGEMENTS: {
                db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                db_c.NOTIFICATION_TYPE_SUCCESS: False,
                db_c.NOTIFICATION_TYPE_CRITICAL: False,
            },
            AUDIENCES: {
                db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                db_c.NOTIFICATION_TYPE_SUCCESS: False,
                db_c.NOTIFICATION_TYPE_CRITICAL: False,
            },
            DELIVERY_TAG: {
                db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                db_c.NOTIFICATION_TYPE_SUCCESS: True,
                db_c.NOTIFICATION_TYPE_CRITICAL: False,
            },
        },
    }
}
USER_DEMO_CONFIG_SAMPLE = {
    USER_DEMO_MODE: True,
    INDUSTRY: "Healthcare",
    DESCRIPTION: "Health Care Industry",
    TARGET: "Patients",
    TRACK: "Prescriptions",
}

# Trust ID
TRUST_ID_ENDPOINT = "/trust_id"
TRUST_ID_TAG = "trust-id"
DEFAULT = "default"
DEFAULT_TRUST_SEGMENT = "All Customers"
MAX_SEGMENTS_ALLOWED = 5
COMPARISON = "comparison"

CAPABILITY = "capability"
RELIABILITY = "reliability"
HUMANITY = "humanity"
TRANSPARENCY = "transparency"

HX_TRUST_ID = "HX TrustID"
TRUST_ID_LIST_OF_FACTORS = [CAPABILITY, RELIABILITY, HUMANITY, TRANSPARENCY]
TRUST_ID_SEGMENT_TYPE = "segment_type"
TRUST_ID_SEGMENTS = "segments"
TRUST_ID_SEGMENT_NAME = "segment_name"
TRUST_ID_SEGMENT_FILTERS = "segment_filters"
IS_BOOLEAN = "is_boolean"
TRUST_ID_SCORE = "trust_id_score"
TRUST_ID_ATTRIBUTE_TYPE = "attribute_type"
TRUST_ID_ATTRIBUTE_NAME = "attribute_name"
TRUST_ID_ATTRIBUTE_SCORE = "attribute_score"
TRUST_ID_ATTRIBUTE_DESCRIPTION = "attribute_description"
TRUST_ID_ATTRIBUTE_SHORT_DESCRIPTION = "attribute_short_description"
OVERALL_CUSTOMER_RATING = "overall_customer_rating"
RATING = "rating"
AGREE = "agree"
NEUTRAL = "neutral"
DISAGREE = "disagree"
TRUST_ID_FACTORS = "factors"
TRUST_ID_FACTOR_NAME = "factor_name"
TRUST_ID_FACTOR_SCORE = "factor_score"
TRUST_ID_FACTOR_DESCRIPTION = "factor_description"
TRUST_ID_RATING_MAP = {
    "-1": DISAGREE,
    "0": NEUTRAL,
    "1": AGREE,
}
TRUST_ID_FACTOR_DESCRIPTION_MAP = {
    HX_TRUST_ID: "TrustID is scored on a scale between -100 to 100",
    HUMANITY: (
        "Humanity is demonstrating empathy and kindness towards "
        "customers, and treating everyone fairly. It is scored "
        "on a scale between -100 to 100"
    ),
    TRANSPARENCY: (
        "Transparency is openly sharing all information, motives, and "
        "choices in straightforward and plain language. It is scored "
        "on a scale between -100 to 100"
    ),
    RELIABILITY: (
        "Reliability is consistently and dependably delivering on "
        "promises. It is scored on a scale between -100 to 100"
    ),
    CAPABILITY: (
        "Capability is creating quality products, services, and/or "
        "experiences. It is scored on a scale between -100 to 100"
    ),
}

TRUST_ID_SEGMENT_TYPE_MAP = {
    OVERVIEW: "composite & factor scores",
    CAPABILITY: "capability attributes",
    HUMANITY: "humanity attributes",
    RELIABILITY: "reliability attributes",
    TRANSPARENCY: "transparency attributes",
}

PERFORMANCE_METRIC_EMAIL_STUB = {
    "sent": 2045,
    "hard_bounces": 197,
    "hard_bounces_rate": 0,
    "delivered": 1578,
    "delivered_rate": 0,
    "open": 0,
    "open_rate": 0,
    "clicks": 719,
    "conversions": 0,
    "click_through_rate": 0.23,
    "click_to_open_rate": 0,
    "unique_clicks": 704,
    "unique_opens": 937,
    "unsubscribe": 0,
    "unsubscribe_rate": 0,
}

PERFORMANCE_METRIC_DISPLAY_STUB = {
    "spend": 100,
    "reach": 300,
    "impressions": 239,
    "conversions": 188,
    "clicks": 55,
    "frequency": 10,
    "cost_per_thousand_impressions": 434,
    "click_through_rate": 0.23,
    "cost_per_action": 7.56,
    "cost_per_click": 9.67,
    "engagement_rate": 0.23,
}

PERFORMANCE_METRIC_EMAIL_STUB_NO_DELIVERY = {
    "sent": 0,
    "hard_bounces": 0,
    "hard_bounces_rate": 0,
    "delivered": 0,
    "delivered_rate": 0,
    "open": 0,
    "open_rate": 0,
    "clicks": 0,
    "conversions": 0,
    "click_through_rate": 0.23,
    "click_to_open_rate": 0,
    "unique_clicks": 0,
    "unique_opens": 0,
    "unsubscribe": 0,
    "unsubscribe_rate": 0,
}

PERFORMANCE_METRIC_DISPLAY_STUB_NO_DELIVERY = {
    "spend": 0,
    "reach": 0,
    "impressions": 0,
    "conversions": 0,
    "clicks": 0,
    "frequency": 0,
    "cost_per_thousand_impressions": 0,
    "click_through_rate": 0,
    "cost_per_action": 0,
    "cost_per_click": 0,
    "engagement_rate": 0,
}

APPLICATION_CATEGORIES = [
    "Modeling",
    "Reporting",
    "Data Processing",
    "Data Storage",
    "Monitoring",
    "Uncategorized",
]

HEALTHCARE = "healthcare"
RETAIL = "retail"
HOSPITALITY = "hospitality"
AUTOMOTIVE = "automotive"
FINANCIAL_SERVICES = "financial_services"
ALL_INDUSTRY_TYPES = [
    HEALTHCARE,
    RETAIL,
    HOSPITALITY,
    AUTOMOTIVE,
    FINANCIAL_SERVICES,
]

MODEL_NAME_TAGS_MAP = {
    "LTV": dict(industry=ALL_INDUSTRY_TYPES),
    "Propensity to Purchase": dict(
        industry=[HEALTHCARE, RETAIL, HOSPITALITY, AUTOMOTIVE]
    ),
    "Propensity to Unsubscribe": dict(industry=[RETAIL, HOSPITALITY]),
    "Propensity to Churn": dict(
        industry=[HEALTHCARE, RETAIL, HOSPITALITY, AUTOMOTIVE]
    ),
    "Propensity Type Cancelled": dict(industry=[RETAIL, HOSPITALITY]),
    "Propensity Type Transaction": dict(industry=[RETAIL, HOSPITALITY]),
    "Propensity to Click": dict(industry=ALL_INDUSTRY_TYPES),
    "Propensity to Open": dict(industry=ALL_INDUSTRY_TYPES),
    "Propensity to place web order": dict(industry=[RETAIL]),
    "Propensity to view blanket products": dict(industry=[RETAIL]),
    "Propensity to view jacket products": dict(industry=[RETAIL]),
    "Propensity to view men’s products": dict(industry=[RETAIL]),
    "Propensity to view shirt products": dict(industry=[RETAIL]),
    "Propensity to view women’s products": dict(industry=[RETAIL]),
    "Propensity to view wool products": dict(industry=[RETAIL]),
    "Product Portfolio Marketing": dict(
        industry=[RETAIL, HOSPITALITY, AUTOMOTIVE]
    ),
    "Product Recommendation System": dict(
        industry=[RETAIL, HOSPITALITY, AUTOMOTIVE, FINANCIAL_SERVICES]
    ),
    "Product Return": dict(industry=[RETAIL, AUTOMOTIVE]),
    "Promotion Attributable Analysis": dict(
        industry=[RETAIL, HOSPITALITY, AUTOMOTIVE]
    ),
    "Sales Forecasting model": dict(
        industry=[HEALTHCARE, RETAIL, HOSPITALITY, AUTOMOTIVE]
    ),
    "Fraud Payment Detection": dict(industry=[FINANCIAL_SERVICES]),
    "Loan Default Prediction": dict(industry=[FINANCIAL_SERVICES]),
    "Personalization": dict(industry=[FINANCIAL_SERVICES]),
    "Uplift Model": dict(industry=ALL_INDUSTRY_TYPES),
}
