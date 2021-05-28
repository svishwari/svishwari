"""
Purpose of this file is to have Customer APIs
"""
from http import HTTPStatus
from typing import Tuple
import datetime
from random import randint, uniform
from flask import Blueprint
from flasgger import SwaggerView


from huxunify.api.schema.customers import (
    CustomerOverviewSchema,
    CustomersSchema,
)
from huxunify.api.route.utils import add_view_to_blueprint, secured
from huxunify.api.schema.utils import AUTH401_RESPONSE
import huxunify.api.constants as c


# setup the Customers blueprint
customers_bp = Blueprint(
    c.CUSTOMERS_ENDPOINT, import_name=__name__, url_prefix="/cdp"
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
        c.TOTAL_RECORDS: randint(10000000, 99999999),
        c.MATCH_RATE: round(uniform(0, 1), 5),
        c.TOTAL_UNIQUE_IDS: randint(10000000, 99999999),
        c.TOTAL_UNKNOWN_IDS: randint(10000000, 99999999),
        c.TOTAL_KNOWN_IDS: randint(10000000, 99999999),
        c.TOTAL_INDIVIDUAL_IDS: randint(10000000, 99999999),
        c.TOTAL_HOUSEHOLD_IDS: randint(10000000, 99999999),
        c.UPDATED: datetime.datetime.now(),
        c.TOTAL_CUSTOMERS: randint(10000000, 99999999),
        c.COUNTRIES: randint(1, 3),
        c.STATES: randint(1, 51),
        c.CITIES: randint(5, 50),
        c.MIN_AGE: randint(1, 10),
        c.MAX_AGE: randint(11, 100),
        c.GENDER_WOMEN: round(uniform(0, 1), 5),
        c.GENDER_MEN: round(uniform(0, 1), 5),
        c.GENDER_OTHER: round(uniform(0, 1), 5),
        c.MIN_LTV_PREDICTED: round(uniform(1, 100), 4),
        c.MAX_LTV_PREDICTED: round(uniform(1, 100), 4),
        c.MIN_LTV_ACTUAL: round(uniform(1, 100), 4),
        c.MAX_LTV_ACTUAL: round(uniform(1, 100), 4),
    }
    return customers_overview_data


@add_view_to_blueprint(
    customers_bp,
    f"/{c.CUSTOMERS_TAG}/{c.CUSTOMERS_OVERVIEW_ENDPOINT}",
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
    tags = [c.CUSTOMERS_TAG]

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
    f"/{c.CUSTOMERS_TAG}",
    "CustomersSchema",
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
    tags = [c.CUSTOMERS_TAG]

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
            "customers": [
                {
                    "id": "1531-2039-22",
                    "first_name": "Bertie",
                    "last_name": "Fox",
                    "match_confidence": round(uniform(0, 1), 5),
                }
            ],
        }

        return (
            CustomersSchema().dump(customers_stub_data),
            HTTPStatus.OK,
        )
