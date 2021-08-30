# pylint: disable=too-many-lines
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
DEFAULT_AUDIENCE_DELIVERY_COUNT = 2
OVERVIEW = "overview"
DATE_RANGE = "date_range"
HUX_ID = "hux_id"
TOP_FEATURES = "top_features"
LIMIT = "limit"
OFFSET = "offset"

QUERY_PARAMETER_BATCH_SIZE = "batch_size"
QUERY_PARAMETER_BATCH_NUMBER = "batch_number"
QUERY_PARAMETER_SORT_ORDER = "sort_order"

HEALTH_CHECK_ENDPOINT = "/health-check"
HEALTH_CHECK = "healthcheck"

TOTAL_RECORDS = "total_records"
MATCH_RATE = "match_rate"
TOTAL = "total"
TOTAL_UNIQUE_IDS = "total_unique_ids"
TOTAL_UNKNOWN_IDS = "total_unknown_ids"
TOTAL_KNOWN_IDS = "total_known_ids"
TOTAL_INDIVIDUAL_IDS = "total_individual_ids"
TOTAL_HOUSEHOLD_IDS = "total_household_ids"
UPDATED = "updated"
TOTAL_CUSTOMERS = "total_customers"
NEW_CUSTOMERS_ADDED = "new_customers_added"
COUNTRIES = "total_countries"
TOTAL_COUNT = "total_count"
TOTAL_STATES = "total_us_states"
TOTAL_CITIES = "total_cities"
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
COUNTRY = "country"
POPULATION_PERCENTAGE = "population_percentage"
INCOME = "income"
CDP_SERVICE_URL = "CDP_SERVICE_URL"
COUNT = "count"
AVG_SPENT_WOMEN = "avg_spent_women"
AVG_SPENT_MEN = "avg_spent_men"
AVG_SPENT_OTHER = "avg_spent_other"
YEAR = "year"
MONTH = "month"
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
DEMOGRAPHIC = "demo"
DATE = "date"
RECORDED = "recorded"
DIFFERENCE_COUNT = "diff_count"

# AWS defines
AWS_MODULE_NAME = "huxunify.api.data_connectors.aws"
AWS_SSM_NAME = "ssm"
AWS_EVENTS_NAME = "events"
AWS_BATCH_NAME = "batch"
AWS_HEALTH_TESTS = {
    AWS_SSM_NAME: ["get_parameter", {"Name": "unifieddb_host_alias"}],
    AWS_BATCH_NAME: ["cancel_job", {"jobId": "test", "reason": "test"}],
}

REQUIRED = "required"
DELIVERY_SCHEDULE = "delivery_schedule"
START_DATE = "start_date"
END_DATE = "end_date"
ENABLED = "enabled"
DISABLED = "disabled"
SIZE = "size"
IS_ADDED = "is_added"
UNKNOWN = "unknown"

STATUS_NOT_DELIVERED = "Not Delivered"
STATUS_DELIVERED = "Delivered"
STATUS_DELIVERING = "Delivering"
STATUS_DELIVERY_PAUSED = "Delivery Paused"
STATUS_ACTIVE = "Active"
STATUS_INACTIVE = "Inactive"
STATUS_DISABLED = "Disabled"
STATUS_DRAFT = "Draft"
STATUS_PENDING = "Pending"
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
SFMC_PERFORMANCE_METRICS_DATA_EXTENSIONS = "perf_data_extensions"
SFMC_PERFORMANCE_METRICS_DATA_EXTENSION = "perf_data_extension"
SFMC_DATA_EXTENSION_NAME = "Name"
SFMC_CUSTOMER_KEY = "CustomerKey"

# Twilio connector defines
TWILIO_AUTH_TOKEN = "twilio_auth_token"

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
    db_c.DELIVERY_PLATFORM_TWILIO: {
        TWILIO_AUTH_TOKEN: {
            NAME: "Auth Token",
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
    db_c.DELIVERY_PLATFORM_TWILIO: {
        MONGO: [],
        AWS_SSM_NAME: [TWILIO_AUTH_TOKEN],
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
BSON_INVALID_ID = (
    lambda invalid_id: f"'{invalid_id}' is not a valid ObjectId, it must be a "
    f"12-byte input or a 24-character hex string"
)

EMPTY_OBJECT_ERROR_MESSAGE = "Data not provided."
INVALID_DELIVERY_SCHEDULE = "Delivery schedule is not valid."
DUPLICATE_NAME = "Name already exists."
PERFORMANCE_METRIC_DE_NOT_ASSIGNED = (
    "Performance metrics data extension not assigned."
)
INVALID_AUTH_DETAILS = "Invalid authentication details."
INVALID_AUTH_HEADER = "Authorization header is invalid."
INVALID_AUTH = "You are not authorized to visit this page."
INVALID_BATCH_PARAMS = "Invalid Batch Number or Batch Size"

AUDIENCE_NOT_FOUND = "Audience not found."
DESTINATION_NOT_FOUND = "Destination not found."
ENGAGEMENT_NOT_FOUND = "Engagement not found."
DESTINATION_NOT_SUPPORTED = "Destination is not supported."
SUCCESSFUL_DELIVERY_JOB_NOT_FOUND = "No successful delivery job found"
ZERO_AUDIENCE_SIZE = "Sum of Audience(s) is zero"

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
LATEST_DELIVERY = "latest_delivery"
CONNECTION_STATUS = "connection_status"
AUTHENTICATION_DETAILS = "authentication_details"
DESTINATION_AUTHENTICATION_SUCCESS = "Destination authentication successful."
DESTINATION_AUTHENTICATION_FAILED = "Destination authentication failed."
INVALID_STATUS = "Invalid status value."
INVALID_COMPONENT_NAME = "Invalid component name."
DATA_EXTENSIONS = "data-extensions"
DATA_EXTENSION = "data_extension"
DATA_EXTENSION_ID = "data_extension_id"
DATA_EXTENSION_FAILED = "Unable to retrieve destination data extension."

# Engagement fields
ENGAGEMENT = "engagement"
ENGAGEMENT_ID = "engagement_id"
ENGAGEMENT_IDS = "engagement_ids"
ENGAGEMENT_NAME = "engagement_name"
ENGAGEMENT_ENDPOINT = "/engagements"
ENGAGEMENT_TAG = "engagements"
DELIVERY_TAG = "delivery"
DELIVER = "deliver"
DELIVERY_HISTORY = "delivery-history"
CAMPAIGNS = "campaigns"
CAMPAIGN_ID = "campaign_id"
AD_SET_ID = "ad_set_id"
AD_SET_NAME = "ad_set_name"
DELIVERY_MOMENT = "delivery_moment"
DELIVERY_JOB_ID = "delivery_job_id"
AUDIENCE_PERFORMANCE = "audience-performance"
AUDIENCE_PERFORMANCE_LABEL = "audience_performance"
DISPLAY_ADS = "display-ads"

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
    "click",
    "click_to_open_rate",
    "unique_clicks",
    "unique_opens",
    "unsubscribe",
    "unsubscribe_rate",
]
SUMMARY = "summary"
IS_MAPPED = "is_mapped"
DELIVERED = "delivered"
UNSUBSCRIBE = "unsubscribe"
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
SOURCE_AUDIENCE_ID = "source_audience_id"
AUDIENCE_NAME = "name"
AUDIENCE_FILTERS = "filters"
AUDIENCE_SECTION_AGGREGATOR = "section_aggregator"
AUDIENCE_SECTION_FILTERS = "section_filters"
AUDIENCE_INSIGHTS = "audience_insights"
INSIGHTS = "insights"
AUDIENCE_FILTER_FIELD = "field"
AUDIENCE_FILTER_TYPE = "type"
AUDIENCE_FILTER_VALUE = "value"
AUDIENCE_LAST_DELIVERED = "last_delivered"
AUDIENCE_ENGAGEMENTS = "engagements"
AUDIENCE_SIZE = "audience_size"
AUDIENCE_SIZE_PERCENTAGE = "audience_size_percentage"
AUDIENCE_STATUS = "audience_status"
AUDIENCE_ROUTER_STUB_TEST = "AUDIENCE_ROUTER_STUB_TEST"
AUDIENCE_ROUTER_STUB_VALUE = "1"
AUDIENCE_ROUTER_CERT_PATH = "../rds-combined-ca-bundle.pem"
AUDIENCE_ROUTER_MONGO_PASSWORD_FROM = "unifieddb_rw"
LOOKALIKE_AUDIENCES = "lookalike_audiences"
LOOKALIKE_AUDIENCES_ENDPOINT = "/lookalike-audiences"
LOOKALIKEABLE = "lookalikeable"
IS_LOOKALIKE = "is_lookalike"

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
# TODO: Remove relevant constants from here once integrated with Tecton API
MODELS_TAG = "model"
MODELS_DESCRIPTION = "MODEL API"
MODELS_ENDPOINT = "/models"
MODELS_VERSION_HISTORY = "version-history"
MODEL_NAME = "model_name"
MODEL_TYPE = "model_type"
MODEL_ID = "model_id"
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
MODEL_TYPE_PARAMS = [
    {
        "name": MODEL_TYPE,
        "description": "Model type",
        "type": "string",
        "in": "path",
        "required": True,
        "example": "ltv",
    }
]
MODEL_ID_PARAMS = [
    {
        "name": MODEL_ID,
        "description": "Model id",
        "type": "integer",
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
FEATURE_IMPORTANCE = "feature_importance"
SCORE = "score"
FEATURE_LIFT_MODEL_SERVICE = "ui_metadata_model_lift_service"
FEATURE_DRIFT_REGRESSION_MODEL_SERVICE = (
    "ui_metadata_model_metrics_regression_service"
)
FEATURE_DRIFT_CLASSIFICATION_MODEL_SERVICE = (
    "ui_metadata_model_metrics_classification_service"
)

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
VERSION = "version"
FULCRUM_DATE = "fulcrum_date"
LAST_TRAINED = "last_trained"
LOOKBACK_WINDOW = "lookback_window"
PREDICTION_WINDOW = "prediction_window"
PAST_VERSION_COUNT = "past_version_count"
LIFT_DATA = "lift_data"
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

# used for the icons on front-end.
MODEL_TYPES_MAPPING = {
    "lifetime value": LTV,
    "propensity to purchase": PURCHASE,
    "propensity to unsubscribe": UNSUBSCRIBE,
}

# CDP DATA SOURCES
CDP_DATA_SOURCES_TAG = "data sources"
CDP_DATA_SOURCES_DESCRIPTION = "CDP DATA SOURCES API"
CDP_DATA_SOURCES_ENDPOINT = "/data-sources"
CDP_DATA_SOURCE_IDS = "data_source_ids"

# Customers
CUSTOMER_ID = "customer_id"
CUSTOMERS_ENDPOINT = "/customers"
CUSTOMERS_TAG = "customers"
CUSTOMERS_INSIGHTS = "customers-insights"
GEOGRAPHICAL = "geo"
CUSTOMERS_DESCRIPTION = "Customers API"
CUSTOMERS_API_HEADER_KEY = "x-api-key"
CUSTOMERS_DEFAULT_BATCH_SIZE = 1000
CUSTOMER_COUNT = "customer_count"

# Demographic
CITIES_DEFAULT_BATCH_SIZE = 100

# Notifications
NOTIFICATIONS_TAG = "notifications"
NOTIFICATIONS_DESCRIPTION = "Notifications API"
NOTIFICATIONS_ENDPOINT = "/notifications"

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

START_DATE_PARAMS = {
    "name": START_DATE,
    "description": "Start date.",
    "type": "string",
    "in": "query",
    "required": True,
    "example": "2021-04-01",
}

END_DATE_PARAMS = {
    "name": END_DATE,
    "description": "End date.",
    "type": "string",
    "in": "query",
    "required": True,
    "example": "2021-08-01",
}

# IDR Fields
IDR_TAG = "idr"
IDR_ENDPOINT = "/idr"
DATA_FEEDS = "datafeeds"
DATA_FEED = "datafeed"
INPUT_RECORDS = "input_records"
OUTPUT_RECORDS = "output_records"
EMPTY_RECORDS = "empty_records"
INDIVIDUAL_ID_MATCH = "individual_id_match"
HOUSEHOLD_ID_MATCH = "household_id_match"
COMPANY_ID_MATCH = "company_id_match"
ADDRESS_ID_MATCH = "address_id_match"
DB_READS = "db_reads"
DB_WRITES = "db_writes"
FILENAME = "filename"
NEW_INDIVIDUAL_IDS = "new_individual_ids"
NEW_HOUSEHOLD_IDS = "new_household_ids"
NEW_COMPANY_IDS = "new_company_ids"
NEW_ADDRESS_IDS = "new_address_ids"
PROCESS_TIME = "process_time"
DATE_TIME = "date_time"
DIGITAL_IDS_ADDED = "digital_ids_added"
DIGITAL_IDS_MERGED = "digital_ids_merged"
MERGE_RATE = "merge_rate"
RECORDS_SOURCE = "records_source"
TIME_STAMP = "time_stamp"
STITCHED = "stitched"
PINNING = "pinning"

# IDR Matching Trends
MATCHING_TRENDS = "matching-trends"

KNOWN_IDS = "known_ids"
UNIQUE_HUX_IDS = "unique_hux_ids"
ANONYMOUS_IDS = "anonymous_ids"

KNOWN_IDS_MIN_COUNT = 50000
KNOWN_IDS_MAX_COUNT = 79000
KNOWN_IDS_LAMBDA = 1.6

UNIQUE_HUX_IDS_MIN_COUNT = 100000
UNIQUE_HUX_IDS_MAX_COUNT = 156000
UNIQUE_HUX_IDS_LAMBDA = 1.5

ANONYMOUS_IDS_MIN_COUNT = 79000
ANONYMOUS_IDS_MAX_COUNT = 120000
ANONYMOUS_IDS_LAMBDA = 5

# IDR Data feeds
DATAFEED_ID = "datafeed_id"
DATAFEED_NAME = "datafeed_name"
DATAFEED_DATA_SOURCE = "data_source_type"
DATAFEED_NEW_IDS_COUNT = "new_ids_generated"
DATAFEED_RECORDS_PROCESSED_COUNT = "num_records_processed"
DATAFEED_LAST_RUN_DATE = "last_run"

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

# Alerts Fields
DEFAULT_BATCH_SIZE = 5
DEFAULT_ALERT_SORT_ORDER = "descending"
DEFAULT_BATCH_NUMBER = 1

NOTIFICATION_TYPE = "notification_type"

# Download Audience Fields
DOWNLOAD_TYPE = "download_type"
GOOGLE_ADS = "google_ads"
AMAZON_ADS = "amazon_ads"

DOWNLOAD_TYPES = {
    GOOGLE_ADS: {
        db_c.S_TYPE_EMAIL_HASHED: "Email",
        db_c.S_TYPE_FIRST_NAME_HASHED: "First Name",
        db_c.S_TYPE_FIRST_NAME_INITIAL_HASHED: "First Name Initial",
        db_c.S_TYPE_LAST_NAME_HASHED: "Last Name",
        db_c.S_TYPE_MOBILE_DEVICE_ID: "Mobile Device ID",
        db_c.S_TYPE_PHONE_NUMBER_HASHED: "Phone",
        db_c.S_TYPE_POSTAL_CODE_HASHED: "Zip",
    },
    AMAZON_ADS: {
        db_c.S_TYPE_CITY_HASHED: "city",
        db_c.S_TYPE_EMAIL_HASHED: "email",
        db_c.S_TYPE_FIRST_NAME_HASHED: "first_name",
        db_c.S_TYPE_LAST_NAME_HASHED: "last_name",
        db_c.S_TYPE_PHONE_NUMBER_HASHED: "phone",
        db_c.S_TYPE_POSTAL_CODE_HASHED: "zip",
        db_c.S_TYPE_STATE_OR_PROVINCE_HASHED: "state",
        # TODO Add address once CDP returns it
        # db_c.S_TYPE_ADDRESS: "address"
    },
}
