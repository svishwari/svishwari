"""This module contains database defines."""

# General Defines
ID = "_id"
CONNECT_RETRY_INTERVAL = 1
DUPLICATE_ERR_CODE = 11000
FAVORITE = "favorite"
ENABLED = "enabled"
OKTA_ID = "okta_id"
ADDED = "added"
STATUS = "status"
ACTIVE = "Active"
PENDING = "Pending"
DELETED = "deleted"
NAME = "name"
TYPE = "type"
OBJECT_ID = "id"
CONFIGURATION = "configuration"
SIZE = "size"
DOCUMENTS = "documents"

# general fields
AGE = "age"
MIN = "min"
MAX = "max"

# Data Management Defines
DATA_MANAGEMENT_DATABASE = "data_management"
CONSTANTS_COLLECTION = "constants"
DATA_SOURCES_COLLECTION = "data_sources"
CDP_DATA_SOURCES_COLLECTION = "cdp_data_sources"
ENGAGEMENTS_COLLECTION = "engagements"
INGESTION_JOBS_COLLECTION = "ingestion_jobs"
INGESTED_DATA_COLLECTION = "ingested_data"
INGESTED_DATA_STATS_COLLECTION = "ingested_data_stats"
AUDIENCES_COLLECTION = "audiences"
AUDIENCE_CUSTOMERS_COLLECTION = "audience_customers"
AUDIENCE_INSIGHTS_COLLECTION = "audience_insights"
DELIVERY_JOBS_COLLECTION = "delivery_jobs"
DELIVERY_PLATFORM_COLLECTION = "delivery_platforms"
LOOKALIKE_AUDIENCE_COLLECTION = "lookalike_audiences"
PERFORMANCE_METRICS_COLLECTION = "performance_metrics"
CAMPAIGN_ACTIVITY_COLLECTION = "campaign_activity"
USER_COLLECTION = "users"
NOTIFICATIONS_COLLECTION = "notifications"
CONFIGURATIONS_COLLECTION = "configurations"
CACHE_COLLECTION = "cache"
AUDIENCE_AUDIT_COLLECTION = "audit_logs"
PENDING_WITHIN_TIMEOUT_COLLECTION = "pending_within_timeout"

CONSTANT_NAME = "constant"
CONSTANT_KEY = "key"
CONSTANT_VALUE = "value"

STATE_ALPHA_CODE_MAPPING = "state_alpha_code_mapping"

DATA_SOURCE_NAME = "name"
DATA_SOURCE_TYPE = "type"
DATA_SOURCE_FORMAT = "format"
DATA_SOURCE_FORMATS = "data_source_formats"
DATA_SOURCE_ID = "data_source_id"
DATA_SOURCE_LOCATIONS = "data_source_locations"
DATA_SOURCE_LOCATION_TYPE = "location_type"
DATA_SOURCE_LOCATION_DETAILS = "location_details"
DATA_SOURCE_FIELDS = "fields"
DATA_SOURCE_FIELD_MAP = "data_source_field_map"
DATA_SOURCE_FIELD_NAME = "name"
DATA_SOURCE_FIELD_TYPE = "type"
DATA_SOURCE_RECENT_JOB_ID = "recent_ingestion_job_id"
DATA_SOURCE_NON_BREAKDOWN_FIELDS = "non_breakdown_fields"

DATA_SOURCE_PLATFORM_ODATA = "odata"
DATA_SOURCE_PLATFORM_REST_API = "rest_api"
DATA_SOURCE_PLATFORM_APACHE_HIVE = "apache-hive"
DATA_SOURCE_PLATFORM_APACHE_SPARK = "apache_spark"
DATA_SOURCE_PLATFORM_MICROSOFT_DYNAMICS = "microsoft_dynamics"
DATA_SOURCE_PLATFORM_NETSUITE = "netsuite"
DATA_SOURCE_PLATFORM_ORACLE_CRM = "oracle_crm"
DATA_SOURCE_PLATFORM_SALESFORCE = "salesforce"
DATA_SOURCE_PLATFORM_SAP = "sap"
DATA_SOURCE_PLATFORM_SERVICE_NOW = "servicenow"
DATA_SOURCE_PLATFORM_ZENDESK = "zendesk_crm"
DATA_SOURCE_PLATFORM_DROPBOX = "dropbox"
DATA_SOURCE_PLATFORM_MICROSOFT_SHAREPOINT = "microsoft_sharepoint"
DATA_SOURCE_PLATFORM_SFTP = "sftp"
DATA_SOURCE_PLATFORM_WINDOWS_FILESHARE = "windows"
DATA_SOURCE_PLATFORM_AMAZON_AURORA = "amazon_aurora"
DATA_SOURCE_PLATFORM_BIG_QUERY = "google_bigquery"
DATA_SOURCE_PLATFORM_IBMDB2 = "IBMDB2"
DATA_SOURCE_PLATFORM_MARIADB = "mariaDB"
DATA_SOURCE_PLATFORM_AZURESQL = "microsoftAzureSQL"
DATA_SOURCE_PLATFORM_MONGODB = "mongo_db"
DATA_SOURCE_PLATFORM_MYSQL = "mysql"
DATA_SOURCE_PLATFORM_ORACLE_DB = "oracle_db"
DATA_SOURCE_PLATFORM_TABLEAU = "tableau"
DATA_SOURCE_PLATFORM_BLUECORE = "bluecore"
DATA_SOURCE_PLATFORM_SHOPIFY = "shopify"
DATA_SOURCE_PLATFORM_GOOGLE_ANALYTICS = "google-analytics"
DATA_SOURCE_PLATFORM_HTTP = "http"
DATA_SOURCE_PLATFORM_BING = "ms_bing"
DATA_SOURCE_PLATFORM_AMPLITUDE = "amplitude"
DATA_SOURCE_PLATFORM_AQFER = "aqfer"
DATA_SOURCE_PLATFORM_GOOGLEADS = "google-ads"
DATA_SOURCE_PLATFORM_HUBSPOT = "hubspot"
DATA_SOURCE_PLATFORM_MAILCHIMP = "mailchimp"
DATA_SOURCE_PLATFORM_MARKETO = "marketo"
DATA_SOURCE_PLATFORM_MICROSOFT_ADS = "microsoft_ads"
DATA_SOURCE_PLATFORM_SFMC = "sfmc"
DATA_SOURCE_PLATFORM_AMAZONS3 = "amazon-s3"
DATA_SOURCE_PLATFORM_AZUREBLOB = "azure-blob"
DATA_SOURCE_PLATFORM_GOOGLE_CLOUD_STORAGE = "google_cloud"
DATA_SOURCE_PLATFORM_GOOGLE_SHEETS = "google_sheets"
DATA_SOURCE_PLATFORM_MICROSOFT_EXCEL = "microsoft_xls"
DATA_SOURCE_PLATFORM_PAYPAL = "paypal"
DATA_SOURCE_PLATFORM_QUICKBOOKS = "quickbooks"
DATA_SOURCE_PLATFORM_SQUARE = "square"
DATA_SOURCE_PLATFORM_STRIPE = "stripe"
DATA_SOURCE_PLATFORM_AOL = "aol"
DATA_SOURCE_PLATFORM_GMAIL = "gmail"
DATA_SOURCE_PLATFORM_INSIGHTIQ = "insightIQ"
DATA_SOURCE_PLATFORM_JIRA = "jira"
DATA_SOURCE_PLATFORM_MANDRILL = "mandrill"
DATA_SOURCE_PLATFORM_MEDALLIA = "medallia"
DATA_SOURCE_PLATFORM_OUTLOOK = "outlook"
DATA_SOURCE_PLATFORM_QUALTRICS = "qualtrics"
DATA_SOURCE_PLATFORM_SENDGRID = "sendgrid"
DATA_SOURCE_PLATFORM_SURVEY_MONKEY = "surveymonkey"
DATA_SOURCE_PLATFORM_TWILIO = "twilio"
DATA_SOURCE_PLATFORM_YAHOO = "yahoo"
DATA_SOURCE_PLATFORM_FACEBOOK = "facebook"
DATA_SOURCE_PLATFORM_INSTAGRAM = "instagram"
DATA_SOURCE_PLATFORM_LINKEDIN = "linkedIn"
DATA_SOURCE_PLATFORM_SNAPCHAT = "snapchat"
DATA_SOURCE_PLATFORM_TWITTER = "twitter"
DATA_SOURCE_PLATFORM_YOUTUBE = "youtube"

# Uncategorised Data Sources (Not in 6.0 designs)
DATA_SOURCE_PLATFORM_ADOBE = "adobe-experience"
DATA_SOURCE_PLATFORM_AMAZONADS = "amazon-advertising"
DATA_SOURCE_PLATFORM_GA360 = "GA360"

CATEGORY_API = "API"
CATEGORY_BIG_DATA = "Big data"
CATEGORY_CRM = "CRM"
CATEGORY_CUSTOMER_SERVICE = "Customer service"
CATEGORY_DATA_FILE_STORAGE = "Data & file storage"
CATEGORY_DATABASES = "Databases"
CATEGORY_DATA_VISUALIZATION = "Data visualization"
CATEGORY_ECOMMERCE = "E-commerce"
CATEGORY_MARKETING = "Marketing"
CATEGORY_OBJECT_STORAGE = "Object storage"
CATEGORY_FILES = "Files"
CATEGORY_FINANCE = "Finance"
CATEGORY_INTERNET = "Internet"
CATEGORY_PRODUCTIVITY = "Productivity"
CATEGORY_SOCIAL_MEDIA = "Social media"
CATEGORY_REPORTING = "Reporting"
CATEGORY_STORAGE = "Storage"
CATEGORY_UNKNOWN = "Unknown"

DATA_SOURCE_TYPE_FIRST_PARTY = 1
DATA_SOURCE_TYPE_THIRD_PARTY = 3

JOB_STATUS = "status"
STATUS_MESSAGE = "status_message"
RECENT_INGESTION_JOB_STATUS = "recent_ingestion_job_status"
EXPIRE_AT = "expireAt"
TS = "_ts"
CREATE_TIME = "create_time"
UPDATE_TIME = "update_time"
CREATED_BY = "created_by"
UPDATED_BY = "updated_by"
JOB_START_TIME = "start_time"
JOB_END_TIME = "end_time"
JOB_ID = "ingestion_job_id"

# category constants
CATEGORY = "category"
ADVERTISING = "Advertising"
MARKETING = "Marketing"
COMMERCE = "Commerce"
ANALYTICS = "Analytics"
SURVEY = "Survey"

STATUS_PENDING = "Pending"
STATUS_REQUESTED = "Requested"
STATUS_IN_PROGRESS = "In progress"
STATUS_FAILED = "Failed"
STATUS_SUCCEEDED = "Succeeded"
STATUS_PAUSED = "Paused"
STATUS_DELIVERED = "Delivered"
STATUS_TRANSFERRED_FOR_FEEDBACK = "transferred_for_feedback"
STATUS_TRANSFERRED_FOR_REPORT = "transferred_for_report"

INGESTED_DATA = "data"

# special types and transformations
S_TYPE_ADDRESS = "address"
S_TYPE_AGE = "age"  # internal only
S_TYPE_CITY = "city"
S_TYPE_COUNTRY_CODE = "country_code"
S_TYPE_CUSTOMER_ID = "hux_id"
S_TYPE_GENDER = "gender"
S_TYPE_DOB = "date_of_birth"
S_TYPE_DOB_DAY = "date_of_birth_day"
S_TYPE_DOB_MONTH = "date_of_birth_month"
S_TYPE_DOB_YEAR = "date_of_birth_year"
S_TYPE_EMAIL = "email_address"
S_TYPE_DOB_DAY_HASHED = "date_of_birth_day_hashed"  # internal only
S_TYPE_DOB_MONTH_HASHED = "date_of_birth_month_hashed"  # internal only
S_TYPE_DOB_YEAR_HASHED = "date_of_birth_year_hashed"  # internal only
S_TYPE_EMAIL_HASHED = "email_address_hashed"  # internal only
S_TYPE_CITY_HASHED = "city_hashed"  # internal only
S_TYPE_COUNTRY_CODE_HASHED = "country_code_hashed"  # internal only
S_TYPE_GENDER_HASHED = "gender_hashed"  # internal only
S_TYPE_PHONE_NUMBER_HASHED = "phone_number_digits_only_hashed"  # internal only
S_TYPE_POSTAL_CODE_HASHED = "postal_code_hashed"  # internal only
S_TYPE_STATE_OR_PROVINCE_HASHED = "state_or_province_hashed"  # internal only
S_TYPE_FIRST_NAME = "first_name"
S_TYPE_FIRST_NAME_HASHED = "first_name_hashed"  # internal only
S_TYPE_FIRST_NAME_INITIAL = "first_name_initial"
S_TYPE_FIRST_NAME_INITIAL_HASHED = "first_name_initial_hashed"  # internal only
S_TYPE_GOOGLE_PHONE_NUMBER = "google_phone_number"  # internal only
S_TYPE_LAST_NAME = "last_name"
S_TYPE_LAST_NAME_HASHED = "last_name_hashed"  # internal only
S_TYPE_MOBILE_DEVICE_ID = "mobile_device_id"
S_TYPE_PHONE_NUMBER = "phone_number"
S_TYPE_POSTAL_CODE = "postal_code"
S_TYPE_STATE_OR_PROVINCE = "state_or_province"

DESTINATION_COLUMN = "destination_column"
TRANSFORMER = "transformer"
TRANSFORMATIONS = "transformations"

STATS_COVERAGE = "coverage"
STATS_BREAKDOWN = "breakdown"

DATA_COUNT = "count"

AUDIENCE_ID = "audience_id"
AUDIENCE_NAME = "name"
AUDIENCE_FILTERS = "filters"
AUDIENCE_FILTERS_AGGREGATOR = "filters_aggregator"
AUDIENCE_FILTERS_SECTION_AGGREGATOR = "section_aggregator"
AUDIENCE_FILTERS_SECTION = "section_filters"
AUDIENCE_STATUS = "status"
AUDIENCE_FILTER_FIELD = "field"
AUDIENCE_FILTER_TYPE = "type"
AUDIENCE_FILTER_VALUE = "value"
AUDIENCE_FILTER_MIN = "min"
AUDIENCE_FILTER_MAX = "max"
AUDIENCE_FILTER_OPERATORS = "operators"
AUDIENCE_FILTER_INCLUDE = "inclusion"
AUDIENCE_FILTER_EXCLUDE = "exclusion"
AUDIENCE_FILTER_EXISTS = "exists"
DEFAULT_AUDIENCE = "default_audience"
DEFAULT_AUDIENCE_ID = "default_audience_id"
DEFAULT_AUDIENCE_STR = "Default Audience"
MAX_AUDIENCE_SIZE_FOR_HASHED_FILE_DOWNLOAD = (
    "max_audience_size_for_hashed_file_download"
)
AUDIENCE_FILTER_AGGREGATOR_ANY = "any"
AUDIENCE_FILTER_AGGREGATOR_ALL = "all"
AUDIENCE_CUSTOMER_LIST = "customer_list"
ATTRIBUTE = "attribute"
ATTRIBUTE_FILTER_FIELD = "filters.section_filters.field"
WORKED_BY = "worked_by"
# Audience types
CUSTOM_AUDIENCE = "custom_audience"
CUSTOM_AUDIENCE_STR = "Custom Audience"
WIN_BACK_AUDIENCE = "win_back_audience"
WIN_BACK_AUDIENCE_STR = "Win-back Audience"

AUDIENCE_TYPE = "audience_type"
AUDIENCE_TYPE_NAME = "name"
AUDIENCE_TYPE_DESC = "description"

AUDIENCE_LAST_DELIVERED = "last_delivered"
AUDIENCE_STATUS_DELIVERED = "Delivered"
AUDIENCE_STATUS_DELIVERING = "Delivering"
AUDIENCE_STATUS_NOT_DELIVERED = "Not Delivered"
AUDIENCE_STATUS_DRAFT = "Draft"
AUDIENCE_STATUS_ERROR = "Error"
AUDIENCE_STATUS_PAUSED = "Paused"

AUDIENCE_NAME_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

DELIVERIES = "deliveries"
DELIVERY_PLATFORM_ID = "delivery_platform_id"
DELIVERY_PLATFORM_CONTACT_LIST = "contact_list"
DELIVERY_PLATFORM_AUD_SIZE = "delivery_platform_audience_size"
DELIVERY_PLATFORM_LOOKALIKE_AUDS = "delivery_platform_lookalike_audiences"
DELIVERY_PLATFORM_NAME = "name"
DELIVERY_PLATFORM_TYPE = "delivery_platform_type"
DELIVERY_PLATFORM_AUTH = "authentication_details"
DELIVERY_PLATFORM_STATUS = "connection_status"
DELIVERY_PLATFORM_CONFIG = "delivery_platform_config"
DELIVERY_PLATFORM_SFMC_DATA_EXT_NAME = "data_extension_name"
DELIVERY_PLATFORM_SFMC_DATA_EXT_ID = "data_extension_id"
DELIVERY_PLATFORM_FACEBOOK = "facebook"
DELIVERY_PLATFORM_AMAZON = "amazon-advertising"
DELIVERY_PLATFORM_GOOGLE = "google-ads"
DELIVERY_PLATFORM_SFMC = "sfmc"
DELIVERY_PLATFORM_SENDGRID = "sendgrid"
DELIVERY_PLATFORM_TWILIO = "twilio"
DELIVERY_PLATFORM_QUALTRICS = "qualtrics"
DELIVERY_PLATFORM_ADOBE = "adobe-experience"
DELIVERY_PLATFORM_SAP = "sap"
DELIVERY_PLATFORM_LITMUS = "litmus"
DELIVERY_PLATFORM_FULLSTORY = "fullstory"
DELIVERY_PLATFORM_QUANTUMMETRIC = "quantummetric"
DELIVERY_PLATFORM_MEDALLIA = "medallia"
DELIVERY_PLATFORM_MAILCHIMP = "mailchimp"
DELIVERY_PLATFORM_LIVERAMP = "liveramp"
DELIVERY_PLATFORM_PINTEREST = "pinterest"
DELIVERY_PLATFORM_THE_TRADEDESK = "the_trade_desk"
DELIVERY_PLATFORM_TWITTER = DATA_SOURCE_PLATFORM_TWITTER
DELIVERY_PLATFORM_GOOGLE_DV360 = "google_dv360"
DELIVERY_PLATFORM_SFCC = "salesforce_commerce_cloud"
DELIVERY_PLATFORM_ADOBE_CAMPAIGN = "adobe_campaign"
DELIVERY_PLATFORM_SALESFORCE_CDP = "salesforce_cdp"
DELIVERY_PLATFORM_SALESFORCE_DATORAMA = "salesforce_datorama"
DELIVERY_PLATFORM_TABLEAU = DATA_SOURCE_PLATFORM_TABLEAU
DELIVERY_PLATFORM_AMAZONS3 = DATA_SOURCE_PLATFORM_AMAZONS3
DELIVERY_PLATFORM_AZUREBLOB = DATA_SOURCE_PLATFORM_AZUREBLOB
DELIVERY_PLATFORM_GOOGLE_CLOUD_STORAGE = (
    DATA_SOURCE_PLATFORM_GOOGLE_CLOUD_STORAGE
)
DELIVERY_PLATFORM_SFTP = DATA_SOURCE_PLATFORM_SFTP
SUPPORTED_DELIVERY_PLATFORMS = [
    DELIVERY_PLATFORM_FACEBOOK,
    DELIVERY_PLATFORM_SFMC,
    DELIVERY_PLATFORM_GOOGLE,
    DELIVERY_PLATFORM_AMAZON,
    DELIVERY_PLATFORM_SENDGRID,
    DELIVERY_PLATFORM_QUALTRICS,
]
IS_AD_PLATFORM = "is_ad_platform"
CONTACT_EMAIL = "contact_email"
CLIENT_REQUEST = "client_request"
CLIENT_ACCOUNT = "client_account"
USE_CASE = "use_case"

LOOKALIKE = "lookalike"
LOOKALIKE_AUD_NAME = "name"
LOOKALIKE_AUD_SIZE_PERCENTAGE = "audience_size_percentage"
LOOKALIKE_AUD_COUNTRY = "country"
LOOKALIKE_SOURCE_AUD_ID = "source_audience_id"
LOOKALIKE_SOURCE_AUD_NAME = "source_audience_name"
LOOKALIKE_SOURCE_AUD_SIZE = "source_audience_size"
LOOKALIKE_SOURCE_AUD_FILTERS = "source_audience_filters"

USER_ROLE = "role"
USER_ID = "user_id"
USER_ORGANIZATION = "organization"
USER_SUBSCRIPTION = "subscription"
USER_FAVORITES = "favorites"
USER_DISPLAY_NAME = "display_name"
USER_LAST_LOGIN = "last_login"
USER_PROFILE_PHOTO = "profile_photo"
USER_LOGIN_COUNT = "login_count"
USER_DASHBOARD_CONFIGURATION = "dashboard_configuration"
USER_ROLE_ADMIN = "admin"
USER_ROLE_EDITOR = "editor"
USER_ROLE_VIEWER = "viewer"
USER_ROLES = [USER_ROLE_ADMIN, USER_ROLE_EDITOR, USER_ROLE_VIEWER]
COMPONENT_ID = "component_id"
COMPONENT_NAME = "component_name"
USER_PII_ACCESS = "pii_access"

CAMPAIGNS = "campaigns"
DESTINATIONS = "destinations"
AUDIENCES = "audiences"
ENGAGEMENTS = "engagements"
FAVORITE_COMPONENTS = [AUDIENCES, ENGAGEMENTS, LOOKALIKE]

DELIVERY_JOB_ID = "delivery_job_id"
DELIVERY_PLATFORM_GENERIC_CAMPAIGN_ID = "delivery_platform_generic_campaign_id"
DELIVERY_PLATFORM_GENERIC_CAMPAIGNS = "delivery_platform_generic_campaigns"
METRICS_DELIVERY_PLATFORM_ID = "delivery_platform_id"
METRICS_DELIVERY_PLATFORM_NAME = "delivery_platform_name"
METRICS_DELIVERY_PLATFORM_TYPE = "delivery_platform_type"
METRICS_START_TIME = "start_time"
METRICS_END_TIME = "end_time"
PERFORMANCE_METRICS = "performance_metrics"
EVENT_DETAILS = "event_details"
EVENT_DATE = "event_date"
PERFORMANCE_METRICS_DATA_EXTENSION = "performance_metrics_data_extension"
CAMPAIGN_ACTIVITY_DATA_EXTENSION = "campaign_activity_data_extension"
DATA_EXTENSION_NAME = "data_extension_name"
DATA_EXTENSION_ID = "data_extension_id"
LATEST_DELIVERY = "latest_delivery"

# Data source constants
FIELD_SPECIAL_TYPE = "special_type"
FIELD_CUSTOM_TYPE = "custom_type"
FIELD_HEADER = "header"
FIELD_FIELD_MAPPING = "field_mapping"
FIELD_FIELD_MAPPING_DEFAULT = "field_mapping_default"

# CDP Data Source constants
CDP_DATA_SOURCE_ID = "data_source_id"
CDP_DATA_SOURCE_FIELD_NAME = "name"
CDP_DATA_SOURCE_FIELD_CATEGORY = "category"
CDP_DATA_SOURCE_FIELD_FEED_COUNT = "feed_count"
CDP_DATA_SOURCE_FIELD_STATUS = "status"

CDP_DATA_SOURCE_STATUS_ACTIVE = "Active"
CDP_DATA_SOURCE_STATUS_PENDING = "Pending"

DATA_ROUTER_BATCH_SIZE = "data_router_batch_size"
AUDIENCE_ROUTER_BATCH_SIZE = "audience_router_batch_size"
AWS_BATCH_MEM_LIMIT = "aws_batch_mem_limit"

# Notifications constants
NOTIFICATION_TYPE_SUCCESS = "success"
NOTIFICATION_TYPE_INFORMATIONAL = "informational"
NOTIFICATION_TYPE_CRITICAL = "critical"
NOTIFICATION_TYPES = [
    NOTIFICATION_TYPE_SUCCESS,
    NOTIFICATION_TYPE_INFORMATIONAL,
    NOTIFICATION_TYPE_CRITICAL,
]
NOTIFICATION_FIELD_TYPE = "type"
NOTIFICATION_FIELD_DESCRIPTION = "description"
NOTIFICATION_FIELD_CREATED = "created"
NOTIFICATION_FIELD_CATEGORY = "category"
NOTIFICATION_FIELD_USERNAME = "username"

NOTIFICATION_QUERY_PARAMETER_BATCH_SIZE = "batch_size"
NOTIFICATION_QUERY_PARAMETER_SORT_ORDER = "sort_order"
NOTIFICATION_QUERY_PARAMETER_BATCH_NUMBER = "batch_number"

# Configuration constants

CONFIGURATION_FIELD_NAME = "name"
CONFIGURATION_FIELD_ICON = "icon"
CONFIGURATION_FIELD_TYPE = "type"
CONFIGURATION_FIELD_DESCRIPTION = "description"
CONFIGURATION_FIELD_STATUS = "status"
CONFIGURATION_FIELD_ENABLED = "enabled"
CONFIGURATION_FIELD_ROADMAP = "roadmap"
CONFIGURATION_TYPE_MODULE = "module"
CONFIGURATION_TYPE_BUSINESS_SOLUTION = "business_solution"

# Audience constants
AUDIENCE_FILTER_CONSTANTS = "audience_filter_constants"
AGE_FILTER = "age_filter"
FIRST_NAME_FILTER = "first_name_filter"

# Engagement constants
ENGAGEMENT_ID = "engagement_id"
ENGAGEMENT = "engagement"
ENGAGEMENT_NAME = "name"
ENGAGEMENT_DESCRIPTION = "description"
ENGAGEMENT_DELIVERY_SCHEDULE = "delivery_schedule"

# pagination constants
PAGINATION_ASCENDING = "ascending"
PAGINATION_DESCENDING = "descending"

# Custom type definitions
CUSTOM_TYPE_BOOL = "boolean"
CUSTOM_TYPE_CAT = "categorical"
CUSTOM_TYPE_INT = "integer"
CUSTOM_TYPE_FLOAT = "float"

CUSTOM_TYPE_BOOL_MAPPING = "custom_type_boolean_mapping"
CUSTOM_TYPE_FRIENDLY_NAME_MAPPING = "custom_type_friendly_name_mapping"

CUSTOM_TYPE_FIELD_MAPPING = "custom_field_mapping"

FIELD_MAP_ORDER_QUANTITY_12M = "order_quantity_12m"
FIELD_MAP_ORDER_QUANTITY_13M_24M = "order_quantity_13m_24m"

EMAIL_REGEX = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

# Audit Logs Defination
DOWNLOAD_TIME = "download_time"
FILE_NAME = "file_name"
USER_NAME = "user_name"
DOWNLOAD_TYPE = "download_type"


# Required Fields per collection

REQUIRED_FIELDS = {
    CONFIGURATIONS_COLLECTION: [
        CONFIGURATION_FIELD_NAME,
        CONFIGURATION_FIELD_TYPE,
    ],
}
# Allowed Fields per collection
ALLOWED_FIELDS = {
    CONFIGURATIONS_COLLECTION: [
        OBJECT_ID,
        CONFIGURATION_FIELD_NAME,
        CONFIGURATION_FIELD_ICON,
        CONFIGURATION_FIELD_TYPE,
        CONFIGURATION_FIELD_DESCRIPTION,
        CONFIGURATION_FIELD_STATUS,
        CONFIGURATION_FIELD_ENABLED,
        CONFIGURATION_FIELD_ROADMAP,
    ],
}

# Allowed collections
ALLOWED_COLLECTIONS = [
    CONFIGURATIONS_COLLECTION,
    DELIVERY_PLATFORM_COLLECTION,
    LOOKALIKE_AUDIENCE_COLLECTION,
]

# 30 minutes.
DELIVERY_JOB_TIMEOUT = 30
