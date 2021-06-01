# pylint: disable=no-self-use
"""
Paths for customer API
"""

from http import HTTPStatus
from typing import Tuple

from flask import Blueprint
from flask_apispec import marshal_with
from flasgger import SwaggerView

from huxunify.api.data_connectors import cdp
from huxunify.api.schema.customers import CustomerProfileSchema
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    handle_api_exception,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c

customer_bp = Blueprint(api_c.CUSTOMERS_ENDPOINT, import_name=__name__)


@add_view_to_blueprint(
    customer_bp,
    f"{api_c.CUSTOMERS_ENDPOINT}/<customer_id>",
    "CustomerProfileSearch",
)
class CustomerProfileSearch(SwaggerView):
    """
    Individual Customer Profile Search Class
    """

    parameters = [
        {
            "name": api_c.CUSTOMER_ID,
            "description": "Customer ID.",
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
    tags = ([api_c.CUSTOMERS_TAG],)

    # pylint: disable=no-self-use
    @marshal_with(CustomerProfileSchema)
    def get(self, customer_id: str) -> Tuple[dict, int]:
        """Retrieves a customer profile.

        Args:
            customer_id: ID of the customer

        Returns:
            Tuple[dict, int]: dict of customer profile and http code

        """

        try:
            return cdp.get_customer_profile(customer_id), HTTPStatus.OK.value
        except Exception as exc:
            raise handle_api_exception(
                exc, "Unable to get customer profile."
            ) from exc
