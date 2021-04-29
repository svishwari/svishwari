"""
purpose of this file is for housing the config settings for the API
ensure that all config values are pulled in a single spot.
"""
from decouple import config


# AWS CONFIG
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_REGION = config("AWS_REGION")
AWS_SERVICE_URL = config("AWS_SERVICE_URL")
AWS_SSM_NAME = config("AWS_SSM_NAME", default="SSM")

# MONGO CONFIG
MONGO_DB_HOST = config("MONGO_DB_HOST", default="localhost")
MONGO_DB_PORT = config("MONGO_DB_PORT", default=27017, cast=int)
MONGO_DB_USERNAME = config("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = config("MONGO_DB_PASSWORD")
MONGO_DB_USE_SSL = config("MONGO_DB_USE_SSL", default=True, cast=bool)
MONGO_SSL_CERT = config("MONGO_SSL_CERT")

# SNOWFLAKE CONFIG
SNOWFLAKE_USERNAME = config("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = config("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = config("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = config("SNOWFLAKE_WAREHOUSE")

# TECTON
TECTON_API_KEY = config("TECTON_API_KEY")

# set Algorithmia vars
ALGORITHMIA_API_KEY = config("ALGORITHMIA_API_KEY")
ALGORITHMIA_API = config("ALGORITHMIA_API")
