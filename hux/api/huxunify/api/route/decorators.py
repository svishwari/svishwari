"""File for decorators used in the API routes"""
# pylint: disable=too-many-statements,disable=unused-argument
import getpass
from functools import wraps
from typing import Any
from http import HTTPStatus

import requests
from bson import ObjectId
from bson.errors import InvalidId

import facebook_business.exceptions
from flask import request
from marshmallow import ValidationError

from huxunifylib.util.general.logging import logger
from huxunifylib.connectors import (
    CustomAudienceDeliveryStatusError,
)
from huxunifylib.database.engagement_management import get_engagement
from huxunifylib.database import (
    orchestration_management,
    constants as db_c,
    delivery_platform_management as destination_management,
)
import huxunifylib.database.db_exceptions as de

from huxunify.api.route.utils import get_db_client, get_user_from_db
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.okta import (
    introspect_token,
    get_token_from_request,
)
from huxunify.api.exceptions import (
    integration_api_exceptions as iae,
    unified_exceptions as ue,
)
from huxunify.api.config import get_config


def add_view_to_blueprint(self, rule: str, endpoint: str, **options) -> object:
    """This decorator takes a blueprint and assigns the view function directly
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
        **options (Any): options to be added to URL rule

    Returns:
        Response (object): decorator
    """

    def decorator(cls) -> Any:
        """Decorator function.

        Args:
            cls (object): a function to decorate

        Returns:
            Response (Any): Returns the decorated object.
        """

        # add the url to the flask object
        self.add_url_rule(rule, view_func=cls.as_view(endpoint), **options)
        return cls

    return decorator


def secured() -> object:
    """This decorator takes an API request and validates
    if the user provides a JWT token and if that token is valid.

    Eventually this decorator will extract the ROLE from
    OKTA when it is available, and a user can submit role as a param here.

    Example: @secured()

    Returns:
        Response (object): decorator
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
               Response (object): returns a decorated function object.
            """
            # override if flag set locally
            if get_config().TEST_AUTH_OVERRIDE:
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

            return {api_c.MESSAGE: api_c.INVALID_AUTH}, HTTPStatus.BAD_REQUEST

        # set tag so we can assert if a function is secured via this decorator
        decorator.__wrapped__ = in_function
        return decorator

    return wrapper


def requires_access_levels(access_levels: list) -> object:
    """Purpose of this decorator is for validating access levels for requests.

    Example: @requires_access_level()

    Args:
        access_levels (list): list of access levels.

    Returns:
        Response (object): decorator
    """

    def wrapper(in_function) -> object:
        """Decorator for wrapping a function.

        Args:
            in_function (object): function object.

        Returns:
           Response (object): returns a wrapped decorated function object.
        """

        @wraps(in_function)
        def decorator(*args, **kwargs) -> object:
            """Decorator for validating access level and returning a
            user object.

            Args:
                *args (object): function arguments.
                **kwargs (dict): function keyword arguments.

            Returns:
               Response (object): returns a decorated function object.
            """

            # override if flag set locally
            if get_config().TEST_AUTH_OVERRIDE:
                # return a default user name
                kwargs[api_c.USER] = {
                    api_c.USER_NAME: getpass.getuser(),
                    api_c.USER_ACCESS_LEVEL: db_c.USER_ROLE_ADMIN,
                    api_c.USER_PII_ACCESS: True,
                }
                return in_function(*args, **kwargs)

            # get the access token
            logger.info("Getting okta access token from request.")
            token_response = get_token_from_request(request)

            # if not 200, return response
            if token_response[1] != 200:
                return token_response

            # get the user info and the corresponding user document from db
            # from the access_token
            user = get_user_from_db(token_response[0])

            # if the user_response object is of type tuple, then return it as
            # such since a failure must have occurred while fetching user data
            # from db
            if isinstance(user, tuple):
                return user

            # check access level
            access_level = api_c.AccessLevel(user.get(db_c.USER_ROLE))
            if access_level not in access_levels:
                logger.info(
                    "User has an invalid access level to access this resource."
                )
                return {
                    api_c.MESSAGE: api_c.INVALID_AUTH
                }, HTTPStatus.UNAUTHORIZED

            user[api_c.USER_NAME] = user.get(db_c.USER_DISPLAY_NAME, None)
            user[api_c.USER_PII_ACCESS] = user.get(db_c.USER_PII_ACCESS, False)

            # return found user
            kwargs[api_c.USER] = user

            return in_function(*args, **kwargs)

        return decorator

    return wrapper


# pylint: disable=too-many-return-statements
def api_error_handler(custom_message: dict = None) -> object:
    """This decorator handles generic errors for API requests.

    Eventually this decorator will handle more types of errors.

    Example: @api_error_handler()

    Args:
        custom_message (dict): Optional; A dict containing custom messages for
            particular exceptions.

    Returns:
        Response (object): decorator.
    """

    def wrapper(in_function) -> object:
        """Decorator for wrapping a function.

        Args:
            in_function (object): function object.

        Returns:
           Response (object): returns a wrapped decorated function object.
        """

        # pylint: disable=too-many-return-statements, too-many-branches
        @wraps(in_function)
        def decorator(*args, **kwargs) -> object:
            """Decorator for handling errors.

            Args:
                *args (object): function arguments.
                **kwargs (dict): function keyword arguments.

            Returns:
               Response (object): returns a decorated function object.
            """
            try:
                return in_function(*args, **kwargs)

            except ValidationError as validation_error:
                if custom_message:
                    error_message = custom_message.get(
                        ValidationError, validation_error.messages
                    )
                else:
                    error_message = validation_error.messages
                logger.error(
                    "%s: %s while executing %s in module %s.",
                    validation_error.__class__,
                    validation_error.messages,
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return error_message, HTTPStatus.BAD_REQUEST

            except InvalidId as invalid_id:
                logger.error(
                    "%s: %s while executing %s in module %s.",
                    invalid_id.__class__,
                    str(invalid_id),
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {"message": str(invalid_id)}, HTTPStatus.BAD_REQUEST

            except de.InvalidID as invalid_id:
                logger.error(
                    "%s: %s while executing %s in module %s.",
                    invalid_id.__class__,
                    str(invalid_id),
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {"message": str(invalid_id)}, HTTPStatus.BAD_REQUEST

            except facebook_business.exceptions.FacebookRequestError as exc:
                logger.error(
                    "%s: %s while executing %s in module %s.",
                    exc.__class__,
                    exc.api_error_message(),
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {
                    "message": "Error connecting to Facebook"
                }, HTTPStatus.BAD_REQUEST

            except ValueError as value_error:
                logger.error(
                    "%s: %s Error encountered while executing %s in module %s.",
                    value_error.__class__,
                    value_error.args[0],
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {
                    "message": custom_message
                    if custom_message
                    else "Value Error Encountered"
                }, HTTPStatus.INTERNAL_SERVER_ERROR

            except ZeroDivisionError:
                return {
                    "message": custom_message
                    if custom_message
                    else "Division by zero Error Encountered"
                }, HTTPStatus.INTERNAL_SERVER_ERROR

            except de.DuplicateName as exc:
                logger.error(
                    "%s: %s Error encountered while executing %s in module %s.",
                    exc.__class__,
                    exc.args[0] if exc.args else exc.exception_message,
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {"message": api_c.DUPLICATE_NAME}, HTTPStatus.FORBIDDEN

            except CustomAudienceDeliveryStatusError as exc:
                logger.error(
                    "%s: %s while executing %s in module %s.",
                    exc.__class__,
                    exc.exception_message,
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {
                    "message": "Delivered custom audience is inactive or unusable."
                }, HTTPStatus.NOT_FOUND

            except iae.FailedAPIDependencyError as exc:
                logger.error(
                    "%s: %s while executing %s in module %s.",
                    exc.__class__,
                    exc.args[0] if exc.args else exc.exception_message,
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {
                    "message": api_c.FAILED_DEPENDENCY_ERROR_MESSAGE
                }, HTTPStatus.FAILED_DEPENDENCY

            except iae.FailedDestinationDependencyError as exc:
                error_message = (
                    exc.args[0]
                    if exc.args
                    else api_c.DESTINATION_CONNECTION_FAILED
                )
                logger.error(
                    "%s: %s Error encountered while executing %s in module %s.",
                    exc.__class__,
                    error_message,
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {"message": error_message}, HTTPStatus.FAILED_DEPENDENCY

            except iae.EmptyAPIResponseError as exc:
                logger.error(
                    "%s: %s while executing %s in module %s.",
                    exc.__class__,
                    exc.args[0] if exc.args else exc.exception_message,
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {
                    "message": api_c.EMPTY_RESPONSE_DEPENDENCY_ERROR_MESSAGE
                }, HTTPStatus.NOT_FOUND

            except ue.InputParamsValidationError as exc:
                logger.error(
                    "%s: %s Error encountered while executing %s in module %s.",
                    exc.__class__,
                    exc.args[0] if exc.args else exc.exception_message,
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {"message": exc.args[0]}, HTTPStatus.BAD_REQUEST

            except requests.exceptions.ConnectionError as exc:
                logger.error(
                    "%s: Failed connecting to %s in %s in module %s.",
                    exc.__class__,
                    exc.request.url,
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {
                    "message": api_c.FAILED_DEPENDENCY_CONNECTION_ERROR_MESSAGE
                }, HTTPStatus.FAILED_DEPENDENCY

            except iae.FailedSSMDependencyError as exc:
                logger.error(
                    "%s: %s Error encountered while executing %s in module %s.",
                    exc.__class__,
                    exc.args[0] if exc.args else exc.exception_message,
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {
                    "message": api_c.AWS_SSM_PARAM_NOT_FOUND_ERROR_MESSAGE
                }, HTTPStatus.FAILED_DEPENDENCY

            except Exception as exc:  # pylint: disable=broad-except
                # log error, but return vague description to client.
                logger.error(
                    "%s: %s while executing %s in module %s.",
                    exc.__class__,
                    exc,
                    in_function.__qualname__,
                    in_function.__module__,
                )
                if custom_message:
                    return custom_message, HTTPStatus.BAD_REQUEST

                return {
                    "message": "Internal Server Error"
                }, HTTPStatus.INTERNAL_SERVER_ERROR

        # set tag so we can assert if a function is secured via this decorator
        decorator.__wrapped__ = in_function
        return decorator

    return wrapper


def validate_delivery_params(func) -> object:
    """A decorator for common validations in delivery.py.

    Performs checks to determine if object ids are valid,
    engagement id exists, engagements have audiences,
    audience id exists,audience is attached. Also converts
    all string ids to ObjectId.

    Example: @validate_delivery_params

    Args:
        func(object): function object.

    Returns:
        Response (object): returns a wrapped decorated function object.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> object:
        """Decorator for validation and converting to ObjectId.

        Args:
            *args (object): function arguments.
            **kwargs (dict): function keyword arguments.

        Returns:
           Response (object): returns a decorated function object.
        """

        # convert to object id
        for key, val in kwargs.items():
            kwargs[key] = ObjectId(val)

        database = get_db_client()
        # check if engagement id exists
        engagement_id = kwargs.get(api_c.ENGAGEMENT_ID, None)
        if engagement_id:
            engagement = get_engagement(database, ObjectId(engagement_id))
            if engagement:
                if db_c.AUDIENCES not in engagement:
                    logger.error(
                        "Engagement has no audiences while executing while executing %s in %s.",
                        func.__qualname__,
                        func.__module__,
                    )
                    return {
                        "message": "Engagement has no audiences."
                    }, HTTPStatus.BAD_REQUEST
            else:
                # validate that the engagement has audiences
                logger.error(
                    "Engagement not found while executing  %s in %s.",
                    func.__qualname__,
                    func.__module__,
                )
                return {
                    "message": api_c.ENGAGEMENT_NOT_FOUND
                }, HTTPStatus.NOT_FOUND
        # check if audience id exists
        audience_id = kwargs.get(api_c.AUDIENCE_ID, None)
        if audience_id:
            # check if audience id exists
            audience = orchestration_management.get_audience(
                database, ObjectId(audience_id)
            )
            if not audience:
                logger.error(
                    "Audience does not exist while executing  %s in %s.",
                    func.__qualname__,
                    func.__module__,
                )
                return {
                    "message": "Audience does not exist."
                }, HTTPStatus.BAD_REQUEST

            if audience_id and engagement_id:
                # validate that the audience is attached
                audience_ids = [
                    x[db_c.OBJECT_ID] for x in engagement[db_c.AUDIENCES]
                ]
                if ObjectId(audience_id) not in audience_ids:
                    logger.error(
                        "Audience %s is not attached to engagement %s while executing %s in %s.",
                        audience_id,
                        engagement_id,
                        func.__qualname__,
                        func.__module__,
                    )
                    return {
                        "message": "Audience is not attached to the engagement."
                    }, HTTPStatus.BAD_REQUEST

        return func(*args, **kwargs)

    return wrapper


def validate_destination(
    check_if_destination_in_db: bool = True,
) -> object:
    """This decorator handles validation of destination objects.

    Example: @validate_destination_wrapper()

    Args:
        check_if_destination_in_db (bool): Optional; If check_destination_exists
            a check is performed to verify if destination exists in the db.

    Returns:
        Response (object): decorator.
    """

    def wrapper(in_function) -> object:
        """Decorator for wrapping a function.

        Args:
            in_function (object): function object.

        Returns:
           Response (object): returns a wrapped decorated function object.
        """

        @wraps(in_function)
        def decorator(*args, **kwargs) -> object:
            """Decorator for handling destination validation.

            Args:
                *args (object): function arguments.
                **kwargs (dict): function keyword arguments.

            Returns:
               Response (object): returns a decorated function object.
            """

            destination_id = ObjectId(kwargs.get("destination_id", None))

            if check_if_destination_in_db:
                if not destination_management.get_delivery_platform(
                    get_db_client(), destination_id
                ):
                    logger.error(
                        "Could not find destination with id %s.",
                        destination_id,
                    )
                    return {
                        "message": api_c.DESTINATION_NOT_FOUND
                    }, HTTPStatus.NOT_FOUND

            kwargs["destination_id"] = destination_id

            return in_function(*args, **kwargs)

        decorator.__wrapped__ = in_function
        return decorator

    return wrapper


def validate_engagement_and_audience() -> object:
    """This decorator handles validation of engagement and audience objects.

    Example: @validate_engagement_and_audience()

    Returns:
        Response (object): decorator.
    """

    def wrapper(in_function) -> object:
        """Decorator for wrapping a function.

        Args:
            in_function (object): function object.

        Returns:
           Response (object): returns a wrapped decorated function object.
        """

        @wraps(in_function)
        def decorator(*args, **kwargs) -> object:
            """Decorator for handling engagement validation.

            Args:
                *args (object): function arguments.
                **kwargs (dict): function keyword arguments.

            Returns:
               Response (object): returns a decorated function object.
            """

            database = get_db_client()

            # engagement validation
            engagement_id = kwargs.get(api_c.ENGAGEMENT_ID, None)

            if engagement_id is not None:
                engagement_id = ObjectId(engagement_id)
                if not get_engagement(database, engagement_id):
                    logger.error(
                        "Engagement with engagement ID %s not found.",
                        engagement_id,
                    )
                    return {
                        api_c.MESSAGE: api_c.ENGAGEMENT_NOT_FOUND
                    }, HTTPStatus.NOT_FOUND

                kwargs[api_c.ENGAGEMENT_ID] = engagement_id

            # audience validation
            audience_id = kwargs.get(api_c.AUDIENCE_ID, None)

            if audience_id is not None:
                audience_id = ObjectId(audience_id)
                if not orchestration_management.get_audience(
                    database, audience_id
                ):
                    logger.error(
                        "Audience with audience ID %s not found.",
                        audience_id,
                    )
                    return {
                        api_c.MESSAGE: api_c.AUDIENCE_NOT_FOUND
                    }, HTTPStatus.NOT_FOUND

                kwargs[api_c.AUDIENCE_ID] = audience_id

            return in_function(*args, **kwargs)

        # set tag so we can assert if a function is secured via this decorator
        decorator.__wrapped__ = in_function

        return decorator

    return wrapper
