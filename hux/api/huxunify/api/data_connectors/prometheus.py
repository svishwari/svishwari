import time
import prometheus_client
from prometheus_client import CollectorRegistry, Histogram
from flask import request, Response, Flask

# pylint: disable=attribute-defined-outside-init
class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError("Singletons must be accessed through `instance()`.")

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

# pylint: disable=no-self-use, assigning-non-slot
@Singleton
class PrometheusClient:
    """
    Prometheus Helper class to manage the recorded metrics
    and generate metric reports for consumption
    """

    def __init__(self):
        """Initialize Prometheus Helper variables"""

        self.app = None
        self.prometheus_registry = None

        # instantiate metrics
        self.metrics = {}
        self.latency = None

    def set_app(self, app: Flask) -> None:
        """Populate Prometheus Helper variables"""

        self.app = app
        self.setup_metrics(app)

        self.prometheus_registry = CollectorRegistry()

        # create metrics
        self.latency = Histogram(
            name="hux_api_request_duration",
            documentation="Elapsed time for API request execution.",
            registry=self.prometheus_registry,
        )

        self.metrics["latency"] = self.latency

    def setup_metrics(self, app: Flask) -> None:
        """Setup methods that should run before and after requests"""

        app.before_request(self._start_timer)
        app.after_request(self._stop_timer)

    def _start_timer(self) -> None:
        """Start a timer to record latency for requests"""
        request.start_time = time.time()

    def _stop_timer(self, response: Response) -> Response:
        """
        Stop a timer to record latency for requests

        Returns:
            Response: Flask Response object
        """
        response_time = time.time() - request.start_time
        # may want to exclude a time recording for metrics requests. Could throw off average times.
        self.latency.observe(response_time)
        return response

    def generate_metrics(self) -> list:
        """Generates prometheus metrics for consumption

        Returns:
            list: List of prometheus metrics
        """
        return [
            prometheus_client.generate_latest(x) for x in self.metrics.values()
        ]
