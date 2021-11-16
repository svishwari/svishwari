# pylint: disable=no-self-use
"""Purpose of this file is to test the engagement schemas."""
from unittest import TestCase
from datetime import datetime, timedelta
from bson import ObjectId

from huxunifylib.database import constants as db_c
from huxunify.api.schema.engagement import (
    EngagementGetSchema,
    EngagementPostSchema,
    EngagementPutSchema,
    CampaignSchema,
    CampaignPutSchema,
    CampaignMappingSchema,
    weighted_engagement_status,
    weight_delivery_status,
)
from huxunify.api import constants as api_c


class EngagementSchemaTest(TestCase):
    """Test Engagement Schema Classes."""

    def test_successful_engagement_get_schema(self) -> None:
        """Test Successful EngagementGetSchema."""

        doc = {
            api_c.ID: "5f5f7262997acad4bac4373b",
            api_c.NAME: "Engagement 1",
            api_c.DESCRIPTION: "Engagement 1 description",
            db_c.AUDIENCES: [],
            api_c.STATUS: api_c.STATUS_ACTIVE,
            api_c.DELIVERY_SCHEDULE: {},
        }

        assert EngagementGetSchema().validate(doc) == {}

    def test_successful_engagement_post_schema(self) -> None:
        """Test Successful EngagementPostSchema."""

        doc = {
            api_c.NAME: "Engagement 1",
            api_c.DESCRIPTION: "Engagement 1 description",
            db_c.AUDIENCES: [],
            api_c.DELIVERY_SCHEDULE: {},
        }

        assert EngagementPostSchema().validate(doc) == {}

    def test_successful_engagement_put_schema(self) -> None:
        """Test Successful EngagementPutSchema."""

        doc = {
            api_c.NAME: "Engagement 1",
            api_c.DESCRIPTION: "Engagement 1 description",
            api_c.AUDIENCES: [
                {
                    db_c.OBJECT_ID: str(ObjectId()),
                    db_c.DESTINATIONS: [
                        {
                            db_c.OBJECT_ID: str(ObjectId()),
                            db_c.DELIVERY_JOB_ID: str(ObjectId()),
                        }
                    ],
                }
            ],
        }

        # ensure schema validates correctly
        self.assertFalse(EngagementPutSchema().validate(doc))

        # ensure each of the following fields are type ObjectId
        engagement = EngagementPutSchema().load(doc)

        for audience in engagement[db_c.AUDIENCES]:
            # check audience id
            self.assertIsInstance(audience[db_c.OBJECT_ID], ObjectId)
            for destination in audience[db_c.DESTINATIONS]:
                # test destination id and delivery job id
                self.assertIsInstance(destination[db_c.OBJECT_ID], ObjectId)
                self.assertIsInstance(
                    destination[db_c.DELIVERY_JOB_ID], ObjectId
                )

    def test_unsuccessful_engagement_get_schema_bad_name(self) -> None:
        """Test unsuccessful EngagementGetSchema."""

        doc = {
            api_c.ID: "5f5f7262997acad4bac4373b",
            api_c.NAME: 3,
            api_c.DESCRIPTION: "Engagement 1 description",
            db_c.AUDIENCES: [],
            api_c.STATUS: api_c.STATUS_ACTIVE,
            api_c.DELIVERY_SCHEDULE: {},
        }

        assert EngagementGetSchema().validate(doc) != {}

    def test_unsuccessful_engagement_get_schema_missing_audiences(
        self,
    ) -> None:
        """Test unsuccessful EngagementGetSchema."""

        doc = {
            api_c.ID: "5f5f7262997acad4bac4373b",
            api_c.NAME: "Engagement 1",
            api_c.DESCRIPTION: "Engagement 1 description",
            api_c.STATUS: api_c.STATUS_ACTIVE,
            api_c.DELIVERY_SCHEDULE: {},
            api_c.ENABLED: True,
        }

        assert EngagementGetSchema().validate(doc) != {}

    def test_unsuccessful_engagement_post_schema_bad_name(self) -> None:
        """Test unsuccessful EngagementPostSchema."""

        doc = {
            api_c.NAME: 3,
            api_c.DESCRIPTION: "Engagement 1 description",
            db_c.AUDIENCES: [],
            api_c.DELIVERY_SCHEDULE: {},
        }

        assert EngagementPostSchema().validate(doc) != {}

    def test_unsuccessful_engagement_put_schema_bad_field(self) -> None:
        """Test unsuccessful EngagementPutSchema."""

        doc = {"SomeRandomField": "Some Random String"}

        assert EngagementPutSchema().validate(doc) != {}

    def test_successful_engagement_schedule_post_schema(self) -> None:
        """Test Successful EngagementPostSchema with a null delivery schedule."""

        doc = {
            api_c.NAME: "Engagement 1",
            api_c.DESCRIPTION: "Engagement 1 description",
            db_c.AUDIENCES: [],
            api_c.DELIVERY_SCHEDULE: None,
        }

        assert EngagementPostSchema().validate(doc) == {}

    def test_successful_engagement_no_schedule_post_schema(self) -> None:
        """Test Successful EngagementPostSchema with no delivery schedule."""

        doc = {
            api_c.NAME: "Engagement 1",
            api_c.DESCRIPTION: "Engagement 1 description",
            db_c.AUDIENCES: [],
        }

        assert EngagementPostSchema().validate(doc) == {}

    def test_successful_campaign_put_schema(self) -> None:
        """Test Successful EngagementPutSchema."""

        doc = {
            api_c.CAMPAIGNS: [
                {
                    api_c.NAME: "Engagement 1",
                    api_c.ID: "campaign_id",
                    api_c.DELIVERY_JOB_ID: "delivery_job_id",
                }
            ]
        }
        assert CampaignPutSchema().validate(doc) == {}

    def test_unsuccessful_campaign_put_schema(self) -> None:
        """Test Successful EngagementPutSchema."""

        doc = {
            api_c.CAMPAIGNS: {
                api_c.NAME: "Engagement 1",
                api_c.ID: "campaign_id",
                api_c.DELIVERY_JOB_ID: "delivery_job_id",
            }
        }
        assert CampaignPutSchema().validate(doc) != {}

    def test_successful_campaign_get_schema(self) -> None:
        """Test Successful EngagementPutSchema."""

        doc = {
            api_c.NAME: "Engagement 1",
            api_c.ID: "5f5f7262997acad4bac4373b",
            api_c.DELIVERY_JOB_ID: "5f5f7262997acad4bac4373c",
            db_c.CREATE_TIME: "2021-07-06T13:21:11.181000",
        }
        assert CampaignSchema().validate(doc) == {}

    def test_unsuccessful_campaign_get_schema_missing_field(self) -> None:
        """Test Successful EngagementPutSchema."""

        doc = {
            api_c.NAME: "Engagement 1",
            api_c.ID: str(ObjectId()),
            db_c.CREATE_TIME: "2021-10-10",
        }
        assert CampaignSchema().validate(doc) != {}

    def test_unsuccessful_campaign_get_schema_invalid_objectid(self) -> None:
        """Test Successful EngagementPutSchema."""

        doc = {
            api_c.NAME: "Engagement 1",
            api_c.ID: str(ObjectId()),
            db_c.CREATE_TIME: "2021-10-10",
        }
        assert CampaignSchema().validate(doc) != {}

    def test_successful_campaignmapping_get_schema(self) -> None:
        """Test Successful EngagementPutSchema."""

        doc = {
            api_c.CAMPAIGNS: [
                {
                    api_c.NAME: "Engagement 1",
                    api_c.ID: "5f5f7262997acad4bac4373b",
                }
            ],
            "delivery_jobs": [
                {
                    api_c.ID: "5f5f7262997acad4bac4373c",
                    db_c.CREATE_TIME: "2021-07-06T13:21:11.181000",
                }
            ],
        }
        assert CampaignMappingSchema().validate(doc) == {}

    def test_weighted_ranking(self) -> None:
        """Test weighted ranking logic."""

        engagement = {
            db_c.ID: ObjectId(),
            api_c.AUDIENCES: [
                {
                    api_c.DESTINATIONS: [
                        {
                            api_c.ID: ObjectId(),
                            api_c.NAME: "Facebook",
                            api_c.LATEST_DELIVERY: {
                                db_c.ID: ObjectId(),
                                api_c.STATUS: api_c.STATUS_DELIVERING,
                            },
                        },
                        {
                            api_c.ID: ObjectId(),
                            api_c.NAME: "Facebook",
                            api_c.LATEST_DELIVERY: {
                                db_c.ID: ObjectId(),
                                api_c.STATUS: api_c.STATUS_DELIVERED,
                            },
                        },
                    ],
                    api_c.NAME: "SFMC Demo",
                    api_c.ID: ObjectId(),
                }
            ],
        }

        # test the weights
        weighted = weighted_engagement_status([engagement])[0]

        # check audience status per weighting
        for audience in weighted[api_c.AUDIENCES]:
            self.assertEqual(audience[api_c.STATUS], api_c.STATUS_DELIVERING)

        # check engagement status per weighting
        self.assertEqual(weighted[api_c.STATUS], api_c.STATUS_DELIVERING)

        # Test "Active" status for engagement
        engagement = {
            db_c.ID: ObjectId(),
            api_c.AUDIENCES: [
                {
                    api_c.DESTINATIONS: [
                        {
                            api_c.ID: ObjectId(),
                            api_c.NAME: "Facebook",
                            api_c.LATEST_DELIVERY: {
                                db_c.ID: ObjectId(),
                                api_c.STATUS: api_c.STATUS_DELIVERED,
                            },
                        },
                    ],
                    api_c.NAME: "SFMC Demo",
                    api_c.ID: ObjectId(),
                }
            ],
            api_c.DELIVERY_SCHEDULE: {
                api_c.START_DATE: datetime.today() - timedelta(days=10),
                api_c.END_DATE: datetime.today() + timedelta(days=5),
                api_c.SCHEDULE: {
                    api_c.EVERY: 3,
                    api_c.MINUTE: 15,
                    api_c.PERIODICIY: "Daily",
                    api_c.HOUR: 11,
                    api_c.PERIOD: "PM",
                },
                api_c.SCHEDULE_CRON: "15 23 */3 * ? *",
            },
        }

        weighted = weighted_engagement_status([engagement])[0]
        self.assertEqual(weighted[api_c.STATUS], api_c.STATUS_ACTIVE)

        # Test "Inactive" status for engagement
        engagement[api_c.DELIVERY_SCHEDULE] = {
            api_c.START_DATE: datetime.today() - timedelta(days=10),
            api_c.END_DATE: datetime.today() - timedelta(days=5),
            api_c.SCHEDULE: {
                api_c.EVERY: 3,
                api_c.MINUTE: 15,
                api_c.PERIODICIY: "Daily",
                api_c.HOUR: 11,
                api_c.PERIOD: "PM",
            },
            api_c.SCHEDULE_CRON: "15 23 */3 * ? *",
        }
        weighted = weighted_engagement_status([engagement])[0]
        self.assertEqual(weighted[api_c.STATUS], api_c.STATUS_INACTIVE)

        engagement[api_c.STATUS] = api_c.STATUS_INACTIVE
        engagement[api_c.DELIVERY_SCHEDULE] = {
            api_c.START_DATE: datetime.today() - timedelta(days=10),
            api_c.END_DATE: datetime.today() + timedelta(days=5),
            api_c.SCHEDULE: {
                api_c.EVERY: 3,
                api_c.MINUTE: 15,
                api_c.PERIODICIY: "Daily",
                api_c.HOUR: 11,
                api_c.PERIOD: "PM",
            },
            api_c.SCHEDULE_CRON: "15 23 */3 * ? *",
        }
        weighted = weighted_engagement_status([engagement])[0]
        self.assertEqual(weighted[api_c.STATUS], api_c.STATUS_INACTIVE)

    def test_weighted_ranking_bad_status(self) -> None:
        """Test weighted ranking logic."""

        bad_status_value = "bad_status_value"
        engagement = {
            db_c.ID: ObjectId(),
            api_c.AUDIENCES: [
                {
                    api_c.DESTINATIONS: [
                        {
                            api_c.ID: ObjectId(),
                            api_c.NAME: "Facebook",
                            api_c.LATEST_DELIVERY: {
                                db_c.ID: ObjectId(),
                                api_c.STATUS: bad_status_value,
                            },
                        },
                    ],
                    api_c.NAME: "SFMC Demo",
                    api_c.ID: ObjectId(),
                }
            ],
        }

        # test the weights
        weighted = weighted_engagement_status([engagement])[0]

        # check engagement status per weighting
        self.assertEqual(weighted[api_c.STATUS], api_c.STATUS_ERROR)

        # check audience status per weighting
        for audience in weighted[api_c.AUDIENCES]:
            self.assertEqual(audience[api_c.STATUS], api_c.STATUS_ERROR)

    def test_weight_delivery_status(self) -> None:
        """Test weight delivery status."""

        engagement = {
            "deliveries": [
                {
                    "status": "Failed",
                },
                {
                    "status": "In progress",
                },
            ],
        }

        # check engagement status per weighting
        self.assertEqual(
            db_c.STATUS_FAILED, weight_delivery_status(engagement)
        )

    def test_weight_delivery_bad_status(self) -> None:
        """Test weight delivery status with a bad status."""

        engagement = {
            "deliveries": [
                {
                    "status": "bad",
                },
                {
                    "status": "In progress",
                },
            ],
        }

        # check engagement status per weighting
        self.assertEqual("bad", weight_delivery_status(engagement))

    def test_match_rate_engagement_get_schema(self) -> None:
        """Test engagement get schema match_rate."""

        engagement = {
            api_c.ID: "5f5f7262997acad4bac4374a",
            api_c.NAME: "Engagement 1",
            api_c.STATUS: api_c.STATUS_ACTIVE,
            api_c.AUDIENCES: [
                {
                    api_c.ID: "5f5f7262997acad4bac4373a",
                    api_c.NAME: "facebook",
                    api_c.DESTINATIONS: [
                        {
                            api_c.ID: "5f5f7262997acad4bac4373b",
                            api_c.NAME: "Facebook",
                            api_c.LATEST_DELIVERY: {
                                api_c.ID: "5f5f7262997acad4bac4373c",
                                api_c.STATUS: api_c.STATUS_ERROR,
                                api_c.MATCH_RATE: 0,
                            },
                        },
                        {
                            api_c.ID: "5f5f7262997acad4bac4373d",
                            api_c.NAME: "Facebook",
                            api_c.LATEST_DELIVERY: {
                                api_c.ID: "5f5f7262997acad4bac4373e",
                                api_c.STATUS: api_c.STATUS_DELIVERED,
                                api_c.MATCH_RATE: 0,
                            },
                        },
                    ],
                }
            ],
        }

        self.assertFalse(EngagementGetSchema().validate(engagement))

        # deserialize the json document by loading it into the schema and
        # test the schema to have the match_rate value set
        schema = EngagementGetSchema().load(engagement)

        destinations = schema[api_c.AUDIENCES][0][api_c.DESTINATIONS]
        self.assertGreaterEqual(
            destinations[0][api_c.LATEST_DELIVERY][api_c.MATCH_RATE], 0
        )
        self.assertGreaterEqual(
            destinations[1][api_c.LATEST_DELIVERY][api_c.MATCH_RATE], 0
        )
