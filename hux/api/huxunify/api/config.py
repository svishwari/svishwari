"""
purpose of this file is for housing the config settings for the API
Ensure that all config values are pulled in a single spot.

Decouple always searches for Options in this order:
1. Environment variables
2. Repository: ini or .env file
3. Default argument passed to config.
"""
import logging
from importlib import import_module
from os import environ
from pathlib import Path
from decouple import config
from huxunify.api import constants as api_c


SECRET_STORE_INVOKE = "aws.parameter_store.get_store_value"


LOAD_VAR_DICT = {
    "TECTON_API_KEY": "TECTON_API_KEY",
    "MONGO_DB_HOST": "unifieddb_host_alias",
}


class Config:
    """
    Config Object
    """

    DEBUG = False

    # AWS_CONFIG
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
    AWS_REGION = config("AWS_REGION", default="us-east-2")
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

    OKTA_CLIENT_ID = config("OKTA_CLIENT_ID", default="")
    OKTA_ISSUER = config("OKTA_ISSUER", default="")

    MONITORING_CONFIG = config("OKTA_ISSUER", default="MONITORING-CONFIG")

    # TECTON
    TECTON_API_KEY = config("TECTON_API_KEY", default="")
    TECTON_API = config(
        "TECTON_API", default="https://decisioning-client.tecton.ai/api/v1"
    )
    TECTON_API_HEADERS = {
        "Authorization": f"Tecton-key {TECTON_API_KEY}",
    }
    TECTON_FEATURE_SERVICE = f"{TECTON_API}/feature-service/query-features"


class ProductionConfig(Config):
    """
    Production Config Object
    """

    ...


class DevelopmentConfig(Config):
    """
    Development Config Object
    """

    DEBUG = False
    MONGO_DB_USERNAME = config("MONGO_DB_USERNAME", default="read_write_user")


def load_env_vars(flask_env=config("FLASK_ENV", default="")) -> None:
    """Load variables from secret store into ENV before we load the config.

    Args:
        flask_env (str): Flask environment value.

    Returns:

    """

    # import the aws module to prevent app context issues.
    aws = import_module(api_c.AWS_MODULE_NAME)

    if flask_env in [api_c.DEVELOPMENT_MODE, api_c.PRODUCTION_MODE]:
        # load in variables before running flask app.
        for key, value in LOAD_VAR_DICT.items():
            try:
                environ[key] = aws.parameter_store.get_store_value(value)
            except ValueError:
                logging.info("Unable to connect to AWS Parameter Store.")


def get_config(flask_env=config("FLASK_ENV", default="")) -> Config:
    """Get configuration for the environment.

    Args:
        flask_env (str): Flask environment value.

    Returns:

    """
    if flask_env == api_c.DEVELOPMENT_MODE:
        return DevelopmentConfig
    return Config
