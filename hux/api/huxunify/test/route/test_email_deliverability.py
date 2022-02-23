# pylint: disable=too-many-public-methods
"""Tests for email deliverability APIs."""
import datetime
from http import HTTPStatus
from unittest import mock

from huxunify.api.schema.email_deliverability import (
    EmailDeliverabilityOverviewSchema,
    EmailDeliverabiliyDomainsSchema,
)
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase

import huxunify.test.constants as t_c
from huxunify.api import constants as api_c

from huxunifylib.database import constants as db_c
from huxunifylib.database.delivery_platform_management import (
    set_deliverability_metrics,
    set_delivery_platform,
)


class TestDestinationRoutes(RouteTestCase):
    """Test Destination Routes."""

    def setUp(self) -> None:
        """Setup resources before each test."""

        super().setUp()

        # mock get db client from destinations
        mock.patch(
            "huxunify.api.route.email_deliverability.get_db_client",
            return_value=self.database,
        ).start()

        self.delivery_platform_doc = set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_SPARKPOST,
            "My delivery platform for Sparkpost",
        )

        set_deliverability_metrics(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            delivery_platform_type="sparkpost",
            metrics_dict={
                "domain_inbox_percentage": 0.49605484706467184,
                "isp_metrics": [
                    {
                        "isp_name": "Gmail",
                        "isp_inbox_percentage": 0.49605484706467184,
                    },
                    {
                        "isp_name": "Mail.com",
                        "isp_inbox_percentage": 0.1994866805871396,
                    },
                ],
            },
            start_time=datetime.datetime.utcnow(),
            end_time=datetime.datetime.utcnow(),
            domain="domain_1",
        )

    def test_email_deliverability_overview(self):
        """Test for email_deliverability overview endpoint."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/"
            f"{api_c.EMAIL_DELIVERABILITY_ENDPOINT}/overview",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                EmailDeliverabilityOverviewSchema(), response.json
            )
        )
        self.assertEqual(
            api_c.SENDING_DOMAINS_OVERVIEW_STUB,
            response.json.get(api_c.SENDING_DOMAINS_OVERVIEW),
        )

    def test_email_deliverability_all_domain_data(self):
        """Test email deliverability data for all domains."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/"
            f"{api_c.EMAIL_DELIVERABILITY_ENDPOINT}/domains",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                EmailDeliverabiliyDomainsSchema(), response.json
            )
        )

        # Ensure all domains present in data.
        self.assertIn(api_c.DOMAIN_1, response.json.get(api_c.SENT)[0].keys())

    def test_email_deliverability_select_domain_data(self):
        """Test email deliverability data for select domains."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/"
            f"{api_c.EMAIL_DELIVERABILITY_ENDPOINT}/domains?"
            f"{api_c.DOMAIN_NAME}={api_c.DOMAIN_1}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                EmailDeliverabiliyDomainsSchema(), response.json
            )
        )

        self.assertIn(api_c.DOMAIN_1, response.json.get(api_c.SENT)[0].keys())

    def test_email_deliverability_invalid_domain(self):
        """Test email deliverability data for select domains."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/"
            f"{api_c.EMAIL_DELIVERABILITY_ENDPOINT}/domains?"
            f"{api_c.DOMAIN_NAME}={api_c.OPEN_RATE}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
