"""Purpose of this file is for housing pytest startup scripts."""
import logging
from pathlib import Path
from os import getenv, environ
from collections import namedtuple
import pytest
from _pytest.config import Config
from requests.exceptions import MissingSchema
from bson import ObjectId
from pymongo import MongoClient
from get_okta_token import OktaOIDC


# change log level from WARNING to INFO and initialise logger for conftest
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
# ENV VARS
OKTA_PARAM_DICT = {
    "org_url": getenv("OKTA_ISSUER"),
    "user": getenv("OKTA_TEST_USER_NAME"),
    "pw": getenv("OKTA_TEST_USER_PW"),
    "client_id": getenv("OKTA_CLIENT_ID"),
    "scopes": "openid+profile+email",
    "redirect_uri": getenv("OKTA_REDIRECT_URI"),
}
MONGO_DB_CONFIG = {
    "host": getenv("MONGO_DB_HOST"),
    "port": int(getenv("MONGO_DB_PORT")),
    "w": 1,
    "username": getenv("MONGO_DB_USERNAME"),
    "password": getenv("MONGO_DB_PASSWORD"),
    "ssl": True,
    "tlsCAFile": str(
        Path(__file__).parent.parent.joinpath("rds-combined-ca-bundle.pem")
    ),
}
ACCESS_TOKEN = "ACCESS_TOKEN"
DATABASE = "data_management"
INT_TEST_API_VERSION = "INT_TEST_API_VERSION"
INT_TEST_HOST = "INT_TEST_HOST"
AUTHORIZATION = "Authorization"
BEARER = "Bearer"
ID = "_id"
CLEAN_UP_COLLECTIONS_DICT = {
    "applications": "created_by",
    "audiences": "created_by",
    "client_projects": "created_by",
    "configurations": "created_by",
    "delivery_jobs": "username",
    "engagements": "created_by",
    "lookalike_audiences": "created_by",
    "notifications": "username",
}


# Declaring Crud namedtuple()
Crud = namedtuple("Crud", ["collection", "id"])


# pylint: disable=unused-argument
def pytest_configure(config: Config):
    """Override the pytest plugin. This hook is called for every plugin and
        initial conftest file after command line options have been parsed.

    Args:
        config (Config): Existing pytest config.
    """

    # set global IDs
    pytest.CRUD_OBJECTS = []
    pytest.APP_URL = getenv(INT_TEST_HOST)
    pytest.API_URL = f"{getenv(INT_TEST_HOST)}/{getenv(INT_TEST_API_VERSION)}"
    pytest.DB_CLIENT = MongoClient(**MONGO_DB_CONFIG)[DATABASE]

    try:
        # setup the oidc class.
        okta_oidc = OktaOIDC(**OKTA_PARAM_DICT)

        # set the token for pytest usage.
        environ[ACCESS_TOKEN] = okta_oidc.get_access_token(False)

        # set the auth header
        pytest.HEADERS = {AUTHORIZATION: f"{BEARER} {environ[ACCESS_TOKEN]}"}
    except MissingSchema:
        pass


# pylint: disable=unused-argument, disable=broad-except
def pytest_unconfigure(config):
    """Override the pytest plugin. This hook is called for every plugin and
        initial conftest file after command line options have been parsed.

    Args:
        config (Config): Existing pytest config.
    """

    # clean crud objects
    crud_obj: Crud
    for crud_obj in pytest.CRUD_OBJECTS:
        try:
            LOGGER.info(
                "Cleaning Object ID %s for %s.",
                crud_obj.id,
                crud_obj.collection,
            )
            pytest.DB_CLIENT[crud_obj.collection].delete_one(
                {ID: ObjectId(crud_obj.id)}
            )
            LOGGER.info(
                "Cleaning Object ID %s for %s complete.",
                crud_obj.id,
                crud_obj.collection,
            )
        except BaseException as exception:
            LOGGER.error(
                "Cleaning Object ID %s for %s failed: %s.",
                crud_obj.id,
                crud_obj.collection,
                str(exception),
            )

    # clean stranded documents created by integration tests in various
    # collections
    int_test_user_name = getenv("INT_TEST_USER_NAME")
    LOGGER.info("Integration test user's user name: %s", int_test_user_name)

    for (
        collection_name,
        collection_field,
    ) in CLEAN_UP_COLLECTIONS_DICT.items():
        try:
            LOGGER.info(
                "Cleaning up left out documents in collection %s using field "
                "%s start.",
                collection_name,
                collection_field,
            )
            deleted_count = (
                pytest.DB_CLIENT[collection_name]
                .delete_many({collection_field: int_test_user_name})
                .deleted_count
            )
            LOGGER.info(
                "Cleaning up left out documents in collection %s using field "
                "%s complete. Deleted documents count: %s.",
                collection_name,
                collection_field,
                deleted_count,
            )
        except BaseException as exception:
            LOGGER.error(
                "Cleaning stranded documents from collection %s failed: %s.",
                collection_name,
                str(exception),
            )
