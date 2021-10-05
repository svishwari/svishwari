"""Locust file."""

from os import getenv
from dotenv import load_dotenv
from locust import HttpUser, task, between
from locust.log import setup_logging
from huxunifylib.util.general.logging import logger
from get_okta_token import OktaOIDC

load_dotenv()
setup_logging("INFO", None)


# ENV VARS
OKTA_PARAM_DICT = {
    "org_url": getenv("OKTA_ISSUER"),
    "user": getenv("OKTA_TEST_USER_NAME"),
    "pw": getenv("OKTA_TEST_USER_PW"),
    "client_id": getenv("OKTA_CLIENT_ID"),
    "scopes": "openid+profile+email",
    "redirect_uri": getenv("OKTA_REDIRECT_URI"),
}
ACCESS_TOKEN = "ACCESS_TOKEN"


class APIUser(HttpUser):
    """Load test User class."""

    # How long a simulated user should wait between executing tasks
    wait_time = between(1, 3)
    host = "https://unified-ui-dev.main.use1.hux-unified-dev1.in/api/v1"

    # A User will call its on_start method when it starts running
    def on_start(self):
        logger.info("Starting load tests")
        self.host = "https://unified-ui-dev.main.use1.hux-unified-dev1.in/api/v1"
        okta_oidc = OktaOIDC(**OKTA_PARAM_DICT)
        # set the token for pytest usage.
        access_token = okta_oidc.get_access_token(False)
        # pylint: disable=attribute-defined-outside-init
        self.headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

    # When the instance of this user stops, the initialized test data is deleted.
    def on_stop(self):
        logger.info("Stopping load tests")

    # When a load test is started, an instance of a User
    # class will be created for each simulated user.
    # Each user will start running within their own green thread.
    # When these users run they pick tasks that they execute,
    # sleep for a while, and then pick a new task and so on.
    @task
    def get_audiences(self):
        """Load test method for GET all audiences."""

        with self.client.get(
            f"{self.host}/audiences", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure("Got wrong response")
            elif response.elapsed.total_seconds() > 0.0001:
                response.failure("Audience GET all request took too long")

    @task
    def get_destinations(self):
        """Load test method for GET all destinations."""
        with self.client.get(
            f"{self.host}/destinations", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure("Got wrong response")
            elif response.elapsed.total_seconds() > 0.0001:
                response.failure("Destinations GET all request took too long")
