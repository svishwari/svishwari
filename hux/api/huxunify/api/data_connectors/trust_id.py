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
        for factor_name, values in survey_response[db_c.FACTORS].items():
            for attribute in values[db_c.ATTRIBUTES]:
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

    for factor_name, values in attribute_aggregated_values.items():
        for attribute_values in values.values():
            attribute_values.update(
                {
                    api_c.SCORE: (
                        attribute_values.get(api_c.AGREE, 0)
                        - attribute_values.get(api_c.DISAGREE, 0)
                    )
                    / len(survey_responses)
                    * 100
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
                    statistics.mean(
                        [
                            val[api_c.SCORE]
                            for x, val in values.items()
                            if isinstance(val, dict)
                        ]
                    )
                ),
                api_c.FACTOR_DESCRIPTION: api_c.FACTOR_DESCRIPTION_MAP[
                    factor_name
                ],
                api_c.OVERALL_CUSTOMER_RATING: {
                    api_c.TOTAL_CUSTOMERS: len(survey_responses),
                    api_c.RATING: {
                        customer_rating: {
                            api_c.COUNT: values.get(customer_rating, 0),
                            api_c.PERCENTAGE: values.get(customer_rating, 0)
                            / len(survey_responses),
                        }
                        for customer_rating in api_c.RATING_MAP.values()
                    },
                },
            }
            for factor_name, values in aggregated_attributes.items()
        ]
    }

    overview_data[api_c.TRUST_ID_SCORE] = int(
        statistics.mean(
            [x[api_c.FACTOR_SCORE] for x in overview_data[db_c.FACTORS]]
        )
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
                            api_c.PERCENTAGE: attribute_aggregated_values[
                                attribute[api_c.FACTOR_NAME]
                            ][attribute[api_c.ATTRIBUTE_DESCRIPTION]].get(
                                customer_rating, 0
                            )
                            / len(survey_responses),
                        }
                        for customer_rating in api_c.RATING_MAP.values()
                    },
                },
            }
        )

    return trust_id_attributes
