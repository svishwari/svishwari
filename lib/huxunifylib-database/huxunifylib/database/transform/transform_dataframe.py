"""Methods transforming dataframe."""
import copy
from typing import Iterable, Tuple

import pandas as pd
import huxunifylib.database.constants as dc
from huxunifylib.database.transform.const import (
    FileMatchType,
    FILE_UPLOAD_GOOGLE_FIELD_MAP,
    FILE_UPLOAD_AMAZON_FIELD_MAP,
)
from huxunifylib.database.db_exceptions import HuxAdvException


def _get_full_match_columns_by_type(
    dataframe: pd.DataFrame,
    field_map_by_match_type: dict,
    delivery_platform_match_types: Iterable,
) -> Tuple[dict, dict, set]:
    """Determines what specified match types dataframe header fully matches.
    Generates special type -> delivery platform field mapping.
    Derives dataframe column names that are relevant for delivry platform
    file upload.

    Args:
        dataframe (pd.DataFrame): dataframe with Special Type header.
        field_map_by_match_type (dict):
            special type -> delivery platform field map by match type.
        delivery_platform_match_types (Iterable):
            delivery platform match types.

    Returns:
        Tuple[dict, dict, set]:
            (
                <special type -> delivery platform field map by match type
                    for each match type dataframe columns match fully>,
                <special type -> delivery platform field mapping>,
                relevant to delivery platform datadrame columns,
            )
    """

    match_types = (
        match_type.name for match_type in delivery_platform_match_types
    )
    mapping_s_type_to_delivery_platform = {
        s_type: platform_type
        for match_type, col_map in field_map_by_match_type.items()
        if match_type in match_types
        for s_type, platform_type in col_map.items()
    }

    # Take only columns that are qualified for delivery platform
    col_list = set(dataframe.columns).intersection(
        set(mapping_s_type_to_delivery_platform.keys())
    )

    # Determine match types which column set is
    # entirely in dataframe column set
    full_match_columns_by_type = {}
    for match_type in delivery_platform_match_types:
        # Dataset columns that are part of match
        match_columns = set(
            field_map_by_match_type[match_type.name].keys()
        ).intersection(col_list)

        # Only register columns match
        # if columns match the match type fully
        if match_columns == set(
            field_map_by_match_type[match_type.name].keys()
        ):
            full_match_columns_by_type[match_type.name] = match_columns

    return (
        full_match_columns_by_type,
        mapping_s_type_to_delivery_platform,
        col_list,
    )


def transform_fields_google_file(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Transforms Special Types dataframe to Google fields for hashed file
    upload. The method examines dataframe for match criteria and if detected,
    retains all the columns that are allowed to be present for that match.
    The column names are transformed to Google field names.

    Args:
        dataframe (pd.DataFrame): Dataframe with special types header.

    Returns:
        pd.DataFrame: Dataframe with Google header for file upload.

    Raises:
        HuxAdvException: If not enough columns for a match criteria.
    """
    delivery_platform_match_types = (
        FileMatchType.EMAIL,
        FileMatchType.PHONE,
        FileMatchType.MAILING_ADDRESS,
        FileMatchType.MOBILE_DEVICE_ID,
    )
    field_map_by_match_type = copy.deepcopy(FILE_UPLOAD_GOOGLE_FIELD_MAP)
    col_list = set(dataframe.columns)

    # Take First Name Initial only if First Name is not present
    # Leave either First Name or First Name Initial in the mapping.
    if dc.S_TYPE_FIRST_NAME_HASHED in col_list:
        col_list = set(dataframe.columns) - {
            dc.S_TYPE_FIRST_NAME_INITIAL_HASHED
        }
        del field_map_by_match_type[FileMatchType.MAILING_ADDRESS.name][
            dc.S_TYPE_FIRST_NAME_INITIAL_HASHED
        ]
    elif dc.S_TYPE_FIRST_NAME_INITIAL_HASHED in col_list:
        del field_map_by_match_type[FileMatchType.MAILING_ADDRESS.name][
            dc.S_TYPE_FIRST_NAME_HASHED
        ]

    (
        full_match_columns_by_type,
        mapping_s_type_to_delivery_platform,
        col_list,
    ) = _get_full_match_columns_by_type(
        dataframe, field_map_by_match_type, delivery_platform_match_types
    )

    if (
        full_match_columns_by_type.get(FileMatchType.EMAIL.name)
        or full_match_columns_by_type.get(FileMatchType.PHONE.name)
        or full_match_columns_by_type.get(FileMatchType.MAILING_ADDRESS.name)
    ):
        col_list = col_list - {dc.S_TYPE_MOBILE_DEVICE_ID}
    elif full_match_columns_by_type.get(FileMatchType.MOBILE_DEVICE_ID.name):
        col_list = {dc.S_TYPE_MOBILE_DEVICE_ID}
    else:
        raise HuxAdvException("Not enough columns for a match criteria.")

    return dataframe[col_list].rename(
        columns=mapping_s_type_to_delivery_platform
    )


def transform_fields_amazon_file(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Transforms Special Types dataframe to Amazon fields for hashed file
    upload. The method examines dataframe for match criteria and if detected,
    retains all the columns that are allowed to be present for that match.
    The column names are transformed to Amazon field names.

    Args:
        dataframe (pd.DataFrame): Dataframe with special types header.

    Returns:
        pd.DataFrame: Dataframe with Amazon header for file upload.
    """
    delivery_platform_match_types = (FileMatchType.EMAIL_ADDRESS_PHONE,)
    col_list = set(dataframe.columns)

    (
        _,
        mapping_s_type_to_delivery_platform,
        col_list,
    ) = _get_full_match_columns_by_type(
        dataframe, FILE_UPLOAD_AMAZON_FIELD_MAP, delivery_platform_match_types
    )

    return dataframe[col_list].rename(
        columns=mapping_s_type_to_delivery_platform
    )
