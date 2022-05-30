"""Purpose of this file is to get data from TrustID"""
import statistics
from collections import defaultdict

from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c


def aggregate_attributes(survey_responses: list) -> dict:
    """Aggregate attribute data

    Args:
        survey_responses (list): List of survey responses

    Returns:
        (dict): Aggregated attribute data object
    """
    attribute_aggregated_values = defaultdict(dict)

    # Calculate cumulative attribute score and rating
    for survey_response in survey_responses:
        for factor_name, factor_values in survey_response[
            db_c.FACTORS
        ].items():
            for attribute in factor_values[db_c.ATTRIBUTES]:
                if attribute.get(api_c.RATING):
                    if (
                        attribute[db_c.DESCRIPTION]
                        not in attribute_aggregated_values[
                            factor_name.lower()
                        ].keys()
                    ):
                        attribute_aggregated_values[factor_name.lower()][
                            attribute[db_c.DESCRIPTION]
                        ] = {}

                    attribute_aggregated_values[factor_name.lower()][
                        attribute[db_c.DESCRIPTION]
                    ][api_c.RATING_MAP[attribute.get(api_c.RATING)]] = (
                        int(
                            attribute_aggregated_values[factor_name.lower()][
                                attribute[db_c.DESCRIPTION]
                            ].get(
                                api_c.RATING_MAP[attribute[api_c.RATING]],
                                0,
                            )
                        )
                        + 1
                    )

            # set factor ratings
            attribute_aggregated_values[factor_name.lower()][
                api_c.RATING_MAP[factor_values[api_c.RATING]]
            ] = (
                attribute_aggregated_values[factor_name.lower()].get(
                    api_c.RATING_MAP[factor_values[api_c.RATING]], 0
                )
                + 1
            )
    for factor_name, factor_values in attribute_aggregated_values.items():
        for attribute_values in factor_values.values():
            if isinstance(attribute_values, dict):
                attribute_values.update(
                    {
                        api_c.SCORE: int(
                            (
                                attribute_values.get(api_c.AGREE, 0)
                                - attribute_values.get(api_c.DISAGREE, 0)
                            )
                            / len(survey_responses)
                            * 100
                        )
                    }
                )

    return attribute_aggregated_values


def get_trust_id_overview(survey_responses: list) -> dict:
    """Fetch trust id overview data

    Args:
        survey_responses (list): List of survey responses

    Returns:
        (dict): Trust ID overview data
    """
    aggregated_attributes = aggregate_attributes(survey_responses)

    overview_data = {
        db_c.FACTORS: [
            {
                api_c.FACTOR_NAME: factor_name,
                api_c.FACTOR_SCORE: int(
                    (
                        (
                            factor_values.get(api_c.AGREE, 0)
                            - factor_values.get(api_c.DISAGREE, 0)
                        )
                        / len(survey_responses)
                    )
                    * 100
                ),
                api_c.FACTOR_DESCRIPTION: api_c.FACTOR_DESCRIPTION_MAP[
                    factor_name
                ],
                api_c.OVERALL_CUSTOMER_RATING: {
                    api_c.TOTAL_CUSTOMERS: len(survey_responses),
                    api_c.RATING: {
                        customer_rating: {
                            api_c.COUNT: factor_values.get(customer_rating, 0),
                            api_c.PERCENTAGE: round(
                                factor_values.get(customer_rating, 0)
                                / len(survey_responses),
                                4,
                            ),
                        }
                        for customer_rating in api_c.RATING_MAP.values()
                    },
                },
            }
            for factor_name, factor_values in aggregated_attributes.items()
        ]
    }

    overview_data[api_c.TRUST_ID_SCORE] = (
        int(
            statistics.mean(
                [x[api_c.FACTOR_SCORE] for x in overview_data[db_c.FACTORS]]
            )
        )
        if overview_data.get(db_c.FACTORS)
        else 0
    )

    return overview_data


def get_trust_id_attributes(survey_responses: list) -> list:
    """Get trust id values details

    Args:
        survey_responses (list): List or survey responses

    Returns:
          (list): List of values and their details

    """
    trust_id_attributes = []

    attribute_aggregated_values = aggregate_attributes(survey_responses)

    for factor_name, values in survey_responses[0][db_c.FACTORS].items():
        for attribute in values[db_c.ATTRIBUTES]:
            if attribute.get(api_c.RATING):
                trust_id_attributes.append(
                    {
                        api_c.FACTOR_NAME: factor_name.lower(),
                        api_c.ATTRIBUTE_DESCRIPTION: attribute[
                            db_c.DESCRIPTION
                        ],
                    }
                )

    for attribute in list(trust_id_attributes):
        attribute.update(
            {
                api_c.ATTRIBUTE_SCORE: attribute_aggregated_values[
                    attribute[api_c.FACTOR_NAME]
                ][attribute[api_c.ATTRIBUTE_DESCRIPTION]][api_c.SCORE],
                api_c.OVERALL_CUSTOMER_RATING: {
                    api_c.TOTAL_CUSTOMERS: len(survey_responses),
                    api_c.RATING: {
                        customer_rating: {
                            api_c.COUNT: attribute_aggregated_values[
                                attribute[api_c.FACTOR_NAME]
                            ][attribute[api_c.ATTRIBUTE_DESCRIPTION]].get(
                                customer_rating, 0
                            ),
                            api_c.PERCENTAGE: round(
                                attribute_aggregated_values[
                                    attribute[api_c.FACTOR_NAME]
                                ][attribute[api_c.ATTRIBUTE_DESCRIPTION]].get(
                                    customer_rating, 0
                                )
                                / len(survey_responses),
                                4,
                            ),
                        }
                        for customer_rating in api_c.RATING_MAP.values()
                    },
                },
            }
        )

    return trust_id_attributes


def get_trust_id_comparison_data(data_by_segment: list) -> list:
    """Get comparison data for trust id

    Args:
        data_by_segment (list): List of segment data

    Returns:
         (list): Segment-wise comparison data
    """
    segment_data_by_factors = defaultdict(dict)
    overview_data = {}

    for segment_data in data_by_segment:
        attributes_data = get_trust_id_attributes(
            segment_data[api_c.SURVEY_RESPONSES]
        )
        overview_data[
            segment_data[api_c.SEGMENT_NAME]
        ] = get_trust_id_overview(segment_data[api_c.SURVEY_RESPONSES])

        for factor_name in api_c.LIST_OF_FACTORS:
            if (
                segment_data[api_c.SEGMENT_NAME]
                not in segment_data_by_factors[factor_name].keys()
            ):
                segment_data_by_factors[factor_name].update(
                    {segment_data[api_c.SEGMENT_NAME]: []}
                )
            segment_data_by_factors[factor_name][
                segment_data[api_c.SEGMENT_NAME]
            ].extend(
                [
                    x
                    for x in attributes_data
                    if x[api_c.FACTOR_NAME] == factor_name
                ]
            )

    composite_factor_scores = {
        api_c.SEGMENT_TYPE: api_c.SEGMENT_TYPES[0],
        api_c.SEGMENTS: [],
    }

    for segment_data in data_by_segment:
        composite_factor_scores[api_c.SEGMENTS].append(
            {
                api_c.SEGMENT_NAME: segment_data[api_c.SEGMENT_NAME],
                api_c.DEFAULT: bool(
                    segment_data.get(api_c.SEGMENT_NAME)
                    == api_c.DEFAULT_TRUST_SEGMENT
                ),
                api_c.SEGMENT_FILTERS: segment_data[api_c.SEGMENT_FILTERS],
                api_c.ATTRIBUTES: [
                    {
                        api_c.ATTRIBUTE_TYPE: x[api_c.FACTOR_NAME],
                        api_c.ATTRIBUTE_NAME: x[api_c.FACTOR_NAME].title(),
                        api_c.ATTRIBUTE_DESCRIPTION: x[
                            api_c.FACTOR_DESCRIPTION
                        ],
                        api_c.ATTRIBUTE_SCORE: x[api_c.FACTOR_SCORE],
                    }
                    for x in overview_data[segment_data[api_c.SEGMENT_NAME]][
                        api_c.FACTORS
                    ]
                ],
            }
        )
        composite_factor_scores[api_c.SEGMENTS][-1][api_c.ATTRIBUTES].insert(
            0,
            {
                api_c.ATTRIBUTE_TYPE: "trust_id",
                api_c.ATTRIBUTE_NAME: "HX TrustID",
                api_c.ATTRIBUTE_DESCRIPTION: "TrustID is scored on a scale between -100 to 100",
                api_c.ATTRIBUTE_SCORE: overview_data[
                    segment_data[api_c.SEGMENT_NAME]
                ][api_c.TRUST_ID_SCORE],
            },
        )

    trust_id_comparison_data = []
    for factor_name, data_by_factor in segment_data_by_factors.items():
        factor_comparison_data = {
            api_c.SEGMENT_TYPE: api_c.SEGMENT_TYPE_MAP[factor_name],
            api_c.SEGMENTS: [],
        }
        for segment_name, data in data_by_factor.items():
            factor_comparison_data[api_c.SEGMENTS].append(
                {
                    api_c.SEGMENT_NAME: segment_name,
                    api_c.DEFAULT: bool(
                        segment_name == api_c.DEFAULT_TRUST_SEGMENT
                    ),
                    api_c.SEGMENT_FILTERS: [
                        segment[api_c.SEGMENT_FILTERS]
                        for segment in data_by_segment
                        if segment[api_c.SEGMENT_NAME] == segment_name
                    ][0],
                    api_c.ATTRIBUTES: [
                        {
                            api_c.ATTRIBUTE_DESCRIPTION: x[
                                api_c.ATTRIBUTE_DESCRIPTION
                            ],
                            api_c.ATTRIBUTE_SCORE: x[api_c.ATTRIBUTE_SCORE],
                            api_c.ATTRIBUTE_TYPE: api_c.ATTRIBUTE_DESCRIPTION_TYPE_MAP[
                                x[api_c.ATTRIBUTE_DESCRIPTION].lower()
                            ][
                                api_c.TYPE
                            ],
                            api_c.ATTRIBUTE_NAME: api_c.ATTRIBUTE_DESCRIPTION_TYPE_MAP[
                                x[api_c.ATTRIBUTE_DESCRIPTION].lower()
                            ][
                                api_c.NAME
                            ],
                        }
                        for x in data
                    ],
                }
            )
            for factor_data in composite_factor_scores[api_c.SEGMENTS]:
                if factor_data[api_c.SEGMENT_NAME] != segment_name:
                    continue
                factor_comparison_data[api_c.SEGMENTS][-1][
                    api_c.ATTRIBUTES
                ].insert(
                    0,
                    [
                        x
                        for x in factor_data[api_c.ATTRIBUTES]
                        if x[api_c.ATTRIBUTE_TYPE] == factor_name
                    ][0],
                )

        trust_id_comparison_data.append(factor_comparison_data)
    trust_id_comparison_data.insert(0, composite_factor_scores)

    return trust_id_comparison_data
