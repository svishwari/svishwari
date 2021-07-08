# pylint: disable=no-self-use
"""
Paths for customer API
"""

from http import HTTPStatus
from random import choice
from typing import Tuple
from faker import Faker
from datetime import datetime
import pandas as pd
from pandas import to_datetime

from flask import Blueprint, request, jsonify
from flask_apispec import marshal_with
from flasgger import SwaggerView

from huxunify.api.schema.customers import (
    CustomerProfileSchema,
    CustomerGeoVisualSchema, CustomerDemographicInsightsSchema,
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
    f"/{api_c.CUSTOMERS_INSIGHTS}/{api_c.GEOGRAPHICAL}",
    "CustomerInsightsGeo",
)
class CustomerGeoVisualView(SwaggerView):
    """
    Customers Dashboard Overview class
    """

    responses = {
        HTTPStatus.OK.value: {
            "schema": {"type": "array", "items": CustomerGeoVisualSchema},
            "description": "Customer Identity Resolution Dashboard overview.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get customers identity dashboard overview."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    def get(self) -> Tuple[list, int]:
        """Retrieves a customer data dashboard overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] list of Customer insights on geo overview and http code
        """
        geo_visuals = [
            {
                api_c.NAME: state,
                api_c.POPULATION_PERCENTAGE: choice([0.3012, 0.1910, 0.2817]),
                api_c.SIZE: choice([28248560, 39510225, 7615887]),
                api_c.GENDER_WOMEN: 0.50,
                api_c.GENDER_MEN: 0.49,
                api_c.GENDER_OTHER: 0.01,
                api_c.LTV: choice([3848.50, 3971.50, 3952]),
            }
            for state in api_c.STATE_NAMES
        ]
        return (
            jsonify(CustomerGeoVisualSchema().dump(geo_visuals, many=True)),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.CUSTOMERS_INSIGHTS}/{api_c.DEMOGRAPHIC}",
    "CustomerInsightsDemo",
)
class CustomerDemoVisualView(SwaggerView):
    """
    Customers Dashboard Overview class
    """

    responses = {
        HTTPStatus.OK.value: {
            "schema": {"type": "array", "items": CustomerDemographicInsightsSchema},
            "description": "Customer Demographical Visual Insights overview.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get customers Demographical Visual Insights overview."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    def post(self) -> Tuple[dict, int]:
        """Retrieves a customer data dashboard overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] list of Customer insights on demo overview and http code
        """

        start_date = datetime(2020, 11, 30)
        dates = [(start_date + pd.DateOffset(months=x)).to_pydatetime() for x in range(0, 5)]
        output = {
            api_c.GENDER: {gender: {
                api_c.POPULATION_PERCENTAGE: population_percent,
                api_c.SIZE: size
            } for gender, population_percent, size in
                zip(api_c.GENDERS, [0.5201, 0.4601, 0.0211], [6955119, 5627732, 289655])},

            api_c.INCOME: [{api_c.NAME: city, api_c.LTV: ltv} for city, ltv in
                           zip(["Houston", "San Antonio", "Dallas", "Austin", "Fort Worth"],
                               [4008, 3922, 4231, 4198, 4011])],
            api_c.SPEND: {
                api_c.GENDER_WOMEN: [{api_c.DATE: date, api_c.LTV: ltv} for date, ltv in
                                     zip(dates, [3199, 4265, 4986, 4986, 6109])],
                api_c.GENDER_MEN: [{api_c.DATE: date, api_c.LTV: ltv} for date, ltv in
                                   zip(dates, [3088, 3842, 3999, 3999, 6109])],
                api_c.GENDER_OTHER: [{api_c.DATE: date, api_c.LTV: ltv} for date, ltv in
                                     zip(dates, [2144, 3144, 3211, 3211, 4866])],
            }
        }

        response = CustomerDemographicInsightsSchema().dump(output)
        return (
            response,
            HTTPStatus.OK,
        )
