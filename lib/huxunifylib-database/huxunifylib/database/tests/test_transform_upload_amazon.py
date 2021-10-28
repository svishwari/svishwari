"""Dataframe transformation for File upload to Amazon unittests."""
import unittest
from typing import Dict

import pandas as pd
from pandas._testing import assert_frame_equal

import huxunifylib.database.constants as dc
from huxunifylib.database.transform import transform_dataframe as td
from huxunifylib.database.db_exceptions import HuxAdvException


class TestUploadFieldsAmazon(unittest.TestCase):
    """Dataframe is transformed for file upload to Amazon."""

    @staticmethod
    def _test_upload_fields_amazon(
        special_types_data: Dict[str, list],
        expected_data: Dict[str, list],
    ):
        """Transform special types, auxiliary method.

        Args:
            special_types_data (Dict[str, list]): Special types data.
            expected_data (Dict[str, list]): Expected Amazon field data.
        """
        special_types_df = pd.DataFrame(special_types_data)

        actual = td.transform_fields_amazon_file(special_types_df)

        assert_frame_equal(
            actual,
            pd.DataFrame(expected_data),
            check_like=True,
        )

    def test_full_match(self):
        """Special Types are transformed to amazon field names with
        all amazon match criteria satisfied.
        """
        special_types_data = {
            dc.S_TYPE_EMAIL_HASHED: ["email1", "email2"],
            dc.S_TYPE_FIRST_NAME_HASHED: ["first_name1", "first_name2"],
            dc.S_TYPE_LAST_NAME_HASHED: ["last_name1", "last_name2"],
            dc.S_TYPE_PHONE_NUMBER_HASHED: ["11234567890", "441234567890"],
            dc.S_TYPE_POSTAL_CODE_HASHED: ["12345", "67890"],
            dc.S_TYPE_ADDRESS: ["123n92ndstunitb", "765w34thave"],
        }

        expected_data = {
            "email": ["email1", "email2"],
            "first_name": ["first_name1", "first_name2"],
            "last_name": ["last_name1", "last_name2"],
            "phone": ["11234567890", "441234567890"],
            "zip": ["12345", "67890"],
            "address": ["123n92ndstunitb", "765w34thave"],
        }

        self._test_upload_fields_amazon(special_types_data, expected_data)

    def test_extra_field_discarded(self):
        """Special Types are transformed to amazon field names with
        non-match special type specified.
        """
        special_types_data = {
            dc.S_TYPE_COUNTRY_CODE_HASHED: ["US", "UK"],
            dc.S_TYPE_EMAIL_HASHED: ["email1", "email2"],
            dc.S_TYPE_FIRST_NAME_HASHED: ["first_name1", "first_name2"],
            dc.S_TYPE_LAST_NAME_HASHED: ["last_name1", "last_name2"],
            dc.S_TYPE_PHONE_NUMBER_HASHED: ["11234567890", "441234567890"],
            dc.S_TYPE_POSTAL_CODE_HASHED: ["12345", "67890"],
            dc.S_TYPE_ADDRESS: ["123n92ndstunitb", "765w34thave"],
        }

        expected_data = {
            "email": ["email1", "email2"],
            "first_name": ["first_name1", "first_name2"],
            "last_name": ["last_name1", "last_name2"],
            "phone": ["11234567890", "441234567890"],
            "zip": ["12345", "67890"],
            "address": ["123n92ndstunitb", "765w34thave"],
        }

        self._test_upload_fields_amazon(special_types_data, expected_data)

    def test_insufficient_match(self):
        """Exception is thrown if insufficient column match
        for file upload is detected.
        """
        special_types_data = {
            dc.S_TYPE_FIRST_NAME_HASHED: ["first_name1", "first_name2"],
            dc.S_TYPE_LAST_NAME_HASHED: ["last_name1", "last_name2"],
            dc.S_TYPE_PHONE_NUMBER_HASHED: ["11234567890", "441234567890"],
            dc.S_TYPE_POSTAL_CODE_HASHED: ["12345", "67890"],
            dc.S_TYPE_ADDRESS: ["123n92ndstunitb", "765w34thave"],
        }

        special_types_df = pd.DataFrame(special_types_data)

        try:
            td.transform_fields_amazon_file(special_types_df)
        except HuxAdvException as exc:
            self.assertEqual(
                str(exc), "Not enough columns for a match criteria."
            )
