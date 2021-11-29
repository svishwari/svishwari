"""DB Utils tests."""
from unittest import TestCase

import huxunifylib.database.constants as db_c
from huxunifylib.database.db_exceptions import DuplicateDataSourceFieldType
from huxunifylib.database.audience_data_management_util import (
    validate_data_source_fields,
)


class TestDBUtils(TestCase):
    """Tests for db_utils module."""

    def test_validate_data_source_fields__duplicate_special_type(self):
        """Validation with duplicate special type."""
        fields = [
            {
                "header": "ph",
                "special_type": db_c.S_TYPE_PHONE_NUMBER,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "phone_number",
                "special_type": db_c.S_TYPE_PHONE_NUMBER,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": db_c.FIELD_MAP_ORDER_QUANTITY_12M,
                "field_mapping_default": None,
            },
            {
                "header": "past_order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": db_c.FIELD_MAP_ORDER_QUANTITY_13M_24M,
                "field_mapping_default": None,
            },
        ]
        with self.assertRaises(DuplicateDataSourceFieldType):
            validate_data_source_fields(fields)

    def test_validate_data_source_fields__different_special_type(self):
        """Validation with different special type."""
        fields = [
            {
                "header": "first_name",
                "special_type": db_c.S_TYPE_FIRST_NAME,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "phone_number",
                "special_type": db_c.S_TYPE_PHONE_NUMBER,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": db_c.FIELD_MAP_ORDER_QUANTITY_12M,
                "field_mapping_default": None,
            },
            {
                "header": "past_order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": db_c.FIELD_MAP_ORDER_QUANTITY_13M_24M,
                "field_mapping_default": None,
            },
            {
                "header": "Number .Of Children",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": None,
                "field_mapping_default": "number_of_children",
            },
        ]

        self.assertIsNone(validate_data_source_fields(fields))

    def test_validate_data_source_fields__duplicate_custom_type_field_mapping_default(
        self,
    ):
        """Validation with duplicate custom type and default field mapping."""
        fields = [
            {
                "header": "ph",
                "special_type": db_c.S_TYPE_PHONE_NUMBER,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "fn",
                "special_type": db_c.S_TYPE_FIRST_NAME,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": None,
                "field_mapping_default": "order",
            },
            {
                "header": "past_order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": None,
                "field_mapping_default": "past_order",
            },
        ]

        self.assertIsNone(validate_data_source_fields(fields))

    def test_validate_data_source_fields__different_custom_type_field_mapping_default(
        self,
    ):
        """Validation with different custom type and default field mapping."""
        fields = [
            {
                "header": "ph",
                "special_type": db_c.S_TYPE_PHONE_NUMBER,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "fn",
                "special_type": db_c.S_TYPE_FIRST_NAME,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": None,
                "field_mapping_default": "order",
            },
            {
                "header": "past_order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_FLOAT,
                "field_mapping": None,
                "field_mapping_default": "past_order",
            },
        ]

        self.assertIsNone(validate_data_source_fields(fields))

    def test_validate_data_source_fields__duplicate_custom_type_duplicate_field_mapping(
        self,
    ):
        """Validation with duplicate custom type and duplicate field mapping."""
        fields = [
            {
                "header": "ph",
                "special_type": db_c.S_TYPE_PHONE_NUMBER,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "fn",
                "special_type": db_c.S_TYPE_FIRST_NAME,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": db_c.FIELD_MAP_ORDER_QUANTITY_12M,
                "field_mapping_default": None,
            },
            {
                "header": "past_order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": db_c.FIELD_MAP_ORDER_QUANTITY_12M,
                "field_mapping_default": None,
            },
        ]

        with self.assertRaises(DuplicateDataSourceFieldType):
            validate_data_source_fields(fields)

    def test_validate_data_source_fields__duplicate_custom_type_different_field_mapping(
        self,
    ):
        """Validation with duplicate custom type and different field mapping."""
        fields = [
            {
                "header": "ph",
                "special_type": db_c.S_TYPE_PHONE_NUMBER,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "fn",
                "special_type": db_c.S_TYPE_FIRST_NAME,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": db_c.FIELD_MAP_ORDER_QUANTITY_12M,
                "field_mapping_default": None,
            },
            {
                "header": "past_order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": db_c.FIELD_MAP_ORDER_QUANTITY_13M_24M,
                "field_mapping_default": None,
            },
        ]

        self.assertIsNone(validate_data_source_fields(fields))

    def test_validate_data_source_fields__different_custom_type_different_field_mapping(
        self,
    ):
        """Validation with different custom type and different field mapping."""
        fields = [
            {
                "header": "ph",
                "special_type": db_c.S_TYPE_PHONE_NUMBER,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "fn",
                "special_type": db_c.S_TYPE_FIRST_NAME,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_INT,
                "field_mapping": db_c.FIELD_MAP_ORDER_QUANTITY_12M,
                "field_mapping_default": None,
            },
            {
                "header": "past_order",
                "special_type": None,
                "custom_type": db_c.CUSTOM_TYPE_FLOAT,
                "field_mapping": None,
                "field_mapping_default": "past_order",
            },
        ]

        self.assertIsNone(validate_data_source_fields(fields))

    def test_validate_data_source_fields__no_type_assigned(
        self,
    ):
        """Validation when no field type is assigned."""
        fields = [
            {
                "header": "ph",
                "special_type": None,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "fn",
                "special_type": None,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "order",
                "special_type": None,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
            {
                "header": "past_order",
                "special_type": None,
                "custom_type": None,
                "field_mapping": None,
                "field_mapping_default": None,
            },
        ]

        self.assertIsNone(validate_data_source_fields(fields))
