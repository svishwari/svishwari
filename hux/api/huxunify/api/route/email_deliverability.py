# pylint: disable=no-self-use,disable=unused-argument
"""Paths for the email deliverability API."""
import datetime
from datetime import timedelta
from random import uniform, randint
from http import HTTPStatus
from typing import Tuple

from flasgger import SwaggerView
from flask import Blueprint, request
from huxunify.api import constants as api_c

from huxunify.api.route.decorators import (
    secured,
    add_view_to_blueprint,
    api_error_handler,
    requires_access_levels,
)

from huxunify.api.route.return_util import HuxResponse
from huxunify.api.route.utils import get_start_end_dates
from huxunify.api.schema.email_deliverability import (
    EmailDeliverabilityOverviewSchema,
    EmailDeliverabiliyDomainsSchema,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE

email_deliverability_bp = Blueprint(
    api_c.EMAIL_DELIVERABILITY_ENDPOINT, import_name=__name__
)


@email_deliverability_bp.before_request
@secured()
def before_request():
    """Protect all of the email_deliverability endpoints."""

    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    email_deliverability_bp,
    f"{api_c.EMAIL_DELIVERABILITY_ENDPOINT}/overview",
    "EmailDeliverabilityOverview",
)
class EmailDeliverabilityOverview(SwaggerView):
    """Email Deliverability overview Class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "Email deliverability overview data",
            "schema": EmailDeliverabilityOverviewSchema,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.MEASUREMENT_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves email deliverability overview data.

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

        # TODO Remove stub when email deliverability data available.

        delivered_open_rate_overview = []
        # Default 3 months.
        start_date, end_date = get_start_end_dates(request, delta=3)

        curr_date = datetime.datetime.strptime(
            start_date, api_c.DEFAULT_DATE_FORMAT
        )
        end_date = datetime.datetime.strptime(
            end_date, api_c.DEFAULT_DATE_FORMAT
        )

        while curr_date <= end_date:
            delivered_open_rate_overview.append(
                {
                    api_c.DATE: curr_date,
                    api_c.OPEN_RATE: uniform(0.6, 0.9),
                    api_c.DELIVERED_COUNT: randint(600, 900),
                }
            )
            curr_date = curr_date + timedelta(days=1)

        return HuxResponse.OK(
            data={
                api_c.OVERALL_INBOX_RATE: uniform(0.8, 0.95),
                api_c.SENDING_DOMAINS_OVERVIEW: api_c.SENDING_DOMAINS_OVERVIEW_STUB,
                api_c.DELIVERED_OPEN_RATE_OVERVIEW: delivered_open_rate_overview,
            },
            data_schema=EmailDeliverabilityOverviewSchema(),
        )


@add_view_to_blueprint(
    email_deliverability_bp,
    f"{api_c.EMAIL_DELIVERABILITY_ENDPOINT}/domains",
    "EmailDeliverabilityDomains",
)
class EmailDeliverabilityDomains(SwaggerView):
    """Email Deliverability domains test Class."""

    parameters = [
        {
            "name": api_c.DOMAIN_NAME,
            "description": "Only return data for the domains",
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "collectionFormat": "multi",
            "required": False,
            "example": "domain_1",
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Email deliverability domains data",
            "schema": EmailDeliverabiliyDomainsSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Could not fetch domain data"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.MEASUREMENT_TAG]

    # pylint: disable=too-many-locals
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves email deliverability domains data.

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

        # TODO Remove stub when email deliverability data available.

        sent_data = []

        unsubscribe_rate_data = []
        open_rate_data = []
        click_rate_data = []
        complaints_rate_data = []
        delivered_rate_data = []

        percent_data_field_list = [
            unsubscribe_rate_data,
            open_rate_data,
            click_rate_data,
            complaints_rate_data,
            delivered_rate_data,
        ]

        domains = request.args.getlist(api_c.DOMAIN_NAME)
        if not domains:
            domains = api_c.ALLOWED_EMAIL_DOMAIN_NAMES
        else:
            for domain_name in domains:
                if domain_name not in api_c.ALLOWED_EMAIL_DOMAIN_NAMES:
                    return HuxResponse.BAD_REQUEST(
                        message=f"Domain name"
                        f" {domain_name} "
                        f"is invalid."
                    )
        # Default 3 months.
        start_date, end_date = get_start_end_dates(request, delta=3)

        curr_date = datetime.datetime.strptime(
            start_date, api_c.DEFAULT_DATE_FORMAT
        )

        end_date = datetime.datetime.strptime(
            end_date, api_c.DEFAULT_DATE_FORMAT
        )

        while curr_date <= end_date:
            count_data = {domain: randint(400, 900) for domain in domains}
            count_data.update({api_c.DATE: curr_date})

            sent_data.append(count_data)

            for i in range(5):
                percent_data = {
                    domain: uniform(0.4, 0.8) for domain in domains
                }
                percent_data.update({api_c.DATE: curr_date})
                percent_data_field_list[i].append(percent_data)

            curr_date = curr_date + timedelta(days=1)

        return HuxResponse.OK(
            data={
                api_c.SENT: sent_data,
                api_c.DELIVERED_RATE: delivered_rate_data,
                api_c.OPEN_RATE: open_rate_data,
                api_c.CLICK_RATE: click_rate_data,
                api_c.UNSUBSCRIBE_RATE: unsubscribe_rate_data,
                api_c.COMPLAINTS_RATE: complaints_rate_data,
            },
            data_schema=EmailDeliverabiliyDomainsSchema(),
        )
