# pylint: disable=too-many-public-methods
"""Tests for email deliverability APIs."""

from http import HTTPStatus

from huxunify.api.schema.email_deliverability import (
    EmailDeliverabilityOverviewSchema,
    EmailDeliverabiliyDomainsSchema,
)
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase

import huxunify.test.constants as t_c
from huxunify.api import constants as api_c


class TestDestinationRoutes(RouteTestCase):
    """Test Destination Routes."""

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
        self.assertIn(api_c.DOMAIN_2, response.json.get(api_c.SENT)[0].keys())
        self.assertIn(api_c.DOMAIN_3, response.json.get(api_c.SENT)[0].keys())

    def test_email_deliverability_select_domain_data(self):
        """Test email deliverability data for select domains."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/"
            f"{api_c.EMAIL_DELIVERABILITY_ENDPOINT}/domains?"
            f"{api_c.DOMAIN_NAME}={api_c.DOMAIN_1}&"
            f"{api_c.DOMAIN_NAME}={api_c.DOMAIN_2}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                EmailDeliverabiliyDomainsSchema(), response.json
            )
        )

        # Ensure 2 domains present in data.
        self.assertIn(api_c.DOMAIN_1, response.json.get(api_c.SENT)[0].keys())
        self.assertIn(api_c.DOMAIN_2, response.json.get(api_c.SENT)[0].keys())

        # Ensure 3rd domain not present in data.
        self.assertNotIn(
            api_c.DOMAIN_3, response.json.get(api_c.SENT)[0].keys()
        )

    def test_email_deliverability_invalid_domain(self):
        """Test email deliverability data for select domains."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/"
            f"{api_c.EMAIL_DELIVERABILITY_ENDPOINT}/domains?"
            f"{api_c.DOMAIN_NAME}={api_c.OPEN_RATE}&"
            f"{api_c.DOMAIN_NAME}={api_c.DOMAIN_2}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
