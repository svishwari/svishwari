"""Purpose of this file is for housing the config settings for the API.
Ensure that all config values are pulled in a single spot.

Decouple always searches for Options in this order:
1. Environment variables
2. Repository: ini or .env file
3. Default argument passed to config.
"""
from importlib import import_module
from os import environ
from pathlib import Path
from typing import Union
from decouple import config
from huxunifylib.util.general.logging import logger
from huxunify.api import constants as api_c


class Config:
    """Config Object."""

    DEBUG = True
    FLASK_ENV = "test"

    # AWS_CONFIG
    AWS_REGION = config(api_c.AWS_REGION, default="")
    S3_DATASET_BUCKET = config(api_c.AWS_S3_BUCKET_CONST, default="")
    DISABLE_DELIVERIES = config(
        api_c.DISABLE_DELIVERIES, default=False, cast=bool
    )

    # MONGO CONFIG
    MONGO_DB_HOST = config(api_c.MONGO_DB_HOST, default="localhost")
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
        api_c.USERNAME: MONGO_DB_USERNAME,
        api_c.PASSWORD: MONGO_DB_PASSWORD,
        api_c.SSL_CERT_PATH: MONGO_SSL_CERT,
    }

    # OKTA CONFIGURATION
    OKTA_CLIENT_ID = config(api_c.OKTA_CLIENT_ID, default="")
    OKTA_ISSUER = config(api_c.OKTA_ISSUER, default="")

    # TECTON
    TECTON_API_KEY = config(api_c.TECTON_API_KEY, default="")
    TECTON_API = config("TECTON_API", default="")
    TECTON_API_HEADERS = {
        "Authorization": f"Tecton-key {TECTON_API_KEY}",
    }
    TECTON_FEATURE_SERVICE = f"{TECTON_API}/feature-service/query-features"

    # JIRA
    JIRA_PROJECT_KEY = config(api_c.JIRA_PROJECT_KEY, default="")
    JIRA_API_KEY = config(api_c.JIRA_API_KEY, default="")
    JIRA_SERVER = config(api_c.JIRA_SERVER, default="")

    # audience router config
    AUDIENCE_ROUTER_JOB_ROLE_ARN = config(
        api_c.AUDIENCE_ROUTER_JOB_ROLE_ARN_CONST, default=""
    )
    AUDIENCE_ROUTER_EXECUTION_ROLE_ARN = config(
        api_c.AUDIENCE_ROUTER_EXECUTION_ROLE_ARN_CONST, default=""
    )
    AUDIENCE_ROUTER_IMAGE = config(
        api_c.AUDIENCE_ROUTER_IMAGE_CONST, default=""
    )
    AUDIENCE_ROUTER_JOB_QUEUE = config(
        api_c.AUDIENCE_ROUTER_JOB_QUEUE_CONST, default=""
    )

    # campaign data performance router scheduled event name
    CDPR_EVENT_NAME = config(api_c.CDPR_EVENT_CONST, default="")

    # feedback loop data router scheduled event name
    FLDR_EVENT_NAME = config(api_c.FLDR_EVENT_CONST, default="")

    EVENT_ROUTERS = [CDPR_EVENT_NAME, FLDR_EVENT_NAME]

    CDP_SERVICE = config(api_c.CDP_SERVICE, default="")
    CDP_CONNECTION_SERVICE = config(api_c.CDP_CONNECTION_SERVICE, default="")

    # setting to enable/disable downloading of empty audience file in
    # /audiences/{audience_id}/{download_type} endpoint
    RETURN_EMPTY_AUDIENCE_FILE = config(
        api_c.RETURN_EMPTY_AUDIENCE_FILE, default=True, cast=bool
    )

    # Preserve ordering in json
    JSON_SORT_KEYS = config(
        api_c.JSON_SORT_KEYS_CONST, default=False, cast=bool
    )

    TEST_AUTH_OVERRIDE = config(
        api_c.TEST_AUTH_OVERRIDE, default=False, cast=bool
    )


class ProductionConfig(Config):
    """Production Config Object."""

    DEBUG = False
    FLASK_ENV = api_c.PRODUCTION_MODE


class DevelopmentConfig(Config):
    """Development Config Object."""

    FLASK_ENV = api_c.DEVELOPMENT_MODE
    MONGO_DB_USERNAME = config(api_c.MONGO_DB_USERNAME, default="")
    MONGO_DB_CONFIG = {
        api_c.HOST: Config.MONGO_DB_HOST,
        api_c.PORT: Config.MONGO_DB_PORT,
        api_c.USERNAME: MONGO_DB_USERNAME,
        api_c.PASSWORD: Config.MONGO_DB_PASSWORD,
        api_c.SSL_CERT_PATH: Config.MONGO_SSL_CERT,
    }

    RETURN_EMPTY_AUDIENCE_FILE = config(
        api_c.RETURN_EMPTY_AUDIENCE_FILE, default=False, cast=bool
    )
    TEST_AUTH_OVERRIDE = False


class PyTestConfig(Config):
    """Test Config Object."""

    DEBUG = True
    FLASK_ENV = api_c.TEST_MODE
    AWS_REGION = "fake-fake-1"
    S3_DATASET_BUCKET = "test-bucket"
    MONGO_DB_USERNAME = config(api_c.MONGO_DB_USERNAME, default="")
    MONGO_DB_CONFIG = {
        api_c.HOST: Config.MONGO_DB_HOST,
        api_c.PORT: Config.MONGO_DB_PORT,
        api_c.USERNAME: MONGO_DB_USERNAME,
        api_c.PASSWORD: Config.MONGO_DB_PASSWORD,
        api_c.SSL_CERT_PATH: Config.MONGO_SSL_CERT,
    }

    # OKTA CONFIGURATION
    OKTA_CLIENT_ID = "test-client-id"
    OKTA_ISSUER = "https://fake.fake"

    # JIRA
    JIRA_PROJECT_KEY = "fake-jira-project"
    JIRA_API_KEY = "fake-jira-key"
    JIRA_SERVER = "https://fake.fake.jira.fake"

    # TECTON CONFIGURATION
    TECTON_API_KEY = "fake-key"
    TECTON_API = "https://fake.fake.com"
    TECTON_API_HEADERS = {
        "Authorization": f"Tecton-key {TECTON_API_KEY}",
    }
    TECTON_FEATURE_SERVICE = f"{TECTON_API}/feature-service/query-features"

    # CDP CONFIGURATION
    CDP_SERVICE = "https://fake.fake.com"
    CDP_CONNECTION_SERVICE = "https://fake.fake.com"

    RETURN_EMPTY_AUDIENCE_FILE = config(
        api_c.RETURN_EMPTY_AUDIENCE_FILE, default=False, cast=bool
    )
    TEST_AUTH_OVERRIDE = False


def load_env_vars(flask_env=config(api_c.FLASK_ENV, default="")) -> None:
    """Load variables from secret store into ENV before we load the config.

    Args:
        flask_env (str): Flask environment value.
    """

    # import the aws module to prevent app context issues.
    aws = import_module(api_c.AWS_MODULE_NAME)

    # set flask key based on derived setting
    environ[api_c.FLASK_ENV] = get_config().FLASK_ENV

    if flask_env in [api_c.DEVELOPMENT_MODE, api_c.PRODUCTION_MODE]:
        # load in variables before running flask app.
        for i in range(0, 50):
            # attempt to grab the SSM from the ini file
            load_ssm_key = config(f"SSM_{i}", None)

            # if empty, break loop
            if not load_ssm_key:
                break

            # ensure the ssm key has the expected delimiter
            if api_c.SSM_INIT_LOAD_DELIMITER not in load_ssm_key:
                logger.error(
                    "SSM Key '%s' missing %s delimiter.",
                    load_ssm_key,
                    api_c.SSM_INIT_LOAD_DELIMITER,
                )
                break

            # split the ssm env var into key and value.
            ssm_key, ssm_value = load_ssm_key.split(
                api_c.SSM_INIT_LOAD_DELIMITER
            )

            # attempt to pull the ssm from the store and set env key value.
            try:
                environ[ssm_key] = aws.parameter_store.get_store_value(
                    ssm_value
                )
            except ValueError:
                logger.info("Unable to connect to AWS Parameter Store.")


def get_config(
    flask_env=config(api_c.FLASK_ENV, default="")
) -> Union[DevelopmentConfig, Config, PyTestConfig]:
    """Get configuration for the environment.

    Args:
        flask_env (str): Flask environment value.

    Returns:
        Union[DevelopmentConfig, Config, PyTestConfig]: config object.
    """

    if flask_env == api_c.DEVELOPMENT_MODE:
        return DevelopmentConfig
    if flask_env == api_c.TEST_MODE:
        return PyTestConfig
    return Config
