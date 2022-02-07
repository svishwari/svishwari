"""Purpose of this class is to get data from TrustID"""
import random
from collections import defaultdict
from random import randint
from typing import Union

from huxunify.api import constants as api_c


# TODO Replace stub, use OOP when data is available.
# pylint: disable=unused-argument
def get_trust_id_overview_data(filters: Union[dict, None] = None) -> dict:
    """Returns Overview data of all signals and attributes from TrustID.

    Args:
        filters (dict, Optional): Filters to be applied to get TrustID data.
    Returns:
        dict: Trust ID overview data.
    """
    signal_scores_overview = defaultdict(list)
    attribute_scores = []

    for signal, attributes in api_c.TRUST_ID_ATTRIBUTE_STUB.items():
        for attribute in attributes:
            attribute_score = randint(-20, 100)
            signal_scores_overview[signal].append(attribute_score)
            attribute_scores.append(
                {
                    api_c.NAME_OF_SIGNAL: signal,
                    api_c.ATTRIBUTE_SCORE: attribute_score,
                    api_c.ATTRIBUTE_DESCRIPTION: attribute,
                }
            )

    signal_scores_overview = {
        signal: sum(scores) // len(scores) + 1
        for signal, scores in signal_scores_overview.items()
    }

    trust_id_score_overview = sum(signal_scores_overview.values()) // len(
        signal_scores_overview.values()
    )

    return {
        api_c.TRUST_ID_SCORE_OVERVIEW: trust_id_score_overview,
        api_c.SIGNAL_SCORES_OVERVIEW: signal_scores_overview,
        api_c.ATTRIBUTE_SCORES: attribute_scores,
    }


def get_trust_id_signal_data(signal_name: str) -> dict:
    """Returns detailed information for a given signal.

    Args:
        signal_name (str): Name of the signal for which information is needed.
    Returns:
        dict: Signal information.
    """
    # TODO Replace stub, use OOP when data is available.

    customer_attribute_ratings = []

    total_customers_agree = 0
    total_customers_neutral = 0
    total_customers_disagree = 0
    total_attribute_score = 0

    for attribute in api_c.TRUST_ID_ATTRIBUTE_STUB.get(signal_name):
        agree_customers = random.randint(0, 100000)
        disagree_customers = random.randint(0, 100000)
        neutral_customers = random.randint(0, 100000)

        total_customers = (
            agree_customers + disagree_customers + neutral_customers
        )

        attribute_score = int(((
            agree_customers + (disagree_customers * -1) +
            (neutral_customers *0.5)
        ) / total_customers) *100)

        customer_attribute_ratings.append(
            {
                api_c.ATTRIBUTE_DESCRIPTION: attribute,
                api_c.ATTRIBUTE_SCORE: attribute_score,
                api_c.OVERALL_CUSTOMER_RATING: {
                    api_c.TOTAL_CUSTOMERS: total_customers,
                    api_c.RATING: {
                        api_c.AGREE: {
                            api_c.COUNT: agree_customers,
                            api_c.PERCENTAGE: round(
                                (agree_customers / total_customers) * 100, 2
                            ),
                        },
                        api_c.NEUTRAL: {
                            api_c.COUNT: neutral_customers,
                            api_c.PERCENTAGE: round(
                                (neutral_customers / total_customers) * 100, 2
                            ),
                        },
                        api_c.DISAGREE: {
                            api_c.COUNT: disagree_customers,
                            api_c.PERCENTAGE: round(
                                (disagree_customers / total_customers) * 100, 2
                            ),
                        },
                    },
                },
            }
        )

        total_customers_agree += agree_customers
        total_customers_neutral += neutral_customers
        total_customers_disagree += disagree_customers
        total_attribute_score += attribute_score

    total_attributes = len(api_c.TRUST_ID_ATTRIBUTE_STUB.get(signal_name))

    approx_total_customers = (
        total_customers_agree
        + total_customers_neutral
        + total_customers_disagree
    ) // total_attributes

    return {
        api_c.SIGNAL_NAME: signal_name,
        api_c.SIGNAL_SCORE: total_attribute_score // total_attributes,
        api_c.OVERALL_CUSTOMER_RATING: {
            api_c.TOTAL_CUSTOMERS: approx_total_customers,
            api_c.RATING: {
                api_c.AGREE: {
                    api_c.COUNT: total_customers_agree // total_attributes,
                    api_c.PERCENTAGE: round(
                        (
                            (total_customers_agree // total_attributes)
                            / approx_total_customers
                        )
                        * 100,
                        2,
                    ),
                },
                api_c.DISAGREE: {
                    api_c.COUNT: total_customers_disagree // total_attributes,
                    api_c.PERCENTAGE: round(
                        (
                            (total_customers_disagree // total_attributes)
                            / approx_total_customers
                        )
                        * 100,
                        2,
                    ),
                },
                api_c.NEUTRAL: {
                    api_c.COUNT: total_customers_neutral // total_attributes,
                    api_c.PERCENTAGE: round(
                        (
                            (total_customers_neutral // total_attributes)
                            / approx_total_customers
                        )
                        * 100,
                        2,
                    ),
                },
            },
        },
        api_c.CUSTOMER_ATTRIBUTE_RATINGS: customer_attribute_ratings,
    }
