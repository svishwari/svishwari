"""File for decorators used in the API routes"""
from functools import wraps
from typing import Any
from http import HTTPStatus
from bson import ObjectId
from bson.errors import InvalidId

import facebook_business.exceptions
from decouple import config
from flask import request
from marshmallow import ValidationError

from huxunifylib.util.general.logging import logger
from huxunifylib.connectors import (
    CustomAudienceDeliveryStatusError,
)
from huxunifylib.database.user_management import get_user, set_user
from huxunifylib.database.engagement_management import get_engagement
from huxunifylib.database import (
    orchestration_management,
    constants as db_c,
    delivery_platform_management as destination_management,
)
import huxunifylib.database.db_exceptions as de

from huxunify.api.route.utils import get_db_client
from huxunify.api import constants
from huxunify.api.data_connectors.okta import (
    introspect_token,
    get_token_from_request,
    get_user_info,
)
from huxunify.api.exceptions import integration_api_exceptions as iae


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

            # set of keys required from userinfo
            required_keys = {
                constants.OKTA_ID_SUB,
                constants.EMAIL,
                constants.NAME,
            }

            if config("TEST_AUTH_OVERRIDE", cast=bool, default=False):
                # return a default user id
                kwargs[constants.USER_NAME] = "test user"
                return in_function(*args, **kwargs)

            # get the auth token
            logger.info("Getting user info from OKTA.")
            token_response = get_token_from_request(request)

            # if not 200, return response.
            if token_response[1] != 200:
                return token_response

            # get the user information
            user_info = get_user_info(token_response[0])

            # checking if required keys are present in user_info
            if not required_keys.issubset(user_info.keys()):
                return {
                    "message": constants.AUTH401_ERROR_MESSAGE
                }, HTTPStatus.UNAUTHORIZED

            logger.info("Successfully got user info from OKTA.")
            # check if the user is in the database
            database = get_db_client()
            user = get_user(database, user_info[constants.OKTA_ID_SUB])
            # return found user, or create one and return it.
            kwargs[constants.USER_NAME] = (
                user[db_c.USER_DISPLAY_NAME]
                if user
                else set_user(
                    database,
                    user_info[constants.OKTA_ID_SUB],
                    user_info[constants.EMAIL],
                    display_name=user_info[constants.NAME],
                )[db_c.USER_DISPLAY_NAME]
            )

            return in_function(*args, **kwargs)

        return decorator

    return wrapper


# pylint: disable=too-many-return-statements
def api_error_handler(custom_message: dict = None) -> object:
    """
    This decorator handles generic errors for API requests.

    Eventually this decorator will handle more types of errors.

    Example: @api_error_handler()

    Args:
        custom_message (dict): Optional; A dict containing custom messages for
            particular exceptions

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

        # pylint: disable=too-many-return-statements, too-many-branches
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

            except ValueError:
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
                    "%s: %s while executing %s in module %s.",
                    exc.__class__,
                    exc.exception_message,
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return {
                    "message": constants.DUPLICATE_NAME
                }, HTTPStatus.BAD_REQUEST.value

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
                    "message": constants.FAILED_DEPENDENCY_ERROR_MESSAGE
                }, HTTPStatus.FAILED_DEPENDENCY

            except iae.FailedDateFilterIssue as exc:
                return {
                    "message": custom_message
                    if custom_message
                    else exc.exception_message
                }, HTTPStatus.BAD_REQUEST.value

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
    """A decorator for common validations in delivery.py

    Performs checks to determine if object ids are valid,
    engagement id exists, engagements have audiences,
    audience id exists,audience is attached. Also converts
    all string ids to ObjectId.

    Example: @validate_delivery_params

    Args:
        func(object): function object
    Returns:
        object: returns a wrapped decorated function object.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> object:
        """Decorator for validation and converting to ObjectId.
        Args:
            *args (object): function arguments.
            **kwargs (dict): function keyword arguments.

        Returns:
           object: returns a decorated function object.
        """

        # convert to object id
        for key, val in kwargs.items():
            kwargs[key] = ObjectId(val)

        database = get_db_client()
        # check if engagement id exists
        engagement_id = kwargs.get(constants.ENGAGEMENT_ID, None)
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
                    "message": constants.ENGAGEMENT_NOT_FOUND
                }, HTTPStatus.NOT_FOUND
        # check if audience id exists
        audience_id = kwargs.get(constants.AUDIENCE_ID, None)
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
    """
    This decorator handles validation of destination objects.
    Example: @validate_destination_wrapper()

    Args:
        check_if_destination_in_db (bool): Optional; If check_destination_exists
            a check is performed to verify if destination exists in the db.

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
            """Decorator for handling destination validation.

            Args:
                *args (object): function arguments.
                **kwargs (dict): function keyword arguments.

            Returns:
               object: returns a decorated function object.
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
                        "message": constants.DESTINATION_NOT_FOUND
                    }, HTTPStatus.NOT_FOUND

            kwargs["destination_id"] = destination_id

            return in_function(*args, **kwargs)

        decorator.__wrapped__ = in_function
        return decorator

    return wrapper
