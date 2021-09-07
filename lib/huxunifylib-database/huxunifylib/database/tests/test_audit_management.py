"""This module is to park all unit tests of audit_management.py"""
from datetime import datetime
from unittest import TestCase

import mongomock
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database import constants as db_c, audit_management

from huxunify.api import constants as api_c


class AudienceAuditTest(TestCase):
    """
    Test Audience Audit
    """

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):
        """
        Setup resources before each test
        """
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

    def test_create_audience_audit(self):
        """
        Test creating a audience audit
        """
        audience_audit = audit_management.create_audience_audit(
            database=self.database,
            audience_id="611d12f9d80297f5a7328779",
            download_type=api_c.GOOGLE_ADS,
            download_time=datetime.now(),
            file_name="09082021003424_611d12f9d80297f5a7328779_google_ads.csv",
        )

        self.assertTrue(audience_audit is not None)
