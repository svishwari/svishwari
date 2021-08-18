# pylint: disable=no-self-use
"""
Paths for customer API
"""
from http import HTTPStatus
from random import choice, randint
from typing import Tuple, List
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from faker import Faker
import pandas as pd

from flask import Blueprint, request, jsonify
from flask_apispec import marshal_with
from flasgger import SwaggerView

from huxunify.api.schema.customers import (
    CustomerProfileSchema,
    DataFeedSchema,
    DataFeedDetailsSchema,
    CustomerGeoVisualSchema,
    CustomerDemographicInsightsSchema,
    MatchingTrendsSchema,
    CustomerEventsSchema,
    TotalCustomersInsightsSchema,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import (
    secured,
    add_view_to_blueprint,
    api_error_handler,
    get_token_from_request,
)
from huxunify.api.data_connectors.cdp import (
    get_customer_profiles,
    get_customer_profile,
    get_customers_overview,
    get_idr_data_feeds,
    get_idr_matching_trends,
    get_customer_events_data,
    get_spending_by_cities,
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
    @api_error_handler()
    def get(self) -> Tuple[dict, int]:
        """Retrieves a customer data overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] dict of Customer data overview and http code
        """

        # TODO - resolve post demo, set unique IDs as total customers.
        token_response = get_token_from_request(request)
        customers = get_customers_overview(token_response[0])

        return (
            CustomerOverviewSchema().dump(customers),
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
    @api_error_handler()
    def post(self) -> Tuple[dict, int]:
        """Retrieves the overview of customer data with the requested filters applied.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:


        Returns:
            Tuple[dict, int] dict of Customer data overview and http code
        """

        # TODO - cdm to return single field
        token_response = get_token_from_request(request)
        customers = get_customers_overview(token_response[0], request.json)

        return (
            CustomerOverviewSchema().dump(customers),
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
    @api_error_handler()
    def get(self) -> Tuple[dict, int]:
        """Retrieves a customer data dashboard overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] dict of Customer data overview and http code
        """
        token_response = get_token_from_request(request)
        return (
            CustomerOverviewSchema().dump(
                get_customers_overview(token_response[0])
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp, f"/{api_c.CUSTOMERS_ENDPOINT}", "Customersview"
)
class Customersview(SwaggerView):
    """
    Customers Overview class
    """

    parameters = [
        {
            "name": api_c.QUERY_PARAMETER_BATCH_SIZE,
            "in": "query",
            "type": "string",
            "description": "Max number of customers to be returned.",
            "example": api_c.CUSTOMERS_DEFAULT_BATCH_SIZE,
            "required": False,
            "default": api_c.CUSTOMERS_DEFAULT_BATCH_SIZE,
        },
        {
            "name": api_c.QUERY_PARAMETER_BATCH_NUMBER,
            "in": "query",
            "type": "string",
            "description": "Number of which batch of customers should be returned.",
            "example": api_c.CUSTOMERS_DEFAULT_BATCH_NUMBER,
            "required": False,
            "default": api_c.CUSTOMERS_DEFAULT_BATCH_NUMBER,
        },
    ]
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
    @api_error_handler(
        custom_message={ValueError: {"message": api_c.INVALID_BATCH_PARAMS}}
    )
    def get(self) -> Tuple[dict, int]:
        """Retrieves a list of customers.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] dict of Customers and http code
        """

        # get token
        token_response = get_token_from_request(request)
        batch_size = request.args.get(
            api_c.QUERY_PARAMETER_BATCH_SIZE,
            default=api_c.CUSTOMERS_DEFAULT_BATCH_SIZE,
        )
        batch_number = request.args.get(
            api_c.QUERY_PARAMETER_BATCH_NUMBER,
            default=api_c.CUSTOMERS_DEFAULT_BATCH_NUMBER,
        )
        offset = (int(batch_number) - 1) * int(batch_size)
        return (
            CustomersSchema().dump(
                get_customer_profiles(token_response[0], batch_size, offset)
            ),
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
        token_response = get_token_from_request(request)

        return (
            redact_fields(
                get_customer_profile(token_response[0], hux_id),
                api_c.CUSTOMER_PROFILE_REDACTED_FIELDS,
            ),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.IDR_ENDPOINT}/{api_c.DATA_FEEDS}",
    "IDRDataFeeds",
)
class IDRDataFeeds(SwaggerView):
    """IDR Data Feeds Report"""

    responses = {
        HTTPStatus.OK.value: {
            "schema": {"type": "array", "items": DataFeedSchema},
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
    def get(self) -> Tuple[List[dict], int]:
        """Retrieves a IDR data feeds.
        ---
        security:
            - Bearer: ["Authorization"]\

        Args:

        Returns:
            Tuple[List[dict], int] list of IDR data feeds object dicts
        """

        return (
            jsonify(DataFeedSchema().dump(get_idr_data_feeds(), many=True)),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.IDR_ENDPOINT}/{api_c.DATA_FEEDS}/<datafeed>",
    "IDRDataFeedDetails",
)
class IDRDataFeedDetails(SwaggerView):
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
            "schema": DataFeedDetailsSchema,
            "description": "Identity Resolution Data Feed Waterfall Report",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get IDR Data Feed Waterfall Report."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use,unused-argument
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
            DataFeedDetailsSchema().dump(
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


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.CUSTOMERS_INSIGHTS}/{api_c.GEOGRAPHICAL}",
    "CustomerInsightsGeo",
)
class CustomerGeoVisualView(SwaggerView):
    """
    Customer Profiles Geographical insights class
    """

    responses = {
        HTTPStatus.OK.value: {
            "schema": {"type": "array", "items": CustomerGeoVisualSchema},
            "description": "Customer Profiles Geographical Insights .",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Customer Profiles Geographical Insights."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[list, int]:
        """Retrieves a Customer profiles geographical insights.

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
    Customers Profiles Demographic Insights class
    """

    parameters = [
        {
            "name": "body",
            "description": "Customer Insights Demographic Filters",
            "type": "object",
            "in": "body",
            "example": {
                "filters": {
                    "start_date": "2020-11-30T00:00:00Z",
                    "end_date": "2021-04-30T00:00:00Z",
                }
            },
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": {
                "type": "body",
                "items": CustomerDemographicInsightsSchema,
            },
            "description": "Customer Demographical Visual Insights.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get customers Demographical Visual Insights."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def post(self) -> Tuple[dict, int]:
        """Retrieves a Demographical customer insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] list of Customer insights on demo overview and http code
        """

        token_response = get_token_from_request(request)

        start_date = datetime(2020, 11, 30)
        dates = [
            (start_date + pd.DateOffset(months=x)).to_pydatetime()
            for x in range(0, 5)
        ]
        output = {
            api_c.GENDER: {
                gender: {
                    api_c.POPULATION_PERCENTAGE: population_percent,
                    api_c.SIZE: size,
                }
                for gender, population_percent, size in zip(
                    api_c.GENDERS,
                    [0.5201, 0.4601, 0.0211],
                    [6955119, 5627732, 289655],
                )
            },
            api_c.INCOME: get_spending_by_cities(token_response[0]),
            api_c.SPEND: {
                api_c.GENDER_WOMEN: [
                    {api_c.DATE: date, api_c.LTV: ltv}
                    for date, ltv in zip(dates, [3199, 4265, 4986, 4986, 6109])
                ],
                api_c.GENDER_MEN: [
                    {api_c.DATE: date, api_c.LTV: ltv}
                    for date, ltv in zip(dates, [3088, 3842, 3999, 3999, 6109])
                ],
                api_c.GENDER_OTHER: [
                    {api_c.DATE: date, api_c.LTV: ltv}
                    for date, ltv in zip(dates, [2144, 3144, 3211, 3211, 4866])
                ],
            },
        }

        return (
            CustomerDemographicInsightsSchema().dump(output),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.IDR_ENDPOINT}/{api_c.MATCHING_TRENDS}",
    "IDRMatchingTrends",
)
class IDRMatchingTrends(SwaggerView):
    """IDR Matching Trends YTD"""

    responses = {
        HTTPStatus.OK.value: {
            "schema": {"type": "array", "items": MatchingTrendsSchema},
            "description": "Identity Resolution Matching Trends YTD Data",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get IDR Matching Trends"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use,unused-argument
    @api_error_handler()
    def get(self) -> Tuple[dict, int]:
        """Retrieves IDR Matching trends YTD data

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] dict of IDR Matching trends YTD and http code
        """
        token_response = get_token_from_request(request)
        return (
            jsonify(
                MatchingTrendsSchema().dump(
                    get_idr_matching_trends(token_response[0]), many=True
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.CUSTOMERS_ENDPOINT}/<{api_c.HUX_ID}>/events",
    "CustomerEvents",
)
class CustomerEvents(SwaggerView):
    """
    Customer events under customer profile
    """

    parameters = [
        {
            "name": api_c.HUX_ID,
            "description": "ID of the customer whose events need to be fetched.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "1531-1234-21",
        },
        {
            "name": "body",
            "description": "Customer Events Filters",
            "type": "object",
            "in": "body",
            "example": {
                "start_date": "2021-07-25T00:00:00Z",
                "end_date": "2021-08-02T00:00:00Z",
            },
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": {
                "type": "array",
                "items": CustomerEventsSchema,
            },
            "description": "Events for a Customer grouped by day.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get events for customer."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    # @api_error_handler()
    def post(self, hux_id: str) -> Tuple[dict, int]:
        """Retrieves events for a given HUX ID.

        ---
        security:
            - Bearer: ["Authorization"]
        Args:
            hux_id (str): ID of the customer
        Returns:
            Tuple[dict, int] list of Customer events grouped by day and http code
        """
        token_response = get_token_from_request(request)
        return (
            jsonify(
                CustomerEventsSchema().dump(
                    get_customer_events_data(
                        token_response[0], hux_id, request.json
                    ),
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.CUSTOMERS_INSIGHTS}/{api_c.TOTAL}",
    "TotalCustomersGraphView",
)
class TotalCustomersGraphView(SwaggerView):
    """
    Total customer insights graph view class
    """

    responses = {
        HTTPStatus.OK.value: {
            "schema": {"type": "array", "items": TotalCustomersInsightsSchema},
            "description": "Total Customer Insights .",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Total Customer Insights."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[list, int]:
        """Retrieves total customer insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] list of total customers & new customers added, http code
        """
        last_date = datetime.today() - relativedelta(months=6)
        today = datetime.today()
        total_customers = []
        while last_date <= today:
            total_customers.append(
                {
                    api_c.TOTAL_CUSTOMERS: randint(50000, 156000),
                    api_c.NEW_CUSTOMERS_ADDED: randint(1, 5000),
                    api_c.DATE: last_date,
                }
            )
            last_date += timedelta(days=1)
        return (
            jsonify(
                TotalCustomersInsightsSchema().dump(total_customers, many=True)
            ),
            HTTPStatus.OK,
        )
