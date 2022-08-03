# pylint: disable=no-self-use,too-many-lines,unused-argument
"""Paths for customer API"""
from http import HTTPStatus
from typing import Tuple
from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask import Blueprint, request, jsonify, Response
from flasgger import SwaggerView
from huxunifylib.util.general.logging import logger

from huxunifylib.database.cache_management import (
    create_cache_entry,
    get_cache_entry,
)

from huxunify.api.config import get_config
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
    CustomerRevenueInsightsSchema,
)
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    requires_access_levels,
)
from huxunify.api.data_connectors.cache import Caching
from huxunify.api.data_connectors.okta import (
    get_token_from_request,
)
from huxunify.api.data_connectors.cdp import (
    get_customer_profiles,
    get_customer_profile,
    get_customers_overview,
    get_customer_events_data,
    get_demographic_by_state,
    get_spending_by_cities,
    get_customers_insights_count_by_day,
    get_city_ltvs,
    get_spending_by_gender,
    get_demographic_by_country,
    get_revenue_by_day,
    get_customer_event_types,
)
from huxunify.api.data_connectors.cdp_connection import (
    get_idr_data_feeds,
    get_idr_data_feed_details,
    get_idr_matching_trends,
    get_identity_overview,
)
from huxunify.api.route.utils import (
    add_chart_legend,
    get_start_end_dates,
    get_db_client,
    convert_unique_city_filter,
    convert_filters_for_events,
    convert_filters_for_contact_preference,
)
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
from huxunify.api.route.utils import group_gender_spending, Validation

customers_bp = Blueprint(
    api_c.CUSTOMERS_ENDPOINT, import_name=__name__, url_prefix="/cdp"
)


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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves a customer data overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object

        Returns:
            Tuple[dict, int]: dict of Customer data overview, HTTP status code.
        """

        # check if cache entry
        token_response = get_token_from_request(request)
        customers_overview = Caching.check_and_return_cache(
            f"{api_c.CUSTOMERS_ENDPOINT}.{api_c.OVERVIEW}",
            get_customers_overview,
            {"token": token_response[0]},
        )

        customers_overview[api_c.IDR_INSIGHTS] = Caching.check_and_return_cache(
            f"{api_c.IDR_ENDPOINT}.{api_c.OVERVIEW}",
            get_identity_overview,
            {"token": token_response[0]},
        )

        customers_overview[api_c.GEOGRAPHICAL] = Caching.check_and_return_cache(
            f"{api_c.CUSTOMERS_ENDPOINT}.{api_c.GEOGRAPHICAL}",
            get_demographic_by_state,
            {
                "token": token_response[0],
                "filters": api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER[
                    api_c.AUDIENCE_FILTERS
                ],
            },
        )

        return (
            CustomerOverviewSchema().dump(customers_overview),
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def post(self, user: dict) -> Tuple[dict, int]:
        """Retrieves the overview of customer data with the requested filters
        applied.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc

        Returns:
            Tuple[dict, int]: dict of Customer data overview, HTTP status code.
        """

        # filter out any invalid filters.
        if any(
            y
            for x in request.json.get(api_c.AUDIENCE_FILTERS, [])
            for y in x.get(api_c.AUDIENCE_SECTION_FILTERS, [])
            if y == {api_c.AUDIENCE_FILTER_VALUE: ""}
        ):
            logger.error("Invalid filter passed in to retrieve customer data overview.")
            return (
                CustomerOverviewSchema().dump({}),
                HTTPStatus.OK,
            )

        token_response = get_token_from_request(request)

        # Fetch events from CDM. Check cache first.
        event_types = Caching.check_and_return_cache(
            f"{api_c.CUSTOMERS_ENDPOINT}.{api_c.EVENTS}",
            get_customer_event_types,
            {"token": token_response[0]},
        )

        filters = convert_unique_city_filter(request.json)
        convert_filters_for_events(filters, event_types)
        convert_filters_for_contact_preference(filters=filters, convert_for_cdm=True)

        # check range filters
        # if a range type was passed in but range is empty.
        # instead of raising 500, lets return empty and log the error instead.
        for audience_filter in filters.get(api_c.AUDIENCE_FILTERS, []):
            for section_filter in audience_filter.get(
                api_c.AUDIENCE_SECTION_FILTERS, []
            ):
                if section_filter.get(
                    api_c.TYPE
                ) == api_c.AUDIENCE_FILTER_RANGE and not section_filter.get(
                    api_c.VALUE, False
                ):
                    logger.error(
                        "Invalid range filter passed in to retrieve customer data overview."
                    )
                    return (
                        CustomerOverviewSchema().dump({}),
                        HTTPStatus.OK,
                    )

        customers_overview = Caching.check_and_return_cache(
            {
                "endpoint": f"{api_c.CUSTOMERS_ENDPOINT}.{api_c.OVERVIEW}",
                **filters,
            },
            get_customers_overview,
            {"token": token_response[0], api_c.AUDIENCE_FILTERS: filters},
        )

        customers_overview[api_c.IDR_INSIGHTS] = Caching.check_and_return_cache(
            {"endpoint": f"{api_c.IDR_ENDPOINT}.{api_c.OVERVIEW}", **filters},
            get_identity_overview,
            {"token": token_response[0], api_c.AUDIENCE_FILTERS: filters},
        )

        customers_overview[api_c.GEOGRAPHICAL] = Caching.check_and_return_cache(
            {
                "endpoint": f"{api_c.CUSTOMERS_ENDPOINT}.{api_c.GEOGRAPHICAL}",
                **filters,
            },
            get_demographic_by_state,
            {
                "token": token_response[0],
                "filters": request.json[api_c.AUDIENCE_FILTERS],
            },
        )

        return (
            CustomerOverviewSchema().dump(customers_overview),
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

    # pylint: disable=no-self-use,too-many-locals
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves a customer data dashboard overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc

        Returns:
            Tuple[dict, int]: dict of Customer data overview, HTTP status code.
        """
        current_env = get_config().ENV_NAME

        # default to five years lookup to find the event date range.
        start_date, end_date = get_start_end_dates(request, 60)
        Validation.validate_date_range(start_date, end_date)

        cache_key = f"{api_c.IDR_TAG}.{start_date}.{end_date}"

        if current_env == "RC1":
            start_date = datetime.strftime(
                datetime.utcnow().date() - relativedelta(months=60),
                api_c.DEFAULT_DATE_FORMAT,
            )
            end_date = datetime.strftime(
                datetime.utcnow().date(),
                api_c.DEFAULT_DATE_FORMAT,
            )

        # check if cache entry
        database = get_db_client()
        idr_overviews = get_cache_entry(
            database,
            cache_key,
        )
        if not idr_overviews:
            token_response = get_token_from_request(request)

            # TODO - when the CDP endpoint for getting the max and min date range
            #  is available, we will call that instead of iterating all events to get them.
            # get date range from IDR matching trends.
            trend_data = get_idr_matching_trends(
                token_response[0],
                start_date,
                end_date,
            )

            # get IDR overview
            idr_overview = get_identity_overview(
                token_response[0],
                {
                    api_c.START_DATE: start_date,
                    api_c.END_DATE: end_date,
                },
            )

            # cache
            create_cache_entry(
                database,
                cache_key,
                {
                    api_c.OVERVIEW: idr_overview,
                    api_c.MATCHING_TRENDS: trend_data,
                },
            )
        else:
            idr_overview = idr_overviews.get(api_c.OVERVIEW)
            trend_data = idr_overviews.get(api_c.MATCHING_TRENDS)

        return (
            IDROverviewWithDateRangeSchema().dump(
                {
                    api_c.OVERVIEW: idr_overview,
                    api_c.DATE_RANGE: {
                        api_c.START_DATE: min([x[api_c.DAY] for x in trend_data])
                        if trend_data
                        else datetime.strptime(start_date, api_c.DEFAULT_DATE_FORMAT),
                        api_c.END_DATE: max([x[api_c.DAY] for x in trend_data])
                        if trend_data
                        else datetime.strptime(end_date, api_c.DEFAULT_DATE_FORMAT),
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
        HTTPStatus.BAD_REQUEST.value: {"description": "Failed to get customers."},
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves a list of customers.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc

        Returns:
            Tuple[dict, int]: dict of Customers, HTTP status code.
        """

        # get token
        token_response = get_token_from_request(request)
        database = get_db_client()

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

        if user.get(api_c.USER_PII_ACCESS) is True:
            redacted_data = get_customer_profiles(token_response[0], batch_size, offset)
        else:
            Caching.check_and_return_cache(
                f"{api_c.CUSTOMERS_ENDPOINT}.{batch_number}.{batch_size}",
                get_customer_profiles,
                {
                    "token": token_response[0],
                    "batch_size": batch_size,
                    "offset": offset,
                },
            )
            redacted_data = get_cache_entry(
                database,
                f"{api_c.CUSTOMERS_ENDPOINT}.{batch_number}.{batch_size}",
            )
            if not redacted_data:
                customer_list = get_customer_profiles(
                    token_response[0], batch_size, offset
                )
                redacted_data = {
                    api_c.TOTAL_CUSTOMERS: customer_list.get(api_c.TOTAL_CUSTOMERS),
                    api_c.CUSTOMERS_TAG: [
                        redact_fields(x, api_c.CUSTOMER_PROFILE_REDACTED_FIELDS)
                        for x in customer_list.get(api_c.CUSTOMERS_TAG)
                    ],
                }
                create_cache_entry(
                    database,
                    f"{api_c.CUSTOMERS_ENDPOINT}.{batch_number}.{batch_size}",
                    redacted_data,
                )

        return (
            CustomersSchema().dump(redacted_data),
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
        },
        {
            "name": api_c.REDACT_FIELD,
            "description": "Redact Field",
            "type": "boolean",
            "in": "query",
            "required": False,
            "example": "True",
        },
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, hux_id: str, user: dict) -> Tuple[dict, int]:
        """Retrieves a customer profile.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc
            hux_id (str): ID of the customer.

        Returns:
            Tuple[dict, int]: dict of customer profile, HTTP status code.
        """
        token_response = get_token_from_request(request)
        redact = Validation.validate_bool(request.args.get(api_c.REDACT_FIELD, "True"))

        if user.get(api_c.USER_PII_ACCESS) is True and not redact:
            redacted_data = get_customer_profile(token_response[0], hux_id)
        else:
            redacted_data = redact_fields(
                get_customer_profile(token_response[0], hux_id),
                api_c.CUSTOMER_PROFILE_REDACTED_FIELDS,
            )

        return (
            CustomerProfileSchema().dump(
                {
                    api_c.OVERVIEW: redacted_data,
                    api_c.INSIGHTS: redacted_data,
                    api_c.CONTACT_PREFERENCES: redacted_data,
                    api_c.IDENTITY_RESOLUTION: add_chart_legend(
                        redacted_data.get(api_c.IDENTITY_RESOLUTION, {})
                    ),
                    api_c.USER_PII_ACCESS: user[api_c.USER_PII_ACCESS],
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
        HTTPStatus.BAD_REQUEST.value: {"description": "Failed to get IDR Data Feeds."},
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use,unused-argument
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[Response, int]:
        """Retrieves all IDR data feeds.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc

        Returns:
            Tuple[Response, int]: Response list of IDR data feeds object dicts,
                HTTP status code.
        """

        token_response = get_token_from_request(request)

        start_date, end_date = get_start_end_dates(request, 6)
        Validation.validate_date_range(start_date, end_date)

        data_feeds = Caching.check_and_return_cache(
            f"{api_c.IDR_ENDPOINT}.{api_c.DATAFEEDS}.{start_date}.{end_date}",
            get_idr_data_feeds,
            {
                "token": token_response[0],
                "start_date": start_date,
                "end_date": end_date,
            },
        )

        return (
            jsonify(
                DataFeedSchema().dump(
                    data_feeds,
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, datafeed_id: str, user: dict) -> Tuple[dict, int]:
        """Retrieves an IDR data feed waterfall report.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            datafeed_id (str): Data feed ID.
            user (dict): User object.

        Returns:
            Tuple[dict, int]: dict of IDR data feed waterfall,
                HTTP status code.
        """

        token_response = get_token_from_request(request)
        datafeed_id = Validation.validate_integer(datafeed_id)

        data_feed = Caching.check_and_return_cache(
            f"{api_c.IDR_ENDPOINT}.{api_c.DATAFEEDS}." f"{datafeed_id}",
            get_idr_data_feed_details,
            {"token": token_response[0], "datafeed_id": datafeed_id},
        )
        # TODO Only for demo purpose remove after actual data integration
        if get_config().ENV_NAME == "RC1":
            start_date, end_date = get_start_end_dates(request, 6)
            Validation.validate_date_range(start_date, end_date)

            data_feeds = Caching.check_and_return_cache(
                f"{api_c.IDR_ENDPOINT}.{api_c.DATAFEEDS}.{start_date}.{end_date}",
                get_idr_data_feeds,
                {
                    "token": token_response[0],
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )
            stub_end_date = datetime.utcnow() - relativedelta(days=1)
            delta_days = (
                stub_end_date - max([data[api_c.TIMESTAMP] for data in data_feeds])
            ).days
            data_feed[api_c.STITCHED][api_c.STITCHED_TIMESTAMP] = data_feed[
                api_c.STITCHED
            ][api_c.STITCHED_TIMESTAMP] + relativedelta(days=delta_days)
            data_feed[api_c.PINNING][api_c.PINNING_TIMESTAMP] = data_feed[
                api_c.PINNING
            ][api_c.PINNING_TIMESTAMP] + relativedelta(days=delta_days)
        return (
            DataFeedDetailsSchema().dump(data_feed),
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
            "description": "Customer Profiles Geographical Insights.",
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
        custom_message={ZeroDivisionError: {"message": api_c.ZERO_AUDIENCE_SIZE}}
    )
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[Response, int]:
        """Retrieves a Customer profiles geographical insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc

        Returns:
            Tuple[Response, int]: Response list of Customer insights on geo overview,
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
            "description": "Customer Demographic Visual Insights.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get customers Demographic Visual Insights."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves customer demographic insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc

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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[Response, int]:
        """Retrieves IDR Matching trends YTD data.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc

        Returns:
            Tuple[Response, int]: Response dict of IDR Matching trends YTD,
                HTTP status code.
        """
        token_response = get_token_from_request(request)

        start_date, end_date = get_start_end_dates(request, 6)
        Validation.validate_date_range(start_date, end_date)

        matching_trends = Caching.check_and_return_cache(
            f"{api_c.IDR_ENDPOINT}.{api_c.MATCHING_TRENDS}.{start_date}.{end_date}",
            get_idr_matching_trends,
            {
                "token": token_response[0],
                "start_date": start_date,
                "end_date": end_date,
            },
        )

        return (
            jsonify(
                MatchingTrendsSchema().dump(
                    matching_trends,
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
            "name": api_c.INTERVAL,
            "description": "Interval Unit.",
            "type": "string",
            "in": "query",
            "required": False,
            "example": "day",
            "default": "day",
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def post(self, hux_id: str, user: dict) -> Tuple[Response, int]:
        """Retrieves events for a given HUX ID.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            hux_id (str): ID of the customer
            user (dict): User object

        Returns:
            Tuple[Response, int]: Response dict of Customer events grouped by day,
                HTTP status code.
        """
        token_response = get_token_from_request(request)

        interval = request.args.get(api_c.INTERVAL, api_c.DAY).lower()

        if request.json:
            start_date = request.json.get(api_c.START_DATE)
            end_date = min(
                request.json.get(api_c.END_DATE),
                datetime.strftime(datetime.utcnow(), api_c.DEFAULT_DATE_FORMAT),
            )
        else:
            start_date, end_date = get_start_end_dates(request, 6)
        Validation.validate_date_range(start_date, end_date)

        return (
            jsonify(
                CustomerEventsSchema().dump(
                    get_customer_events_data(
                        token_response[0],
                        hux_id,
                        start_date,
                        end_date,
                        interval,
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[Response, int]:
        """Retrieves total customer insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc

        Returns:
            Tuple[Response, int]: Response list of total customers & new customers added,
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

        customers_insight_total = Caching.check_and_return_cache(
            f"{api_c.CUSTOMERS_INSIGHTS}.{api_c.TOTAL}.{start_date}.{end_date}",
            get_customers_insights_count_by_day,
            {"token": token_response[0], "date_filters": date_filters},
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
    f"/{api_c.CUSTOMERS_INSIGHTS}/{api_c.REVENUE}",
    "CustomersRevenueInsightsGraphView",
)
class CustomersRevenueInsightsGraphView(SwaggerView):
    """Customer revenue insights graph view class."""

    responses = {
        HTTPStatus.OK.value: {
            "schema": {
                "type": "array",
                "items": CustomerRevenueInsightsSchema,
            },
            "description": "Customer Revenue Insights .",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Customer Revenue Insights."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[Response, int]:
        """Retrieves customer revenue insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc

        Returns:
            Tuple[Response, int]: Response list of revenue details by date,
                HTTP status code.
        """

        # get auth token from request
        token_response = get_token_from_request(request)
        start_date, end_date = get_start_end_dates(request, 6)

        customers_revenue_insight = Caching.check_and_return_cache(
            f"{api_c.CUSTOMERS_INSIGHTS}.{api_c.REVENUE}.{start_date}.{end_date}",
            get_revenue_by_day,
            {
                "token": token_response[0],
                "start_date": start_date,
                "end_date": end_date,
            },
        )

        return (
            jsonify(
                CustomerRevenueInsightsSchema().dump(
                    customers_revenue_insight,
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[Response, int]:
        """Retrieves country-level geographic customer insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc

        Returns:
            Tuple[Response, int]: Response list of spend and size data by country,
                HTTP status code.
        """

        # get auth token from request
        token_response = get_token_from_request(request)

        customers_insight_countries = Caching.check_and_return_cache(
            f"{api_c.CUSTOMERS_INSIGHTS}.{api_c.COUNTRIES}",
            get_demographic_by_country,
            {"token": token_response[0]},
        )

        return (
            jsonify(
                CustomersInsightsCountriesSchema().dump(
                    customers_insight_countries,
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[Response, int]:
        """Retrieves state-level geographic customer insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc

        Returns:
            Tuple[Response, int]: Response list of spend and size data by state,
                HTTP status code.
        """

        # get auth token from request
        token_response = get_token_from_request(request)

        customers_insight_states = Caching.check_and_return_cache(
            f"{api_c.CUSTOMERS_INSIGHTS}.{api_c.STATES}",
            get_demographic_by_state,
            {"token": token_response[0]},
        )

        return (
            jsonify(
                CustomersInsightsStatesSchema().dump(
                    customers_insight_states,
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[Response, int]:
        """Retrieves city-level geographic customer insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User doc

        Returns:
            Tuple[Response, int]: Response list of spend and size by city, HTTP status code.
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

        customers_insight_cities = Caching.check_and_return_cache(
            f"{api_c.CUSTOMERS_INSIGHTS}.{api_c.CITIES}.{batch_number}.{batch_size}",
            get_city_ltvs,
            {
                "token": token_response[0],
                "offset": batch_size * (batch_number - 1),
                "limit": batch_size,
            },
        )

        return (
            jsonify(
                CustomersInsightsCitiesSchema().dump(
                    customers_insight_cities,
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )
