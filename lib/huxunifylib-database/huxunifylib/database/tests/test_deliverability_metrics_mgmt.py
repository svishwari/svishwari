"""Database client deliverability metrics management tests."""

import unittest
import datetime

import mongomock

import huxunifylib.database.constants as db_c

from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.deliverability_metrics_management import (
    get_domain_wise_inbox_percentage_data,
    get_overall_inbox_rate,
    get_deliverability_data_performance_metrics,
    get_campaign_aggregated_sent_count,
)
from huxunifylib.database.delivery_platform_management import (
    set_deliverability_metrics,
    set_delivery_platform,
    set_performance_metrics,
    set_delivery_job,
)
from huxunifylib.database.orchestration_management import create_audience


class TestDeliverabilityMetricsMgmt(unittest.TestCase):
    """Test deliverability metrics management module."""

    def setUp(self) -> None:
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # Connect
        self.database = DatabaseClient(host="localhost", port=27017).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        self.delivery_platform_doc = set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_SPARKPOST,
            "My delivery platform for Sparkpost",
            status=db_c.STATUS_SUCCEEDED,
        )

        # Domain 1 data
        set_deliverability_metrics(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            delivery_platform_type="sparkpost",
            metrics_dict={
                "domain_inbox_percentage": 0.6797261053530265,
                "isp_metrics": [
                    {
                        "isp_name": "Yahoo",
                        "isp_inbox_percentage": 0.9841529332369692,
                    },
                    {
                        "isp_name": "Hotmail",
                        "isp_inbox_percentage": 0.7224674943461542,
                    },
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
            domain="test.com",
        )

        # Domain 1 repeat
        set_deliverability_metrics(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            delivery_platform_type="sparkpost",
            metrics_dict={
                "domain_inbox_percentage": 0.6797261053530265,
                "isp_metrics": [
                    {
                        "isp_name": "Yahoo",
                        "isp_inbox_percentage": 0.9841529332369692,
                    },
                    {
                        "isp_name": "Hotmail",
                        "isp_inbox_percentage": 0.7224674943461542,
                    },
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
            domain="test.com",
        )

        # Domain 2 data
        set_deliverability_metrics(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            delivery_platform_type="sparkpost",
            metrics_dict={
                "domain_inbox_percentage": 0.6797261053530265,
                "isp_metrics": [
                    {
                        "isp_name": "Yahoo",
                        "isp_inbox_percentage": 0.9841529332369692,
                    },
                    {
                        "isp_name": "Hotmail",
                        "isp_inbox_percentage": 0.7224674943461542,
                    },
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
            domain="test2.com",
        )
        generic_campaigns = [
            {"campaign_id": "campaign_id_1", "ad_set_id": "ad_set_id_2"}
        ]

        audience = create_audience(
            database=self.database,
            name="all",
            audience_filters=[],
            user_name="test_user",
        )

        # Create a delivery job.
        delivery_job_doc = set_delivery_job(
            self.database,
            audience[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            generic_campaigns,
            "test_user",
        )

        start_date = end_date = datetime.datetime.strptime(
            str(datetime.datetime.utcnow().date()), "%Y-%m-%d"
        )

        metrics_1 = set_performance_metrics(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            delivery_job_id=delivery_job_doc[db_c.ID],
            delivery_platform_type=db_c.DELIVERY_PLATFORM_SFMC,
            generic_campaigns=generic_campaigns[0]["campaign_id"],
            metrics_dict={
                "journey_name": "SFMCJourney_2",
                "journey_id": "43925808-c52e-11eb-826e-bae5bebfd7a3",
                "from_addr": "dev-sfmc@domain1.com",
                "journey_creation_date": "2021-09-01T12:14:46Z",
                "hux_engagement_id": "60c2fd6515eb844f53cdc669",
                "hux_audience_id": "60a7a15cc1e230dbd54ef428",
                "sent": 200,
                "delivered": 0,
                "opens": 107,
                "unique_opens": 91,
                "clicks": 71,
                "unique_clicks": 67,
                "bounces": 0,
                "hard_bounces": 0,
                "unsubscribes": 27,
                "complaints": 11,
            },
            start_time=start_date,
            end_time=end_date,
        )

        metrics_2 = set_performance_metrics(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            delivery_job_id=delivery_job_doc[db_c.ID],
            delivery_platform_type=db_c.DELIVERY_PLATFORM_SFMC,
            generic_campaigns=generic_campaigns[0]["campaign_id"],
            metrics_dict={
                "journey_name": "SFMCJourney_2",
                "journey_id": "43925808-c52e-11eb-826e-bae5bebfd7a3",
                "from_addr": "dev-sfmc@domain1.com",
                "journey_creation_date": "2021-09-01T12:14:46Z",
                "hux_engagement_id": "60c2fd6515eb844f53cdc669",
                "hux_audience_id": "60a7a15cc1e230dbd54ef428",
                "sent": 200,
                "delivered": 0,
                "opens": 107,
                "unique_opens": 91,
                "clicks": 71,
                "unique_clicks": 67,
                "bounces": 0,
                "hard_bounces": 0,
                "unsubscribes": 27,
                "complaints": 11,
            },
            start_time=start_date,
            end_time=end_date,
        )

        self.aggregated_sent = metrics_1.get(db_c.PERFORMANCE_METRICS).get(
            "sent"
        ) + metrics_2.get(db_c.PERFORMANCE_METRICS).get("sent")

        self.aggregated_opens = metrics_1.get(db_c.PERFORMANCE_METRICS).get(
            "opens"
        ) + metrics_2.get(db_c.PERFORMANCE_METRICS).get("opens")

        self.aggregated_clicks = metrics_1.get(db_c.PERFORMANCE_METRICS).get(
            "clicks"
        ) + metrics_2.get(db_c.PERFORMANCE_METRICS).get("clicks")

    def test_domain_wise_inbox_percentage_data(self):
        """Test for domain wise inbox percentage data."""

        data = get_domain_wise_inbox_percentage_data(self.database)
        self.assertIsInstance(data, list)

        # Ensure both the domains are existing.
        self.assertEqual("test.com", data[0].get(db_c.DOMAIN_NAME))
        self.assertEqual("test2.com", data[1].get(db_c.DOMAIN_NAME))

        self.assertIsInstance(
            data[0].get(db_c.INBOX_PERCENTAGE_DATA)[0][db_c.INBOX_PERCENTAGE],
            float,
        )
        self.assertTrue(
            data[0].get(db_c.INBOX_PERCENTAGE_DATA)[0][db_c.CREATE_TIME]
        )

    def test_inbox_percentage_data_parameters(self):
        """Test for domain inbox percentage data with start and end date."""

        data = get_domain_wise_inbox_percentage_data(
            self.database,
            domain_name=["test.com"],
            start_date=datetime.datetime.utcnow() - datetime.timedelta(days=1),
            end_date=datetime.datetime.utcnow(),
        )
        self.assertIsInstance(data, list)
        self.assertEqual(1, len(data))
        # Ensure the domain is existing.
        self.assertEqual("test.com", data[0].get(db_c.DOMAIN_NAME))

        self.assertIsInstance(
            data[0].get(db_c.INBOX_PERCENTAGE_DATA)[0][db_c.INBOX_PERCENTAGE],
            float,
        )
        self.assertTrue(
            data[0].get(db_c.INBOX_PERCENTAGE_DATA)[0][db_c.CREATE_TIME]
        )

    def test_get_overall_inbox_rate(self):
        """Test get overall inbox rate"""
        overall_inbox_rate = get_overall_inbox_rate(self.database)
        self.assertIsInstance(overall_inbox_rate, float)

    def test_get_deliverability_data_performance_metrics(self):
        """Test get deliverability data from performance metrics."""

        performance_metrics = get_deliverability_data_performance_metrics(
            database=self.database,
            domains=["domain1.com"],
            start_date=datetime.datetime.utcnow() - datetime.timedelta(days=1),
            end_date=datetime.datetime.utcnow(),
            mock=True,
        )

        self.assertIsInstance(performance_metrics, list)
        self.assertIsInstance(
            performance_metrics[0].get(db_c.DOMAIN_NAME), str
        )
        self.assertIsInstance(
            performance_metrics[0].get(db_c.DELIVERABILITY_METRICS), list
        )

        self.assertIsInstance(
            performance_metrics[0]
            .get(db_c.DELIVERABILITY_METRICS)[0]
            .get("sent"),
            int,
        )

        self.assertEqual(
            self.aggregated_sent,
            performance_metrics[0]
            .get(db_c.DELIVERABILITY_METRICS)[0]
            .get("sent"),
        )

        self.assertIsInstance(
            performance_metrics[0]
            .get(db_c.DELIVERABILITY_METRICS)[0]
            .get("opens"),
            int,
        )
        self.assertEqual(
            self.aggregated_opens,
            performance_metrics[0]
            .get(db_c.DELIVERABILITY_METRICS)[0]
            .get("opens"),
        )

        self.assertIsInstance(
            performance_metrics[0]
            .get(db_c.DELIVERABILITY_METRICS)[0]
            .get("clicks"),
            int,
        )
        self.assertEqual(
            self.aggregated_clicks,
            performance_metrics[0]
            .get(db_c.DELIVERABILITY_METRICS)[0]
            .get("clicks"),
        )

    def test_get_deliverability_data_aggregate(self):
        """Test get aggregated deliverability data from performance metrics."""

        performance_metrics = get_deliverability_data_performance_metrics(
            database=self.database,
            domains=["domain1.com"],
            start_date=datetime.datetime.utcnow() - datetime.timedelta(days=1),
            end_date=datetime.datetime.utcnow(),
            aggregate=True,
            mock=True,
        )

        self.assertIsInstance(performance_metrics, list)
        self.assertIsInstance(
            performance_metrics[0].get(db_c.DOMAIN_NAME), str
        )

        self.assertIsInstance(performance_metrics[0].get("sent"), int)
        self.assertEqual(
            self.aggregated_sent, performance_metrics[0].get("sent")
        )
        self.assertIsInstance(performance_metrics[0].get("opens"), int)
        self.assertEqual(
            self.aggregated_opens, performance_metrics[0].get("opens")
        )
        self.assertIsInstance(performance_metrics[0].get("clicks"), int)
        self.assertEqual(
            self.aggregated_clicks,
            performance_metrics[0].get("clicks"),
        )

    def test_get_campaign_aggregated_sent_count(self):
        """Test for aggregated sent count."""
        campaign_aggregated_sent_count = get_campaign_aggregated_sent_count(
            database=self.database,
            domains=["domain1.com"],
            start_date=datetime.datetime.utcnow() - datetime.timedelta(days=1),
            end_date=datetime.datetime.utcnow(),
        )

        self.assertEqual(len(campaign_aggregated_sent_count), 1)
        self.assertEqual(
            self.aggregated_sent, campaign_aggregated_sent_count[0].get("sent")
        )
