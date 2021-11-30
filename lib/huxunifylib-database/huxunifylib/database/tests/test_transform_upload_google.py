"""Dataframe transformation for File upload to Google unittests."""
import unittest
from typing import Dict

import pandas as pd
from pandas._testing import assert_frame_equal

import huxunifylib.database.constants as db_c
from huxunifylib.database.transform import transform_dataframe as td
from huxunifylib.database.db_exceptions import HuxAdvException


class TestUploadFieldsGoogle(unittest.TestCase):
    """Dataframe is transformed for file upload to Google."""

    @staticmethod
    def _test_upload_fields_google(
        special_types_data: Dict[str, list],
        expected_data: Dict[str, list],
    ):
        """Transform special types, auxiliary method.

        Args:
            special_types_data (Dict[str, list]): Special types data.
            expected_data (Dict[str, list]): Expected Google field data.
        """
        special_types_df = pd.DataFrame(special_types_data)

        actual = td.transform_fields_google_file(special_types_df)

        assert_frame_equal(
            actual,
            pd.DataFrame(expected_data),
            check_like=True,
        )

    def test_full_match_firstname_initial(self):
        """Special Types are transformed to google field names with
        all google match criteria satisfied.
        Both First Name and First Name Initial are specified.
        """
        special_types_data = {
            db_c.S_TYPE_COUNTRY_CODE_HASHED: ["US", "UK"],
            db_c.S_TYPE_MOBILE_DEVICE_ID: ["123-456", "987-654"],
            db_c.S_TYPE_EMAIL_HASHED: ["email1", "email2"],
            db_c.S_TYPE_FIRST_NAME_HASHED: ["first_name1", "first_name2"],
            db_c.S_TYPE_FIRST_NAME_INITIAL_HASHED: ["initial_1", "initial_2"],
            db_c.S_TYPE_LAST_NAME_HASHED: ["last_name1", "last_name2"],
            db_c.S_TYPE_PHONE_NUMBER_HASHED: ["+11234567890", "+441234567890"],
            db_c.S_TYPE_POSTAL_CODE_HASHED: ["12345", "67890"],
        }

        expected_data = {
            "Country": ["US", "UK"],
            "Email": ["email1", "email2"],
            "First Name": ["first_name1", "first_name2"],
            "Last Name": ["last_name1", "last_name2"],
            "Phone": ["+11234567890", "+441234567890"],
            "Zip": ["12345", "67890"],
        }

        self._test_upload_fields_google(special_types_data, expected_data)

    def test_extra_field_discarded(self):
        """Special Types are transformed to google field names with
        non-match special type specified.
        """
        special_types_data = {
            db_c.S_TYPE_COUNTRY_CODE_HASHED: ["US", "UK"],
            db_c.S_TYPE_MOBILE_DEVICE_ID: ["123-456", "987-654"],
            db_c.S_TYPE_EMAIL_HASHED: ["email1", "email2"],
            db_c.S_TYPE_FIRST_NAME_HASHED: ["first_name1", "first_name2"],
            db_c.S_TYPE_FIRST_NAME_INITIAL_HASHED: ["initial_1", "initial_2"],
            db_c.S_TYPE_LAST_NAME_HASHED: ["last_name1", "last_name2"],
            db_c.S_TYPE_PHONE_NUMBER_HASHED: ["+11234567890", "+441234567890"],
            db_c.S_TYPE_POSTAL_CODE_HASHED: ["12345", "67890"],
            "extra_field": ["abc", "def"],
        }

        expected_data = {
            "Country": ["US", "UK"],
            "Email": ["email1", "email2"],
            "First Name": ["first_name1", "first_name2"],
            "Last Name": ["last_name1", "last_name2"],
            "Phone": ["+11234567890", "+441234567890"],
            "Zip": ["12345", "67890"],
        }

        self._test_upload_fields_google(special_types_data, expected_data)

    def test_full_match_firstname_no_initial(self):
        """Special Types are transformed to upload google field names with
        all google match criteria satisfied.
        First Name is specified, First Name Initial is omitted.
        """
        special_types_data = {
            db_c.S_TYPE_COUNTRY_CODE_HASHED: ["US", "UK"],
            db_c.S_TYPE_MOBILE_DEVICE_ID: ["123-456", "987-654"],
            db_c.S_TYPE_EMAIL_HASHED: ["email1", "email2"],
            db_c.S_TYPE_FIRST_NAME_HASHED: ["first_name1", "first_name2"],
            db_c.S_TYPE_LAST_NAME_HASHED: ["last_name1", "last_name2"],
            db_c.S_TYPE_PHONE_NUMBER_HASHED: ["+11234567890", "+441234567890"],
            db_c.S_TYPE_POSTAL_CODE_HASHED: ["12345", "67890"],
        }

        expected_data = {
            "Country": ["US", "UK"],
            "Email": ["email1", "email2"],
            "First Name": ["first_name1", "first_name2"],
            "Last Name": ["last_name1", "last_name2"],
            "Phone": ["+11234567890", "+441234567890"],
            "Zip": ["12345", "67890"],
        }

        self._test_upload_fields_google(special_types_data, expected_data)

    def test_full_match_initial_no_firstname(self):
        """Special Types are transformed to upload google field names with
        all google match criteria satisfied.
        First Name is omitted, First Name Initial is specified.
        """
        special_types_data = {
            db_c.S_TYPE_COUNTRY_CODE_HASHED: ["US", "UK"],
            db_c.S_TYPE_MOBILE_DEVICE_ID: ["123-456", "987-654"],
            db_c.S_TYPE_EMAIL_HASHED: ["email1", "email2"],
            db_c.S_TYPE_FIRST_NAME_INITIAL_HASHED: ["initial_1", "initial_2"],
            db_c.S_TYPE_LAST_NAME_HASHED: ["last_name1", "last_name2"],
            db_c.S_TYPE_PHONE_NUMBER_HASHED: ["+11234567890", "+441234567890"],
            db_c.S_TYPE_POSTAL_CODE_HASHED: ["12345", "67890"],
        }

        expected_data = {
            "Country": ["US", "UK"],
            "Email": ["email1", "email2"],
            "First Name": ["initial_1", "initial_2"],
            "Last Name": ["last_name1", "last_name2"],
            "Phone": ["+11234567890", "+441234567890"],
            "Zip": ["12345", "67890"],
        }

        self._test_upload_fields_google(special_types_data, expected_data)

    def test_email_only_match(self):
        """Special Types are transformed to upload google field names with
        only Email is specified.
        """
        special_types_data = {
            db_c.S_TYPE_EMAIL_HASHED: ["email1", "email2"],
        }

        expected_data = {"Email": ["email1", "email2"]}

        self._test_upload_fields_google(special_types_data, expected_data)

    def test_email_match_mobile_id(self):
        """Special Types are transformed to upload google field names with
        Email and Mobile ID specified.
        """
        special_types_data = {
            db_c.S_TYPE_EMAIL_HASHED: ["email1", "email2"],
            db_c.S_TYPE_MOBILE_DEVICE_ID: ["123-456", "987-654"],
        }

        expected_data = {"Email": ["email1", "email2"]}

        self._test_upload_fields_google(special_types_data, expected_data)

    def test_email_match_partial_address(self):
        """Special Types are transformed to upload google field names with
        Email and partial address match specified.
        """
        special_types_data = {
            db_c.S_TYPE_COUNTRY_CODE_HASHED: ["US", "UK"],
            db_c.S_TYPE_EMAIL_HASHED: ["email1", "email2"],
            db_c.S_TYPE_LAST_NAME_HASHED: ["last_name1", "last_name2"],
            db_c.S_TYPE_POSTAL_CODE_HASHED: ["12345", "67890"],
        }

        expected_data = {
            "Country": ["US", "UK"],
            "Email": ["email1", "email2"],
            "Last Name": ["last_name1", "last_name2"],
            "Zip": ["12345", "67890"],
        }

        self._test_upload_fields_google(special_types_data, expected_data)

    def test_email_and_phone_match(self):
        """Special Types are transformed to upload google field names with
        Email and Phone is specified.
        """
        special_types_data = {
            db_c.S_TYPE_EMAIL_HASHED: ["email1", "email2"],
            db_c.S_TYPE_PHONE_NUMBER_HASHED: ["+11234567890", "+441234567890"],
        }

        expected_data = {
            "Email": ["email1", "email2"],
            "Phone": ["+11234567890", "+441234567890"],
        }

        self._test_upload_fields_google(special_types_data, expected_data)

    def test_address_match(self):
        """Special Types are transformed to upload google field names with
        Only full address match is satisfied.
        """
        special_types_data = {
            db_c.S_TYPE_COUNTRY_CODE_HASHED: ["US", "UK"],
            db_c.S_TYPE_FIRST_NAME_INITIAL_HASHED: ["initial_1", "initial_2"],
            db_c.S_TYPE_LAST_NAME_HASHED: ["last_name1", "last_name2"],
            db_c.S_TYPE_POSTAL_CODE_HASHED: ["12345", "67890"],
        }

        expected_data = {
            "Country": ["US", "UK"],
            "First Name": ["initial_1", "initial_2"],
            "Last Name": ["last_name1", "last_name2"],
            "Zip": ["12345", "67890"],
        }

        self._test_upload_fields_google(special_types_data, expected_data)

    def test_mobile_id_match(self):
        """Special Types are transformed to google field names with
        only Mobile ID specified.
        """
        special_types_data = {
            db_c.S_TYPE_MOBILE_DEVICE_ID: ["123-456", "987-654"],
        }

        expected_data = {"Mobile Device ID": ["123-456", "987-654"]}

        self._test_upload_fields_google(special_types_data, expected_data)

    def test_mobile_id_match_extra_field_discarded(self):
        """Special Types are transformed to google field names with
        only Mobile ID specified with non matching field.
        """
        special_types_data = {
            db_c.S_TYPE_MOBILE_DEVICE_ID: ["123-456", "987-654"],
            "extra_field": ["abc", "def"],
        }

        expected_data = {"Mobile Device ID": ["123-456", "987-654"]}

        self._test_upload_fields_google(special_types_data, expected_data)

    def test_insufficient_match(self):
        """Exception is thrown if insufficient column match
        for file upload is detected.
        """
        special_types_data = {
            db_c.S_TYPE_FIRST_NAME_INITIAL_HASHED: ["initial_1", "initial_2"],
            db_c.S_TYPE_LAST_NAME_HASHED: ["last_name1", "last_name2"],
            db_c.S_TYPE_POSTAL_CODE_HASHED: ["12345", "67890"],
        }

        special_types_df = pd.DataFrame(special_types_data)

        try:
            td.transform_fields_google_file(special_types_df)
        except HuxAdvException as exc:
            self.assertEqual(
                str(exc), "Not enough columns for a match criteria."
            )
