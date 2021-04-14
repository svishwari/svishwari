"""This module contains connector defines."""

# General Defines
ID = "_id"
CONNECT_RETRY_INTERVAL = 1

# Mongo connector defines
MONGO_HOST = "host"
MONGO_PORT = "port"
MONGO_USERNAME = "username"
MONGO_PASSWORD = "password"

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

# AWS Batch definitions
AWS_BATCH_REGION = "us-east-1"
AWS_BATCH_NUM_CPUS = 1
AWS_BATCH_QUEUE = "adperf_batch_queue"

# error messages
CANNOT_DELETE_DESTINATIONS = "Error deleting delivery platform"

# Delivery Platform API fields
DESTINATION_ID = "destination_id"
DESTINATION_TYPE = "destination_type"
DESTINATION_NAME = "destination_name"
DESTINATION_STATUS = "destination_status"
AUTHENTICATION_DETAILS = "authentication_details"
