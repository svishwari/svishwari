"""Model Schema Tests."""
import re
from datetime import datetime
from unittest import TestCase
from bson import ObjectId

from huxunify.api.schema.model import (
    ModelSchema,
    ModelVersionSchema,
    ModelDashboardSchema,
)
from huxunify.api import constants as api_c
from huxunify.test import constants as t_c
from huxunifylib.database import constants as db_c


class TestModelSchema(TestCase):
    """Test model related schemas."""

    def test_model_schema(self):
        """Test ModelSchema."""

        doc = dict(
            _id=str(ObjectId()),
            name="Customer Lifetime Value",
            is_enabled=True,
            type=db_c.MODEL_TYPE_REGRESSION,
            description="Predicting the lifetime value of customers over a "
            "defined time range.",
            added=False,
            status=api_c.STATUS_PENDING,
            category="Sales forecasting",
        )

        response = ModelSchema().dump(doc)

        self.assertIsInstance(response[api_c.ID], str)
        self.assertTrue(re.search("Consumer", response[api_c.NAME]))
        self.assertFalse(re.search("Customer", response[api_c.NAME]))
        self.assertEqual(response[api_c.TYPE], doc[api_c.TYPE])
        self.assertTrue(re.search("consumers", response[api_c.DESCRIPTION]))
        self.assertFalse(re.search("customers", response[api_c.DESCRIPTION]))
        self.assertEqual(response[api_c.CATEGORY], doc[api_c.CATEGORY])
        self.assertEqual(response[api_c.STATUS], doc[api_c.STATUS])
        self.assertEqual(response[api_c.IS_ADDED], doc[db_c.ADDED])

    def test_model_version_schema(self):
        """Test ModelVersionSchema."""

        doc = dict(
            id=str(ObjectId()),
            name="Propensity to Purchase by a Customer",
            current_version="22.8.30",
            lookback_window=90,
            prediction_window=90,
            description="Propensity of a customer making a purchase after "
            "receiving an email.",
            status=api_c.STATUS_ACTIVE,
            fulcrum_date=datetime.utcnow(),
            last_trained=datetime.utcnow(),
        )

        response = ModelVersionSchema().dump(doc)

        self.assertIsInstance(response[api_c.ID], str)
        self.assertTrue(re.search("Consumer", response[api_c.NAME]))
        self.assertFalse(re.search("Customer", response[api_c.NAME]))
        self.assertEqual(response[api_c.VERSION], doc[api_c.CURRENT_VERSION])
        self.assertEqual(
            response[api_c.LOOKBACK_WINDOW], doc[api_c.LOOKBACK_WINDOW]
        )
        self.assertEqual(
            response[api_c.PREDICTION_WINDOW], doc[api_c.PREDICTION_WINDOW]
        )
        self.assertTrue(re.search("consumer", response[api_c.DESCRIPTION]))
        self.assertFalse(re.search("customer", response[api_c.DESCRIPTION]))
        self.assertEqual(response[api_c.STATUS], doc[api_c.STATUS])
        self.assertIn(api_c.FULCRUM_DATE, response)
        self.assertIn(t_c.TRAINED_DATE, response)

    def test_model_dashboard_schema(self):
        """Test ModelDashboardSchema."""

        doc = dict(
            model_name="Propensity to Purchase by a Customer",
            model_type="purchase",
            description="Predicts the propensity of customers to make a "
            "purchase after receiving an email.",
            performance_metric=dict(
                rmse=-1,
                auc=0.82,
                precision=0.81,
                recall=0.59,
                current_version="22.8.32",
            ),
        )

        response = ModelDashboardSchema().dump(doc)

        self.assertTrue(re.search("Consumer", response[api_c.MODEL_NAME]))
        self.assertFalse(re.search("Customer", response[api_c.MODEL_NAME]))
        self.assertEqual(response[api_c.MODEL_TYPE], doc[api_c.MODEL_TYPE])
        self.assertTrue(re.search("consumers", response[api_c.DESCRIPTION]))
        self.assertFalse(re.search("customers", response[api_c.DESCRIPTION]))
        self.assertEqual(
            response[api_c.PERFORMANCE_METRIC], doc[api_c.PERFORMANCE_METRIC]
        )
