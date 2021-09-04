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


LOAD_VAR_DICT = {
    api_c.TECTON_API_KEY: api_c.TECTON_API_KEY,
    api_c.MONGO_DB_HOST: "unifieddb_host_alias",
    api_c.MONGO_DB_PASSWORD: "unifieddb_rw",
}


class Config:
    """
    Config Object
    """

    DEBUG = False
    FLASK_ENV = "test"

    # AWS_CONFIG
    AWS_REGION = config(api_c.AWS_REGION)

    # MONGO CONFIG
    MONGO_DB_HOST = config(api_c.MONGO_DB_HOST)
    MONGO_DB_PORT = config(api_c.MONGO_DB_PORT, default=27017, cast=int)
    MONGO_DB_USERNAME = config(api_c.MONGO_DB_USERNAME, default="")
    MONGO_DB_PASSWORD = config(api_c.MONGO_DB_PASSWORD, default="")
    # grab the SSL cert path
    MONGO_SSL_CERT = str(
        Path(__file__).parent.parent.joinpath("rds-combined-ca-bundle.pem")
    )

    MONGO_DB_CONFIG = {
        api_c.HOST: MONGO_DB_HOST,
        api_c.PORT: MONGO_DB_PORT,
        api_c.USER_NAME: MONGO_DB_USERNAME,
        api_c.PASSWORD: MONGO_DB_PASSWORD,
        api_c.SSL_CERT_PATH: MONGO_SSL_CERT,
    }

    # OKTA CONFIGURATION
    OKTA_CLIENT_ID = config(api_c.OKTA_CLIENT_ID)
    OKTA_ISSUER = config(api_c.OKTA_ISSUER)

    # TECTON
    TECTON_API_KEY = config(api_c.TECTON_API_KEY)
    TECTON_API = config(api_c.TECTON_API)
    TECTON_API_HEADERS = {
        "Authorization": f"Tecton-key {TECTON_API_KEY}",
    }
    TECTON_FEATURE_SERVICE = f"{TECTON_API}/feature-service/query-features"

    # audience router config
    AUDIENCE_ROUTER_JOB_ROLE_ARN = config(
        api_c.AUDIENCE_ROUTER_JOB_ROLE_ARN_CONST
    )
    AUDIENCE_ROUTER_EXECUTION_ROLE_ARN = config(
        api_c.AUDIENCE_ROUTER_EXECUTION_ROLE_ARN_CONST
    )
    AUDIENCE_ROUTER_IMAGE = config(api_c.AUDIENCE_ROUTER_IMAGE_CONST)

    # campaign data performance router scheduled event name
    CDPR_EVENT_NAME = config(api_c.CDPR_EVENT_NAME_CONST)

    # feedback loop data router scheduled event name
    FLDR_EVENT_NAME = config(api_c.FLDR_EVENT_NAME_CONST)

    EVENT_ROUTERS = [CDPR_EVENT_NAME, FLDR_EVENT_NAME]

    CDP_SERVICE = config(api_c.CDP_SERVICE)
    CDP_CONNECTION_SERVICE = config(api_c.CDP_CONNECTION_SERVICE)

    # Preserve ordering in json
    JSON_SORT_KEYS = config(
        api_c.JSON_SORT_KEYS_CONST, default=False, cast=bool
    )


class ProductionConfig(Config):
    """
    Production Config Object
    """

    FLASK_ENV = api_c.PRODUCTION_MODE


class DevelopmentConfig(Config):
    """
    Development Config Object
    """

    DEBUG = False
    FLASK_ENV = api_c.DEVELOPMENT_MODE
    MONGO_DB_USERNAME = config(api_c.MONGO_DB_USERNAME)
    MONGO_DB_CONFIG = {
        api_c.HOST: Config.MONGO_DB_HOST,
        api_c.PORT: Config.MONGO_DB_PORT,
        api_c.USER_NAME: MONGO_DB_USERNAME,
        api_c.PASSWORD: Config.MONGO_DB_PASSWORD,
        api_c.SSL_CERT_PATH: Config.MONGO_SSL_CERT,
    }


def load_env_vars(flask_env=config("FLASK_ENV", default="")) -> None:
    """Load variables from secret store into ENV before we load the config.

    Args:
        flask_env (str): Flask environment value.

    Returns:

    """

    # import the aws module to prevent app context issues.
    aws = import_module(api_c.AWS_MODULE_NAME)

    # set flask key based on derived setting
    environ[api_c.FLASK_ENV] = get_config().FLASK_ENV

    if flask_env in [api_c.DEVELOPMENT_MODE, api_c.PRODUCTION_MODE]:
        # load in variables before running flask app.
        for key, value in LOAD_VAR_DICT.items():
            try:
                environ[key] = aws.parameter_store.get_store_value(value)
            except ValueError:
                logging.info("Unable to connect to AWS Parameter Store.")


def get_config(flask_env=config(api_c.FLASK_ENV, default="")) -> Config:
    """Get configuration for the environment.

    Args:
        flask_env (str): Flask environment value.

    Returns:

    """
    if flask_env == api_c.DEVELOPMENT_MODE:
        return DevelopmentConfig
    return Config
