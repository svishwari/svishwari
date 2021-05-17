"""This module contains connector defines."""
HEALTH_CHECK_ENDPOINT = "/health-check"
HEALTH_CHECK = "healthcheck"

# AWS defines
AWS_SSM_NAME = "ssm"
AWS_BATCH_NAME = "batch"
AWS_HEALTH_TESTS = {
    AWS_SSM_NAME: "describe_parameters",
    AWS_BATCH_NAME: "list_jobs",
}

# Facebook connector defines
FACEBOOK_NAME = "Facebook"
FACEBOOK_AD_ACCOUNT_ID = "facebook_ad_account_id"
FACEBOOK_APP_ID = "facebook_app_id"
FACEBOOK_APP_SECRET = "facebook_app_secret"
FACEBOOK_ACCESS_TOKEN = "facebook_access_token"

# SFMC connector defines
SFMC_NAME = "SFMC"
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
    FACEBOOK_NAME: {
        FACEBOOK_AD_ACCOUNT_ID: "Ad Account ID",
        FACEBOOK_APP_ID: "Facebook App ID",
        FACEBOOK_APP_SECRET: "App Secret",
        FACEBOOK_ACCESS_TOKEN: "Access Token",
    },
    SFMC_NAME: {
        SFMC_CLIENT_ID: "Client ID",
        SFMC_ACCOUNT_ID: "Account ID",
        SFMC_CLIENT_SECRET: "Client Secret",
        SFMC_AUTH_BASE_URI: "Auth Base URI",
        SFMC_REST_BASE_URI: "REST Base URI",
        SFMC_SOAP_BASE_URI: "SOAP Base URI",
        SFMC_PERFORMANCE_EXT_NAME: "Performance metric data extension name",
        SFMC_PERFORMANCE_EXT_VALUES: [],
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

# Destination API fields
DESTINATIONS_TAG = "destinations"
DESTINATIONS_DESCRIPTION = "Destinations API"
DESTINATIONS_ENDPOINT = "/destinations"
DESTINATION_ID = "destination_id"
DESTINATION_TYPE = "destination_type"
DESTINATION_NAME = "destination_name"
DESTINATION_STATUS = "destination_status"
DESTINATION_CAMPAIGN_COUNT = "destination_campaign_count"
AUTHENTICATION_DETAILS = "authentication_details"
DESTINATION_AUTHENTICATION_SUCCESS = "Destination authentication successful."
DESTINATION_AUTHENTICATION_FAILED = "Destination authentication failed."
DESTINATION_NOT_SUPPORTED = "Destination is not supported yet."

# CDP Data Source Constants
CDP_DATA_SOURCE_NAME = "name"
CDP_DATA_SOURCE_CATEGORY = "category"
CDP_DATA_SOURCE_DESCRIPTION = "CDP data source body"

CDP_DATA_SOURCE_NAME_DESCRIPTION = "Name of the CDP data source"
CDP_DATA_SOURCE_CATEGORY_DESCRIPTION = "Category of the CDP data source"

# Authentication API fields
AUTHENTICATION_TAG = "authenticate"
AUTHENTICATION_DESCRIPTION = "Authentication API"
AUTHENTICATION_ENDPOINT = "/authenticate"
AUTHENTICATION_TOKEN = "access_token"
CANNOT_AUTHENTICATE_USER = "Error authenticating user."

AUTHENTICATION_DETAILS = "authentication_details"
AUTHENTICATION_TOKEN = "token"
AUTHENTICATION_ACCESS_TOKEN = "access_token"
AUTHENTICATION_TOKEN_TYPE_HINT = "token_type_hint"
AUTHENTICATION_OKTA_CLIENT_ID = "OKTA-CLIENT-ID"
AUTHENTICATION_OKTA_ISSUER = "OKTA-ISSUER"

# Orchestration API fields
ORCHESTRATION_ENDPOINT = "/orchestration"
AUDIENCE_ENDPOINT = "/audiences"
ORCHESTRATION_TAG = "orchestration"
AUDIENCE_ID = "audience_id"
AUDIENCE_NAME = "audience_name"
AUDIENCE_FILTERS = "audience_filters"
AUDIENCE_SECTION_AGGREGATOR = "section_aggregator"
AUDIENCE_SECTION_FILTERS = "section_filters"
AUDIENCE_FILTER_FIELD = "filter_field"
AUDIENCE_FILTER_TYPE = "filter_type"
AUDIENCE_FILTER_VALUE = "filter_value"
AUDIENCE_DESTINATIONS = "audience_destinations"
AUDIENCE_ENGAGEMENTS = "audience_engagements"
AUDIENCE_SIZE = "audience_size"
AUDIENCE_STATUS = "audience_status"
AUDIENCE_STATUS_PENDING = "Pending"
AUDIENCE_STATUS_DELIVERED = "Delivered"
AUDIENCE_STATUS_DELIVERING = "Delivering"
AUDIENCE_STATUS_DRAFT = "Draft"
AUDIENCE_STATUS_ERROR = "Error"
AUDIENCE_STATUS_PAUSED = "Paused"
ENGAGEMENT_ID = "engagement_id"
ENGAGEMENT_NAME = "engagement_name"

PARAM_STORE_PREFIX = "huxunify"
PARAMETER_STORE_ERROR_MSG = (
    "An error occurred while attempting to"
    " store secrets in the parameter store."
)

# users
USER_TAG = "user"
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
        "join_key_map": {"model_id": "1"},
    }
}

# CDP DATA SOURCES
CDP_DATA_SOURCES_TAG = "data sources"
CDP_DATA_SOURCES_DESCRIPTION = "CDP DATA SOURCES API"
CDP_DATA_SOURCES_ENDPOINT = "/data-sources"
