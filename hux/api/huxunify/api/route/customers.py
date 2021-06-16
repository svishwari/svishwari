# pylint: disable=no-self-use
"""
Paths for customer API
"""

from http import HTTPStatus
from typing import Tuple
import datetime
from random import randint, uniform
from faker import Faker

from flask import Blueprint
from flask_apispec import marshal_with
from flasgger import SwaggerView

from huxunify.api.schema.customers import (
    CustomerProfileSchema,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import (
    secured,
    add_view_to_blueprint,
    handle_api_exception,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api.schema.customers import (
    CustomerOverviewSchema,
    CustomersSchema,
)
from huxunify.api import constants as api_c

customers_bp = Blueprint(
    api_c.CUSTOMERS_ENDPOINT, import_name=__name__, url_prefix="/cdp"
)

faker = Faker()


@customers_bp.before_request
@secured()
def before_request():
    """Protect all of the customer endpoints."""
    pass  # pylint: disable=unnecessary-pass


def get_customers_overview() -> dict:
    """Fetch customers overview data.

    Args: None

    Returns: dict of overview data

    """
    customers_overview_data = {
        api_c.TOTAL_RECORDS: randint(10000000, 99999999),
        api_c.MATCH_RATE: round(uniform(0, 1), 5),
        api_c.TOTAL_UNIQUE_IDS: randint(10000000, 99999999),
        api_c.TOTAL_UNKNOWN_IDS: randint(10000000, 99999999),
        api_c.TOTAL_KNOWN_IDS: randint(10000000, 99999999),
        api_c.TOTAL_INDIVIDUAL_IDS: randint(10000000, 99999999),
        api_c.TOTAL_HOUSEHOLD_IDS: randint(10000000, 99999999),
        api_c.UPDATED: datetime.datetime.now(),
        api_c.TOTAL_CUSTOMERS: randint(10000000, 99999999),
        api_c.COUNTRIES: randint(1, 3),
        api_c.STATES: randint(1, 51),
        api_c.CITIES: randint(5, 50),
        api_c.MIN_AGE: randint(1, 10),
        api_c.MAX_AGE: randint(11, 100),
        api_c.GENDER_WOMEN: round(uniform(0, 1), 5),
        api_c.GENDER_MEN: round(uniform(0, 1), 5),
        api_c.GENDER_OTHER: round(uniform(0, 1), 5),
        api_c.MIN_LTV_PREDICTED: round(uniform(1, 100), 4),
        api_c.MAX_LTV_PREDICTED: round(uniform(1, 100), 4),
        api_c.MIN_LTV_ACTUAL: round(uniform(1, 100), 4),
        api_c.MAX_LTV_ACTUAL: round(uniform(1, 100), 4),
    }
    return customers_overview_data


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.CUSTOMERS_ENDPOINT}/{api_c.OVERVIEW}",
    "CustomerOverviewSchema",
)
class CustomerOverview(SwaggerView):
    """
    Customers Overview class
    """

    responses = {
        HTTPStatus.OK.value: {
            "description": "Customer Profiles Overview",
            "schema": {
                "type": "array",
                "items": CustomerOverviewSchema,
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get customers overview"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    def get(self) -> Tuple[dict, int]:
        """Retrieves a customer data overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] dict of Customer data overview and http code
        """

        customers_overview_data = get_customers_overview()

        return (
            CustomerOverviewSchema().dump(customers_overview_data),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.CUSTOMERS_ENDPOINT}/{api_c.OVERVIEW}",
    "CustomerOverviewPostSchema",
)
class CustomerPostOverview(SwaggerView):
    """
    Customers Post Overview class
    """

    parameters = [
        {
            "name": "body",
            "description": "Audience Filters",
            "type": "object",
            "in": "body",
            "example": {
                "filters": {
                    "section_aggregator": "ALL",
                    "section_filters": [
                        {"field": "country", "type": "equals", "value": "us"}
                    ],
                }
            },
        }
    ]
    responses = {
        HTTPStatus.CREATED.value: {
            "description": "Customer Profiles Overview",
            "schema": {
                "type": "array",
                "items": CustomerOverviewSchema,
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get customers overview"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    def post(self) -> Tuple[dict, int]:
        """Retrieves a customer data overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:


        Returns:
            Tuple[dict, int] dict of Customer data overview and http code
        """
        # TODO: Integrate with CDM API /customer-profiles/insights once its ready

        return (
            CustomerOverviewSchema().dump(get_customers_overview()),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.IDR_ENDPOINT}/{api_c.OVERVIEW}",
    "CustomerDashboardOverview",
)
class CustomerDashboardOverview(SwaggerView):
    """
    Customers Dashboard Overview class
    """

    responses = {
        HTTPStatus.OK.value: {
            "schema": CustomerOverviewSchema,
            "description": "Customer Identity Resolution Dashboard overview.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get customers identity dashboard overview."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    def get(self) -> Tuple[dict, int]:
        """Retrieves a customer data dashboard overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] dict of Customer data overview and http code
        """

        customers_overview_data = get_customers_overview()

        return (
            CustomerOverviewSchema().dump(customers_overview_data),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp, f"/{api_c.CUSTOMERS_ENDPOINT}", "Customersview"
)
@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.CUSTOMERS_ENDPOINT}",
    "Customersview_no_of_cust",
)
class Customersview(SwaggerView):
    """
    Customers Overview class
    """

    responses = {
        HTTPStatus.OK.value: {
            "schema": CustomersSchema,
            "description": "Customers list.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get customers."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    def get(self) -> Tuple[dict, int]:
        """Retrieves a list of customers.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] dict of Customers and http code
        """

        customer_count = randint(200, 1000)
        customers_stub_data = {
            "total_customers": customer_count,
            "customers": [
                {
                    "id": f"{randint(1000, 9999)}-"
                    f"{randint(1000, 9999)}-{randint(10, 99)}",
                    "first_name": faker.first_name(),
                    "last_name": faker.last_name(),
                    "match_confidence": round(uniform(0, 1), 5),
                }
                for _ in range(customer_count)
            ],
        }

        return (
            CustomersSchema().dump(customers_stub_data),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"{api_c.CUSTOMERS_ENDPOINT}/<customer_id>",
    "CustomerProfileSearch",
)
class CustomerProfileSearch(SwaggerView):
    """
    Individual Customer Profile Search Class
    """

    parameters = [
        {
            "name": api_c.CUSTOMER_ID,
            "description": "Customer ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "1531-1234-21",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieve Individual Customer Profile",
            "schema": CustomerProfileSchema,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    @marshal_with(CustomerProfileSchema)
    def get(self, customer_id: str) -> Tuple[dict, int]:
        """Retrieves a customer profile.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            customer_id (str): ID of the customer

        Returns:
            Tuple[dict, int]: dict of customer profile and http code

        """

        try:
            first_name = faker.first_name()
            last_name = faker.last_name()
            return {
                "id": customer_id,
                "first_name": first_name,
                "last_name": last_name,
                "match_confidence": round(uniform(0, 1), 5),
                "since": faker.date_time_between("-1y", "now"),
                "ltv_actual": round(uniform(20, 60), 2),
                "ltv_predicted": round(uniform(20, 60), 2),
                "conversion_time": faker.date_time_between("-1y", "now"),
                "churn_rate": randint(1, 10),
                "last_click": faker.date_time_between("-1y", "now"),
                "last_purchase": faker.date_time_between("-1y", "now"),
                "last_email_open": faker.date_time_between("-1y", "now"),
                "email": f"{first_name}_{last_name}@fake.com",
                "phone": faker.phone_number(),
                "age": randint(21, 88),
                "gender": "",
                "address": faker.street_address(),
                "city": faker.city(),
                "state": faker.state(),
                "zip": faker.postcode(),
                "preference_email": False,
                "preference_push": False,
                "preference_sms": False,
                "preference_in_app": False,
                "identity_resolution": {
                    "name": {
                        "percentage": 0.26,
                        "data_sources": [
                            {
                                "id": "585t749997acad4bac4373b",
                                "name": "Adobe Experience",
                                "type": "adobe-experience",
                                "percentage": 0.49,
                            },
                            {
                                "id": "685t749997acad4bac4373b",
                                "name": "Google Analytics",
                                "type": "google-analytics",
                                "percentage": 0.51,
                            },
                        ],
                    },
                    "address": {
                        "percentage": 0.34,
                        "data_sources": [],
                    },
                    "email": {
                        "percentage": 0.2,
                        "data_sources": [],
                    },
                    "phone": {
                        "percentage": 0.1,
                        "data_sources": [],
                    },
                    "cookie": {
                        "percentage": 0.1,
                        "data_sources": [],
                    },
                },
                "propensity_to_unsubscribe": round(uniform(0, 1), 2),
                "propensity_to_purchase": round(uniform(0, 1), 2),
            }, HTTPStatus.OK.value
            # TODO use real call when available
            # return cdp.get_customer_profile(customer_id), HTTPStatus.OK.value
        except Exception as exc:
            raise handle_api_exception(
                exc, "Unable to get customer profile."
            ) from exc
