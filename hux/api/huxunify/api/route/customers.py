# pylint: disable=no-self-use
"""
Paths for customer API
"""
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Tuple
from faker import Faker

from flask import Blueprint, request
from flask_apispec import marshal_with
from flasgger import SwaggerView

from huxunifylib.database import constants as db_c
from huxunify.api.schema.customers import (
    CustomerProfileSchema,
    DatafeedSchema,
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
    f"/{api_c.IDR_ENDPOINT}/{api_c.DATAFEEDS}",
    "IDRDataFeeds",
)
class IDRDataFeeds(SwaggerView):
    """IDR Data Feeds Report"""

    responses = {
        HTTPStatus.OK.value: {
            "schema": DatafeedSchema,
            "description": "Identity Resolution Data Feeds",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get IDR Data Feeds."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use,unused-argument
    @api_error_handler()
    @marshal_with(DatafeedSchema(many=True))
    def get(self) -> list:
        """Retrieves a IDR data feeds.
        ---
        security:
            - Bearer: ["Authorization"]
        Args:

        Returns:
            Tuple[dict, int] dict of IDR data feed waterfall
        """

        data_feeds = [
            {
                api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4fc",
                api_c.DATAFEED_NAME: "Really_long_Feed_Name_106",
                api_c.DATAFEED_DATA_SOURCE: db_c.DELIVERY_PLATFORM_SFMC,
                api_c.DATAFEED_NEW_IDS_COUNT: 21,
                api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 2023532,
                api_c.DATAFEED_MATCH_RATE: 0.98,
                api_c.DATAFEED_LAST_RUN_DATE: datetime.utcnow(),
            },
            {
                api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4fd",
                api_c.DATAFEED_NAME: "Really_long_Feed_Name_105",
                api_c.DATAFEED_DATA_SOURCE: db_c.DELIVERY_PLATFORM_FACEBOOK,
                api_c.DATAFEED_NEW_IDS_COUNT: 54,
                api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 3232,
                api_c.DATAFEED_MATCH_RATE: 0.97,
                api_c.DATAFEED_LAST_RUN_DATE: datetime.utcnow()
                - timedelta(days=1),
            },
            {
                api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4fe",
                api_c.DATAFEED_NAME: "Really_long_Feed_Name_102",
                api_c.DATAFEED_DATA_SOURCE: db_c.DELIVERY_PLATFORM_FACEBOOK,
                api_c.DATAFEED_NEW_IDS_COUNT: 300,
                api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 3012,
                api_c.DATAFEED_MATCH_RATE: 0.98,
                api_c.DATAFEED_LAST_RUN_DATE: datetime.utcnow()
                - timedelta(days=7),
            },
            {
                api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4ff",
                api_c.DATAFEED_NAME: "Really_long_Feed_Name_100",
                api_c.DATAFEED_DATA_SOURCE: db_c.DELIVERY_PLATFORM_SFMC,
                api_c.DATAFEED_NEW_IDS_COUNT: 612,
                api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 2045,
                api_c.DATAFEED_MATCH_RATE: 0.98,
                api_c.DATAFEED_LAST_RUN_DATE: datetime.utcnow()
                - timedelta(days=30),
            },
        ]
        return (
            data_feeds,
            HTTPStatus.OK,
        )
