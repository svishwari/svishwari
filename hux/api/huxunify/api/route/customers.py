# pylint: disable=no-self-use, too-many-lines
"""Paths for customer API"""
from http import HTTPStatus
from typing import Tuple, List
from datetime import datetime

from faker import Faker

from flask import Blueprint, request, jsonify
from flasgger import SwaggerView

from huxunify.api.schema.customers import (
    CustomerProfileSchema,
    DataFeedSchema,
    DataFeedDetailsSchema,
    CustomerGeoVisualSchema,
    CustomerDemographicInsightsSchema,
    MatchingTrendsSchema,
    IDROverviewWithDateRangeSchema,
    CustomerEventsSchema,
    TotalCustomersInsightsSchema,
    CustomersInsightsStatesSchema,
    CustomersInsightsCitiesSchema,
    CustomersInsightsCountriesSchema,
)
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
)
from huxunify.api.data_connectors.okta import get_token_from_request
from huxunify.api.data_connectors.cdp import (
    get_customer_profiles,
    get_customer_profile,
    get_customers_overview,
    get_idr_overview,
    get_customer_events_data,
    get_demographic_by_state,
    get_spending_by_cities,
    get_customers_insights_count_by_day,
    get_city_ltvs,
    get_spending_by_gender,
    get_demographic_by_country,
)
from huxunify.api.data_connectors.cdp_connection import (
    get_idr_data_feeds,
    get_idr_data_feed_details,
    get_idr_matching_trends,
)
from huxunify.api.route.utils import add_chart_legend, get_start_end_dates
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.schema.utils import (
    redact_fields,
    AUTH401_RESPONSE,
    FAILED_DEPENDENCY_424_RESPONSE,
)
from huxunify.api.schema.customers import (
    CustomerOverviewSchema,
    CustomersSchema,
)
from huxunify.api import constants as api_c
from huxunify.api.route.utils import (
    group_gender_spending,
    Validation,
)

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
    """Customers Overview class."""

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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[dict, int]:
        """Retrieves a customer data overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int]: dict of Customer data overview, HTTP status code.
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
    """Customers Post Overview class."""

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
                                "field": "country",
                                "type": "equals",
                                "value": "US",
                            },
                            {
                                "field": "age",
                                "type": "range",
                                "value": [40, 50],
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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def post(self) -> Tuple[dict, int]:
        """Retrieves the overview of customer data with the requested filters applied.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int]: dict of Customer data overview, HTTP status code.
        """

        # TODO - cdm to return single field
        token_response = get_token_from_request(request)
        customers = get_customers_overview(token_response[0], request.json)

        customers = {
            overview_key: customers.get(overview_key) or 0
            for overview_key in customers
        }

        return (
            CustomerOverviewSchema().dump(customers),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.IDR_ENDPOINT}/{api_c.OVERVIEW}",
    "IDROverview",
)
class IDROverview(SwaggerView):
    """Customers Dashboard Overview class."""

    parameters = [
        {
            "name": api_c.START_DATE,
            "description": "Start date.",
            "type": "string",
            "in": "query",
            "required": False,
            "example": "05-01-2016",
        },
        {
            "name": api_c.END_DATE,
            "description": "End date.",
            "type": "string",
            "in": "query",
            "required": False,
            "example": "09-01-2019",
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": IDROverviewWithDateRangeSchema,
            "description": "Customer Identity Resolution Dashboard overview.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get customers identity dashboard overview."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[dict, int]:
        """Retrieves a customer data dashboard overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int]: dict of Customer data overview, HTTP status code.
        """
        token_response = get_token_from_request(request)

        # default to five years lookup to find the event date range.
        start_date, end_date = get_start_end_dates(request, 60)
        Validation.validate_date_range(start_date, end_date)

        token_response = get_token_from_request(request)

        # TODO - when the CDP endpoint for getting the max and min date rnge
        #  is available, we will call that instead of iterating all events to get them.
        # get IDR overview
        idr_overview = get_idr_overview(
            token_response[0], start_date, end_date
        )

        # get date range from IDR matching trends.
        trend_data = get_idr_matching_trends(
            token_response[0],
            start_date,
            end_date,
        )

        return (
            IDROverviewWithDateRangeSchema().dump(
                {
                    api_c.OVERVIEW: idr_overview,
                    api_c.DATE_RANGE: {
                        api_c.START_DATE: min(
                            [x[api_c.DAY] for x in trend_data]
                        )
                        if trend_data
                        else datetime.strptime(
                            start_date, api_c.DEFAULT_DATE_FORMAT
                        ),
                        api_c.END_DATE: max([x[api_c.DAY] for x in trend_data])
                        if trend_data
                        else datetime.strptime(
                            end_date, api_c.DEFAULT_DATE_FORMAT
                        ),
                    },
                }
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp, f"/{api_c.CUSTOMERS_ENDPOINT}", "CustomersListview"
)
class CustomersListview(SwaggerView):
    """Customers List class."""

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
            "example": api_c.DEFAULT_BATCH_NUMBER,
            "required": False,
            "default": api_c.DEFAULT_BATCH_NUMBER,
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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[dict, int]:
        """Retrieves a list of customers.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int]: dict of Customers, HTTP status code.
        """

        # get token
        token_response = get_token_from_request(request)

        batch_size = Validation.validate_integer(
            request.args.get(
                api_c.QUERY_PARAMETER_BATCH_SIZE,
                str(api_c.DEFAULT_BATCH_SIZE),
            )
        )

        batch_number = Validation.validate_integer(
            request.args.get(
                api_c.QUERY_PARAMETER_BATCH_NUMBER,
                str(api_c.DEFAULT_BATCH_NUMBER),
            )
        )

        offset = (batch_number - 1) * batch_size
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
    """Individual Customer Profile Search Class."""

    parameters = [
        {
            "name": api_c.HUX_ID,
            "description": "Unique HUX ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "HUX123456789012345",
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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    @api_error_handler()
    def get(self, hux_id: str) -> Tuple[dict, int]:
        """Retrieves a customer profile.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            hux_id (str): ID of the customer.

        Returns:
            Tuple[dict, int]: dict of customer profile, HTTP status code.
        """
        token_response = get_token_from_request(request)

        Validation.validate_hux_id(hux_id)

        redacted_data = redact_fields(
            get_customer_profile(token_response[0], hux_id),
            api_c.CUSTOMER_PROFILE_REDACTED_FIELDS,
        )

        idr_data = api_c.CUSTOMER_IDR_TEST_DATA
        # TODO : Fetch IDR data from CDP once it is ready
        # api_c.IDENTITY_RESOLUTION: redacted_data[api_c.IDENTITY_RESOLUTION]

        return (
            CustomerProfileSchema().dump(
                {
                    api_c.OVERVIEW: redacted_data,
                    api_c.INSIGHTS: redacted_data,
                    api_c.CONTACT_PREFERENCES: redacted_data,
                    api_c.IDENTITY_RESOLUTION: add_chart_legend(idr_data),
                }
            ),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.IDR_ENDPOINT}/{api_c.DATAFEEDS}",
    "IDRDataFeeds",
)
class IDRDataFeeds(SwaggerView):
    """IDR Data Feeds Report."""

    parameters = [
        {
            "name": api_c.START_DATE,
            "description": "Start date.",
            "type": "string",
            "in": "query",
            "required": False,
            "example": "05-01-2016",
        },
        {
            "name": api_c.END_DATE,
            "description": "End date.",
            "type": "string",
            "in": "query",
            "required": False,
            "example": "09-01-2019",
        },
    ]
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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use,unused-argument
    @api_error_handler()
    def get(self) -> Tuple[List[dict], int]:
        """Retrieves a IDR data feeds.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[List[dict], int]: list of IDR data feeds object dicts,
                HTTP status code.
        """

        token_response = get_token_from_request(request)

        start_date, end_date = get_start_end_dates(request, 6)
        Validation.validate_date_range(start_date, end_date)

        return (
            jsonify(
                DataFeedSchema().dump(
                    get_idr_data_feeds(
                        token_response[0],
                        start_date,
                        end_date,
                    ),
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.IDR_ENDPOINT}/{api_c.DATAFEEDS}/<datafeed_id>",
    "IDRDataFeedDetails",
)
class IDRDataFeedDetails(SwaggerView):
    """IDR Data Feeds Report."""

    parameters = [
        {
            "name": api_c.DATAFEED_ID,
            "description": "Data Feed ID",
            "type": "integer",
            "in": "path",
            "required": True,
            "example": "1",
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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self, datafeed_id: str) -> Tuple[dict, int]:
        """Retrieves a IDR data feed waterfall report.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            datafeed_id (str): Data feed ID.

        Returns:
            Tuple[dict, int]: dict of IDR data feed waterfall,
                HTTP status code.
        """

        token_response = get_token_from_request(request)

        datafeed_id = Validation.validate_integer(datafeed_id)

        return (
            DataFeedDetailsSchema().dump(
                get_idr_data_feed_details(token_response[0], datafeed_id)
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.CUSTOMERS_INSIGHTS}/{api_c.GEOGRAPHICAL}",
    "CustomerInsightsGeo",
)
class CustomerGeoVisualView(SwaggerView):
    """Customer Profiles Geographical insights class."""

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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler(
        custom_message={
            ZeroDivisionError: {"message": api_c.ZERO_AUDIENCE_SIZE}
        }
    )
    def get(self) -> Tuple[list, int]:
        """Retrieves a Customer profiles geographical insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[list, int]: list of Customer insights on geo overview,
                HTTP status code.
        """

        token_response = get_token_from_request(request)
        return (
            jsonify(
                CustomerGeoVisualSchema().dump(
                    get_demographic_by_state(token_response[0]), many=True
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.CUSTOMERS_INSIGHTS}/{api_c.DEMOGRAPHIC}",
    "CustomerInsightsDemo",
)
class CustomerDemoVisualView(SwaggerView):
    """Customers Profiles Demographic Insights class."""

    parameters = [
        {
            "name": api_c.START_DATE,
            "description": "Start date.",
            "type": "string",
            "in": "query",
            "required": True,
            "example": "05-01-2016",
        },
        {
            "name": api_c.END_DATE,
            "description": "End date.",
            "type": "string",
            "in": "query",
            "required": True,
            "example": "09-01-2019",
        },
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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[dict, int]:
        """Retrieves a Demographical customer insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int]: dict of Customer insights on demo overview,
                HTTP status code.
        """

        token_response = get_token_from_request(request)

        start_date, end_date = get_start_end_dates(request, 6)
        Validation.validate_date_range(start_date, end_date)

        # get customers overview data from CDP to set gender specific
        # population details
        customers = get_customers_overview(token_response[0])

        gender_spending = get_spending_by_gender(
            token_response[0],
            start_date,
            end_date,
        )

        output = {
            api_c.GENDER: {
                gender: {
                    api_c.POPULATION_PERCENTAGE: customers.get(gender, 0),
                    api_c.SIZE: customers.get(f"{gender}_{api_c.COUNT}", 0),
                }
                for gender in api_c.GENDERS
            },
            api_c.INCOME: get_spending_by_cities(token_response[0]),
            api_c.SPEND: group_gender_spending(gender_spending),
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
    """IDR Matching Trends YTD."""

    parameters = [
        {
            "name": api_c.START_DATE,
            "description": "Start date.",
            "type": "string",
            "in": "query",
            "required": False,
            "example": "05-01-2016",
        },
        {
            "name": api_c.END_DATE,
            "description": "End date.",
            "type": "string",
            "in": "query",
            "required": False,
            "example": "09-01-2019",
        },
    ]
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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use,unused-argument
    @api_error_handler()
    def get(self) -> Tuple[dict, int]:
        """Retrieves IDR Matching trends YTD data.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int]: dict of IDR Matching trends YTD,
                HTTP status code.
        """
        token_response = get_token_from_request(request)

        start_date, end_date = get_start_end_dates(request, 6)
        Validation.validate_date_range(start_date, end_date)

        return (
            jsonify(
                MatchingTrendsSchema().dump(
                    get_idr_matching_trends(
                        token_response[0],
                        start_date,
                        end_date,
                    ),
                    many=True,
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
    """Customer events under customer profile."""

    parameters = [
        {
            "name": api_c.HUX_ID,
            "description": "Unique HUX ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "HUX123456789012345",
        },
        {
            "name": "body",
            "description": "Customer Events Filters",
            "type": "object",
            "required": False,
            "in": "body",
            "example": {
                api_c.START_DATE: datetime.utcnow().strftime("%Y-01-01"),
                api_c.END_DATE: datetime.utcnow().strftime("%Y-%m-%d"),
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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def post(self, hux_id: str) -> Tuple[dict, int]:
        """Retrieves events for a given HUX ID.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            hux_id (str): ID of the customer

        Returns:
            Tuple[dict, int]: dict of Customer events grouped by day,
                HTTP status code.
        """
        token_response = get_token_from_request(request)

        Validation.validate_hux_id(hux_id)

        start_date, end_date = get_start_end_dates(request, 6)
        Validation.validate_date_range(start_date, end_date)

        return (
            jsonify(
                CustomerEventsSchema().dump(
                    get_customer_events_data(
                        token_response[0], hux_id, start_date, end_date
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
    """Total customer insights graph view class."""

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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[list, int]:
        """Retrieves total customer insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[list, int]: list of total customers & new customers added,
                HTTP status code.
        """

        # get auth token from request
        token_response = get_token_from_request(request)

        start_date, end_date = get_start_end_dates(request, 9)
        # create a dict for date_filters required by cdp endpoint
        date_filters = {
            api_c.START_DATE: start_date,
            api_c.END_DATE: end_date,
        }

        customers_insight_total = get_customers_insights_count_by_day(
            token_response[0], date_filters
        )

        return (
            jsonify(
                TotalCustomersInsightsSchema().dump(
                    customers_insight_total,
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.CUSTOMERS_INSIGHTS}/{api_c.COUNTRIES}",
    "CustomersInsightsCountries",
)
class CustomersInsightsCountries(SwaggerView):
    """Customer insights by country"""

    responses = {
        HTTPStatus.OK.value: {
            "schema": {
                "type": "array",
                "items": CustomersInsightsCountriesSchema,
            },
            "description": "Customer Insights by countries.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Customer Insights by countries."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[list, int]:
        """Retrieves country-level geographic customer insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[list, int]: list of spend and size data by country,
                HTTP status code.
        """

        # get auth token from request
        token_response = get_token_from_request(request)

        return (
            jsonify(
                CustomersInsightsCountriesSchema().dump(
                    get_demographic_by_country(token_response[0]),
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.CUSTOMERS_INSIGHTS}/{api_c.STATES}",
    "CustomersInsightsStates",
)
class CustomersInsightsStates(SwaggerView):
    """Customer insights by state."""

    responses = {
        HTTPStatus.OK.value: {
            "schema": {
                "type": "array",
                "items": CustomersInsightsStatesSchema,
            },
            "description": "Customer Insights by states.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Customer Insights by states."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[list, int]:
        """Retrieves state-level geographic customer insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[list, int]: list of spend and size data by state,
                HTTP status code.
        """

        # get auth token from request
        token_response = get_token_from_request(request)

        return (
            jsonify(
                CustomersInsightsStatesSchema().dump(
                    get_demographic_by_state(token_response[0]),
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    customers_bp,
    f"/{api_c.CUSTOMERS_INSIGHTS}/{api_c.CITIES}",
    "CustomersInsightsCities",
)
class CustomersInsightsCities(SwaggerView):
    """Customer insights by city."""

    parameters = [
        {
            "name": api_c.QUERY_PARAMETER_BATCH_SIZE,
            "in": "query",
            "type": "integer",
            "description": "Max number of cities to be returned.",
            "example": "5",
            "required": False,
            "default": api_c.CITIES_DEFAULT_BATCH_SIZE,
        },
        {
            "name": api_c.QUERY_PARAMETER_BATCH_NUMBER,
            "in": "query",
            "type": "string",
            "description": "Number of which batch of cities should be returned.",
            "example": "10",
            "required": False,
            "default": api_c.DEFAULT_BATCH_NUMBER,
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": {
                "type": "array",
                "items": CustomersInsightsCitiesSchema,
            },
            "description": "Customer Insights by cities.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Customer Insights by cities."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[list, int]:
        """Retrieves customer lifetime values.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[list, int]: list of spend and size by city, HTTP status code.
        """

        # get auth token from request
        token_response = get_token_from_request(request)

        batch_size = Validation.validate_integer(
            request.args.get(
                api_c.QUERY_PARAMETER_BATCH_SIZE,
                str(api_c.DEFAULT_BATCH_SIZE),
            )
        )

        batch_number = Validation.validate_integer(
            request.args.get(
                api_c.QUERY_PARAMETER_BATCH_NUMBER,
                str(api_c.DEFAULT_BATCH_NUMBER),
            )
        )

        return (
            jsonify(
                CustomersInsightsCitiesSchema().dump(
                    get_city_ltvs(
                        token_response[0],
                        offset=batch_size * (batch_number - 1),
                        limit=batch_size,
                    ),
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )
