# pylint: disable=no-self-use,disable=unused-argument
"""Paths for TrustID APIs."""

from http import HTTPStatus
from typing import Tuple

from flasgger import SwaggerView
from flask import Blueprint, request

from huxunifylib.database import constants as db_c
from huxunifylib.database.user_management import (
    get_user_trust_id_segments,
    add_user_trust_id_segments,
)

from huxunify.api import constants as api_c

from huxunify.api.route.decorators import (
    secured,
    add_view_to_blueprint,
    api_error_handler,
    requires_access_levels,
)

from huxunify.api.route.return_util import HuxResponse
from huxunify.api.route.utils import get_db_client
from huxunify.api.schema.trust_id import (
    TrustIdOverviewSchema,
    TrustIdAttributesSchema,
    TrustIdComparisonSchema,
    TrustIdSegmentFilterSchema,
    TrustIdSegmentPostSchema,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api.stubbed_data.trust_id_stub import (
    trust_id_overview_stub_data,
    trust_id_attribute_stub_data,
    trust_id_comparison_stub_data,
    trust_id_filters_stub,
)


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

    responses = {
        HTTPStatus.OK.value: {
            "description": "Trust ID overview data",
            "schema": TrustIdOverviewSchema,
        }
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.TRUST_ID_TAG]

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

        return HuxResponse.OK(
            data=trust_id_overview_stub_data,
            data_schema=TrustIdOverviewSchema(),
        )


@add_view_to_blueprint(
    trust_id_bp,
    f"{api_c.TRUST_ID_ENDPOINT}/attributes",
    "TrustIdAttributes",
)
class TrustIdAttributes(SwaggerView):
    """Trust ID attributes data fetch Class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "Trust ID attributes data",
            "schema": {"type": "array", "items": TrustIdAttributesSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to fetch signal data"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.TRUST_ID_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[list, int]:
        """Retrieves Trust ID attributes data.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[list, int]: list of attribute-wise data, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """

        return HuxResponse.OK(
            data=trust_id_attribute_stub_data,
            data_schema=TrustIdAttributesSchema(),
        )


@add_view_to_blueprint(
    trust_id_bp,
    f"{api_c.TRUST_ID_ENDPOINT}/comparison",
    "TrustIdAttributeComparison",
)
class TrustIdAttributeComparison(SwaggerView):
    """Trust ID comparison data fetch Class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "Trust ID comparison data",
            "schema": {"type": "array", "items": TrustIdComparisonSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to fetch comparison data"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.TRUST_ID_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[list, int]:
        """Retrieves Trust ID comparison data.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[list, int]: list of comparison data, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """

        return HuxResponse.OK(
            data=trust_id_comparison_stub_data,
            data_schema=TrustIdComparisonSchema(),
        )


@add_view_to_blueprint(
    trust_id_bp,
    f"{api_c.TRUST_ID_ENDPOINT}/user_filters",
    "TrustIdSegmentFilters",
)
class TrustIdSegmentFilters(SwaggerView):
    """Trust ID segment filters fetch Class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "Trust ID segment filters",
            "schema": {"type": "array", "items": TrustIdSegmentFilterSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to fetch comparison data"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.TRUST_ID_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[list, int]:
        """Retrieves Trust ID segment filters.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[list, int]: list of segment filters, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """

        return HuxResponse.OK(
            data=trust_id_filters_stub,
            data_schema=TrustIdSegmentFilterSchema(),
        )


@add_view_to_blueprint(
    trust_id_bp,
    f"{api_c.TRUST_ID_ENDPOINT}/segment",
    "TrustIdAddSegment",
)
class TrustIdAddSegment(SwaggerView):
    """Trust ID add segment class."""

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Segment with selected filters.",
            "example": {
                api_c.SEGMENT_NAME: "Segment 1",
                api_c.SEGMENT_FILTERS: [
                    {
                        api_c.TYPE: "age",
                        api_c.DESCRIPTION: "Age",
                        api_c.VALUES: ["18-20 years", "21-24 years"],
                    }
                ],
            },
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Trust ID segment added successfully",
            "schema": {"type": "array", "items": TrustIdComparisonSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to add new segment"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.TRUST_ID_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def post(self, user: dict) -> Tuple[list, int]:
        """Retrieves Trust ID segment filters.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[list, int]: list of segment filters, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """

        segment_details = TrustIdSegmentPostSchema().load(request.json)
        database = get_db_client()

        # Return the trust id segments for user
        segments = get_user_trust_id_segments(database, user[db_c.OKTA_ID])

        if len(segments) >= 5:
            return HuxResponse.FORBIDDEN(
                message="Threshold of maximum segments reached."
            )

        # Check if a segment with the specified name exists
        if segment_details[api_c.SEGMENT_NAME] in [
            x[api_c.SEGMENT_NAME] for x in segments
        ]:
            return HuxResponse.CONFLICT(
                message=(
                    f"Segment with name {segment_details[api_c.NAME]} "
                    f"already exists !"
                )
            )

        # pylint: disable=unused-variable
        updated_segments = add_user_trust_id_segments(
            database, user[db_c.OKTA_ID], segment_details
        )[db_c.TRUST_ID_SEGMENTS]

        # Update logic to filter trust id data based on added segments using updated_segments
        return HuxResponse.CREATED(
            data=trust_id_comparison_stub_data,
            data_schema=TrustIdComparisonSchema,
        )
