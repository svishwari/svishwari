"""
Paths for metrics API
"""
from http import HTTPStatus

from flasgger import SwaggerView
from flask import Blueprint, Response

from huxunify.api.route.utils import (
    secured,
    add_view_to_blueprint,
    PrometheusHelper,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE

metrics_bp = Blueprint("/metrics", import_name=__name__)


@metrics_bp.before_request
@secured()
def before_request():
    """Protect all of the metrics endpoints."""
    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(metrics_bp, "metrics", "MetricsView")
class MetricsView(SwaggerView):
    """
    Metrics View Class
    """

    parameters = []

    responses = {
        HTTPStatus.OK.value: {
            "description": "Returns plain text of prometheus metrics"
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to return plain text of prometheus metrics"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = ["metrics"]

    def get(self) -> Response:
        """Retrieves plain text metrics for prometheus consumption

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Response: Flask Response Object with the generated prometheus metrics

        """

        prometheus_helper = PrometheusHelper.instance()
        metrics = prometheus_helper.generate_metrics()

        return Response(metrics, mimetype="text/plain")
