"""
purpose of this file is to house route utilities
"""
from datetime import datetime
from functools import wraps
from typing import Any, Tuple, Union, Dict
from http import HTTPStatus
from bson import ObjectId
from bson.errors import InvalidId

import facebook_business.exceptions
from healthcheck import HealthCheck
from decouple import config
from flask import request
from connexion.exceptions import ProblemException
from pymongo import MongoClient
from marshmallow import ValidationError

from huxunifylib.util.general.logging import logger
from huxunifylib.connectors.util.client import db_client_factory
from huxunifylib.connectors import (
    CustomAudienceDeliveryStatusError,
)
from huxunifylib.database.cdp_data_source_management import (
    get_all_data_sources,
)
from huxunifylib.database.user_management import get_user, set_user
from huxunifylib.database.engagement_management import get_engagement
from huxunifylib.database import (
    orchestration_management,
    delivery_platform_management as destination_management,
    constants as db_c,
)
import huxunifylib.database.db_exceptions as de

from huxunify.api.config import get_config
from huxunify.api import constants
from huxunify.api.data_connectors.tecton import check_tecton_connection
from huxunify.api.data_connectors.aws import (
    check_aws_ssm,
    check_aws_batch,
)
from huxunify.api.data_connectors.okta import (
    check_okta_connection,
    introspect_token,
    get_token_from_request,
    get_user_info,
)
from huxunify.api.data_connectors.cdp import check_cdm_api_connection


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
    logger.error(
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
    health.add_check(check_cdm_api_connection)
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

        # pylint: disable=too-many-return-statements
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


def group_perf_metric(perf_metrics: list, metric_type: str) -> dict:
    """Group performance metrics
    ---

        Args:
            perf_metrics (list): List of performance metrics.
            metric_type (list): Type of performance metrics.

        Returns:
            perf_metric (dict): Grouped performance metric .

    """

    metric = {}

    if metric_type == constants.DISPLAY_ADS:
        for name in constants.DISPLAY_ADS_METRICS:
            metric[name] = sum(
                [
                    int(item[name])
                    for item in perf_metrics
                    if name in item.keys()
                ]
            )
    elif metric_type == constants.EMAIL:
        for name in constants.EMAIL_METRICS:
            metric[name] = sum(
                [
                    int(item[name])
                    for item in perf_metrics
                    if name in item.keys()
                ]
            )

    return metric


def get_friendly_delivered_time(delivered_time: datetime) -> str:
    """Group performance metrics
    ---

        Args:
            delivered_time (datetime): Delivery time.

        Returns:
            time_difference (str): Time difference as days / hours / mins.

    """

    delivered = (datetime.utcnow() - delivered_time).total_seconds()

    # pylint: disable=no-else-return
    if delivered / (60 * 60 * 24) >= 1:
        return str(int(delivered / (60 * 60 * 24))) + " days ago"
    elif delivered / (60 * 60) >= 1:
        return str(int(delivered / (60 * 60))) + " hours ago"
    elif delivered / 60 >= 1:
        return str(int(delivered / 60)) + " minutes ago"
    else:
        return str(int(delivered)) + " seconds ago"


def update_metrics(
    target_id: ObjectId,
    name: str,
    jobs: list,
    perf_metrics: list,
    metric_type: str,
) -> dict:
    """Update performance metrics

    Args:
        target_id (ObjectId) : Group Id.
        name (str): Name of group object.
        jobs (list): List of delivery jobs.
        perf_metrics (list): List of performance metrics.
        metric_type (str): Type of performance metrics.

    Returns:
        metric (dict): Grouped performance metrics .
    """
    delivery_jobs = [x[db_c.ID] for x in jobs]
    metric = {
        constants.ID: str(target_id),
        constants.NAME: name,
    }
    metric.update(
        group_perf_metric(
            [
                x[db_c.PERFORMANCE_METRICS]
                for x in perf_metrics
                if x[db_c.DELIVERY_JOB_ID] in delivery_jobs
            ],
            metric_type,
        )
    )
    return metric


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

        # check for valid object id and convert to object id
        for key, val in kwargs.items():
            if ObjectId.is_valid(val):
                kwargs[key] = ObjectId(val)
            else:
                # error appropriate
                logger.error(
                    "Encountered an invalid ID while executing %s in %s.",
                    func.__qualname__,
                    func.__module__,
                )
                return {
                    "message": constants.INVALID_OBJECT_ID
                }, HTTPStatus.BAD_REQUEST

        database = get_db_client()

        # check if engagement id exists
        engagement_id = kwargs.get("engagement_id", None)
        if engagement_id:
            engagement = get_engagement(database, engagement_id)
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
        audience_id = kwargs.get("audience_id", None)
        if audience_id:
            # check if audience id exists
            audience = None
            try:
                audience = orchestration_management.get_audience(
                    database, audience_id
                )
            except de.InvalidID:
                # get audience returns invalid if the audience does not exist.
                # pass and catch in the next step.
                pass
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
                if audience_id not in audience_ids:
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


def validate_destination_id(
    destination_id: str, check_if_destination_in_db: bool = True
) -> Union[ObjectId, Tuple[Dict[str, str], int]]:
    """Checks on destination_id

    Check if destination id is valid converts it to object_id.
    Also can check if destination_id is in db

    Args:
        destination_id (str) : Destination id.
        check_if_destination_in_db (bool): Optional; flag to check if destination in db

    Returns:
        response(dict): Message and HTTP status to be returned in response in
            case of failing checks,
        destination_id (ObjectId): Destination id as object id if
            all checks are successful.
    """
    destination_id = ObjectId(destination_id)

    if check_if_destination_in_db:
        if not destination_management.get_delivery_platform(
            get_db_client(), destination_id
        ):
            logger.error(
                "Could not find destination with id %s.", destination_id
            )
            return {
                "message": constants.DESTINATION_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

    return destination_id


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
            destination_id = kwargs.get("destination_id", None)
            return_val = validate_destination_id(
                destination_id, check_if_destination_in_db
            )
            # check if destination_id is returned
            if isinstance(return_val, ObjectId):
                kwargs["destination_id"] = ObjectId(destination_id)
            else:
                # return response message
                logger.error(
                    "%s Encountered executing %s in %s.",
                    return_val[0].get("message"),
                    in_function.__qualname__,
                    in_function.__module__,
                )
                return return_val
            return in_function(*args, **kwargs)

        decorator.__wrapped__ = in_function
        return decorator

    return wrapper
