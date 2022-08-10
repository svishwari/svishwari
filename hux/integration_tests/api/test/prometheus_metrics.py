# pylint: disable=line-too-long
"""This file contains the functionality to record metrics for the end to end tests"""
from functools import wraps
from enum import Enum
from os import getenv

from prometheus_client import Counter, CollectorRegistry, push_to_gateway

registry = CollectorRegistry()
test_metrics = Counter(
    "hux_unified_test_metrics",
    "Hux API end to end test metrics counter",
    labelnames=["method", "route", "result"],
    registry=registry,
)


class Measurements(Enum):
    """Measurements route enum class"""

    GET_EMAIL_DELIVERABILITY_OVERVIEW = "/email_deliverability/overview"
    GET_EMAIL_DELIVERABILITY_DOMAINS = "/email_deliverability/domains"


class Customers(Enum):
    """Customers route enum class"""

    GET_INSIGHTS_COUNTRIES = "/customers-insights/countries"
    GET_INSIGHTS_REVENUE = "/customers-insights/revenue"
    GET_INSIGHTS_STATES = "/customers-insights/states"
    GET_INSIGHTS_CITIES = "/customers-insights/cities"
    GET_INSIGHTS_TOTAL = "/customers-insights/total"
    GET_INSIGHTS_DEMO = "/customers-insights/demo"
    GET_INSIGHTS_GEO = "/customers-insights/geo"
    GET_INSIGHTS_OVERVIEW = "/customers/overview"
    POST_INSIGHTS_OVERVIEW = "/customers/overview"
    GET_IDR_MATCHING_TRENDS = "/idr/matching-trends"
    GET_IDR_DATAFEEDS = "/idr/datafeeds"
    GET_IDR_OVERVIEW = "/idr/overview"
    GET_CUSTOMERS = "/customers"
    GET_AUDIENCE_REVENUE = "/audiences/<audience_id>/revenue"
    POST_CUSTOMER_EVENTS = "/customers/<hux_id>/events"
    GET_AUDIENCE_INSIGHTS = "/audiences/<audience_id>/total"
    GET_IDR_DATAFEED_REPORT = "/idr/datafeeds/<datafeed_id>"
    GET_CUSTOMER_PROFILE = "/customers/<hux_id>"


class Configuration(Enum):
    """Configurations route enum class"""

    GET_ALL_CONFIGURATIONS = "/configurations/navigation"
    PUT_NAVIGATION_SETTINGS = "/configurations/navigation"
    GET_CONFIGURATION_MODULES = "/configurations/modules"


class Notifications(Enum):
    """Notifications route enum class"""

    STREAM_NOTIFICATIONS = "/notifications/stream"
    GET_DISTINCT_USERS = "/notifications/users"
    POST_CREATE_NOTIFICATION = "/notifications"
    GET_ALL_NOTIFICATIONS = "/notifications"
    GET_NOTIFICATION = "/notifications/<notification_id>"
    DELETE_NOTIFICATION = "/notifications/<notification_id>"


class Destinations(Enum):
    """Destinations route enum class"""

    GET_DESTINATION_CONSTANTS = "/destinations/constants"
    POST_VALIDATE_DESTINATION = "/destinations/validate"
    POST_REQUEST_DESTINATION = "/destinations/request"
    GET_ALL_DESTINATIONS = "/destinations"
    GET_DESTINATION_DATA_EXTENSIONS = (
        "/destinations/<destination_id>/data-extensions"
    )
    POST_DESTINATION_DATA_EXTENSIONS = (
        "/destinations/<destination_id>/data-extensions"
    )
    PUT_DESTINATION_DATA_EXTENSIONS = (
        "/destinations/<destination_id>/authentication"
    )
    GET_DESTINATION = "/destinations/<destination_id>"
    PATCH_UPDATE_DESTINATION = "/destinations/<destination_id>"
    DELETE_DESTINATION = "/destinations/<destination_id>"


class Orchestration(Enum):
    """Orchestration route enum class"""

    POST_UPLOAD_AUDIENCE = "/audiences/upload"
    GET_AUDIENCE_RULES = "/audiences/rules"
    POST_CREATE_LOOKALIKE_AUDIENCE = "/lookalike-audiences"
    GET_ALL_AUDIENCES = "/audiences"
    POST_CREATE_AUDIENCE = "/audiences"
    GET_HISTOGRAM_DATA = "/audiences/rules/<field_type>/histogram"
    GET_LOCATION_RULES_CONTSTANTS = "/audiences/rules/<field_type>/<key>"
    GET_AUDIENCE_INSIGHTS = "/audiences/<audience_id>/audience_insights"
    POST_ADD_DESTINATION_TO_AUDIENCE = "/audiences/<audience_id>/destinations"
    DELETE_DESTINATION_FROM_AUDIENCE = "/audiences/<audience_id>/destinations"
    GET_AUDIENCE_INSIGHTS_COUNTRIES = "/audiences/<audience_id>/countries"
    GET_DOWNLOAD_AUDIENCE = "/audiences/<audience_id>/download"
    GET_AUDIENCE_INSIGHTS_STATES = "/audiences/<audience_id>/states"
    GET_AUDIENCE_INSIGHTS_CITIES = "/audiences/<audience_id>/cities"
    PUT_UPDATE_LOOKALIKE_AUDIENCE = "/lookalike-audiences/<audience_id>"
    GET_AUDIENCE = "/audiences/<audience_id>"
    PUT_UPDATE_AUDIENCE = "/audiences/<audience_id>"
    DELETE_AUDIENCE = "/audiences/<audience_id>"


class TrustID(Enum):
    """Trust ID route enum class"""

    GET_SEGMENT_FILTERS = "/trust_id/user_filters"
    GET_ATTRIBUTES = "/trust_id/attributes"
    GET_COMPARISON_DATA = "/trust_id/comparison"
    GET_OVERIVEW = "/trust_id/overview"
    POST_ADD_SEGMENT = "/trust_id/segment"
    DELETE_SEGMENT = "/trust_id/segment"


class User(Enum):
    """User route enum class"""

    GET_SEEN_NOTIFICATIONS = "/users/seen_notifications"
    POST_REQUEST_NEW_USER = "/users/request_new_user"
    GET_REQUESTED_USERS = "/users/requested_users"
    PUT_UPDATE_USER_PREFERENCES = "/users/preferences"
    GET_RBAC_MATRIX = "/users/rbac_matrix"
    POST_CREATE_JIRA_TICKET = "/users/contact-us"
    GET_USER_PROFILE = "/users/profile"
    GET_JIRA_TICKETS = "/users/tickets"
    GET_ALL_USERS = "/users"
    PATCH_UPDATE_USER = "/users"
    POST_CREATE_USER_FAVORITE = (
        "/users/<component_name>/<component_id>/favorite"
    )
    DELETE_USER_FAVORITE = "/users/<component_name>/<component_id>/favorite"
    DELETE_USER = "/users/<user_id>"


class ClientProjects(Enum):
    """Client Projects route enum class"""

    GET_ALL_CLIENT_PROJECTS = "/client-projects"
    PATCH_UPDATE_CLIENT_PROJECT = "/client-projects/<client_project_id>"


class DataSources(Enum):
    """Data Sources route enum class"""

    GET_DATA_SOURCES = "/data-sources"
    POST_CREATE_DATA_SOURCE = "/data-sources"
    DELETE_DATA_SOURCE = "/data-sources"
    PATCH_UPDATE_DATA_SOURCES = "/data-sources"
    GET_DATA_SOURCE_DATAFEED = (
        "/data-sources/<datasource_type>/datafeeds/<datafeed_name>"
    )
    GET_DATA_SOURCE_DATAFEEDS = "/data-sources/<datasource_type>/datafeeds"
    GET_DATA_SOURCE = "/data-sources/<data_source_id>"


class Applications(Enum):
    """Applications route enum class"""

    GET_ALL_APPLICATIONS = "/applications"
    POST_CREATE_APPLICATION = "/applications"
    PATCH_UPDATE_APPLICATION = "/applications/<application_id>"


class Engagements(Enum):
    """Engagements route enum class"""

    GET_ALL_ENGAGEMENTS = "/engagements"
    POST_CREATE_ENGAGEMENT = "/engagements"
    GET_AD_PERFORMANCE_METRICS = (
        "/engagements/<engagement_id>/audience-performance/display-ads"
    )
    GET_DOWNLOAD_EMAIL_PERFORMANCE_METRICS = (
        "/engagements/<engagement_id>/audience-performance/download"
    )
    GET_EMAIL_PERFORMANCE_METRICS = (
        "/engagements/<engagement_id>/audience-performance/email"
    )
    POST_ADD_DESTINATION_ENGAGEMENT_AUDIENCE = (
        "/engagements/<engagement_id>/audience/<audience_id>/destinations"
    )
    DELETE_DESTINATION_ENGAGEMENT_AUDIENCE = (
        "/engagements/<engagement_id>/audience/<audience_id>/destinations"
    )
    POST_ADD_AUDIENCE_TO_ENGAGEMENT = "/engagements/<engagement_id>/audiences"
    DELETE_AUDIENCE_FROM_ENGAGEMENT = "/engagements/<engagement_id>/audiences"
    GET_ENGAGEMENT = "/engagements/<engagement_id>"
    PUT_UPDATE_ENGAGEMENT = "/engagements/<engagement_id>"
    DELETE_ENGAGEMENT = "/engagements/<engagement_id>"


class Model(Enum):
    """Model route enum class"""

    GET_ALL_MODELS = "/models"
    POST_REQUEST_MODEL = "/models"
    DELETE_REQUESTED_MODEL = "/models"
    GET_MODEL_PIPELINE_PERFORMANCE = "/models/<model_id>/pipeline-performance"
    GET_MODEL_VERSION_HISTORY = "/models/<model_id>/version-history"
    GET_MODEL_OVERVIEW = "/models/<model_id>/overview"
    GET_MODEL_FEATURES = "/models/<model_id>/features"
    GET_MODEL_DRIFT = "/models/<model_id>/drift"
    GET_MODEL_LIFT = "/models/<model_id>/lift"


class Campaign(Enum):
    """Campaign route enum class"""

    GET_CAMPAIGN_MAPPINGS = "/engagements/<engagement_id>/audience/<audience_id>/destination/<destination_id>/campaign-mappings"
    PUT_UPDATE_CAMPAIGN_MAPPINGS = "/engagements/<engagement_id>/audience/<audience_id>/destination/<destination_id>/campaigns"
    GET_CAMPAIGNS = "/engagements/<engagement_id>/audience/<audience_id>/destination/<destination_id>/campaigns"


class Delivery(Enum):
    """Delivery route enum class"""

    POST_SET_DELIVERY_SCHEDULE_DESTINATION_ENGAGED_AUDIENCE = "/engagements/<engagement_id>/audience/<audience_id>/destination/<destination_id>/schedule"
    DELETE_DELIVERY_SCHEDULE_DESTINATION_ENGAGED_AUDIENCE = "/engagements/<engagement_id>/audience/<audience_id>/destination/<destination_id>/schedule"
    POST_DELIVER_ENGAGED_AUDIENCE_TO_DESTINATION = "/engagements/<engagement_id>/audience/<audience_id>/destination/<destination_id>/deliver"
    POST_SET_DELIVERY_SCHEDULE_ENGAGED_AUDIENCE = (
        "/engagements/<engagement_id>/audience/<audience_id>/schedule"
    )
    POST_DELIVER_ENGAGED_AUDIENCE = (
        "/engagements/<engagement_id>/audience/<audience_id>/deliver"
    )
    GET_ENGAGEMENT_DELIVERY_HISTORY = (
        "/engagements/<engagement_id>/delivery-history"
    )
    POST_DELIVER_ALL_ENGAGED_AUDIENCES = "/engagements/<engagement_id>/deliver"
    GET_AUDIENCE_DELIVERY_HISTORY = "/audiences/<audience_id>/delivery-history"
    POST_DELIVER_AUDIENCE = "/audiences/<audience_id>/deliver"


class CoreApp(Enum):
    """Core App route enum class"""

    GET_HEALTH_CHECK = "/health-check"
    GET_API_SPEC = "/apispec_1.json"
    GET_SWAGGER_DOCS = "/ui"
    GET_METRICS = "/metrics"


class Endpoints:
    """Endpoints enum class"""

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
    CORE_APP = CoreApp


class HttpMethod(Enum):
    """HttpMethod Enum"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


def record_test_result(method: HttpMethod, route: Enum) -> object:
    """Purpose of this decorator is for recording the health status
    metrics for the various services

    Example: @record_health_status(ConnectionHealth.CONNECTION_NAME)

    Args:
        method (str): method of the being tested.
        route (str): route being tested.

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
            try:
                in_function(*args, **kwargs)
                test_metrics.labels(
                    method=method.value, route=route.value, result="PASS"
                ).inc()
            except Exception as exc:
                test_metrics.labels(
                    method=method.value, route=route.value, result="FAIL"
                ).inc()
                raise exc

        return decorator

    return wrapper


def push_test_metrics():
    """Pushes test metrics to prometheus push gateway.

    Returns:

    """
    push_to_gateway(
        gateway=getenv("PROMETHEUS_PUSHGATEWAY_URL"),
        job="my_job",
        registry=registry,
    )
