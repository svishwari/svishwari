"""
purpose of this file is to house route utilities
"""
import logging
from functools import wraps
from typing import Any, Tuple
from http import HTTPStatus

from healthcheck import HealthCheck
from decouple import config
from bson import ObjectId
from flask import request
from connexion.exceptions import ProblemException
from pymongo import MongoClient
from huxunifylib.connectors.util.client import db_client_factory
from huxunifylib.database.cdp_data_source_management import (
    get_all_data_sources,
)
from huxunifylib.database.user_management import get_user, set_user
from huxunifylib.database.constants import USER_DISPLAY_NAME

from huxunify.api.config import get_config
from huxunify.api import constants
from huxunify.api.data_connectors.tecton import check_tecton_connection
from huxunify.api.data_connectors.aws import check_aws_ssm, check_aws_batch
from huxunify.api.data_connectors.okta import (
    check_okta_connection,
    introspect_token,
    get_token_from_request,
    get_user_info,
)


def add_view_to_blueprint(self, rule: str, endpoint: str, **options) -> object:
    """
    This decorator takes a blueprint and assigns the view function directly
    the alternative to this is having to manually define this in app.py
    or at the bottom of the route file, as the input is a class.

    app.add_url_rule(
        '/colors/<palette>',
        view_func=PaletteView.as_view('colors'),
        methods=['GET']
    )

    Example: @add_view_to_blueprint(cdm_bp, "/datafeeds", "DatafeedSearch")

    Args:
        self (func): a flask/blueprint object, must have 'add_url_rule'
        rule (str): an input rule
        endpoint (str): the name of the endpoint

    Returns:
        Response: decorator

    """

    def decorator(cls) -> Any:
        """decorator function

        Args:
            cls (object): a function to decorate

        Returns:
            Response: Returns the decorated object.

        """
        # add the url to the flask object
        self.add_url_rule(rule, view_func=cls.as_view(endpoint), **options)
        return cls

    return decorator


def handle_api_exception(exc: Exception, description: str = "") -> None:
    """
    Purpose of this function is to handle general api exceptions,
    and reduce code in the route
    Args:
        exc (Exception): Exception object to handle
        description (str): Exception description.

    Returns:
          None
    """
    logging.error(
        "%s: %s.",
        exc.__class__,
        exc,
    )

    return ProblemException(
        status=int(HTTPStatus.BAD_REQUEST.value),
        title=HTTPStatus.BAD_REQUEST.description,
        detail=description,
    )


def get_db_client() -> MongoClient:
    """Get DB client.
    Returns:
        MongoClient: MongoDB client.
    """
    return db_client_factory.get_resource(**get_config().MONGO_DB_CONFIG)


def check_mongo_connection() -> Tuple[bool, str]:
    """Validate mongo DB connection.
    Args:

    Returns:
        tuple[bool, str]: Returns if the connection is valid, and the message.
    """
    try:
        # test finding documents
        get_all_data_sources(get_db_client())
        return True, "Mongo available."
    # pylint: disable=broad-except
    # pylint: disable=unused-variable
    except Exception as exception:
        return False, "Mongo not available."


def get_health_check() -> HealthCheck:
    """build and return the health check object

    Args:

    Returns:
        HealthCheck: HealthCheck object that processes checks when called

    """
    health = HealthCheck()

    # check variable
    health.add_section("flask_env", config("FLASK_ENV", default="UNKNOWN"))

    # add health checks
    health.add_check(check_mongo_connection)
    health.add_check(check_tecton_connection)
    health.add_check(check_okta_connection)
    health.add_check(check_aws_ssm)
    health.add_check(check_aws_batch)

    return health


def secured() -> object:
    """
    This decorator takes an API request and validates
    if the user provides a JWT token and if that token is valid.

    Eventually this decorator will extract the ROLE from
    OKTA when it is available, and a user can submit role as a param here.

    Example: @secured()

    Args:

    Returns:
        Response: decorator

    """

    def wrapper(in_function) -> object:
        """Decorator for wrapping a function

        Args:
            in_function (object): function object.

        Returns:
           object: returns a wrapped decorated function object.
        """

        @wraps(in_function)
        def decorator(*args, **kwargs) -> object:
            """Decorator for validating endpoint security.
            expected header to verify {"Authorization": "Bearer <token>"}

            Args:
                *args (object): function arguments.
                **kwargs (dict): function keyword arguments.

            Returns:
               object: returns a decorated function object.
            """

            # override if flag set locally
            if config("TEST_AUTH_OVERRIDE", cast=bool, default=False):
                return in_function(*args, **kwargs)

            # allow preflight options through
            if request.method == "OPTIONS":
                return "Success", 200

            # get the auth token
            token_response = get_token_from_request(request)

            # if not 200, return response.
            if token_response[1] != 200:
                return token_response

            # introspect token
            if introspect_token(token_response[0]):
                return in_function(*args, **kwargs)

            return constants.INVALID_AUTH, 400

        # set tag so we can assert if a function is secured via this decorator
        decorator.__wrapped__ = in_function
        return decorator

    return wrapper


def get_user_name() -> object:
    """
    This decorator takes an API request and extracts the user namr.

    Example: @get_user_name()

    Args:

    Returns:
        Response: decorator

    """

    def wrapper(in_function) -> object:
        """Decorator for wrapping a function

        Args:
            in_function (object): function object.

        Returns:
           object: returns a wrapped decorated function object.
        """

        @wraps(in_function)
        def decorator(*args, **kwargs) -> object:
            """Decorator for extracting the user_name

            Args:
                *args (object): function arguments.
                **kwargs (dict): function keyword arguments.

            Returns:
               object: returns a decorated function object.
            """

            # override if flag set locally
            if config("TEST_AUTH_OVERRIDE", cast=bool, default=False):
                # return a default user id
                kwargs[constants.OKTA_USER_ID] = ObjectId()
                return in_function(*args, **kwargs)

            # get the auth token
            token_response = get_token_from_request(request)

            # if not 200, return response.
            if token_response[1] != 200:
                return token_response

            # get the user information
            user_info = get_user_info(token_response[0])

            # check if the user is in the database
            database = get_db_client()
            user = get_user(database, user_info[constants.OKTA_ID_SUB])

            # return found user, or create one and return it.
            kwargs[constants.USER_NAME] = (
                user[USER_DISPLAY_NAME]
                if user
                else set_user(
                    database,
                    user_info[constants.OKTA_ID_SUB],
                    user_info[constants.EMAIL],
                    display_name=user_info[constants.NAME],
                )[USER_DISPLAY_NAME]
            )

            return in_function(*args, **kwargs)

        return decorator

    return wrapper


def api_error_handler() -> object:
    """
    This decorator handles generic errors for API requests.

    Eventually this decorator will handle more types of errors.

    Example: @api_error_handler()

    Args:

    Returns:
        Response: decorator

    """

    def wrapper(in_function) -> object:
        """Decorator for wrapping a function

        Args:
            in_function (object): function object.

        Returns:
           object: returns a wrapped decorated function object.
        """

        @wraps(in_function)
        def decorator(*args, **kwargs) -> object:
            """Decorator for handling errors.

            Args:
                *args (object): function arguments.
                **kwargs (dict): function keyword arguments.

            Returns:
               object: returns a decorated function object.
            """
            try:
                return in_function(*args, **kwargs)

            except Exception as exc:  # pylint: disable=broad-except
                # log error, but return vague description to client.
                logging.error(
                    "%s: %s.",
                    exc.__class__,
                    exc,
                )

                return {
                    "message": "Internal Server Error"
                }, HTTPStatus.INTERNAL_SERVER_ERROR

        # set tag so we can assert if a function is secured via this decorator
        decorator.__wrapped__ = in_function
        return decorator

    return wrapper
