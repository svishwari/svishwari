"""Purpose of this file is to house all the models API tests."""
from unittest import mock
from http import HTTPStatus

from huxunify.test.route.route_test_util.route_test_case import RouteTestCase
from huxunifylib.database import collection_management, constants as db_c
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c
from huxunify.api.schema.model import ModelDriftSchema

MOCK_MODEL_RESPONSE = {
    "results": [
        {
            "features": [
                "2021-04-26 00:00:00",
                "2021-04-26 00:00:00",
                "Propensity of a customer making a purchase after "
                "receiving an email.",
                "2021-04-26 00:00:00",
                "365",
                "Propensity to Unsubscribe",
                "unsubscribe",
                "Susan Miller",
                "smiller@xyz.com",
                "7",
                "success",
                "0.2.4",
            ],
            "joinKeys": ["1"],
        },
        {
            "features": [
                "2021-01-25 00:00:00",
                "2021-01-25 00:00:00",
                "Predict the lifetime value of a customer.",
                "2021-01-25 00:00:00",
                "365",
                "Lifetime Value",
                "ltv",
                "John Smith",
                "jsmith@xyz.com",
                "7",
                "success",
                "0.4.5",
            ],
            "joinKeys": ["2"],
        },
    ]
}


class TestModelRoutes(RouteTestCase):
    """Test Model Endpoints."""

    def setUp(self) -> None:
        """Setup resources before each test."""

        self.standard_test_setup()

        # mock get_db_client() in decisioning
        mock.patch(
            "huxunify.api.route.decisioning.get_db_client",
            return_value=self.database,
        ).start()

        self.stub_models = collection_management.create_document(
            database=self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            new_doc={
                db_c.OBJECT_ID: "956a43d17afa4f0fa0070d1ba40c8901",
                db_c.NAME: "Test Stub Model",
                db_c.STATUS: api_c.REQUESTED,
                db_c.TYPE: api_c.MODELS_TAG,
            },
            username="Test User",
        )

    def test_get_all_models(self):
        """Test get all models from Tecton."""

        self.request_mocker.stop()
        self.request_mocker.post(
            t_c.TEST_CONFIG.TECTON_FEATURE_SERVICE,
            json=MOCK_MODEL_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_patch_models(self):
        """Test patch models"""

        models_data = [
            {
                api_c.ID: self.stub_models[db_c.OBJECT_ID],
                api_c.NAME: self.stub_models[db_c.NAME],
                api_c.STATUS: api_c.STATUS_ACTIVE,
            }
        ]

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            json=models_data,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        for model in response.json:
            self.assertEqual(
                self.stub_models.get(db_c.OBJECT_ID), model.get(api_c.ID)
            )
            self.assertEqual(
                self.stub_models.get(db_c.NAME), model.get(api_c.NAME)
            )

    def test_retrieve_version_history_for_model(self):
        """Test get version history for a model from Tecton."""

        # mock the version history
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.TECTON_FEATURE_SERVICE}",
            json=t_c.MOCKED_MODEL_VERSION_HISTORY,
        )
        self.request_mocker.start()

        model_id = "1"
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/version-history",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(response.json)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(response.json[0][api_c.STATUS], api_c.STATUS_ACTIVE)
        self.assertEqual(response.json[0][api_c.VERSION], "21.11.14")
        self.assertEqual(response.json[-1][api_c.VERSION], "21.10.12")

    def test_retrieve_drift_details_for_model(self):
        """Test get drift details for a model from Tecton."""

        # mock the drift data.
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.TECTON_FEATURE_SERVICE}",
            json=t_c.MOCKED_MODEL_DRIFT,
        )
        self.request_mocker.start()

        # mock get version history.
        mock.patch(
            "huxunify.api.route.decisioning.Tecton.get_model_version_history",
            return_value=t_c.MOCKED_MODEL_VERSION_HISTORY_RESPONSE,
        ).start()

        model_id = "1"
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/drift",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(response.json)
        self.assertTrue(
            t_c.validate_schema(ModelDriftSchema(), response.json, True)
        )
