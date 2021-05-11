"""
purpose of this file is for housing the config settings for the API
Ensure that all config values are pulled in a single spot.

Decouple always searches for Options in this order:
1. Environment variables
2. Repository: ini or .env file
3. Default argument passed to config.
"""
from pathlib import Path
from decouple import config


# AWS CONFIG
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_REGION = config("AWS_REGION", default="")
AWS_SERVICE_URL = config("AWS_SERVICE_URL", default="")

# MONGO CONFIG
MONGO_DB_HOST = config("MONGO_DB_HOST", default="localhost")
MONGO_DB_PORT = config("MONGO_DB_PORT", default=27017, cast=int)
MONGO_DB_USERNAME = config("MONGO_DB_USERNAME", default="")
MONGO_DB_PASSWORD = config("MONGO_DB_PASSWORD", default="")
# grab the SSL cert path
MONGO_SSL_CERT = str(
    Path(__file__).parent.parent.joinpath("rds-combined-ca-bundle.pem")
)
MONGO_DB_CONFIG = {
    "host": MONGO_DB_HOST,
    "port": MONGO_DB_PORT,
    "username": MONGO_DB_USERNAME,
    "password": MONGO_DB_PASSWORD,
    "ssl_cert_path": MONGO_SSL_CERT,
}

# TECTON
TECTON_API_KEY = config("TECTON_API_KEY", default="")
TECTON_API = config(
    "TECTON_API", default="https://decisioning-client.tecton.ai/api/v1"
)
TECTON_API_HEADERS = {
    "Authorization": f"Tecton-key {TECTON_API_KEY}",
}
TECTON_FEATURE_SERVICE = f"{TECTON_API}/feature-service/query-features"
