# pylint: disable=no-self-use
"""
Purpose of this file is to test the engagement schemas
"""
from unittest import TestCase

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
    """Test Engagement Schema Classes"""

    def test_successful_engagement_get_schema(self) -> None:
        """Test Successful EngagementGetSchema Serialization

        Returns:
            Response: None

        """
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
        """Test Successful EngagementPostSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.NAME: "Engagement 1",
            api_c.DESCRIPTION: "Engagement 1 description",
            db_c.AUDIENCES: [],
            api_c.DELIVERY_SCHEDULE: {},
        }

        assert EngagementPostSchema().validate(doc) == {}

    def test_successful_engagement_put_schema(self) -> None:
        """Test Successful EngagementPutSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.NAME: "Engagement 1",
            api_c.DESCRIPTION: "Engagement 1 description",
        }

        assert EngagementPutSchema().validate(doc) == {}

    def test_unsuccessful_engagement_get_schema_bad_name(self) -> None:
        """Test unsuccessful EngagementGetSchema Serialization

        Returns:
            Response: None

        """
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
        """Test unsuccessful EngagementGetSchema Serialization

        Returns:
            Response: None

        """
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
        """Test unsuccessful EngagementPostSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.NAME: 3,
            api_c.DESCRIPTION: "Engagement 1 description",
            db_c.AUDIENCES: [],
            api_c.DELIVERY_SCHEDULE: {},
        }

        assert EngagementPostSchema().validate(doc) != {}

    def test_unsuccessful_engagement_put_schema_bad_field(self) -> None:
        """Test unsuccessful EngagementPutSchema Serialization

        Returns:
            Response: None

        """
        doc = {"SomeRandomField": "Some Random String"}

        assert EngagementPutSchema().validate(doc) != {}

    def test_successful_engagement_schedule_post_schema(self) -> None:
        """Test Successful EngagementPostSchema Serialization
        with a null delivery schedule.

        Returns:
            Response: None

        """
        doc = {
            api_c.NAME: "Engagement 1",
            api_c.DESCRIPTION: "Engagement 1 description",
            db_c.AUDIENCES: [],
            api_c.DELIVERY_SCHEDULE: None,
        }

        assert EngagementPostSchema().validate(doc) == {}

    def test_successful_engagement_no_schedule_post_schema(self) -> None:
        """Test Successful EngagementPostSchema Serialization
        with no delivery schedule.

        Returns:
            Response: None

        """
        doc = {
            api_c.NAME: "Engagement 1",
            api_c.DESCRIPTION: "Engagement 1 description",
            db_c.AUDIENCES: [],
        }

        assert EngagementPostSchema().validate(doc) == {}

    def test_successful_campaign_put_schema(self) -> None:
        """Test Successful EngagementPutSchema Serialization

        Returns:
            Response: None

        """
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
        """Test Successful EngagementPutSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.CAMPAIGNS: {
                api_c.NAME: "Engagement 1",
                api_c.ID: "campaign_id",
                api_c.DELIVERY_JOB_ID: "delivery_job_id",
            }
        }
        assert CampaignPutSchema().validate(doc) != {}

    def test_successful_campaign_get_schema(self) -> None:
        """Test Successful EngagementPutSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.NAME: "Engagement 1",
            api_c.ID: "5f5f7262997acad4bac4373b",
            api_c.DELIVERY_JOB_ID: "5f5f7262997acad4bac4373c",
            db_c.CREATE_TIME: "2021-07-06T13:21:11.181000",
        }
        assert CampaignSchema().validate(doc) == {}

    def test_unsuccessful_campaign_get_schema_missing_field(self) -> None:
        """Test Successful EngagementPutSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.NAME: "Engagement 1",
            api_c.ID: "campaign_id",
            db_c.CREATE_TIME: "2021-10-10",
        }
        assert CampaignSchema().validate(doc) != {}

    def test_unsuccessful_campaign_get_schema_invalid_objectid(self) -> None:
        """Test Successful EngagementPutSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.NAME: "Engagement 1",
            api_c.ID: "campaign_id",
            db_c.CREATE_TIME: "2021-10-10",
        }
        assert CampaignSchema().validate(doc) != {}

    def test_successful_campaignmapping_get_schema(self) -> None:
        """Test Successful EngagementPutSchema Serialization

        Returns:
            Response: None

        """
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
        """Test weighted ranking logic.

        Returns:
            Response: None

        """
        engagement = {
            api_c.ID: ObjectId(),
            api_c.AUDIENCES: [
                {
                    api_c.DESTINATIONS: [
                        {
                            api_c.ID: ObjectId(),
                            api_c.NAME: "Facebook",
                            api_c.LATEST_DELIVERY: {
                                db_c.ID: ObjectId(),
                                api_c.STATUS: api_c.STATUS_ERROR,
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

        # check engagement status per weighting
        self.assertEqual(weighted[api_c.STATUS], api_c.STATUS_ERROR)

        # check audience status per weighting
        for audience in weighted[api_c.AUDIENCES]:
            self.assertEqual(audience[api_c.STATUS], api_c.STATUS_ERROR)

    def test_weighted_ranking_bad_status(self) -> None:
        """Test weighted ranking logic.

        Returns:
            Response: None

        """
        bad_status_value = "bad_status_value"
        engagement = {
            api_c.ID: ObjectId(),
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
        self.assertEqual(weighted[api_c.STATUS], bad_status_value)

        # check audience status per weighting
        for audience in weighted[api_c.AUDIENCES]:
            self.assertEqual(audience[api_c.STATUS], bad_status_value)

    def test_weight_delivery_status(self) -> None:
        """Test weight_delivery_status.

        Returns:
            Response: None

        """

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
        """Test weight_delivery_status with a bad status.

        Returns:
            Response: None

        """

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
