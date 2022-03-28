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
    set_delivery_job,
    set_performance_metrics,
)
from huxunifylib.database.orchestration_management import create_audience


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
            database=self.database,
            delivery_platform_type=db_c.DELIVERY_PLATFORM_SPARKPOST,
            name="My delivery platform for Sparkpost",
            status=db_c.STATUS_SUCCEEDED,
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

        self.generic_campaigns = [
            {"campaign_id": "campaign_id_1", "ad_set_id": "ad_set_id_2"}
        ]

        self.audience = create_audience(
            database=self.database,
            name="all",
            audience_filters=[],
            user_name="test_user",
        )

        # Create a delivery job.
        self.delivery_job_doc = set_delivery_job(
            self.database,
            self.audience[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            self.generic_campaigns,
        )

        self.metrics_1 = set_performance_metrics(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            delivery_job_id=self.delivery_job_doc[db_c.ID],
            delivery_platform_type=db_c.DELIVERY_PLATFORM_SFMC,
            generic_campaigns=self.generic_campaigns[0]["campaign_id"],
            metrics_dict={
                "journey_name": "SFMCJourney_2",
                "journey_id": "43925808-c52e-11eb-826e-bae5bebfd7a3",
                "from_addr": "dev-sfmc@domain_1",
                "journey_creation_date": "2021-09-01T12:14:46Z",
                "hux_engagement_id": "60c2fd6515eb844f53cdc669",
                "hux_audience_id": "60a7a15cc1e230dbd54ef428",
                "sent": 200,
                "delivered": 0,
                "opens": 107,
                "unique_opens": 91,
                "clicks": 71,
                "unique_clicks": 67,
                "bounces": 1,
                "hard_bounces": 0,
                "unsubscribes": 27,
                "complaints": 11,
            },
            start_time=datetime.datetime.utcnow(),
            end_time=datetime.datetime.utcnow() + datetime.timedelta(days=-2),
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
        self.assertIsInstance(
            response.json.get(api_c.SENDING_DOMAINS_OVERVIEW), list
        )

        self.assertIsInstance(
            response.json.get(api_c.SENDING_DOMAINS_OVERVIEW)[0].get(
                db_c.DOMAIN_NAME
            ),
            str,
        )

        sent = (
            self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(api_c.SENT)
            - self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(
                api_c.HARD_BOUNCES
            )
            - self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(
                api_c.UNSUBSCRIBES
            )
            - self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(
                api_c.COMPLAINTS
            )
        )
        delivered = sent - (
            self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(api_c.BOUNCES)
            - self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(
                api_c.HARD_BOUNCES
            )
        )

        self.assertIsInstance(
            response.json.get(api_c.SENDING_DOMAINS_OVERVIEW)[0].get(
                api_c.SENT
            ),
            int,
        )
        self.assertEqual(
            sent,
            response.json.get(api_c.SENDING_DOMAINS_OVERVIEW)[0].get(
                api_c.SENT
            ),
        )

        self.assertIsInstance(
            response.json.get(api_c.SENDING_DOMAINS_OVERVIEW)[0].get(
                api_c.OPEN_RATE
            ),
            float,
        )
        self.assertAlmostEqual(
            self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(api_c.OPENS)
            / delivered,
            response.json.get(api_c.SENDING_DOMAINS_OVERVIEW)[0].get(
                api_c.OPEN_RATE
            ),
            places=2,
        )

        self.assertIsInstance(
            response.json.get(api_c.SENDING_DOMAINS_OVERVIEW)[0].get(
                api_c.CLICK_RATE
            ),
            float,
        )
        self.assertAlmostEqual(
            self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(api_c.CLICKS)
            / delivered,
            response.json.get(api_c.SENDING_DOMAINS_OVERVIEW)[0].get(
                api_c.CLICK_RATE
            ),
            places=2,
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

    def test_email_deliverability_multiple_campaigns(self):
        """Test email deliverability data for multiple campaigns."""

        metrics_2 = set_performance_metrics(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            delivery_job_id=self.delivery_job_doc[db_c.ID],
            delivery_platform_type=db_c.DELIVERY_PLATFORM_SFMC,
            generic_campaigns=self.generic_campaigns[0]["campaign_id"],
            metrics_dict={
                "journey_name": "SFMCJourney_2",
                "journey_id": "43925808-c52e-11eb-826e-bae5bebfd7a4",
                "from_addr": "dev-sfmc@domain_1",
                "journey_creation_date": "2021-09-01T12:14:46Z",
                "hux_engagement_id": "60c2fd6515eb844f53cdc669",
                "hux_audience_id": "60a7a15cc1e230dbd54ef428",
                "sent": 199,
                "delivered": 0,
                "opens": 107,
                "unique_opens": 91,
                "clicks": 71,
                "unique_clicks": 67,
                "bounces": 1,
                "hard_bounces": 0,
                "unsubscribes": 27,
                "complaints": 11,
            },
            start_time=datetime.datetime.utcnow(),
            end_time=datetime.datetime.utcnow() + datetime.timedelta(days=-1),
        )

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/"
            f"{api_c.EMAIL_DELIVERABILITY_ENDPOINT}/domains?"
            f"{api_c.DOMAIN_NAME}={api_c.DOMAIN_1}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        response_data = response.json
        self.assertTrue(
            t_c.validate_schema(
                EmailDeliverabiliyDomainsSchema(), response_data
            )
        )

        # Ensure different campaigns data are not aggregated.
        self.assertEqual(
            self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(api_c.SENT),
            response.json.get(api_c.SENT)[0].get(api_c.DOMAIN_1),
        )

        self.assertEqual(
            metrics_2.get(db_c.PERFORMANCE_METRICS).get(api_c.SENT),
            response.json.get(api_c.SENT)[1].get(api_c.DOMAIN_1),
        )

        # Ensure rates are calculated properly.
        self.assertAlmostEqual(
            metrics_2.get(db_c.PERFORMANCE_METRICS).get(api_c.OPENS)
            / metrics_2.get(db_c.PERFORMANCE_METRICS).get(api_c.SENT),
            response.json.get(api_c.OPEN_RATE)[1].get(api_c.DOMAIN_1),
            places=2,
        )

        self.assertAlmostEqual(
            metrics_2.get(db_c.PERFORMANCE_METRICS).get(api_c.CLICKS)
            / metrics_2.get(db_c.PERFORMANCE_METRICS).get(api_c.SENT),
            response.json.get(api_c.CLICK_RATE)[1].get(api_c.DOMAIN_1),
            places=2,
        )

        self.assertAlmostEqual(
            metrics_2.get(db_c.PERFORMANCE_METRICS).get(api_c.UNSUBSCRIBES)
            / metrics_2.get(db_c.PERFORMANCE_METRICS).get(api_c.SENT),
            response.json.get(api_c.UNSUBSCRIBE_RATE)[1].get(api_c.DOMAIN_1),
            places=2,
        )

    def test_email_deliverability_single_campaign(self):
        """Test email deliverability data for single campaign."""

        metrics_2 = set_performance_metrics(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            delivery_job_id=self.delivery_job_doc[db_c.ID],
            delivery_platform_type=db_c.DELIVERY_PLATFORM_SFMC,
            generic_campaigns=self.generic_campaigns[0]["campaign_id"],
            metrics_dict={
                "journey_name": "SFMCJourney_2",
                "journey_id": "43925808-c52e-11eb-826e-bae5bebfd7a3",
                "from_addr": "dev-sfmc@domain_1",
                "journey_creation_date": "2021-09-01T12:14:46Z",
                "hux_engagement_id": "60c2fd6515eb844f53cdc669",
                "hux_audience_id": "60a7a15cc1e230dbd54ef428",
                "sent": 200,
                "delivered": 0,
                "opens": 107,
                "unique_opens": 91,
                "clicks": 71,
                "unique_clicks": 67,
                "bounces": 1,
                "hard_bounces": 0,
                "unsubscribes": 27,
                "complaints": 11,
            },
            start_time=datetime.datetime.utcnow(),
            end_time=datetime.datetime.utcnow() + datetime.timedelta(days=-1),
        )

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/"
            f"{api_c.EMAIL_DELIVERABILITY_ENDPOINT}/domains?"
            f"{api_c.DOMAIN_NAME}={api_c.DOMAIN_1}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        response_data = response.json
        self.assertTrue(
            t_c.validate_schema(
                EmailDeliverabiliyDomainsSchema(), response_data
            )
        )

        sent_day_1 = self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(
            api_c.SENT
        ) + metrics_2.get(db_c.PERFORMANCE_METRICS).get(api_c.SENT)
        # Ensure different campaigns data are aggregated.
        self.assertEqual(
            sent_day_1, response.json.get(api_c.SENT)[0].get(api_c.DOMAIN_1)
        )

        # Ensure sent on second day is calculated as
        # sent - (hard bounces, unsubscribes, complaints)
        sent_day_2 = (
            self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(api_c.SENT)
            + metrics_2.get(db_c.PERFORMANCE_METRICS).get(api_c.SENT)
            - self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(
                api_c.HARD_BOUNCES
            )
            - self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(
                api_c.UNSUBSCRIBES
            )
            - self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(
                api_c.COMPLAINTS
            )
        )
        delivered_day_2 = sent_day_2 - (
            self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(api_c.BOUNCES)
            - self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(
                api_c.HARD_BOUNCES
            )
        )

        self.assertEqual(
            sent_day_2, response.json.get(api_c.SENT)[1].get(api_c.DOMAIN_1)
        )

        # Ensure rates are calculated properly.
        self.assertAlmostEqual(
            self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(api_c.OPENS)
            / sent_day_1,
            response.json.get(api_c.OPEN_RATE)[0].get(api_c.DOMAIN_1),
            places=2,
        )
        self.assertAlmostEqual(
            metrics_2.get(db_c.PERFORMANCE_METRICS).get(api_c.OPENS)
            / delivered_day_2,
            response.json.get(api_c.OPEN_RATE)[1].get(api_c.DOMAIN_1),
            places=2,
        )

        self.assertAlmostEqual(
            self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(api_c.CLICKS)
            / sent_day_1,
            response.json.get(api_c.CLICK_RATE)[0].get(api_c.DOMAIN_1),
            places=2,
        )
        self.assertAlmostEqual(
            metrics_2.get(db_c.PERFORMANCE_METRICS).get(api_c.CLICKS)
            / delivered_day_2,
            response.json.get(api_c.CLICK_RATE)[1].get(api_c.DOMAIN_1),
            places=2,
        )
        self.assertAlmostEqual(
            self.metrics_1.get(db_c.PERFORMANCE_METRICS).get(
                api_c.UNSUBSCRIBES
            )
            / sent_day_1,
            response.json.get(api_c.UNSUBSCRIBE_RATE)[0].get(api_c.DOMAIN_1),
            places=2,
        )
        self.assertAlmostEqual(
            metrics_2.get(db_c.PERFORMANCE_METRICS).get(api_c.UNSUBSCRIBES)
            / delivered_day_2,
            response.json.get(api_c.UNSUBSCRIBE_RATE)[1].get(api_c.DOMAIN_1),
            places=2,
        )
