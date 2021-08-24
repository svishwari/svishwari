"""Prometheus Helper module to house functions that manage sending metrics to Prometheus server"""

from flask import request, g, Response, current_app, Flask
from prometheus_client import (
    CollectorRegistry,
    Gauge,
    Counter,
    Histogram,
    push_to_gateway
)
import time


class PrometheusHelper:

    def __init__(self, app: Flask):
        self.setup_metrics(app)

        self.prometheus_registry = CollectorRegistry()

        self.endpoint_durations = Histogram(
            name="hux_api_request_duration",
            documentation="Elapsed time for API request execution.",
            labelnames=["method", "path", "status"],
            registry=self.prometheus_registry
        )

        self.test_metric = Counter(
            name="hux_api_jim_test_metric",
            documentation="Metric used to test connection to Prometheus Server",
            registry=self.prometheus_registry
        )

        self.test_metric.inc(77)

    def setup_metrics(self, app: Flask):
        app.before_request(self._before_request)
        app.after_request(self.record_request_data)
        app.after_request(self._after_request)

    def push_to_gateway(self):
        push_to_gateway(
            "https://prometheus.i.hux-unified-dev1.in/",
            job="hux_api_monitoring",
            registry=self.prometheus_registry
        )

    def _before_request(self):
        g.start = time.time()

    def _after_request(self, response: Response) -> Response:

        try:
            elapsed_time = time.time() - g.start
        except Exception as error:
            pass

        return response

    def record_request_data(self, response):
        return response
