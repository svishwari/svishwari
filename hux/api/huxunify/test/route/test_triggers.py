"""Purpose of this file is to house all the triggers API tests."""
from unittest import TestCase, mock
from http import HTTPStatus
import mongomock
from huxunifylib.database.client import DatabaseClient
import huxunify.test.constants as t_c
import huxunify.api.constants as api_c
from huxunify.app import create_app


class TestTriggersRoute(TestCase):
    """Test Triggers Endpoints."""

    # pylint: disable=unused-variable
    def setUp(self) -> None:
        """Setup resources before each test."""
        self.app = create_app().test_client()

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # mock get db client from delivery
        mock.patch(
            "huxunify.api.route.triggers.get_db_client",
            return_value=self.database,
        ).start()

        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        self.addCleanup(mock.patch.stopall)

    def test_delivery_pending_jobs_zero(self):
        """Test delivery of pending jobs no jobs endpoint"""
        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}/{api_c.TRIGGERS_TAG}/"
                f"{api_c.DELIVERIES}/{api_c.PENDING_JOBS}"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(
            {
                api_c.DELIVERIES: {
                    api_c.PENDING_JOBS: 0,
                    api_c.ORCH_INTEGRATION_TEST: 0,
                }
            },
            response.json,
        )

    def test_delivery_pending_jobs(self):
        """Test delivery of pending jobs endpoint"""

        with mock.patch(
            "huxunify.api.route.triggers.get_documents",
            return_value={api_c.TOTAL_RECORDS: 58},
        ):
            response = self.app.get(
                (
                    f"{t_c.BASE_ENDPOINT}/{api_c.TRIGGERS_TAG}/"
                    f"{api_c.DELIVERIES}/{api_c.PENDING_JOBS}"
                ),
                headers=t_c.STANDARD_HEADERS,
            )

            self.assertEqual(HTTPStatus.OK, response.status_code)
            self.assertDictEqual(
                {
                    api_c.DELIVERIES: {
                        api_c.PENDING_JOBS: 58,
                        api_c.ORCH_INTEGRATION_TEST: 58,
                    }
                },
                response.json,
            )
