"""Prometheus Helper module to house functions that manage sending metrics to Prometheus server"""

from flask import request
from prometheus_client import (
    CollectorRegistry,
    Gauge,
    Counter,
    push_to_gateway
)
import time


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    response_time = time.time() - request.start_time
    return response


def record_request_data(response):
    return response


def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(record_request_data)
    app.after_request(stop_timer)
