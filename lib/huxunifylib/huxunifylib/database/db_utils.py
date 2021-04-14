"""This module utility functions for database libraries."""

import logging
from enum import Enum
from collections import defaultdict
import pandas as pd
from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.db_exceptions import DuplicateDataSourceFieldType


class DataStorage(Enum):
    """Data storage definitions."""

    S3 = object()
    MONGODB = object()


class DataLocationS3Config(Enum):
    """S3 configuration."""

    BUCKET = object()
    KEY = object()
    FILENAME = object()
    FOLDER = object()


class DataFormat(Enum):
    """Data format definitions and their file extentions."""

    CSV = "csv"
    TSV = "tsv"
    JSON = "json"


class TransformerNames(Enum):
    """Transformer names."""

    PASS_THROUGH = object()
    PASS_THROUGH_HASHED = object()

    STRIP_SPACE_LOWER_CASE = object()
    STRIP_SPACE_LOWER_CASE_HASHED = object()

    STRIP_SPACE_UPPER_CASE = object()
    STRIP_SPACE_UPPER_CASE_HASHED = object()

    FIRST_LAST_NAME = object()
    FIRST_NAME_INITIAL = object()

    CUSTOMER_ID = object()

    DOB_TO_AGE = object()
    DOB_YEAR_TO_AGE = object()

    DOB_TO_DOB_DAY = object()
    DOB_TO_DOB_MONTH = object()
    DOB_TO_DOB_YEAR = object()

    DOB_DAY = object()
    DOB_MONTH = object()
    DOB_YEAR = object()

    FACEBOOK_CITY = object()
    FACEBOOK_COUNTRY_CODE = object()
    FACEBOOK_GENDER = object()
    FACEBOOK_PHONE_NUMBER = object()
    FACEBOOK_POSTAL_CODE = object()
    FACEBOOK_STATE_OR_PROVINCE = object()

    GOOGLE_PHONE_NUMBER = object()

    GENDER = object()

    MOBILE_DEVICE_ID = object()
    POSTAL_CODE = object()
    STATE_OR_PROVINCE = object()

    TO_INTEGER = object()
    TO_FLOAT = object()
    TO_BOOLEAN = object()


def add_stats_to_update_dict(
    update_dict: dict,
    new_data: pd.DataFrame,
    old_stats_doc: dict,
    custom_breakdown_fields: list = None,
) -> dict:
    """A function to add statistics to an update dict.

    Args:
        update_dict (dict): A dict for updating a statistics/insights document.
        new_data (pd.DataFrame): New data in Pandas DataFrame format.
        old_stats_doc (dict): The exisiting statistics/insights document.
        custom_breakdown_fields (list): A list of custom field names for which
            breakdowns should be calculated.

    Returns:
        dict: Updated dict.

    """

    new_count = new_data.shape[0]
    col_list = new_data.columns

    # Remove no-insights fields from col_list
    no_insight_fields = [
        c.S_TYPE_FACEBOOK_CITY,
        c.S_TYPE_FACEBOOK_COUNTRY_CODE,
        c.S_TYPE_FACEBOOK_GENDER,
        c.S_TYPE_FACEBOOK_PHONE_NUMBER,
        c.S_TYPE_FACEBOOK_POSTAL_CODE,
        c.S_TYPE_FACEBOOK_STATE_OR_PROVINCE,
        c.S_TYPE_GOOGLE_PHONE_NUMBER,
    ]

    col_list = list(set(col_list) - set(no_insight_fields))

    # Get breakdown fields
    breakdown_fields = [
        c.S_TYPE_AGE,
        c.S_TYPE_CITY,
        c.S_TYPE_STATE_OR_PROVINCE,
        c.S_TYPE_COUNTRY_CODE,
        c.S_TYPE_GENDER,
    ]

    if custom_breakdown_fields is not None:
        breakdown_fields += custom_breakdown_fields

    # Getting invert of the count as it is needed for coverage calculation
    new_count_inv = 0.0
    if new_count > 0:
        new_count_inv = 1.0 / new_count

    # Casting age from integers to string as MongoDB only accepts strings
    if c.S_TYPE_AGE in col_list:
        new_data[c.S_TYPE_AGE] = (
            new_data[c.S_TYPE_AGE][new_data[c.S_TYPE_AGE].notnull()]
            .astype(int)
            .astype(str)
        )

    # Check the sanity of the existing doc if applicable
    # If there is no existing doc intialize a dict properly
    if old_stats_doc is not None:
        if c.DATA_COUNT not in old_stats_doc:
            logging.warning(
                "The field <%s> was not found in the existing "
                "document! "
                "Ignoring the existing document!",
                c.DATA_COUNT,
            )
            old_stats_doc = {c.DATA_COUNT: 0}
    else:
        old_stats_doc = {c.DATA_COUNT: 0}

    # Get the count of the existing doc
    old_count = int(old_stats_doc[c.DATA_COUNT])

    # Get the total count and its inverse
    tot_count = old_count + new_count

    tot_count_inv = tot_count
    if tot_count_inv > 0:
        tot_count_inv = 1.0 / tot_count_inv

    # Set count
    update_dict[c.DATA_COUNT] = tot_count

    # Loop through all the fields in the ingested data
    for item in col_list:

        col_count = new_data[item].count()

        col_count_inv = 0.0
        if col_count > 0:
            col_count_inv = 1.0 / col_count

        if item not in breakdown_fields:

            # Calculate the coverage ratio from new data
            new_cov_ratio = col_count * new_count_inv

            # Get the coverage ratio from the existig doc
            if (
                item in old_stats_doc
                and c.STATS_COVERAGE in old_stats_doc[item]
            ):
                old_cov_ratio = old_stats_doc[item][c.STATS_COVERAGE]
            else:
                old_cov_ratio = 0.0

            # Compute the overall coverage ratio of the new and old data
            cov_ratio = tot_count_inv * (
                old_count * old_cov_ratio + new_count * new_cov_ratio
            )

            update_dict[item] = {
                c.STATS_COVERAGE: cov_ratio,
            }

        else:
            # Calculate the coverage and breakdown from new data
            new_cov_ratio = col_count * new_count_inv
            new_break_dict = dict(
                new_data[item].value_counts() * col_count_inv
            )
            new_break_dict = defaultdict(float, new_break_dict)

            # Calculate the coverage from the existing doc
            if (
                item in old_stats_doc
                and c.STATS_COVERAGE in old_stats_doc[item]
            ):
                old_cov_ratio = old_stats_doc[item][c.STATS_COVERAGE]
            else:
                old_cov_ratio = 0.0

            # Calculate the breakdown from the existing doc
            if (
                item in old_stats_doc
                and c.STATS_BREAKDOWN in old_stats_doc[item]
            ):
                old_break_dict = old_stats_doc[item][c.STATS_BREAKDOWN]
            else:
                old_break_dict = defaultdict(float)

            old_break_dict = defaultdict(float, old_break_dict)

            # Calculate the coverage from new and old data. It can be
            # shown that the overal coverage is the weighted average
            # of the new and old data
            cov_ratio = tot_count_inv * (
                old_count * old_cov_ratio + new_count * new_cov_ratio
            )

            tmp_inv = old_count * old_cov_ratio + new_count * new_cov_ratio
            if tmp_inv > 0:
                tmp_inv = 1.0 / tmp_inv

            # Calculate the overal breakdown from old and new data
            # breakdowns. We loop through teh union of keys of old and
            # new breakdown dicts and calculate the overal breakdown.
            break_dict = {}
            all_vals = set(new_break_dict.keys()).union(
                set(old_break_dict.keys())
            )
            for val in all_vals:
                break_dict[val] = tmp_inv * (
                    old_count * old_cov_ratio * old_break_dict[val]
                    + new_count * new_cov_ratio * new_break_dict[val]
                )

            update_dict[item] = {
                c.STATS_COVERAGE: cov_ratio,
                c.STATS_BREAKDOWN: break_dict,
            }

    return update_dict


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def name_exists(
    database: DatabaseClient,
    database_name: str,
    collection_name: str,
    name_field: str,
    name: str,
) -> bool:
    """A function to ensure uniqueness of an entity name.

    Args:
        database (DatabaseClient): A database client.
        database_name (str): Name of database.
        collection_name (str): Name of collection.
        name_field (str): Field used to store name of the entity.
        name (str): Name of the entity.

    Returns:
        bool: A flag indicating existence of an entity name in database.

    """

    exists_flag = False
    doc = None
    dm_db = database[database_name]
    collection = dm_db[collection_name]

    try:
        doc = collection.find_one({name_field: name})
        if doc is not None:
            exists_flag = True
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return exists_flag


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def audience_name_exists(
    database: DatabaseClient,
    ingestion_job_id: ObjectId,
    name: str,
) -> bool:
    """A function to ensure uniqueness of audience names for an ingestion job.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): Mongo ID of the corresponding ingestion job.
        name (str): Name of the entity.

    Returns:
        bool: A flag indicating existence of an audience name for an ingestion job.

    """

    exists_flag = False
    doc = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    try:
        doc = collection.find_one(
            {"$and": [{c.JOB_ID: ingestion_job_id}, {c.AUDIENCE_NAME: name}]}
        )
        if doc is not None:
            exists_flag = True
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return exists_flag


def detect_non_breakdown_fields(
    new_data: pd.DataFrame,
    fields: list,
) -> list:
    """A function to detect non breakdown fields based on a batch of
       data. These are fields with values that contain "$" or ".". As MongoDB
       does not allow keys that contain these two characters, we cannot store
       breakdowns for them.

    Args:
        new_data (pd.DataFrame): New data in Pandas DataFrame format.
        fields (list): List of fields to check.

    Returns:
        list: List of detected no breakdown fields.

    """

    new_non_breakdown_fields = []

    fields = list(set(fields).intersection(set(new_data.columns)))

    for field in fields:
        if new_data[field].dropna().str.contains("\\$|\\.").any():
            new_non_breakdown_fields.append(field)

    return new_non_breakdown_fields


def validate_data_source_fields(fields: list) -> None:
    """A function to validate data source fields.

    Args:
        fields (list): Data source fields.

    """
    types_dict = {"special_type_dict": dict(), "field_mapping_dict": dict()}

    for field_item in fields:
        if (
            c.FIELD_SPECIAL_TYPE in field_item
            or c.FIELD_CUSTOM_TYPE in field_item
        ):
            if (
                field_item[c.FIELD_SPECIAL_TYPE]
                not in types_dict["special_type_dict"].keys()
                and field_item[c.FIELD_SPECIAL_TYPE]
            ):
                types_dict["special_type_dict"][
                    field_item[c.FIELD_SPECIAL_TYPE]
                ] = True

            elif (
                field_item[c.FIELD_SPECIAL_TYPE]
                not in types_dict["special_type_dict"].keys()
                and not field_item[c.FIELD_SPECIAL_TYPE]
            ):
                if field_item[c.FIELD_CUSTOM_TYPE]:
                    if (
                        field_item[c.FIELD_FIELD_MAPPING]
                        or field_item[c.FIELD_FIELD_MAPPING_DEFAULT]
                    ) not in types_dict["field_mapping_dict"].keys() and (
                        field_item[c.FIELD_FIELD_MAPPING]
                        or field_item[c.FIELD_FIELD_MAPPING_DEFAULT]
                    ):
                        types_dict["field_mapping_dict"][
                            field_item[c.FIELD_FIELD_MAPPING]
                            or field_item[c.FIELD_FIELD_MAPPING_DEFAULT]
                        ] = True
                    elif (
                        field_item[c.FIELD_FIELD_MAPPING]
                        or field_item[c.FIELD_FIELD_MAPPING_DEFAULT]
                    ) not in types_dict["field_mapping_dict"].keys() and not (
                        field_item[c.FIELD_FIELD_MAPPING]
                        or field_item[c.FIELD_FIELD_MAPPING_DEFAULT]
                    ):
                        pass
                    else:
                        raise DuplicateDataSourceFieldType(
                            c.FIELD_FIELD_MAPPING
                        )
            else:
                raise DuplicateDataSourceFieldType(c.FIELD_SPECIAL_TYPE)


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_docs_bulk(
    database: DatabaseClient,
    mongo_ids: list,
    collection_name: str,
    field_name: str,
    ids_only: bool = False,
) -> list:
    """A function to get a list of documents.

    Args:
        database (DatabaseClient): A database client.
        mongo_ids (list): A list of MongoDB IDs.
        collection_name (str): Name of collection.
        field_name (str): Name of corresponding field.
        ids_only (bool): If True, only include IDs in the documents.

    Returns:
        list: A list of documents.

    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[collection_name]
    ret_list = None

    proj_dict = {c.ENABLED: 0}

    if ids_only:
        proj_dict[c.ID] = 1

    try:
        cursor = collection.find(
            {field_name: {"$in": mongo_ids}, c.ENABLED: True},
            projection=proj_dict,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    if cursor is not None:
        ret_list = list(cursor)

    return ret_list
