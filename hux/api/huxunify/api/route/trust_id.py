# pylint: disable=no-self-use,disable=unused-argument
"""Paths for TrustID APIs."""

from http import HTTPStatus
from typing import Tuple

from flasgger import SwaggerView
from flask import Blueprint
from huxunify.api import constants as api_c

from huxunify.api.route.decorators import (
    secured,
    add_view_to_blueprint,
    api_error_handler,
    requires_access_levels,
)

from huxunify.api.route.return_util import HuxResponse
from huxunify.api.schema.trust_id import (
    TrustIdOverviewSchema,
    TrustIdAttributesSchema,
    TrustIdComparisonSchema,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api.stubbed_data.trust_id_stub import (
    trust_id_overview_stub_data,
    trust_id_attribute_stub_data,
    trust_id_comparison_stub_data,
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
