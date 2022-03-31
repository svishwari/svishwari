"""Database client Trust ID survey metrics management tests."""

import unittest
import datetime
import mongomock
import huxunifylib.database.constants as db_c

from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
)
from huxunifylib.database.survey_metrics_management import (
    set_survey_response,
    set_survey_responses_bulk,
)


class TestSurveyMetricsManagement(unittest.TestCase):
    """Test survey metrics management module."""

    def setUp(self) -> None:
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # Connect
        self.database = DatabaseClient(host="localhost", port=27017).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        self.delivery_platform_doc = set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_TRUST_ID,
            "Delivery platform for Trust ID",
            status=db_c.STATUS_SUCCEEDED,
        )

    def test_set_survey_response(self):
        """Test set survey response in Survey Metrics collection"""

        # Survey Response 1
        responses = {
            "signals": [
                {
                    "HUMANITY": {
                        "attributes": [
                            {
                                "description": "Takes care of employees",
                                "score": 4,
                                "rating": 0,
                            }
                        ],
                        "score": 4,
                        "rating": 0,
                    },
                    "CAPABILITY": {
                        "attributes": [
                            {
                                "description": "Creates long term solutions that work well",
                                "score": 4,
                                "rating": 0,
                            }
                        ],
                        "score": 5,
                        "rating": 0,
                    },
                    "TRANSPARENCY": {
                        "attributes": [
                            {
                                "description": "marketing and communications are accurate",
                                "score": 5,
                                "rating": 0,
                            }
                        ],
                        "score": 5,
                        "rating": 0,
                    },
                    "RELIABILITY": {
                        "attributes": [
                            {
                                "description": "Consistently delivers upon promises it makes",
                                "score": 4,
                                "rating": 0,
                            }
                        ],
                        "score": 5,
                        "rating": 0,
                    },
                }
            ],
            "VXID": 232134,
            "Adobe ID": 482628359,
            "Customer Email": "sample@email.com",
            "Survey Time to Complete (in Minutes)": 59,
            "survey_is_mobile": "Yes",
            "Banner Indicator": "Yes",
            "trustid_brand_unit": "brand_unit",
            "Consent Statement": "Yes, I agree to proceed",
            "Children in Household": "",
            "Household Seniors Y/N": "",
            "Employment Status": "",
            "Opinion_Bucket": "",
            "TopCategory": "",
            "TopCategory_HL": "",
            "desktop": "",
            "Tenure (days)": "",
            "Tenure (months)": "",
            "channel": "",
            "recency": "",
            "freq": "",
        }

        insert_doc = set_survey_response(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            delivery_platform_type="trust_id",
            survey_id="05957cf207be7d88638",
            url="sample@trustdomain.com",
            response_date=datetime.datetime.utcnow(),
            customer_id="127956489",
            responses_dict=responses,
        )

        self.assertIsNotNone(insert_doc)
        self.assertEqual(insert_doc[db_c.SURVEY_ID], "05957cf207be7d88638")
        self.assertEqual(insert_doc[db_c.DELIVERY_PLATFORM_TYPE], "trust_id")
        self.assertEqual(
            insert_doc[db_c.S_TYPE_SURVEY_CUSTOMER_ID], "127956489"
        )
        self.assertEqual(insert_doc[db_c.URL], "sample@trustdomain.com")

    def test_set_survey_responses_bulk(self):
        """Test set survey response bulk in Survey Metrics collection"""

        # Sample Response 1
        responses_1 = {
            "signals": [
                {
                    "HUMANITY": {
                        "attributes": [
                            {
                                "description": "Takes care of employees",
                                "score": 4,
                                "rating": 0,
                            }
                        ],
                        "score": 4,
                        "rating": 0,
                    },
                    "CAPABILITY": {
                        "attributes": [
                            {
                                "description": "Creates long term solutions that work well",
                                "score": 4,
                                "rating": 0,
                            }
                        ],
                        "score": 5,
                        "rating": 0,
                    },
                    "TRANSPARENCY": {
                        "attributes": [
                            {
                                "description": "marketing and communications are accurate",
                                "score": 5,
                                "rating": 0,
                            }
                        ],
                        "score": 5,
                        "rating": 0,
                    },
                    "RELIABILITY": {
                        "attributes": [
                            {
                                "description": "Consistently delivers upon promises it makes",
                                "score": 4,
                                "rating": 0,
                            }
                        ],
                        "score": 5,
                        "rating": 0,
                    },
                }
            ],
            "VXID": 232134,
            "Adobe ID": 482628359,
            "Customer Email": "sample@email.com",
            "Survey Time to Complete (in Minutes)": 59,
            "survey_is_mobile": "Yes",
            "Banner Indicator": "Yes",
            "trustid_brand_unit": "brand_unit",
            "Consent Statement": "Yes, I agree to proceed",
            "Children in Household": "",
            "Household Seniors Y/N": "",
            "Employment Status": "",
            "Opinion_Bucket": "",
            "TopCategory": "",
            "TopCategory_HL": "",
            "desktop": "",
            "Tenure (days)": "",
            "Tenure (months)": "",
            "channel": "",
            "recency": "",
            "freq": "",
        }

        # Sample Response 2
        responses_2 = {
            "signals": [
                {
                    "HUMANITY": {
                        "attributes": [
                            {
                                "description": "Takes care of employees",
                                "score": 4,
                                "rating": 0,
                            }
                        ],
                        "score": 4,
                        "rating": 0,
                    },
                    "CAPABILITY": {
                        "attributes": [
                            {
                                "description": "Creates long term solutions that work well",
                                "score": 4,
                                "rating": 0,
                            }
                        ],
                        "score": 5,
                        "rating": 0,
                    },
                    "TRANSPARENCY": {
                        "attributes": [
                            {
                                "description": "marketing and communications are accurate",
                                "score": 5,
                                "rating": 0,
                            }
                        ],
                        "score": 5,
                        "rating": 0,
                    },
                    "RELIABILITY": {
                        "attributes": [
                            {
                                "description": "Consistently delivers upon promises it makes",
                                "score": 4,
                                "rating": 0,
                            }
                        ],
                        "score": 5,
                        "rating": 0,
                    },
                }
            ],
            "VXID": 232134,
            "Adobe ID": 482628359,
            "Customer Email": "sample@email.com",
            "Survey Time to Complete (in Minutes)": 59,
            "survey_is_mobile": "Yes",
            "Banner Indicator": "Yes",
            "trustid_brand_unit": "brand_unit",
            "Consent Statement": "Yes, I agree to proceed",
            "Children in Household": "",
            "Household Seniors Y/N": "",
            "Employment Status": "",
            "Opinion_Bucket": "",
            "TopCategory": "",
            "TopCategory_HL": "",
            "desktop": "",
            "Tenure (days)": "",
            "Tenure (months)": "",
            "channel": "",
            "recency": "",
            "freq": "",
        }

        sample_response_doc1 = {
            db_c.DELIVERY_PLATFORM_TYPE: "trust-id",
            db_c.DELIVERY_PLATFORM_ID: self.delivery_platform_doc[db_c.ID],
            db_c.CREATE_TIME: datetime.datetime(
                2022, 3, 28, 14, 4, 15, 369000
            ),
            db_c.S_TYPE_SURVEY_CUSTOMER_ID: "12424873",
            db_c.SURVEY_RESPONSE_DATE: datetime.datetime(
                2022, 3, 28, 14, 4, 15, 369000
            ),
            db_c.URL: "https://survey-demo.com/v1",
            db_c.SURVEY_ID: "34dmwnkq9ae32fo0s",
            db_c.SURVEY_RESPONSES: responses_2,
            "responses": responses_1,
        }
        sample_response_doc2 = {
            db_c.DELIVERY_PLATFORM_TYPE: "trust_id",
            db_c.DELIVERY_PLATFORM_ID: self.delivery_platform_doc[db_c.ID],
            db_c.CREATE_TIME: datetime.datetime(
                2022, 3, 27, 14, 4, 15, 369000
            ),
            db_c.S_TYPE_SURVEY_CUSTOMER_ID: "12424873",
            db_c.SURVEY_RESPONSE_DATE: datetime.datetime(
                2022, 3, 27, 14, 4, 15, 369000
            ),
            db_c.URL: "https://survey-demo.com/v2",
            db_c.SURVEY_ID: "34dmwn39dmie32fo0s",
            db_c.SURVEY_RESPONSES: responses_2,
        }
        sample_responses_list = [sample_response_doc1, sample_response_doc2]

        # Survey Response 1
        insert_result = set_survey_responses_bulk(
            database=self.database, survey_responses_docs=sample_responses_list
        )

        self.assertTrue(insert_result["insert_status"])
        self.assertIsNotNone(insert_result["inserted_ids"])
