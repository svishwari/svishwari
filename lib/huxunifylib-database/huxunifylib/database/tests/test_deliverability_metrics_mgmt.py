"""Database client deliverability metrics management tests."""

import unittest
import datetime

import mongomock

import huxunifylib.database.constants as db_c

from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.deliverability_metrics_management import (
    get_domain_wise_inbox_percentage_data,
    get_overall_inbox_rate,
)
from huxunifylib.database.delivery_platform_management import (
    set_deliverability_metrics,
    set_delivery_platform,
)


class TestUserManagement(unittest.TestCase):
    """Test user management module."""

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
