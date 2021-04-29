"""
purpose of this file is for housing the config settings for the API
Ensure that all config values are pulled in a single spot.
"""
from decouple import config


# AWS CONFIG
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_REGION = config("AWS_REGION", default="")
AWS_SERVICE_URL = config("AWS_SERVICE_URL", default="")
AWS_SSM_NAME = config("AWS_SSM_NAME", default="SSM")

# MONGO CONFIG
MONGO_DB_HOST = config("MONGO_DB_HOST", default="localhost")
MONGO_DB_PORT = config("MONGO_DB_PORT", default=27017, cast=int)
MONGO_DB_USERNAME = config("MONGO_DB_USERNAME", default="")
MONGO_DB_PASSWORD = config("MONGO_DB_PASSWORD", default="")
MONGO_SSL_CERT = config("MONGO_SSL_CERT", default="")
MONGO_DB_CONFIG = {
    "host": MONGO_DB_HOST,
    "port": MONGO_DB_HOST,
    "username": MONGO_DB_USERNAME,
    "password": MONGO_DB_PASSWORD,
    "ssl_cert_path": MONGO_SSL_CERT,
}

# SNOWFLAKE CONFIG
SNOWFLAKE_USERNAME = config("SNOWFLAKE_USER", default="")
SNOWFLAKE_PASSWORD = config("SNOWFLAKE_PASSWORD", default="")
SNOWFLAKE_ACCOUNT = config("SNOWFLAKE_ACCOUNT", default="")
SNOWFLAKE_WAREHOUSE = config("SNOWFLAKE_WAREHOUSE", default="COMPUTE_WH")

# TECTON
TECTON_API_KEY = config("TECTON_API_KEY", default="")

# ALGORITHMIA
ALGORITHMIA_API_KEY = config("ALGORITHMIA_API_KEY", default="")
ALGORITHMIA_API = config("ALGORITHMIA_API", default="")
