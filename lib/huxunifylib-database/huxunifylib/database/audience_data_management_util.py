"""Audience and Data management utils."""

import logging
from collections import defaultdict
from typing import Union

from bson import ObjectId
import pymongo
import pandas as pd
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as c
from huxunifylib.database.db_exceptions import DuplicateDataSourceFieldType
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def audience_name_exists(
    database: DatabaseClient,
    name: str,
) -> bool:
    """A function to ensure uniqueness of audience names for an ingestion job.

    Args:
        database (DatabaseClient): A database client.
        name (str): Name of the entity.

    Returns:
        bool: A flag indicating existence of an audience name for an ingestion
            job.
    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    try:
        doc = collection.find_one({c.AUDIENCE_NAME: name})
        if doc:
            return True
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


# pylint: disable=R0914,R0912,R0915
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
        c.S_TYPE_CITY_HASHED,
        c.S_TYPE_COUNTRY_CODE_HASHED,
        c.S_TYPE_GENDER_HASHED,
        c.S_TYPE_PHONE_NUMBER_HASHED,
        c.S_TYPE_POSTAL_CODE_HASHED,
        c.S_TYPE_STATE_OR_PROVINCE_HASHED,
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


def validate_data_source_fields(fields: list) -> None:
    """A function to validate data source fields.

    Args:
        fields (list): Data source fields.

    Raises:
        DuplicateDataSourceFieldType: If there are duplicate data source fields
            in the input collection
    """

    types_dict: dict = {
        "special_type_dict": {},
        "field_mapping_dict": {},
    }

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


def clean_dataframe_types(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Resolve Mongo unfriendly types.

    Args:
        dataframe (pd.DataFrame): input dataframe.

    Returns:
        pd.DataFrame: output dataframe
    """

    dataframe[dataframe.select_dtypes(include=["int64"]).columns] = dataframe[
        dataframe.select_dtypes(include=["int64"]).columns
    ].astype("int32")
    dataframe[
        dataframe.select_dtypes(include=["float64"]).columns
    ] = dataframe[dataframe.select_dtypes(include=["float64"]).columns].astype(
        "float32"
    )

    return dataframe


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_audience_doc(
    database: DatabaseClient,
    audience_id: ObjectId,
    update_dict: dict,
) -> Union[dict, None]:
    """Update MongoDb document.

    Args:
        database (DatabaseClient): database client.
        audience_id (ObjectId): MongoDB audience ID.
        update_dict (dict): updating dictionary.

    Returns:
        dict: updated document.
    """

    collection = database[c.DATA_MANAGEMENT_DATABASE][c.AUDIENCES_COLLECTION]

    try:
        return collection.find_one_and_update(
            {c.ID: audience_id, c.DELETED: False},
            {"$set": update_dict},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
