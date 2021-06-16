# pylint: disable=no-self-use
"""
Paths for customer API
"""

from http import HTTPStatus
from typing import Tuple
import datetime
from random import randint, uniform, choice

from flask import Blueprint
from flask_apispec import marshal_with
from flasgger import SwaggerView

from huxunify.api.schema.customers import CustomerProfileSchema
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


def get_stub_customer() -> dict:
    """Fetch customer's stub data.

    Args:

    Returns:
        dict of stub of customer

    """
    random_first_names = [
        "Maryjane",
        "Lillianna",
        "Bertie",
        "Bailey",
        "Bridger",
    ]
    random_last_names = ["Warren", "Holder", "Greene", "Robinson", "Fox"]
    stub_customer = {
        "id": "1531-2039-22",
        "first_name": choice(random_first_names),
        "last_name": choice(random_last_names),
        "match_confidence": round(uniform(0, 1), 5),
    }
    return stub_customer


@add_view_to_blueprint(
    customers_bp, f"/{api_c.CUSTOMERS_ENDPOINT}", "Customersview"
)
@add_view_to_blueprint(
    customers_bp,
    api_c.CUSTOMERS_ENDPOINT,
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

        customers_stub_data = {
            "total_customers": 52456232,
            "customers": [get_stub_customer() for i in range(int(1000))],
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
            return api_c.MOCK_CUSTOMER_PROFILE_RESPONSE, HTTPStatus.OK.value
            # TODO use real call when available
            # return cdp.get_customer_profile(customer_id), HTTPStatus.OK.value
        except Exception as exc:
            raise handle_api_exception(
                exc, "Unable to get customer profile."
            ) from exc
