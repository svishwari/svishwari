# pylint: disable=no-self-use,disable=unused-argument
"""Paths for the email deliverability API."""
import datetime
from datetime import timedelta
from random import uniform, randint
from http import HTTPStatus
from typing import Tuple

from flasgger import SwaggerView
from flask import Blueprint, request

from huxunifylib.database import constants as db_c
from huxunifylib.database.collection_management import get_distinct_values
from huxunifylib.database.deliverability_metrics_management import (
    get_overall_inbox_rate,
    get_deliverability_data_performance_metrics,
)

from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.data_connectors.email_deliverability_metrics import (
    get_delivered_rate_data,
    get_performance_metrics_deliverability_data,
)

from huxunify.api.route.decorators import (
    secured,
    add_view_to_blueprint,
    api_error_handler,
    requires_access_levels,
)

from huxunify.api.route.return_util import HuxResponse
from huxunify.api.route.utils import (
    get_start_end_dates,
    get_db_client,
    clean_domain_name_string,
)
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

        end_date = datetime.datetime.strptime(
            end_date, api_c.DEFAULT_DATE_FORMAT
        )

        database = get_db_client()
        overall_inbox_rate = get_overall_inbox_rate(database)

        # TODO Remove when email deliverability overview data is available.
        domains = get_distinct_values(
            database, db_c.DELIVERABILITY_METRICS_COLLECTION, db_c.DOMAIN
        )
        domain_name = domains[0] if domains else api_c.DOMAIN_1
        api_c.SENDING_DOMAINS_OVERVIEW_STUB[0][api_c.DOMAIN_NAME] = domain_name

        performance_metrics_data = get_deliverability_data_performance_metrics(
            database=database,
            start_date=start_date,
            end_date=end_date,
            mock=bool(get_config().FLASK_ENV == api_c.TEST_MODE),
        )

        for domain_data in performance_metrics_data:
            for metrics in domain_data.get(db_c.DELIVERABILITY_METRICS):
                delivered_open_rate_overview.append(
                    {
                        api_c.DATE: metrics.get(api_c.DATE),
                        api_c.OPEN_RATE: metrics.get(api_c.OPEN_RATE),
                        api_c.DELIVERED_COUNT: metrics.get(api_c.DELIVERED),
                    }
                )

        aggregated_data = get_deliverability_data_performance_metrics(
            database=database,
            domains=[domain_name],
            start_date=start_date,
            end_date=end_date,
            aggregate=True,
            mock=bool(get_config().FLASK_ENV == api_c.TEST_MODE),
        )

        return HuxResponse.OK(
            data={
                api_c.OVERALL_INBOX_RATE: round(overall_inbox_rate, 2),
                api_c.SENDING_DOMAINS_OVERVIEW: aggregated_data,
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

        database = get_db_client()
        allowed_domains = get_distinct_values(
            database, db_c.DELIVERABILITY_METRICS_COLLECTION, db_c.DOMAIN
        )
        # In case no domains in database.
        allowed_domains = (
            allowed_domains
            if allowed_domains
            else api_c.ALLOWED_EMAIL_DOMAIN_NAMES
        )

        if not domains:
            # TODO remove when UI supports multiple domains.
            # By default single domain is supported.
            domains = [allowed_domains[0]]
        else:
            for domain_name in domains:
                if domain_name not in allowed_domains:
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
            count_data = {
                clean_domain_name_string(domain): randint(400, 900)
                for domain in domains
            }
            count_data.update({api_c.DATE: curr_date})

            sent_data.append(count_data)

            for i in range(5):
                percent_data = {
                    clean_domain_name_string(domain): round(
                        uniform(0.6, 0.9), 2
                    )
                    for domain in domains
                }
                percent_data.update({api_c.DATE: curr_date})
                percent_data_field_list[i].append(percent_data)
            curr_date = curr_date + timedelta(days=1)

        data = {
            api_c.DELIVERED_RATE: get_delivered_rate_data(
                database=database,
                domains=domains,
                start_date=datetime.datetime.strptime(
                    start_date, api_c.DEFAULT_DATE_FORMAT
                ),
                end_date=end_date,
            )
        }

        performance_metrics = get_performance_metrics_deliverability_data(
            database=database,
            domains=domains,
            start_date=datetime.datetime.strptime(
                start_date, api_c.DEFAULT_DATE_FORMAT
            ),
            end_date=end_date,
        )
        data.update(performance_metrics)

        return HuxResponse.OK(
            data=data,
            data_schema=EmailDeliverabiliyDomainsSchema(),
        )
