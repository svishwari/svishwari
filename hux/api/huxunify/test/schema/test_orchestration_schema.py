# pylint: disable=no-self-use
"""Purpose of this file is to test the orchestration schemas."""
import random
from unittest import TestCase
from datetime import datetime

import bson

from huxunifylib.database import constants as db_c
from huxunify.api.schema.orchestration import (
    AudienceGetSchema,
    EngagementDeliveryHistorySchema,
    AudienceDeliveryHistorySchema,
    AudienceStandaloneDeliveriesSchema,
)
from huxunify.api import constants as api_c
from huxunify.test import constants as t_c


class OrchestrationSchemaTest(TestCase):
    """Test Orchestration related Schema Classes."""

    def test_successful_audience_get_schema(self) -> None:
        """Test Successful EngagementGetSchema."""

        doc = {
            api_c.ID: "5f5f7262997acad4bac4384a",
            db_c.NAME: "Audience 1",
            db_c.AUDIENCE_FILTERS: [],
            db_c.DESTINATIONS: [],
            db_c.ENGAGEMENTS_COLLECTION: [],
            db_c.DELIVERIES: [
                {
                    db_c.STATUS: "Delivered",
                    db_c.METRICS_DELIVERY_PLATFORM_NAME: "Facebook",
                    db_c.METRICS_DELIVERY_PLATFORM_TYPE: "facebook",
                    db_c.AUDIENCE_LAST_DELIVERED: datetime.strftime(
                        datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
                    ),
                },
            ],
            db_c.SIZE: 1000,
            db_c.STATUS: "Delivered",
            db_c.LOOKALIKE_AUDIENCE_COLLECTION: [],
            api_c.IS_LOOKALIKE: False,
            api_c.LOOKALIKEABLE: api_c.DISABLED,
            db_c.UPDATED_BY: "User",
            db_c.UPDATE_TIME: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        self.assertFalse(AudienceGetSchema().validate(doc))

    def test_successful_lookalike_audience_get_schema(self) -> None:
        """Test Successful EngagementGetSchema."""

        doc = {
            api_c.ID: "5f5f7262997acad4bac4384a",
            db_c.NAME: "Lookalike Audience 1",
            db_c.AUDIENCE_FILTERS: [],
            db_c.DESTINATIONS: [],
            db_c.ENGAGEMENTS_COLLECTION: [],
            db_c.DELIVERIES: [
                {
                    db_c.STATUS: "Delivered",
                    db_c.METRICS_DELIVERY_PLATFORM_NAME: "Facebook",
                    db_c.METRICS_DELIVERY_PLATFORM_TYPE: "facebook",
                    db_c.AUDIENCE_LAST_DELIVERED: datetime.strftime(
                        datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
                    ),
                },
            ],
            db_c.SIZE: 1000,
            db_c.STATUS: "Delivered",
            db_c.LOOKALIKE_AUDIENCE_COLLECTION: [],
            api_c.IS_LOOKALIKE: True,
            t_c.SOURCE_ID: "5f5f7262997acad4bac4385b",
            t_c.SOURCE_NAME: "Audience 1",
            t_c.SOURCE_SIZE: 2000,
            api_c.LOOKALIKE_SOURCE_EXISTS: random.choice([True, False]),
            api_c.LOOKALIKEABLE: api_c.DISABLED,
            db_c.UPDATED_BY: "User",
            db_c.UPDATE_TIME: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        self.assertFalse(AudienceGetSchema().validate(doc))

    def test_unsuccessful_audience_get_schema_bad_name(self) -> None:
        """Test unsuccessful AudienceGetSchema."""

        doc = {
            api_c.ID: "5f5f7262997acad4bac4384a",
            db_c.NAME: 5,
            db_c.AUDIENCE_FILTERS: [],
            db_c.DESTINATIONS: [],
            db_c.ENGAGEMENTS_COLLECTION: [],
            db_c.LOOKALIKE_AUDIENCE_COLLECTION: [],
            api_c.IS_LOOKALIKE: False,
            api_c.LOOKALIKEABLE: api_c.DISABLED,
            db_c.UPDATED_BY: "User",
            db_c.UPDATE_TIME: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        self.assertTrue(AudienceGetSchema().validate(doc))

    def test_unsuccessful_audience_get_schema_engagement_no_name(
        self,
    ) -> None:
        """Test unsuccessful AudienceGetSchema engagement no name."""

        doc = {
            api_c.ID: "5f5f7262997acad4bac4384a",
            db_c.NAME: "Audience 1",
            db_c.AUDIENCE_FILTERS: [],
            db_c.DESTINATIONS: [],
            db_c.ENGAGEMENTS_COLLECTION: [
                {
                    api_c.ID: "5f5f7262997acad4bac4384b",
                }
            ],
            db_c.LOOKALIKE_AUDIENCE_COLLECTION: [],
            api_c.IS_LOOKALIKE: False,
            api_c.LOOKALIKEABLE: api_c.DISABLED,
            db_c.UPDATED_BY: "User",
            db_c.UPDATE_TIME: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        self.assertTrue(AudienceGetSchema().validate(doc))

    def test_match_rate_audience_get_schema(self) -> None:
        """Test audience get schema match_rate."""

        destination_id = str(bson.ObjectId())
        audience = {
            api_c.ID: "5f5f7262997acad4bac4384a",
            db_c.NAME: "Audience 1",
            db_c.AUDIENCE_FILTERS: [],
            db_c.DESTINATIONS: [],
            db_c.ENGAGEMENTS_COLLECTION: [
                {
                    api_c.ID: "5f5f7262997acad4bac4384b",
                    db_c.NAME: "Engagement 1",
                    db_c.DELIVERIES: [
                        {
                            api_c.ID: "5f5f7262997acad4bac4384c",
                            db_c.NAME: "Delivery 1",
                            db_c.SIZE: 1000,
                            api_c.MATCH_RATE: 0,
                            db_c.DELIVERY_PLATFORM_ID: destination_id,
                        },
                        {
                            api_c.ID: "5f5f7262997acad4bac4384d",
                            db_c.NAME: "Delivery 2",
                            db_c.SIZE: 1000,
                            api_c.MATCH_RATE: 0,
                            db_c.DELIVERY_PLATFORM_ID: destination_id,
                        },
                    ],
                }
            ],
            db_c.LOOKALIKE_AUDIENCE_COLLECTION: [],
            api_c.IS_LOOKALIKE: False,
            api_c.LOOKALIKEABLE: api_c.DISABLED,
            db_c.UPDATED_BY: "User",
            db_c.UPDATE_TIME: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        self.assertFalse(AudienceGetSchema().validate(audience))

        # deserialize the json document by loading it into the schema and
        # test the schema to have the match_rate value set
        schema = AudienceGetSchema().load(audience)

        deliveries = schema[db_c.ENGAGEMENTS_COLLECTION][0][db_c.DELIVERIES]
        self.assertGreaterEqual(deliveries[0][api_c.MATCH_RATE], 0)
        self.assertGreaterEqual(deliveries[1][api_c.MATCH_RATE], 0)

        # test to ensure all deliveries are the same and they are set.
        self.assertTrue(
            all(
                [x[db_c.DELIVERY_PLATFORM_ID] for x in deliveries]
                + [destination_id]
            )
        )

    def test_engagement_delivery_history_schema(self) -> None:
        """Test engagement delivery history schema."""

        doc = {
            api_c.AUDIENCE: {
                api_c.ID: "5f5f7262997acad4bac4384a",
                db_c.NAME: "Audience 1",
            },
            api_c.DESTINATION: {
                api_c.ID: "5f5f7262997acad4bac4384b",
                db_c.NAME: "facebook",
                db_c.TYPE: "facebook",
            },
            db_c.SIZE: 1000,
            api_c.MATCH_RATE: 0,
            api_c.DELIVERED: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        self.assertFalse(EngagementDeliveryHistorySchema().validate(doc))

    def test_match_rate_engagement_delivery_history_schema(self) -> None:
        """Test engagement delivery history schema match_rate."""

        delivery_history = {
            api_c.AUDIENCE: {
                api_c.ID: "5f5f7262997acad4bac4384a",
                db_c.NAME: "Audience 1",
            },
            api_c.DESTINATION: {
                api_c.ID: "5f5f7262997acad4bac4384b",
                db_c.NAME: "facebook",
                db_c.TYPE: "facebook",
            },
            db_c.SIZE: 1000,
            api_c.MATCH_RATE: 0,
            api_c.DELIVERED: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        self.assertFalse(
            EngagementDeliveryHistorySchema().validate(delivery_history)
        )

        # deserialize the json document by loading it into the schema and
        # test the schema to have the match_rate value set
        schema = EngagementDeliveryHistorySchema().load(delivery_history)
        self.assertGreaterEqual(schema[api_c.MATCH_RATE], 0)

    def test_audience_delivery_history_schema(self) -> None:
        """Test audience delivery history schema."""

        doc = {
            api_c.ENGAGEMENT: {
                api_c.ID: "5f5f7262997acad4bac4384a",
                db_c.NAME: "Engagement 1",
            },
            api_c.DESTINATION: {
                api_c.ID: "5f5f7262997acad4bac4384b",
                db_c.NAME: "facebook",
                db_c.TYPE: "facebook",
            },
            db_c.SIZE: 1000,
            api_c.MATCH_RATE: 0,
            api_c.DELIVERED: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        self.assertFalse(AudienceDeliveryHistorySchema().validate(doc))

    def test_audience_delivery_history_schema_invalid_id(self) -> None:
        """Test audience delivery history schema."""

        doc = {
            api_c.ENGAGEMENT: {
                api_c.ID: t_c.INVALID_ID,
                db_c.NAME: "Engagement 1",
            },
            api_c.DESTINATION: {
                api_c.ID: "5f5f7262997acad4bac4384b",
                db_c.NAME: "facebook",
                db_c.TYPE: "facebook",
            },
            db_c.SIZE: 1000,
            api_c.MATCH_RATE: 0,
            api_c.DELIVERED: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        with self.assertRaises(bson.errors.InvalidId):
            AudienceDeliveryHistorySchema().validate(doc)

    def test_match_rate_audience_delivery_history_schema(self) -> None:
        """Test audience delivery history schema match_rate."""

        delivery_history = {
            api_c.ENGAGEMENT: {
                api_c.ID: "5f5f7262997acad4bac4384a",
                db_c.NAME: "Engagement 1",
            },
            api_c.DESTINATION: {
                api_c.ID: "5f5f7262997acad4bac4384b",
                db_c.NAME: "Facebook",
                db_c.TYPE: "facebook",
            },
            db_c.SIZE: 1000,
            api_c.MATCH_RATE: 0,
            api_c.DELIVERED: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        self.assertFalse(
            AudienceDeliveryHistorySchema().validate(delivery_history)
        )

        # deserialize the json document by loading it into the schema and
        # test the schema to have the match_rate value set
        schema = AudienceDeliveryHistorySchema().load(delivery_history)
        self.assertGreaterEqual(schema[api_c.MATCH_RATE], 0)

    def test_audience_standalone_deliveries_schema(self) -> None:
        """Test audience standalone deliveries schema."""

        audience_standalone_delivery_doc = {
            db_c.METRICS_DELIVERY_PLATFORM_NAME: "Facebook",
            api_c.DELIVERY_PLATFORM_TYPE: "facebook",
            api_c.STATUS: "Delivered",
            db_c.SIZE: 1000,
            db_c.AUDIENCE_LAST_DELIVERED: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        self.assertFalse(
            AudienceStandaloneDeliveriesSchema().validate(
                audience_standalone_delivery_doc
            )
        )
