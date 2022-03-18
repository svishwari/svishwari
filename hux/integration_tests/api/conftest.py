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
    "port": 27017,
    "w": 1,
    "username": getenv("MONGO_DB_USERNAME"),
    "password": getenv("MONGO_DB_PASSWORD"),
    "ssl": True,
    "ssl_ca_certs": str(
        Path(__file__).parent.joinpath("rds-combined-ca-bundle.pem")
    ),
}
ACCESS_TOKEN = "ACCESS_TOKEN"
DATABASE = "data_management"
TAVERN_TEST_API_VERSION = "TAVERN_TEST_API_VERSION"
TAVERN_TEST_HOST = "TAVERN_TEST_HOST"
AUTHORIZATION = "Authorization"
BEARER = "Bearer"
ID = "_id"


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
    pytest.API_URL = (
        f"{getenv(TAVERN_TEST_HOST)}/" f"{getenv(TAVERN_TEST_API_VERSION)}"
    )
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


# pylint: disable=unused-argument
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
            logging.info(
                "Cleaning Object ID %s for %s.",
                crud_obj.id,
                crud_obj.collection,
            )
            pytest.DB_CLIENT[crud_obj.collection].delete_one(
                {ID: ObjectId(crud_obj.id)}
            )
            logging.info(
                "Cleaning Object ID %s for %s. complete.",
                crud_obj.id,
                crud_obj.collection,
            )
        # pylint: disable=broad-except
        except BaseException as exception:
            logging.error(
                "Cleaning Object ID %s for %s failed: %s.",
                crud_obj.id,
                crud_obj.collection,
                str(exception),
            )
