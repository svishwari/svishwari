"""This module contains connector defines."""

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
DESTINATIONS_ENDPOINT = "destinations"
DESTINATION_ID = "destination_id"
DESTINATION_TYPE = "destination_type"
DESTINATION_NAME = "destination_name"
DESTINATION_STATUS = "destination_status"
DESTINATION_CAMPAIGN_COUNT = "destination_campaign_count"
AUTHENTICATION_DETAILS = "authentication_details"

PARAM_STORE_PREFIX = "huxunify"
PARAMETER_STORE_ERROR_MSG = (
    "An error occurred while attempting to"
    " store secrets in the parameter store."
)

# Models
MODEL_NAME = "model_name"
MODEL_NAME_PARAMS = [
    {
        "name": MODEL_NAME,
        "description": "User ID.",
        "type": "string",
        "in": "path",
        "required": True,
        "example": "churn",
    },
]
