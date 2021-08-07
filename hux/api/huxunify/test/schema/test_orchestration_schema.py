# pylint: disable=no-self-use
"""
Purpose of this file is to test the orchestration schemas
"""
from unittest import TestCase
from datetime import datetime
from random import uniform

from huxunifylib.database import constants as db_c
from huxunify.api.schema.orchestration import (
    AudienceGetSchema,
    EngagementDeliveryHistorySchema,
    AudienceDeliveryHistorySchema,
)
from huxunify.api import constants as api_c


class OrchestrationSchemaTest(TestCase):
    """
    Test Orchestration Schema Classes
    """

    def test_successful_audience_get_schema(self) -> None:
        """
        Test Successful EngagementGetSchema Serialization

        Args:

        Returns:
            None
        """

        doc = {
            api_c.ID: "5f5f7262997acad4bac4384a",
            db_c.NAME: "Audience 1",
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

        self.assertFalse(AudienceGetSchema().validate(doc))

    def test_unsuccessful_audience_get_schema_bad_name(self) -> None:
        """
        Test unsuccessful AudienceGetSchema serialization

        Args:

        Returns:
            None
        """

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
        """
        Test unsuccessful AudienceGetSchema engagement no name serialization

        Args:

        Returns:
            None
        """

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
        """
        Test audience get schema match_rate.

        Args:

        Returns:
            None
        """

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
                            api_c.MATCH_RATE: round(uniform(0.2, 0.9), 2),
                        },
                        {
                            api_c.ID: "5f5f7262997acad4bac4384d",
                            db_c.NAME: "Delivery 2",
                            db_c.SIZE: 1000,
                            api_c.MATCH_RATE: round(uniform(0.2, 0.9), 2),
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

        deliveries = audience[db_c.ENGAGEMENTS_COLLECTION][0][db_c.DELIVERIES]

        self.assertGreater(deliveries[0][api_c.MATCH_RATE], 0.2)
        self.assertGreater(deliveries[1][api_c.MATCH_RATE], 0.2)

    def test_engagement_delivery_history_schema(self) -> None:
        """
        Test engagement delivery history schema.

        Args:

        Returns:
            None
        """

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
        """
        Test engagement delivery history schema match_rate.

        Args:

        Returns:
            None
        """

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
            api_c.MATCH_RATE: round(uniform(0.2, 0.9), 2),
            api_c.DELIVERED: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        self.assertFalse(
            EngagementDeliveryHistorySchema().validate(delivery_history)
        )

        self.assertGreater(delivery_history[api_c.MATCH_RATE], 0.2)

    def test_audience_delivery_history_schema(self) -> None:
        """
        Test audience delivery history schema.

        Args:

        Returns:
            None
        """

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

    def test_match_rate_audience_delivery_history_schema(self) -> None:
        """
        Test audience delivery history schema match_rate.

        Args:

        Returns:
            None
        """

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
            api_c.MATCH_RATE: round(uniform(0.2, 0.9), 2),
            api_c.DELIVERED: datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

        self.assertFalse(
            AudienceDeliveryHistorySchema().validate(delivery_history)
        )

        self.assertGreater(delivery_history[api_c.MATCH_RATE], 0.2)
