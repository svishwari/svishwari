"""Purpose of this file is to get data from TrustID"""
import statistics
from typing import Union

from huxunifylib.database import constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.collection_management import get_document
from huxunifylib.database.survey_metrics_management import (
    get_trust_id_overview,
    get_trust_id_attributes,
)
from huxunify.api import constants as api_c


def get_trust_id_overview_data(
    database: DatabaseClient, filters: list = None
) -> dict:
    """Fetch trust id overview data

    Args:
        database(DatabaseClient): database client
        filters(list): List of filters, default None

    Returns:
        (dict): Trust ID overview data
    """
    overview = get_trust_id_overview(database, filters) or {}

    trust_id_overview = {
        api_c.TRUST_ID_FACTORS: [
            {
                api_c.TRUST_ID_FACTOR_NAME: factor_name,
                api_c.TRUST_ID_FACTOR_SCORE: (
                    (
                        overview[factor_name][api_c.RATING][api_c.AGREE][
                            api_c.PERCENTAGE
                        ]
                        - overview[factor_name][api_c.RATING][api_c.DISAGREE][
                            api_c.PERCENTAGE
                        ]
                    )
                    * 100
                )
                if overview.get(factor_name)
                else None,
                api_c.TRUST_ID_FACTOR_DESCRIPTION: api_c.TRUST_ID_FACTOR_DESCRIPTION_MAP[
                    factor_name
                ],
                api_c.OVERALL_CUSTOMER_RATING: {
                    api_c.RATING: overview[factor_name][api_c.RATING],
                    api_c.TOTAL_CUSTOMERS: overview[factor_name][
                        api_c.TOTAL_CUSTOMERS
                    ],
                }
                if overview.get(factor_name)
                else {
                    api_c.TOTAL_CUSTOMERS: 0,
                    api_c.RATING: {
                        rating: {api_c.COUNT: 0}
                        for rating in api_c.TRUST_ID_RATING_MAP.values()
                    },
                },
            }
            for factor_name in api_c.TRUST_ID_LIST_OF_FACTORS
        ]
    }

    trust_id_overview.update(
        {
            api_c.TRUST_ID_SCORE: statistics.mean(
                [
                    factor[api_c.TRUST_ID_FACTOR_SCORE]
                    for factor in trust_id_overview[api_c.TRUST_ID_FACTORS]
                ]
            )
            if overview
            else None
        }
    )

    return trust_id_overview


def get_trust_id_attributes_data(
    database: DatabaseClient, filters: list = None
) -> list:
    """Get trust id attribute details

    Args:
        database(DatabaseClient): database client
        filters(list): List o filters, default None

    Returns:
        (list): List of attributes_list and their details

    """
    attributes_list = []
    trust_id_attributes = get_document(
        database,
        db_c.CONFIGURATIONS_COLLECTION,
        {"type": db_c.TRUST_ID_ATTRIBUTES},
    )[db_c.ATTRIBUTES]

    trust_id_attribute_ratings = get_trust_id_attributes(database, filters)

    for factor_name, attributes in trust_id_attributes.items():
        for ind, attribute in enumerate(attributes):
            attributes_list.append(
                {
                    api_c.TRUST_ID_FACTOR_NAME: factor_name,
                    api_c.TRUST_ID_ATTRIBUTE_SCORE: (
                        (
                            trust_id_attribute_ratings[db_c.ATTRIBUTES][
                                factor_name
                            ][ind][api_c.AGREE][api_c.PERCENTAGE]
                            - trust_id_attribute_ratings[db_c.ATTRIBUTES][
                                factor_name
                            ][ind][api_c.DISAGREE][api_c.PERCENTAGE]
                        )
                        * 100
                    )
                    if trust_id_attribute_ratings
                    else None,
                    api_c.TRUST_ID_ATTRIBUTE_DESCRIPTION: attribute[
                        db_c.DESCRIPTION
                    ],
                    api_c.TRUST_ID_ATTRIBUTE_SHORT_DESCRIPTION: attribute[
                        db_c.SHORT_DESCRIPTION
                    ],
                    api_c.OVERALL_CUSTOMER_RATING: {
                        api_c.TOTAL_CUSTOMERS: trust_id_attribute_ratings[
                            api_c.TOTAL_CUSTOMERS
                        ],
                        api_c.RATING: trust_id_attribute_ratings[
                            db_c.ATTRIBUTES
                        ][factor_name][ind],
                    }
                    if trust_id_attribute_ratings
                    else {
                        api_c.TOTAL_CUSTOMERS: 0,
                        api_c.RATING: {
                            rating: {api_c.COUNT: 0}
                            for rating in api_c.TRUST_ID_RATING_MAP.values()
                        },
                    },
                }
            )

    return attributes_list


def get_trust_id_comparison_data_by_segment(
    database: DatabaseClient,
    segment_filters: list = None,
) -> Union[dict, None]:
    """Get trust id comparison data by segment

    Args:
        database(DatabaseClient): database client
        segment_filters(list): List of filters, default None
    Returns:
        Union[dict, None]: dict of overview comparison data
    """
    # fetch all details from db
    overview_data = get_trust_id_overview_data(database, segment_filters)

    trust_id_attributes = get_document(
        database,
        db_c.CONFIGURATIONS_COLLECTION,
        {"type": db_c.TRUST_ID_ATTRIBUTES},
    )[db_c.ATTRIBUTES]

    trust_id_attribute_ratings = get_trust_id_attributes(
        database, segment_filters
    )

    comparison_data = {
        api_c.OVERVIEW: {
            api_c.TRUST_ID_SEGMENT_FILTERS: segment_filters,
            api_c.TRUST_ID_ATTRIBUTES: [
                {
                    api_c.TRUST_ID_ATTRIBUTE_TYPE: api_c.TRUST_ID_TAG.replace(
                        "-", "_"
                    ),
                    api_c.TRUST_ID_ATTRIBUTE_NAME: api_c.HX_TRUST_ID,
                    api_c.TRUST_ID_ATTRIBUTE_SCORE: overview_data.get(
                        api_c.TRUST_ID_SCORE, None
                    ),
                    api_c.TRUST_ID_ATTRIBUTE_DESCRIPTION: api_c.TRUST_ID_FACTOR_DESCRIPTION_MAP[
                        api_c.HX_TRUST_ID
                    ],
                }
            ],
        },
    }

    for factor in overview_data[api_c.TRUST_ID_FACTORS]:
        comparison_data[api_c.OVERVIEW][api_c.TRUST_ID_ATTRIBUTES].append(
            {
                api_c.TRUST_ID_ATTRIBUTE_TYPE: factor[
                    api_c.TRUST_ID_FACTOR_NAME
                ],
                api_c.TRUST_ID_ATTRIBUTE_NAME: factor[
                    api_c.TRUST_ID_FACTOR_NAME
                ].title(),
                api_c.TRUST_ID_ATTRIBUTE_SCORE: factor[
                    api_c.TRUST_ID_FACTOR_SCORE
                ],
                api_c.TRUST_ID_ATTRIBUTE_DESCRIPTION: factor[
                    api_c.TRUST_ID_FACTOR_DESCRIPTION
                ],
            }
        )

    for factor_name, attributes in trust_id_attributes.items():
        comparison_data[factor_name] = {
            api_c.TRUST_ID_SEGMENT_FILTERS: segment_filters,
            api_c.TRUST_ID_ATTRIBUTES: [
                {
                    api_c.TRUST_ID_ATTRIBUTE_TYPE: factor_name,
                    api_c.TRUST_ID_ATTRIBUTE_NAME: factor_name.title(),
                    api_c.TRUST_ID_ATTRIBUTE_DESCRIPTION: api_c.TRUST_ID_FACTOR_DESCRIPTION_MAP[
                        factor_name
                    ],
                    api_c.TRUST_ID_ATTRIBUTE_SCORE: [
                        factor[api_c.TRUST_ID_FACTOR_SCORE]
                        for factor in overview_data[api_c.TRUST_ID_FACTORS]
                        if factor[api_c.TRUST_ID_FACTOR_NAME] == factor_name
                    ][0],
                }
            ],
        }
        for ind, attribute in enumerate(attributes):
            comparison_data[factor_name][api_c.TRUST_ID_ATTRIBUTES].append(
                {
                    api_c.TRUST_ID_ATTRIBUTE_TYPE: attribute.get(
                        db_c.SHORT_DESCRIPTION, attribute[db_c.DESCRIPTION]
                    )
                    .lower()
                    .replace(" ", "_"),
                    api_c.TRUST_ID_ATTRIBUTE_NAME: attribute.get(
                        db_c.SHORT_DESCRIPTION,
                        attribute[db_c.SHORT_DESCRIPTION],
                    ),
                    api_c.TRUST_ID_ATTRIBUTE_DESCRIPTION: attribute[
                        api_c.DESCRIPTION
                    ],
                    api_c.TRUST_ID_ATTRIBUTE_SCORE: (
                        (
                            trust_id_attribute_ratings[
                                api_c.TRUST_ID_ATTRIBUTES
                            ][factor_name][ind][api_c.AGREE][api_c.PERCENTAGE]
                            - trust_id_attribute_ratings[
                                api_c.TRUST_ID_ATTRIBUTES
                            ][factor_name][ind][api_c.DISAGREE][
                                api_c.PERCENTAGE
                            ]
                        )
                        * 100
                    )
                    if trust_id_attribute_ratings
                    else None,
                }
            )

    return comparison_data


def get_trust_id_comparison_response(segments: list) -> list:
    """Structure comparison data for response

    Args:
        segments(list): List of segments

    Returns:
         (list): Segment-wise comparison data
    """
    comparison_data = {
        segment_type: [] for segment_type in api_c.TRUST_ID_SEGMENT_TYPE_MAP
    }
    for segment in segments:
        for segment_type in api_c.TRUST_ID_SEGMENT_TYPE_MAP:
            segment[api_c.COMPARISON][segment_type].update(
                {
                    api_c.DEFAULT: segment.get(api_c.DEFAULT, False),
                    api_c.TRUST_ID_SEGMENT_NAME: segment[
                        api_c.TRUST_ID_SEGMENT_NAME
                    ],
                }
            )
            comparison_data[segment_type].append(
                segment[api_c.COMPARISON][segment_type]
            )

    trust_id_comparison_data = [
        {
            api_c.TRUST_ID_SEGMENT_TYPE: api_c.TRUST_ID_SEGMENT_TYPE_MAP[
                factor_name
            ],
            api_c.TRUST_ID_SEGMENTS: segments,
        }
        for factor_name, segments in comparison_data.items()
    ]

    return trust_id_comparison_data
