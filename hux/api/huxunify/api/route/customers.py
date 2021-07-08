# pylint: disable=no-self-use
"""
Paths for customer API
"""
from datetime import datetime
from http import HTTPStatus
from typing import Tuple
from faker import Faker

from flask import Blueprint, request
from flask_apispec import marshal_with
from flasgger import SwaggerView

from huxunify.api.schema.customers import (
    CustomerProfileSchema,
    DataFeedSchema,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import (
    secured,
    add_view_to_blueprint,
    api_error_handler,
)
from huxunify.api.data_connectors.cdp import (
    get_customer_profiles,
    get_customer_profile,
    get_customers_overview,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api.schema.customers import (
    CustomerOverviewSchema,
    CustomersSchema,
)
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import redact_fields

customers_bp = Blueprint(
    api_c.CUSTOMERS_ENDPOINT, import_name=__name__, url_prefix="/cdp"
)

faker = Faker()


@customers_bp.before_request
@secured()
def before_request():
    """Protect all of the customer endpoints."""
    pass  # pylint: disable=unnecessary-pass


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
            "schema": CustomerOverviewSchema,
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

        return (
            CustomerOverviewSchema().dump(get_customers_overview()),
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
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "max_age",
                                "type": "equals",
                                "value": 87,
                            },
                            {
                                "field": "min_age",
                                "type": "equals",
                                "value": 25,
                            },
                            {
                                "field": "match_rate",
                                "type": "equals",
                                "value": 0.5,
                            },
                        ],
                    }
                ]
            },
        }
    ]
    responses = {
        HTTPStatus.CREATED.value: {
            "description": "Customer Profiles Overview",
            "schema": CustomerOverviewSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get customers overview"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    def post(self) -> Tuple[dict, int]:
        """Retrieves the overview of customer data with the requested filters applied.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:


        Returns:
            Tuple[dict, int] dict of Customer data overview and http code
        """

        return (
            CustomerOverviewSchema().dump(
                get_customers_overview(request.json)
            ),
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

        return (
            CustomerOverviewSchema().dump(get_customers_overview()),
            HTTPStatus.OK,
        )


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

        return (
            CustomersSchema().dump(get_customer_profiles()),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"{api_c.CUSTOMERS_ENDPOINT}/<{api_c.HUX_ID}>",
    "CustomerProfileSearch",
)
class CustomerProfileSearch(SwaggerView):
    """
    Individual Customer Profile Search Class
    """

    parameters = [
        {
            "name": api_c.HUX_ID,
            "description": f"{api_c.HUX_ID}.",
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
    @api_error_handler()
    def get(self, hux_id: str) -> Tuple[dict, int]:
        """Retrieves a customer profile.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            hux_id (str): ID of the customer

        Returns:
            Tuple[dict, int]: dict of customer profile and http code

        """
        return (
            redact_fields(
                get_customer_profile(hux_id),
                api_c.CUSTOMER_PROFILE_REDACTED_FIELDS,
            ),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.IDR_ENDPOINT}/{api_c.DATA_FEEDS}/<datafeed>",
    "IDRDataFeeds",
)
class IDRDataFeeds(SwaggerView):
    """IDR Data Feeds Report"""

    parameters = [
        {
            "name": api_c.DATA_FEED,
            "description": "Data Feed Name",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "Really_long_feed_Name_106",
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "schema": DataFeedSchema,
            "description": "Identity Resolution Data Feed Waterfall Report",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get IDR Data Feed Waterfall Report."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    @api_error_handler()
    def get(self, datafeed: str) -> Tuple[dict, int]:
        """Retrieves a IDR data feed waterfall report.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            datafeed (str): Data feed name

        Returns:
            Tuple[dict, int] dict of IDR data feed waterfall
        """

        return (
            DataFeedSchema().dump(
                {
                    api_c.PINNING: {
                        api_c.INPUT_RECORDS: 2,
                        api_c.OUTPUT_RECORDS: 2,
                        api_c.EMPTY_RECORDS: 0,
                        api_c.INDIVIDUAL_ID_MATCH: 1,
                        api_c.HOUSEHOLD_ID_MATCH: 1,
                        api_c.COMPANY_ID_MATCH: 1,
                        api_c.ADDRESS_ID_MATCH: 1,
                        api_c.DB_READS: 1,
                        api_c.DB_WRITES: 1,
                        api_c.FILENAME: "Input.csv",
                        api_c.NEW_INDIVIDUAL_IDS: 1,
                        api_c.NEW_HOUSEHOLD_IDS: 1,
                        api_c.NEW_COMPANY_IDS: 1,
                        api_c.NEW_ADDRESS_IDS: 1,
                        api_c.PROCESS_TIME: 6.43,
                        api_c.DATE_TIME: datetime.now(),
                    },
                    api_c.STITCHED: {
                        api_c.DIGITAL_IDS_ADDED: 3,
                        api_c.DIGITAL_IDS_MERGED: 6,
                        api_c.MATCH_RATE: 0.6606,
                        api_c.MERGE_RATE: 0,
                        api_c.RECORDS_SOURCE: "Input waterfall",
                        api_c.TIME_STAMP: datetime.now(),
                    },
                }
            ),
            HTTPStatus.OK,
        )
