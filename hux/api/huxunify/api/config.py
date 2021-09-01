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


# MONGO CONFIG VARS
HOST = "host"
PORT = "port"
USER_NAME = "username"
PASSWORD = "password"
SSL_CERT_PATH = "ssl_cert_path"


LOAD_VAR_DICT = {
    "TECTON_API_KEY": "TECTON_API_KEY",
    "MONGO_DB_HOST": "unifieddb_host_alias",
    "MONGO_DB_PASSWORD": "unifieddb_rw",
}


class Config:
    """
    Config Object
    """

    DEBUG = False
    FLASK_ENV = "test"

    # AWS_CONFIG
    AWS_REGION = config("AWS_REGION", default="us-east-1")

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

    OKTA_CLIENT_ID = config("OKTA_CLIENT_ID", default="0oab1i3ldgYyRvk5r2p7")
    OKTA_ISSUER = config(
        "OKTA_ISSUER", default="https://deloittedigital-ms.okta.com"
    )

    MONITORING_CONFIG = config("MONITORING-CONFIG", default="")

    # TECTON
    TECTON_API_KEY = config("TECTON_API_KEY", default="")
    TECTON_API = config(
        "TECTON_API", default="https://decisioning-client.tecton.ai/api/v1"
    )
    TECTON_API_HEADERS = {
        "Authorization": f"Tecton-key {TECTON_API_KEY}",
    }
    TECTON_FEATURE_SERVICE = f"{TECTON_API}/feature-service/query-features"

    # MONITORING VARS
    MONITORING_CONFIG_CONST = "MONITORING-CONFIG"
    MONITORING_CONFIG = config(MONITORING_CONFIG_CONST, default="")

    # AWS BATCH
    AUDIENCE_ROUTER_JOB_ROLE_ARN_CONST = "AUDIENCE-ROUTER-JOB-ROLE-ARN"
    AUDIENCE_ROUTER_JOB_ROLE_ARN = config(
        AUDIENCE_ROUTER_JOB_ROLE_ARN_CONST,
        default="arn:aws:iam::062880848536:role/adperf_ecs_execution_role",
    )
    AUDIENCE_ROUTER_EXECUTION_ROLE_ARN_CONST = (
        "AUDIENCE-ROUTER-EXECUTION-ROLE-ARN"
    )
    AUDIENCE_ROUTER_EXECUTION_ROLE_ARN = config(
        AUDIENCE_ROUTER_EXECUTION_ROLE_ARN_CONST,
        default="arn:aws:iam::062880848536:role/adperf_ecs_execution_role",
    )
    AUDIENCE_ROUTER_IMAGE_CONST = "AUDIENCE-ROUTER-IMAGE"
    AUDIENCE_ROUTER_IMAGE = config(
        AUDIENCE_ROUTER_IMAGE_CONST,
        default=(
            "602322178640.dkr.ecr.us-east-1.amazonaws.com/"
            "audience_router:latest"
        ),
    )

    # campaign data performance router scheduled event name
    CDPR_EVENT_NAME_CONST = "cdpr-event"
    CDPR_EVENT_NAME = config(
        CDPR_EVENT_NAME_CONST,
        default="campaign-performance-router-scheduler",
    )

    # feedback loop data router scheduled event name
    FLDR_EVENT_NAME_CONST = "fldr-event"
    FLDR_EVENT_NAME = config(
        FLDR_EVENT_NAME_CONST,
        default="feedback-loop-router-scheduler",
    )

    EVENT_ROUTERS = [CDPR_EVENT_NAME, FLDR_EVENT_NAME]

    CDP_SERVICE = config(
        "CDP_SERVICE",
        default="https://customer-profile-api.main.use1.hux-unified-dev1.in",
    )
    CDP_CONNECTION_SERVICE = config(
        "CDP_CONNECTION_SERVICE",
        default="https://connections-api.main.use1.hux-unified-dev1.in/",
    )
    S3_DATASET_BUCKET = config(
        "S3_DATASET_BUCKET", default="hux-unified-dev1-datasets"
    )
    # Preserve ordering in json
    JSON_SORT_KEYS = False


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
    MONGO_DB_USERNAME = config("MONGO_DB_USERNAME", default="read_write_user")
    MONGO_DB_CONFIG = {
        "host": Config.MONGO_DB_HOST,
        "port": Config.MONGO_DB_PORT,
        "username": MONGO_DB_USERNAME,
        "password": Config.MONGO_DB_PASSWORD,
        "ssl_cert_path": Config.MONGO_SSL_CERT,
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
    environ["FLASK_ENV"] = get_config().FLASK_ENV

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
