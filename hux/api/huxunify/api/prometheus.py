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


def record_health_status_metric(
    connection_name: str, connection_health: int
) -> None:
    """Updates connection health metric for a connection.

    Args:
        connection_name (str): name of the connection metric.
        connection_health (int): value for the health of the connection metric.
    """

    health_check_metrics.labels(name=connection_name).set(connection_health)


class Connections(Enum):
    STORAGE_SERVICE = "cloud_storage_service_connection_health"
    BATCH_SERVICE = "cloud_batch_service_connection_health"
    SECRET_STORAGE_SERVICE = "cloud_secret_service_connection_health"
    JIRA = "jira_connection_health"
    CDM_API = "cdm_api_connection_health"
    CDM_CONNECTION_SERVICE = "cdm_connection_service_connection_health"
    OKTA = "okta_connection_health"
    DB = "hux_unified_db_connection_health"
    TECTON = "tecton_connection_health"


def record_health_status(connection: Connections):
    """Purpose of this decorator is for recording the health status
    metrics for the various services

    Example: @record_health_status(ConnectionHealth.CONNECTION_NAME)

    Args:
        connection (Connections): Connection enum.
    """

    def wrapper(in_function) -> object:
        """Decorator for wrapping a function.

        Args:
            in_function: function object.

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
            health_check_metrics.labels(name=connection.value).set(status[0])
            return status

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
                "filter": f"^{re.sub('<(.*?)>', '[a-zA-Z0-9_]+', rule.rule)}$",
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
