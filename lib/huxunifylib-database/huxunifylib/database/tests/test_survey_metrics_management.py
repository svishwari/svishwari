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

        responses = {
            "VXID": "01202482628359",
            "Adobe ID": "02482628359",
            "Customer Email": "sample@email.com",
            "Survey Time to Complete (in Minutes)": 59,
            "survey_is_mobile": "Yes",
            "Banner Indicator": "Yes",
            "trustid_brand_unit": "brand_unit",
            "Consent Statement": "Yes, I agree to proceed",
            "HUM_Demonstrates empathy and kindness towards me, and treats everyone fairly": 4,
            "REL_Consistently and dependably delivers upon promises it makes": 5,
            "CAP_Creates quality products, services, and/or experiences": 2,
            "TRA_Openly shares all information, motives, and choices in straightforward and plain language": 4,
            "REL_Facilitates digital interactions that run smoothly and work when needed": 3,
            "HUM_Customer support team quickly resolves issues with my safety, security, and satisfaction top of mind": 5,
            "Children in Household": "",
            "Household Seniors Y/N": "",
            "Age": "",
            "Time": "",
            "StraightLine": "",
            "USE": "",
            "prospect_with_vxid": "",
            "HUMANITY": "",
            "RELIABILITY": "",
            "CAPABILITY": "",
            "TRANSPARENCY": "",
            "TopCategory": "",
            "TopCategory_HL": "",
            "Per_Web": "",
            "Prospect_Temp": "",
            "Existing_Class": "",
            "VisitsTotal": "",
            "activeDays": "",
            "VisitsWeb": "",
            "VisitsApps": "",
            "activeDaysThisWeek": "",
            "viewsArts": "",
            "viewsBusiness": 0,
            "viewsCareers": 0,
        }

        # Survey Response 1
        insert_doc = set_survey_response(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            delivery_platform_type="trust-id",
            survey_id="05957cf207be7d88638",
            url="sample@trustdomain.com",
            response_date=datetime.datetime.utcnow(),
            customer_id="127956489",
            responses_dict=responses,
        )

        self.assertIsNotNone(insert_doc)
        self.assertEqual(insert_doc[db_c.SURVEY_ID], "05957cf207be7d88638")
        self.assertEqual(insert_doc[db_c.DELIVERY_PLATFORM_TYPE], "trust-id")
        self.assertEqual(
            insert_doc[db_c.S_TYPE_SURVEY_CUSTOMER_ID], "127956489"
        )
        self.assertEqual(insert_doc[db_c.SURVEY_URL], "sample@trustdomain.com")

    def test_set_survey_responses_bulk(self):
        """Test set survey response bulk in Survey Metrics collection"""

        # Sample Response 1
        responses_1 = {
            "VXID": "01202482628359",
            "Adobe ID": "02482628359",
            "Customer Email": "sample@email.com",
            "Survey Time to Complete (in Minutes)": 59,
            "survey_is_mobile": "Yes",
            "Banner Indicator": "Yes",
            "trustid_brand_unit": "brand_unit",
            "Consent Statement": "Yes, I agree to proceed",
            "HUM_Demonstrates empathy and kindness towards me, and treats everyone fairly": 4,
            "REL_Consistently and dependably delivers upon promises it makes": 5,
            "CAP_Creates quality products, services, and/or experiences": 2,
            "TRA_Openly shares all information, motives, and choices in straightforward and plain language": 4,
            "REL_Facilitates digital interactions that run smoothly and work when needed": 3,
            "HUM_Customer support team quickly resolves issues with my safety, security, and satisfaction top of mind": 5,
            "Children in Household": "",
            "Household Seniors Y/N": "",
            "Age": "",
            "Time": "",
            "StraightLine": "",
            "USE": "",
            "prospect_with_vxid": "",
            "HUMANITY": "",
            "RELIABILITY": "",
            "CAPABILITY": "",
            "TRANSPARENCY": "",
            "TopCategory": "",
            "TopCategory_HL": "",
            "Per_Web": "",
            "Prospect_Temp": "",
            "Existing_Class": "",
            "VisitsTotal": "",
            "activeDays": "",
            "VisitsWeb": "",
            "VisitsApps": "",
            "activeDaysThisWeek": "",
            "viewsArts": "",
            "viewsBusiness": 0,
            "viewsCareers": 0,
        }

        # Sample Response 2
        responses_2 = {
            "VXID": "01202482628359",
            "Adobe ID": "02482628359",
            "Customer Email": "sample@email.com",
            "Survey Time to Complete (in Minutes)": 59,
            "survey_is_mobile": "Yes",
            "Banner Indicator": "Yes",
            "trustid_brand_unit": "brand_unit",
            "Consent Statement": "Yes, I agree to proceed",
            "HUM_Demonstrates empathy and kindness towards me, and treats everyone fairly": 4,
            "REL_Consistently and dependably delivers upon promises it makes": 5,
            "CAP_Creates quality products, services, and/or experiences": 2,
            "TRA_Openly shares all information, motives, and choices in straightforward and plain language": 4,
            "REL_Facilitates digital interactions that run smoothly and work when needed": 3,
            "HUM_Customer support team quickly resolves issues with my safety, security, and satisfaction top of mind": 5,
            "Children in Household": "",
            "Household Seniors Y/N": "",
            "Age": "",
            "Time": "",
            "HUMANITY": "",
            "RELIABILITY": "",
            "CAPABILITY": "",
            "TRANSPARENCY": "",
            "TopCategory": "",
            "activeDays": "",
            "VisitsWeb": "",
            "VisitsApps": "",
            "activeDaysThisWeek": "",
            "viewsArts": "",
            "viewsBusiness": 0,
            "viewsCareers": 0,
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
            db_c.SURVEY_URL: "https://survey-demo.com/v1",
            db_c.SURVEY_ID: "34dmwnkq9ae32fo0s",
            db_c.SURVEY_RESPONSES: responses_2,
            "responses": responses_1,
        }
        sample_response_doc2 = {
            db_c.DELIVERY_PLATFORM_TYPE: "trust-id",
            db_c.DELIVERY_PLATFORM_ID: self.delivery_platform_doc[db_c.ID],
            db_c.CREATE_TIME: datetime.datetime(
                2022, 3, 27, 14, 4, 15, 369000
            ),
            db_c.S_TYPE_SURVEY_CUSTOMER_ID: "12424873",
            db_c.SURVEY_RESPONSE_DATE: datetime.datetime(
                2022, 3, 27, 14, 4, 15, 369000
            ),
            db_c.SURVEY_URL: "https://survey-demo.com/v2",
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
