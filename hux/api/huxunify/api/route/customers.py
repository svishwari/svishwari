"""
Purpose of this file is to have Customer APIs
"""
from http import HTTPStatus
from typing import Tuple

from flask import Blueprint, jsonify

from flasgger import SwaggerView
import datetime

from marshmallow import INCLUDE

from huxunify.api.schema.customers import CustomerProfilesOverviewSchema
from huxunify.api.route.utils import add_view_to_blueprint, secured
from huxunify.api.schema.utils import AUTH401_RESPONSE
import huxunify.api.constants as c

from random import randint


# setup the Customers blueprint
customers_bp = Blueprint(c.CUSTOMERS_TAG, import_name=__name__)


@customers_bp.before_request
@secured()
def before_request():
    """Protect all of the customer endpoints."""
    pass  # pylint: disable=unnecessary-pass


def get_customers_overview() -> dict:
    """Fetch customers overview data.
    ---

        Args: None

        Returns: dict of overview data

    """
    customers_overview_data = {
        c.TOTAL_RECORDS: randint(10000000, 99999999),
        c.MATCH_RATE: 0.60123,
        c.TOTAL_UNIQUE_IDS: randint(10000000, 99999999),
        c.TOTAL_UNKNOWN_IDS: randint(10000000, 99999999),
        c.TOTAL_KNOWN_IDS: randint(10000000, 99999999),
        c.TOTAL_INDIVIDUAL_IDS: randint(10000000, 99999999),
        c.TOTAL_HOUSEHOLD_IDS: randint(10000000, 99999999),
        c.UPDATED: datetime.datetime.now(),
        c.TOTAL_CUSTOMERS: randint(10000000, 99999999),
        c.COUNTRIES: randint(1, 100),
        c.STATES: randint(1, 100),
        c.CITIES: randint(10 ^ 3, 10 ^ 5 - 1),
        c.MIN_AGE: randint(1, 10),
        c.MAX_AGE: randint(11, 100),
        c.GENDER_WOMEN: 0.52123,
        c.GENDER_MEN: 0.46123,
        c.GENDER_OTHER: 0.02123,
        c.MIN_LTV_PREDICTED: 34.1323,
        c.MAX_LTV_PREDICTED: 89.1234,
        c.MIN_LTV_ACTUAL: 14.1234,
        c.MAX_LTV_ACTUAL: 89.1234,
    }
    return customers_overview_data


@add_view_to_blueprint(
    customers_bp,
    f"/{c.CUSTOMER_PROFILES_OVERVIEW_ENDPOINT}",
    "CustomerProfilesOverviewSchema",
)
class CustomerProfilesOverview(SwaggerView):
    """
    Customers Overview class
    """

    responses = {
        HTTPStatus.OK.value: {
            "description": "Customer Profiles Overview",
            "schema": {
                "type": "array",
                "items": CustomerProfilesOverviewSchema,
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get customers overview"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [c.CUSTOMERS_TAG]

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
            CustomerProfilesOverviewSchema().dump(customers_overview_data),
            HTTPStatus.OK,
        )
