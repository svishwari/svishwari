"""This module contains database defines."""

# General Defines
ID = "_id"
CONNECT_RETRY_INTERVAL = 1
DUPLICATE_ERR_CODE = 11000
FAVORITE = "favorite"
ENABLED = "enabled"

# Data Management Defines
DATA_MANAGEMENT_DATABASE = "data_management"
CONSTANTS_COLLECTION = "constants"
DATA_SOURCES_COLLECTION = "data_sources"
INGESTION_JOBS_COLLECTION = "ingestion_jobs"
INGESTED_DATA_COLLECTION = "ingested_data"
INGESTED_DATA_STATS_COLLECTION = "ingested_data_stats"
AUDIENCES_COLLECTION = "audiences"
AUDIENCE_INSIGHTS_COLLECTION = "audience_insights"
DELIVERY_JOBS_COLLECTION = "delivery_jobs"
DELIVERY_PLATFORM_COLLECTION = "delivery_platforms"
LOOKALIKE_AUDIENCE_COLLECTION = "lookalike_audiences"
PERFORMANCE_METRICS_COLLECTION = "performance_metrics"

CONSTANT_NAME = "constant"
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

DATA_SOURCE_TYPE_FIRST_PARTY = 1
DATA_SOURCE_TYPE_THIRD_PARTY = 3

JOB_STATUS = "status"
STATUS_MESSAGE = "status_message"
RECENT_INGESTION_JOB_STATUS = "recent_ingestion_job_status"
CREATE_TIME = "create_time"
UPDATE_TIME = "update_time"
JOB_START_TIME = "start_time"
JOB_END_TIME = "end_time"
JOB_ID = "ingestion_job_id"

STATUS_PENDING = "Pending"
STATUS_IN_PROGRESS = "In progress"
STATUS_FAILED = "Failed"
STATUS_SUCCEEDED = "Succeeded"

INGESTED_DATA = "data"

# special types and transformations
S_TYPE_AGE = "age"  # internal only
S_TYPE_CITY = "city"
S_TYPE_COUNTRY_CODE = "country_code"
S_TYPE_CUSTOMER_ID = "customer_id"
S_TYPE_GENDER = "gender"
S_TYPE_DOB = "date_of_birth"
S_TYPE_DOB_DAY = "date_of_birth_day"
S_TYPE_DOB_MONTH = "date_of_birth_month"
S_TYPE_DOB_YEAR = "date_of_birth_year"
S_TYPE_EMAIL = "email_address"
S_TYPE_FACEBOOK_CITY = "facebook_city"  # internal only
S_TYPE_FACEBOOK_COUNTRY_CODE = "facebook_country_code"  # internal only
S_TYPE_FACEBOOK_GENDER = "facebook_gender"  # internal only
S_TYPE_FACEBOOK_PHONE_NUMBER = "facebook_phone_number"  # internal only
S_TYPE_FACEBOOK_POSTAL_CODE = "facebook_postal_code"  # internal only
S_TYPE_FACEBOOK_STATE_OR_PROVINCE = "facebook_state_or_province"  # internal only
S_TYPE_FIRST_NAME = "first_name"
S_TYPE_FIRST_NAME_INITIAL = "first_name_initial"
S_TYPE_GOOGLE_PHONE_NUMBER = "google_phone_number"  # internal only
S_TYPE_LAST_NAME = "last_name"
S_TYPE_MOBILE_DEVICE_ID = "mobile_device_id"
S_TYPE_PHONE_NUMBER = "phone_number"
S_TYPE_GOOGLE_PHONE_NUMBER = "google_phone_number"
S_TYPE_FACEBOOK_PHONE_NUMBER = "facebook_phone_number"
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
AUDIENCE_FILTER_FIELD = "field"
AUDIENCE_FILTER_TYPE = "type"
AUDIENCE_FILTER_VALUE = "value"
AUDIENCE_FILTER_MIN = "min"
AUDIENCE_FILTER_MAX = "max"
AUDIENCE_FILTER_INCLUDE = "inclusion"
AUDIENCE_FILTER_EXCLUDE = "exclusion"
AUDIENCE_FILTER_EXISTS = "exists"
DEFAULT_AUDIENCE = "default_audience"
DEFAULT_AUDIENCE_ID = "default_audience_id"
DEFAULT_AUDIENCE_STR = "Default Audience"
MAX_AUDIENCE_SIZE_FOR_HASHED_FILE_DOWNLOAD = (
    "max_audience_size_for_hashed_file_download"
)

# Audience types
CUSTOM_AUDIENCE = "custom_audience"
CUSTOM_AUDIENCE_STR = "Custom Audience"
WIN_BACK_AUDIENCE = "win_back_audience"
WIN_BACK_AUDIENCE_STR = "Win-back Audience"

AUDIENCE_TYPE = "audience_type"
AUDIENCE_TYPE_NAME = "name"
AUDIENCE_TYPE_DESC = "description"

DELIVERY_PLATFORM_ID = "delivery_platform_id"
DELIVERY_PLATFORM_AUD_SIZE = "delivery_platform_audience_size"
DELIVERY_PLATFORM_LOOKALIKE_AUDS = "delivery_platform_lookalike_audiences"
DELIVERY_PLATFORM_NAME = "name"
DELIVERY_PLATFORM_TYPE = "delivery_platform_type"
DELIVERY_PLATFORM_AUTH = "authentication_details"
DELIVERY_PLATFORM_STATUS = "connection_status"
DELIVERY_PLATFORM_FACEBOOK = "Facebook"
DELIVERY_PLATFORM_AMAZON = "Amazon"
DELIVERY_PLATFORM_GOOGLE = "Google"

LOOKALIKE_AUD_NAME = "name"
LOOKALIKE_AUD_SIZE_PERCENTAGE = "audience_size_percentage"
LOOKALIKE_AUD_COUNTRY = "country"
LOOKALIKE_SOURCE_AUD_ID = "source_audience_id"

DELIVERY_JOB_ID = "delivery_job_id"
DELIVERY_PLATFORM_CAMPAIGN_ID = "delivery_platform_campaign_id"
DELIVERY_PLATFORM_AD_SET_ID = "delivery_platform_ad_set_id"
METRICS_START_TIME = "start_time"
METRICS_END_TIME = "end_time"
PERFORMANCE_METRICS = "performance_metrics"

# Data source constants
FIELD_SPECIAL_TYPE = "special_type"
FIELD_CUSTOM_TYPE = "custom_type"
FIELD_HEADER = "header"
FIELD_FIELD_MAPPING = "field_mapping"
FIELD_FIELD_MAPPING_DEFAULT = "field_mapping_default"


DATA_ROUTER_BATCH_SIZE = "data_router_batch_size"
AUDIENCE_ROUTER_BATCH_SIZE = "audience_router_batch_size"
AWS_BATCH_MEM_LIMIT = "aws_batch_mem_limit"

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
