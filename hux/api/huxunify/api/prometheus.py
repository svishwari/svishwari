"""File to manage prometheus utilities and metrics"""
import re
from enum import Enum
from functools import wraps

from flask import Flask, request, Request
from prometheus_client import Gauge
from prometheus_flask_exporter import PrometheusMetrics

from huxunifylib.util.general.logging import logger

prometheus_metrics = PrometheusMetrics.for_app_factory()
health_check_metrics = Gauge(
    name="hux_unified_health_check_metrics",
    documentation="health check metrics",
    registry=prometheus_metrics.registry,
    labelnames=["name"],
)


def monitor_app(flask_app: Flask) -> None:
    """Sets up prometheus monitoring for flask app.

    Args:
        flask_app (Flask): Flask application.
    """

    metrics = PrometheusMetrics(
        app=flask_app,
        defaults_prefix="/api/v1/",
        export_defaults=False,
        excluded_paths=[
            "^/metrics$",
            "^/swagger/.*$",
            "^/apispec.*$",
            "^/api/v1/ui/$",
        ],
    )

    routes = get_routes(flask_app)

    metrics.register_default(
        metrics.counter(
            name="hux_unified_by_path_counter",
            description="Request count by request paths",
            labels={"path": lambda: render_path(request, routes)},
        )
    )

    metrics.register_default(
        metrics.counter(
            name="hux_unified_by_status_counter",
            description="Request count by response codes",
            labels={"status": lambda r: r.status_code},
        )
    )

    metrics.register_default(
        metrics.histogram(
            name="hux_unified_requests_by_status_and_path",
            description="Response time by status code, path, and method",
            labels={
                "status": lambda r: r.status_code,
                "path": lambda: render_path(request, routes),
                "method": lambda: request.method,
            },
            buckets=(
                0.005,
                0.01,
                0.025,
                0.05,
                0.075,
                0.1,
                0.25,
                0.5,
                0.75,
                1.0,
                2.5,
                5.0,
            ),
        )
    )


class Connections(Enum):
    """Connection health enum"""

    STORAGE_SERVICE = "hux_unified_cloud_storage_service_connection_health"
    BATCH_SERVICE = "hux_unified_cloud_batch_service_connection_health"
    SECRET_STORAGE_SERVICE = (
        "hux_unified_cloud_secret_service_connection_health"
    )
    JIRA = "hux_unified_jira_connection_health"
    CDM_API = "hux_unified_cdm_api_connection_health"
    CDM_CONNECTION_SERVICE = (
        "hux_unified_cdm_connection_service_connection_health"
    )
    OKTA = "hux_unified_okta_connection_health"
    DB = "hux_unified_db_connection_health"
    DECISIONING = "hux_unified_decisioning_connection_health"


def record_health_status(connection: Connections) -> object:
    """Purpose of this decorator is for recording the health status
    metrics for the various services

    Example: @record_health_status(ConnectionHealth.CONNECTION_NAME)

    Args:
        connection (Connections): Connection enum.

    Returns:
        wrapper: returns the wrapped decorator function.
    """

    def wrapper(in_function: object) -> object:
        """Decorator for wrapping a function.

        Args:
            in_function (object): function object.

        Returns:
            Response (object): returns a wrapped decorated function object.
        """

        @wraps(in_function)
        def decorator(*args, **kwargs) -> object:
            """Decorator for recording health status metrics.

            Args:
                *args (object): function arguments.
                **kwargs (dict): function keyword arguments.
            Returns:
               Response (object): returns a decorated function object.
            """
            status = in_function(*args, **kwargs)
            if not status[0]:
                logger.error(
                    "Connection to %s is down. Error Message: %s",
                    connection.value,
                    status[1],
                )
            health_check_metrics.labels(name=connection.value).set(status[0])
            return status

        return decorator

    return wrapper


def record_test_result(route: str) -> object:
    """Purpose of this decorator is for recording the health status
    metrics for the various services

    Example: @record_health_status(ConnectionHealth.CONNECTION_NAME)

    Args:
        route (str): the route name.

    Returns:
        wrapper: returns the wrapped decorator function.
    """

    def wrapper(in_function: object) -> object:
        """Decorator for wrapping a function.

        Args:
            in_function (object): function object.

        Returns:
            Response (object): returns a wrapped decorated function object.
        """

        @wraps(in_function)
        def decorator(*args, **kwargs) -> object:
            """Decorator for recording health status metrics.

            Args:
                *args (object): function arguments.
                **kwargs (dict): function keyword arguments.
            Returns:
               Response (object): returns a decorated function object.
            """
            print("Running metric recording function!!!")
            try:
                in_function(*args, **kwargs)
                print("record successful test run")
            except Exception as exc:
                print("record failed test run")
                raise exc

            print("Test passed !!!!")
            # health_check_metrics.labels(name=connection.value).set(status[0])
            # return status

        return decorator

    return wrapper


def get_routes(app: Flask) -> list:
    """Gets the routes and applicable information for metric tracking

    Args:
        app (Flask): Flask application

    Returns:
        list: List of tuples with the following information:
            - url
            - url regex string
            - url methods
    """

    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(
            {
                "url": rule.rule,
                "filter": f"^{re.sub('<(.*?)>', '[a-zA-Z0-9_-]+', rule.rule)}$",
                "methods": rule.methods,
            }
        )

    return routes


def render_path(user_request: Request, routes: list) -> str:
    """Renders the proper path for metrics recording

    Args:
        user_request (Request): Flask Request made by the caller.
        routes (list): List of all the routes in the flask_app.

    Returns:
        str: Path to be recorded for the metrics.
    """

    for route in routes:
        if re.match(route["filter"], user_request.path):
            return route["url"]

    logger.error("Path not found for metrics: %s", user_request.path)
    return user_request.path


if __name__ == "__main__":
    from enum import Enum
    from pydantic import BaseModel

    class Measurements(Enum):
        GET_EMAIL_DELIVERABILITY_OVERVIEW = "/email_deliverability/overview"
        GET_EMAIL_DELIVERABILITY_DOMAINS = "/email_deliverability/domains"

    class Customers(Enum):
        GET_INSIGHTS_COUNTRIES = "/api/v1/customers-insights/countries"
        GET_INSIGHTS_REVENUE = "/api/v1/customers-insights/revenue"
        GET_INSIGHTS_STATES = "/api/v1/customers-insights/states"
        GET_INSIGHTS_CITIES = "/api/v1/customers-insights/cities"
        GET_INSIGHTS_TOTAL = "/api/v1/customers-insights/total"
        GET_INSIGHTS_DEMO = "/api/v1/customers-insights/demo"
        GET_INSIGHTS_GEO = "/api/v1/customers-insights/geo"
        GET_INSIGHTS_OVERVIEW = "/api/v1/customers/overview"
        POST_INSIGHTS_OVERVIEW = "/api/v1/customers/overview"
        GET_IDR_MATCHING_TRENDS = "/api/v1/idr/matching-trends"
        GET_IDR_DATAFEEDS = "/api/v1/idr/datafeeds"
        GET_IDR_OVERVIEW = "/api/v1/idr/overview"
        GET_CUSTOMERS = "/api/v1/customers"
        GET_AUDIENCE_REVENUE = "/api/v1/audiences/<audience_id>/revenue"
        POST_CUSTOMER_EVENTS = "/api/v1/customers/<hux_id>/events"
        GET_AUDIENCE_INSIGHTS = "/api/v1/audiences/<audience_id>/total"
        GET_IDR_DATAFEED_REPORT = "/api/v1/idr/datafeeds/<datafeed_id>"
        GET_CUSTOMER_PROFILE = "/api/v1/customers/<hux_id>"

    class Configuration(Enum):
       GET_ALL_CONFIGURATIONS = "/api/v1/configurations/navigation"
       PUT_NAVIGATION_SETTINGS = "/api/v1/configurations/navigation"
       GET_CONFIGURATION_MODULES = "/api/v1/configurations/modules"

    class Notifications(Enum):
       STREAM_NOTIFICATIONS = "/api/v1/notifications/stream"
       GET_DISTINCT_USERS = "/api/v1/notifications/users"
       POST_NOTIFICATIONS = "/api/v1/notifications"
       GET_ALL_NOTIFICATIONS = "/api/v1/notifications"
       GET_NOTIFICATION = "/api/v1/notifications/<notification_id>"
       DELETE_NOTIFICATION = "/api/v1/notifications/<notification_id>"

    class Destinations(Enum):
       GET_DESTINATION_CONSTANTS = "/api/v1/destinations/constants"
       POST_VALIDATE_DESTINATION = "/api/v1/destinations/validate"
       POST_REQUEST_DESTINATION = "/api/v1/destinations/request"
       GET_ALL_NOTIFICATIONS = "/api/v1/destinations"
       GET_DESTINATION_DATA_EXTENSIONS = "/api/v1/destinations/<destination_id>/data-extensions"
       POST_DESTINATION_DATA_EXTENSIONS = "/api/v1/destinations/<destination_id>/data-extensions"
       PUT_DESTINATION_DATA_EXTENSIONS = "/api/v1/destinations/<destination_id>/authentication"
       GET_DESTINATION = "/api/v1/destinations/<destination_id>"
       PATCH_DESTINATION = "/api/v1/destinations/<destination_id>"
       DELETE_DESTINATION = "/api/v1/destinations/<destination_id>"

    class Orchestration(Enum):
       POST_UPLOAD_AUDIENCE = "/api/v1/audiences/upload"
       GET_AUDIENCE_RULES = "/api/v1/audiences/rules"
       POST_CREATE_LOOKALIKE_AUDIENCE = "/api/v1/lookalike-audiences"
       GET_ALL_AUDIENCES = "/api/v1/audiences"
       POST_CREATE_AUDIENCES = "/api/v1/audiences"
       GET_HISTOGRAM_DATA = "/api/v1/audiences/rules/<field_type>/histogram"
       GET_LOCATION_RULES_CONTSTANTS = "/api/v1/audiences/rules/<field_type>/<key>"
       GET_AUDIENCE_INSIGHTS = "/api/v1/audiences/<audience_id>/audience_insights"
       POST_ADD_DESTINATION_TO_AUDIENCE = "/api/v1/audiences/<audience_id>/destinations"
       DELETE_REMOVE_DESTINATION_FROM_AUDIENCE = "/api/v1/audiences/<audience_id>/destinations"
       GET_AUDIENCE_INSIGHTS_COUNTRIES = "/api/v1/audiences/<audience_id>/countries"
       GET_DOWNLOAD_AUDIENCE = "/api/v1/audiences/<audience_id>/download"
       GET_AUDIENCE_INSIGHTS_STATES = "/api/v1/audiences/<audience_id>/states"
       GET_AUDIENCE_INSIGHTS_CITIES = "/api/v1/audiences/<audience_id>/cities"
       PUT_UPDATE_LOOKALIKE_AUDIENCE = "/api/v1/lookalike-audiences/<audience_id>"
       GET_AUDIENCE = "/api/v1/audiences/<audience_id>"
       PUT_UPDATE_AUDIENCE = "/api/v1/audiences/<audience_id>"
       DELETE_AUDIENCE = "/api/v1/audiences/<audience_id>"

    class TrustID(Enum):
       GET_SEGMENT_FILTERS = "/api/v1/trust_id/user_filters"
       GET_ATTRIBUTES = "/api/v1/trust_id/attributes"
       GET_COMPARISON_DATA = "/api/v1/trust_id/comparison"
       GET_OVERIVEW = "/api/v1/trust_id/overview"
       POST_ADD_SEGMENT = "/api/v1/trust_id/segment"
       DELETE_SEGMENT = "/api/v1/trust_id/segment"

    class User(Enum):
       GET_SEEN_NOTIFICATIONS = "/api/v1/users/seen_notifications"
       POST_REQUEST_NEW_USER = "/api/v1/users/request_new_user"
       GET_REQUESTED_USERS = "/api/v1/users/requested_users"
       PUT_UPDATE_USER_PREFERENCES = "/api/v1/users/preferences"
       GET_RBAC_MATRIX = "/api/v1/users/rbac_matrix"
       POST_CREATE_JIRA_TICKET = "/api/v1/users/contact-us"
       GET_USER_PROFILE = "/api/v1/users/profile"
       GET_JIRA_TICKETS = "/api/v1/users/tickets"
       GET_ALL_USERS = "/api/v1/users"
       PATCH_UPDATE_USER = "/api/v1/users"
       POST_CREATE_USER_FAVORITE = "/api/v1/users/<component_name>/<component_id>/favorite"
       DELETE_USER_FAVORITE = "/api/v1/users/<component_name>/<component_id>/favorite"
       DELETE_USER = "/api/v1/users/<user_id>"

    class ClientProjects(Enum):
       GET_ALL_CLIENT_PROJECTS = "/api/v1/client-projects"
       PATCH_UPDATE_CLIENT_PROJECT = "/api/v1/client-projects/<client_project_id>"

    class DataSources(Enum):
       GET_DATA_SOURCES = "/api/v1/data-sources"
       POST_CREATE_DATA_SOURCE = "/api/v1/data-sources"
       DELETE_DATA_SOURCE = "/api/v1/data-sources"
       PATCH_UPDATE_DATA_SOURCES = "/api/v1/data-sources"
       GET_DATA_SOURCE_DATAFEED = "/api/v1/data-sources/<datasource_type>/datafeeds/<datafeed_name>"
       GET_DATA_SOURCE_DATAFEEDS = "/api/v1/data-sources/<datasource_type>/datafeeds"
       GET_DATA_SOURCE = "/api/v1/data-sources/<data_source_id>"

    class Applications(Enum):
       GET_ALL_APPLICATIONS = "/api/v1/applications"
       POST_CREATE_APPLICATION = "/api/v1/applications"
       PATCH_UPDATE_APPLICATION = "/api/v1/applications/<application_id>"

    class Engagements(Enum):
       GET_ALL_ENGAGEMENTS = "/api/v1/engagements"
       POST_CREATE_ENGAGEMENT = "/api/v1/engagements"
       GET_AD_PERFORMANCE_METRICS = "/api/v1/engagements/<engagement_id>/audience-performance/display-ads"
       GET_DOWNLOAD_EMAIL_PERFORMANCE_METRICS = "/api/v1/engagements/<engagement_id>/audience-performance/download"
       GET_EMAIL_PERFORMANCE_METRICS = "/api/v1/engagements/<engagement_id>/audience-performance/email"
       POST_ADD_DESTINATION_ENGAGEMENT_AUDIENCE = "/api/v1/engagements/<engagement_id>/audience/<audience_id>/destinations"
       DELETE_DESTINATION_ENGAGEMENT_AUDIENCE = "/api/v1/engagements/<engagement_id>/audience/<audience_id>/destinations"
       POST_ADD_AUDIENCE_TO_ENGAGEMENT = "/api/v1/engagements/<engagement_id>/audiences"
       DELETE_AUDIENCE_FROM_ENGAGEMENT = "/api/v1/engagements/<engagement_id>/audiences"
       GET_ENGAGEMENT = "/api/v1/engagements/<engagement_id>"
       PUT_UPDATE_ENGAGEMENT = "/api/v1/engagements/<engagement_id>"
       DELETE_ENGAGEMENT = "/api/v1/engagements/<engagement_id>"

    class Model(Enum):
       GET_ALL_MODELS = "/api/v1/models"
       POST_REQUEST_MODEL = "/api/v1/models"
       DELETE_REQUESTED_MODEL = "/api/v1/models"
       GET_MODEL_PIPELINE_PERFORMANCE = "/api/v1/models/<model_id>/pipeline-performance"
       GET_MODEL_VERSION_HISTORY = "/api/v1/models/<model_id>/version-history"
       GET_MODEL_OVERVIEW = "/api/v1/models/<model_id>/overview"
       GET_MODEL_FEATURES = "/api/v1/models/<model_id>/features"
       GET_MODEL_DRIFT = "/api/v1/models/<model_id>/drift"
       GET_MODEL_LIFT = "/api/v1/models/<model_id>/lift"

    class Campaign(Enum):
       GET_CAMPAIGN_MAPPINGS = "/api/v1/engagements/<engagement_id>/audience/<audience_id>/destination/<destination_id>/campaign-mappings"
       PUT_UPDATE_CAMPAIGN_MAPPINGS = "/api/v1/engagements/<engagement_id>/audience/<audience_id>/destination/<destination_id>/campaigns"
       GET_CAMPAIGNS = "/api/v1/engagements/<engagement_id>/audience/<audience_id>/destination/<destination_id>/campaigns"

    class Delivery(Enum):
       POST_SET_DELIVERY_SCHEDULE_DESTINATION_ENGAGED_AUDIENCE = "/api/v1/engagements/<engagement_id>/audience/<audience_id>/destination/<destination_id>/schedule"
       DELETE_DELIVERY_SCHEDULE_DESTINATION_ENGAGED_AUDIENCE = "/api/v1/engagements/<engagement_id>/audience/<audience_id>/destination/<destination_id>/schedule"
       POST_DELIVER_ENGAGED_AUDIENCE_TO_DESTINATION = "/api/v1/engagements/<engagement_id>/audience/<audience_id>/destination/<destination_id>/deliver"
       POST_SET_DELIVERY_SCHEDULE_ENGAGED_AUDIENCE = "/api/v1/engagements/<engagement_id>/audience/<audience_id>/schedule"
       POST_DELIVER_ENGAGED_AUDIENCE = "/api/v1/engagements/<engagement_id>/audience/<audience_id>/deliver"
       GET_ENGAGEMENT_DELIVERY_HISTORY = "/api/v1/engagements/<engagement_id>/delivery-history"
       POST_DELIVER_ALL_ENGAGED_AUDIENCES = "/api/v1/engagements/<engagement_id>/deliver"
       GET_AUDIENCE_DELIVERY_HISTORY = "/api/v1/audiences/<audience_id>/delivery-history"
       POST_DELIVER_AUDIENCE = "/api/v1/audiences/<audience_id>/deliver"


    class Endpoints:
        MEASUREMENTS = Measurements
        CUSTOMERS = Customers
        CONFIGURATION = Configuration
        NOTIFICATIONS = Notifications
        DESTINATIONS = Destinations
        ORCHESTRATION = Orchestration
        TRUST_ID = TrustID
        USER = User
        CLIENT_PROJECTS = ClientProjects
        DATA_SOURCES = DataSources
        APPLICATIONS = Applications
        ENGAGEMENTS = Engagements
        MODEL = Model
        CAMPAIGN = Campaign
        DELIVERY = Delivery


    # print(type(EP.mes.GET_EMAIL_DELIVERABILITY_OVERVIEW))
    print(Endpoints.MEASUREMENTS.GET_EMAIL_DELIVERABILITY_OVERVIEW.value)