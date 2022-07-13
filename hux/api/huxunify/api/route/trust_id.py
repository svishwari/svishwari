# pylint: disable=no-self-use,disable=unused-argument
"""Paths for TrustID APIs."""
from http import HTTPStatus
from typing import Tuple

from flasgger import SwaggerView
from flask import Blueprint, request

from huxunifylib.database import constants as db_c, collection_management
from huxunifylib.database.cache_management import (
    get_cache_entry,
    create_cache_entry,
)
from huxunifylib.database.survey_metrics_management import get_survey_responses
from huxunifylib.database.user_management import (
    get_user_trust_id_segments,
    add_user_trust_id_segments,
    remove_user_trust_id_segments,
)

from huxunify.api import constants as api_c
from huxunify.api.data_connectors.trust_id import (
    populate_trust_id_segments,
    get_trust_id_attributes,
    get_trust_id_overview,
    get_trust_id_comparison_data,
)
from huxunify.api.route.decorators import (
    secured,
    add_view_to_blueprint,
    api_error_handler,
    requires_access_levels,
)

from huxunify.api.route.return_util import HuxResponse
from huxunify.api.route.utils import (
    get_db_client,
    Validation as validation,
)
from huxunify.api.schema.trust_id import (
    TrustIdOverviewSchema,
    TrustIdAttributesSchema,
    TrustIdComparisonSchema,
    TrustIdSegmentFilterSchema,
    TrustIdSegmentPostSchema,
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

    responses = {
        HTTPStatus.OK.value: {
            "description": "Trust ID overview data",
            "schema": TrustIdOverviewSchema,
        }
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.TRUST_ID_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.TRUST_ID_ROLE_ALL)
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

        trust_id_overview = get_cache_entry(
            get_db_client(), f"{api_c.TRUST_ID_TAG}.{api_c.OVERVIEW}"
        )
        if not trust_id_overview:
            survey_responses = get_survey_responses(get_db_client())
            trust_id_overview = get_trust_id_overview(survey_responses)

            # Cache TrustID overview data for 7 days
            create_cache_entry(
                database=get_db_client(),
                cache_key=f"{api_c.TRUST_ID_TAG}.{api_c.OVERVIEW}",
                cache_value=trust_id_overview,
            )

        return HuxResponse.OK(
            data=trust_id_overview,
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
            "description": "Failed to fetch factor data"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.TRUST_ID_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.TRUST_ID_ROLE_ALL)
    def get(self, user: dict) -> Tuple[list, int]:
        """Retrieves Trust ID trust_id_attributes data.

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
        trust_id_attributes = get_cache_entry(
            get_db_client(), f"{api_c.TRUST_ID_TAG}.{api_c.ATTRIBUTES}"
        )
        if not trust_id_attributes:
            survey_responses = get_survey_responses(get_db_client())

            trust_id_attributes = sorted(
                sorted(
                    get_trust_id_attributes(survey_responses),
                    key=lambda x: x[api_c.ATTRIBUTE_SCORE],
                    reverse=True,
                ),
                key=lambda x: x[api_c.FACTOR_NAME],
                reverse=False,
            )

            # Cache TrustID attribute data for 7 days
            create_cache_entry(
                database=get_db_client(),
                cache_key=f"{api_c.TRUST_ID_TAG}.{api_c.ATTRIBUTES}",
                cache_value=trust_id_attributes,
            )

        return HuxResponse.OK(
            data=trust_id_attributes,
            data_schema=TrustIdAttributesSchema(),
        )


@add_view_to_blueprint(
    trust_id_bp,
    f"{api_c.TRUST_ID_ENDPOINT}/comparison",
    "TrustIdAttributeComparison",
)
class TrustIdAttributeComparison(SwaggerView):
    """Trust ID comparison data fetch Class."""

    parameters = [
        {
            "name": api_c.DEFAULT,
            "description": "Flag for returning default segment.",
            "in": "query",
            "type": "boolean",
            "required": False,
            "default": True,
            "example": "False",
        }
    ]
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
    @requires_access_levels(api_c.TRUST_ID_ROLE_ALL)
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
        trust_id_comparison_data = get_cache_entry(
            database=get_db_client(),
            cache_key=f"{api_c.TRUST_ID_TAG}.comparison",
        )
        if not trust_id_comparison_data:
            add_default = validation.validate_bool(
                request.args.get(api_c.DEFAULT, "true")
            )

            custom_segments = get_user_trust_id_segments(
                database=get_db_client(), okta_id=user[db_c.OKTA_ID]
            )

            segments_data = populate_trust_id_segments(
                database=get_db_client(),
                custom_segments=custom_segments,
                add_default=add_default,
            )

            trust_id_comparison_data = get_trust_id_comparison_data(
                segments_data
            )

            # Cache Trust ID comparison data
            create_cache_entry(
                database=get_db_client(),
                cache_key=f"{api_c.TRUST_ID_TAG}.comparison",
                cache_value=trust_id_comparison_data,
            )

        return HuxResponse.OK(
            data=trust_id_comparison_data,
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
    @requires_access_levels(api_c.TRUST_ID_ROLE_ALL)
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
            data=collection_management.get_document(
                database=get_db_client(),
                collection=db_c.CONFIGURATIONS_COLLECTION,
                query_filter={
                    db_c.CONFIGURATION_FIELD_TYPE: db_c.TRUST_ID_FILTERS
                },
            ).get(db_c.TRUST_ID_FILTERS),
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
                        api_c.TYPE: "gender",
                        api_c.DESCRIPTION: "Gender",
                        api_c.VALUES: ["Female", "Male"],
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
    @requires_access_levels(api_c.TRUST_ID_ROLE_ALL)
    def post(self, user: dict) -> Tuple[list, int]:
        """Add Trust ID segment.

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

        if len(segments) >= api_c.MAX_SEGMENTS_ALLOWED:
            return HuxResponse.FORBIDDEN(
                message="Threshold of maximum segments reached."
            )

        added_segments = [
            segment.get(api_c.SEGMENT_NAME) for segment in segments
        ]
        # Check if a segment with the specified name exists
        if segment_details[api_c.SEGMENT_NAME] in added_segments:
            return HuxResponse.CONFLICT(
                message=("Segment with the given name already exists!")
            )

        updated_segments = add_user_trust_id_segments(
            database, user[db_c.OKTA_ID], segment_details
        )[db_c.TRUST_ID_SEGMENTS]

        segments_data = populate_trust_id_segments(
            database=get_db_client(), custom_segments=updated_segments
        )

        trust_id_comparison_data = get_trust_id_comparison_data(segments_data)

        # Create or update cache comparison data
        create_cache_entry(
            database=get_db_client(),
            cache_key=f"{api_c.TRUST_ID_TAG}.comparison",
            cache_value=trust_id_comparison_data,
        )

        return HuxResponse.CREATED(
            data=trust_id_comparison_data,
            data_schema=TrustIdComparisonSchema(),
        )


@add_view_to_blueprint(
    trust_id_bp,
    f"{api_c.TRUST_ID_ENDPOINT}/segment",
    "TrustIdRemoveSegment",
)
class TrustIdRemoveSegment(SwaggerView):
    """Trust ID remove segment class."""

    parameters = [
        {
            "name": "segment_name",
            "in": "query",
            "type": "string",
            "description": "Name of segment to remove.",
            "example": "Segment 1",
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Trust ID segment removed successfully",
            "schema": {"type": "array", "items": TrustIdComparisonSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to remove segment"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.TRUST_ID_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.TRUST_ID_ROLE_ALL)
    def delete(self, user: dict) -> Tuple[list, int]:
        """Remove Trust ID segment.

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

        segment_name = request.args.get(api_c.SEGMENT_NAME)
        if not segment_name:
            return HuxResponse.BAD_REQUEST(
                message="Missing required segment name."
            )

        updated_segments = remove_user_trust_id_segments(
            get_db_client(), user[db_c.OKTA_ID], segment_name
        )[db_c.TRUST_ID_SEGMENTS]

        segments_data = populate_trust_id_segments(
            database=get_db_client(), custom_segments=updated_segments
        )

        trust_id_comparison_data = get_trust_id_comparison_data(segments_data)

        # Create or update cache comparison data
        create_cache_entry(
            database=get_db_client(),
            cache_key=f"{api_c.TRUST_ID_TAG}.comparison",
            cache_value=trust_id_comparison_data,
        )

        return HuxResponse.OK(
            data=trust_id_comparison_data,
            data_schema=TrustIdComparisonSchema(),
        )
