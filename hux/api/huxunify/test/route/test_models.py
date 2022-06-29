"""Purpose of this file is to house all the models API tests."""
import asyncio
from unittest import mock
from http import HTTPStatus

from huxunify.test.route.route_test_util.route_test_case import RouteTestCase
from huxunifylib.database import collection_management, constants as db_c
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c
from huxunify.api.schema.model import (
    ModelDriftSchema,
    ModelVersionSchema,
    ModelSchema,
)
from huxunify.api.data_connectors.decisioning import (
    convert_model_to_dot_notation,
)

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

        super().setUp()

        # mock get_db_client() in decisioning
        mock.patch(
            "huxunify.api.route.decisioning.get_db_client",
            return_value=self.database,
        ).start()

        mock.patch(
            "huxunify.api.data_connectors.cache.get_db_client",
            return_value=self.database,
        ).start()

        self.stub_models = collection_management.create_document(
            database=self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            new_doc={
                db_c.NAME: "Test Stub Model",
                db_c.STATUS: api_c.REQUESTED,
                db_c.TYPE: api_c.MODELS_TAG,
            },
            username="Test User",
        )

    def test_get_all_models(self):
        """Test get all models."""

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
        )

        loop.close()

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(ModelSchema(), response.json, True)
        )

    def test_retrieve_version_history_for_model(self):
        """Test get version history for a model."""

        # mock get version history.
        mock.patch(
            "huxunify.api.data_connectors.decisioning.Decisioning.get_model_info_history",
            return_value=[
                convert_model_to_dot_notation(
                    t_c.MOCKED_MODEL_VERSION_HISTORY_RESPONSE_PROPENSITY[0]
                )
            ],
        ).start()

        model_id = "model-Propensity_Type_Cancelled-v5-dev"
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/version-history",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(ModelVersionSchema(many=True).dump(response.json))

    def test_retrieve_drift_details_for_model(self):
        """Test get drift details for a model."""

        # mock get version history.
        mock.patch(
            "huxunify.api.data_connectors.decisioning.Decisioning.get_model_info_history",
            return_value=[
                convert_model_to_dot_notation(
                    t_c.MOCKED_MODEL_VERSION_HISTORY_RESPONSE_PROPENSITY[0]
                )
            ],
        ).start()

        model_id = "model-Propensity_Type_Cancelled-v5-dev"
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/drift",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(response.json)
        self.assertTrue(
            t_c.validate_schema(ModelDriftSchema(), response.json, True)
        )
