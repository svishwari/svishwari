"""File to manage prometheus utilities and metrics"""
from flask import Flask, request
from prometheus_client import Gauge
from prometheus_flask_exporter import PrometheusMetrics

metrics_reference = PrometheusMetrics.for_app_factory()
health_check_metrics = Gauge(
    name="health_check_metrics",
    documentation="health check metrics",
    registry=metrics_reference.registry,
    labelnames=["name"],
)


def monitor_app(flask_app: Flask) -> None:
    """sets up prometheus monitoring for flask app

    Args:
        flask_app (Flask): Flask application.

    Returns:
        None

    """

    metrics = PrometheusMetrics(
        app=flask_app, defaults_prefix="/api/v1", export_defaults=False
    )

    metrics.register_default(
        metrics.counter(
            name="by_path_counter",
            description="Request count by request paths",
            labels={"path": lambda: request.path},
        )
    )

    metrics.register_default(
        metrics.histogram(
            name="requests_by_status_and_path",
            description="Response time by status and path",
            labels={
                "status": lambda r: r.status_code,
                "path": lambda: request.path,
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
    """Updates connection health metric for a connection

    Args:
        connection_name (str): name of the connection metric.
        connection_health (int): value for the health of the connection metric.

    Returns:

    """

    health_check_metrics.labels(name=connection_name).set(connection_health)
