# pylint: disable=no-self-use,disable=unused-argument
"""Paths for TrustID APIs."""

from http import HTTPStatus
from typing import Tuple

from flasgger import SwaggerView
from flask import Blueprint, request
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.trust_id import (
    get_trust_id_overview_data,
    get_trust_id_signal_data,
)

from huxunify.api.route.decorators import (
    secured,
    add_view_to_blueprint,
    api_error_handler,
    requires_access_levels,
)

from huxunify.api.route.return_util import HuxResponse
from huxunify.api.schema.trust_id import (
    TrustIdOverviewSchema,
    SignalOverviewSchema,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE

trust_id_bp = Blueprint(api_c.TRUST_ID_ENDPOINT, import_name=__name__)


@trust_id_bp.before_request
@secured()
def before_request():
    """Protect all of the trust_id_bp endpoints."""

    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    trust_id_bp,
    f"{api_c.TRUST_ID_ENDPOINT}/overview",
    "TrustIdOverview",
)
class TrustIdOverview(SwaggerView):
    """Trust ID overview Class."""

    # TODO build parameters dynamically when Trust ID serves dynamic filters.
    parameters = [
        {
            "name": api_c.MIN_AGE,
            "description": "Minimum age of customers for Trust ID scores.",
            "in": "query",
            "type": "integer",
            "required": False,
            "example": 23,
        },
        {
            "name": api_c.MAX_AGE,
            "description": "Maximum age of customers for Trust ID scores.",
            "in": "query",
            "type": "integer",
            "required": False,
            "example": 23,
        },
        {
            "name": api_c.GENDER,
            "description": "Gender of customers for Trust ID scores.",
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "collectionFormat": "multi",
            "required": False,
            "example": "male",
        },
        {
            "name": api_c.OCCUPATION,
            "description": "Gender of customers for Trust ID scores.",
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "collectionFormat": "multi",
            "required": False,
            "example": "male",
        },
        {
            "name": api_c.CUSTOMER_TYPE,
            "description": "Gender of customers for Trust ID scores.",
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "collectionFormat": "multi",
            "required": False,
            "example": "male",
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Trust ID overview data",
            "schema": TrustIdOverviewSchema,
        }
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.INSIGHTS]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves Trust ID overview data.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int]: dict of user, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """

        applied_filters = {}

        # TODO Remove stub when Trust ID dynamic filters available.
        # get all list based args
        for list_filter in filter(
            lambda x: x[api_c.TYPE] == "list",
            api_c.TRUST_ID_SUPPORTED_FILTERS_STUB,
        ):
            if request.args.getlist(list_filter.get(api_c.NAME)):
                applied_filters[
                    list_filter.get(api_c.NAME)
                ] = request.args.getlist(list_filter.get(api_c.NAME))

        # get all range based args
        for range_filter in filter(
            lambda x: x[api_c.TYPE] == "range",
            api_c.TRUST_ID_SUPPORTED_FILTERS_STUB,
        ):
            if request.args.get("min_" + range_filter.get(api_c.NAME)):
                applied_filters[
                    "min_" + range_filter.get(api_c.NAME)
                ] = request.args.get("min_" + range_filter.get(api_c.NAME))

            if request.args.get("max_" + range_filter.get(api_c.NAME)):
                applied_filters[
                    "max_" + range_filter.get(api_c.NAME)
                ] = request.args.get("max_" + range_filter.get(api_c.NAME))

        overview_data = get_trust_id_overview_data(applied_filters)
        overview_data[
            api_c.ALLOWED_FILTERS
        ] = api_c.TRUST_ID_SUPPORTED_FILTERS_STUB

        return HuxResponse.OK(
            data=overview_data,
            data_schema=TrustIdOverviewSchema(),
        )


@add_view_to_blueprint(
    trust_id_bp,
    f"{api_c.TRUST_ID_ENDPOINT}/signal/<signal_name>",
    "TrustIdSignal",
)
class TrustIdSignal(SwaggerView):
    """Trust ID signal data fetch Class."""

    # TODO build parameters dynamically when Trust ID serves dynamic filters.
    parameters = [
        {
            "name": api_c.SIGNAL_NAME,
            "description": "Signal name",
            "type": "string",
            "in": "path",
            "required": True,
            "example": api_c.CAPABILITY,
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Trust ID signal data",
            "schema": SignalOverviewSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to fetch signal data"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.INSIGHTS]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, signal_name: str, user: dict) -> Tuple[dict, int]:
        """Retrieves Trust ID signal data.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            signal_name (str): Name of the signal to fetch the data for.
            user (dict): user object.

        Returns:
            Tuple[dict, int]: dict of user, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """

        # TODO Remove stub when Trust ID data available.
        if signal_name not in api_c.LIST_OF_SIGNALS:
            HuxResponse.BAD_REQUEST(
                f"Signal name {signal_name} not supported."
            )

        return HuxResponse.OK(
            data=get_trust_id_signal_data(signal_name),
            data_schema=SignalOverviewSchema(),
        )
