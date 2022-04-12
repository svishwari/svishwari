# pylint: disable=too-many-lines
"""Trust ID response stub data"""

trust_id_overview_stub_data = {
    "trust_id_score": 73,
    "signals": [
        {
            "signal_name": "humanity",
            "signal_score": 71,
            "signal_description": (
                "Humanity is demonstrating empathy and kindness towards "
                "customers, and treating everyone fairly. It is scored "
                "on a scale between -100 to 100"
            ),
            "overall_customer_rating": {
                "total_customers": 190909,
                "rating": {
                    "agree": {"percentage": 0.82, "count": 156545},
                    "neutral": {"percentage": 0.07, "count": 13363},
                    "disagree": {"percentage": 0.11, "count": 21001},
                },
            },
        },
        {
            "signal_name": "transparency",
            "signal_score": 71,
            "signal_description": (
                "Transparency is openly sharing all information, motives, and "
                "choices in straightforward and plain language. It is scored "
                "on a scale between -100 to 100"
            ),
            "overall_customer_rating": {
                "total_customers": 190909,
                "rating": {
                    "agree": {"percentage": 0.82, "count": 156545},
                    "neutral": {"percentage": 0.07, "count": 13363},
                    "disagree": {"percentage": 0.11, "count": 21001},
                },
            },
        },
        {
            "signal_name": "capability",
            "signal_score": 78,
            "signal_description": (
                "Capability is creating quality products, services, and/or "
                "experiences. It is scored on a scale between -100 to 100"
            ),
            "overall_customer_rating": {
                "total_customers": 190909,
                "rating": {
                    "agree": {"percentage": 0.88, "count": 168000},
                    "neutral": {"percentage": 0.02, "count": 3818},
                    "disagree": {"percentage": 0.10, "count": 19091},
                },
            },
        },
        {
            "signal_name": "reliability",
            "signal_score": 71,
            "signal_description": (
                "Reliability is consistently and dependably delivering on "
                "promises. It is scored on a scale between -100 to 100"
            ),
            "overall_customer_rating": {
                "total_customers": 190909,
                "rating": {
                    "agree": {"percentage": 0.82, "count": 156545},
                    "neutral": {"percentage": 0.07, "count": 13363},
                    "disagree": {"percentage": 0.11, "count": 21001},
                },
            },
        },
    ],
}

trust_id_comparison_stub_data = [
    {
        "segment_type": "composite & signal scores",
        "segments": [
            {
                "segment_name": "Segment 1",
                "segment_filters": [],
                "attributes": [
                    {
                        "attribute_type": "trust_id",
                        "attribute_name": "HX TrustID",
                        "attribute_score": 73,
                        "attribute_description": (
                            "TrustID is scored on a scale between -100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "humanity",
                        "attribute_name": "Humanity",
                        "attribute_score": 71,
                        "attribute_description": (
                            "Humanity is demonstrating empathy and kindness "
                            "towards customers, and treating everyone fairly."
                            " It is scored on a scale between -100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "transparency",
                        "attribute_name": "Transparency",
                        "attribute_score": 71,
                        "attribute_description": (
                            "Transparency is openly sharing all information, "
                            "motives, and choices in straightforward and "
                            "plain language. It is scored on a scale between "
                            "-100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "capability",
                        "attribute_name": "Capability",
                        "attribute_score": 78,
                        "attribute_description": (
                            "Capability is creating quality products, "
                            "services, and/or experiences. It is scored on a "
                            "scale between -100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "reliability",
                        "attribute_name": "Reliability",
                        "attribute_score": 71,
                        "attribute_description": (
                            "Reliability is consistently and dependably "
                            "delivering on promises. It is scored on a "
                            "scale between -100 to 100"
                        ),
                    },
                ],
            },
            {
                "segment_name": "Segment 2",
                "segment_filters": [
                    {
                        "type": "age",
                        "description": "Age",
                        "values": [
                            "18-20 years",
                            "21-24 years",
                            "50-54 years",
                            "55-59 years",
                        ],
                    },
                    {
                        "type": "gender",
                        "description": "Gender",
                        "values": ["Female"],
                    },
                ],
                "attributes": [
                    {
                        "attribute_type": "trust_id",
                        "attribute_name": "HX TrustID",
                        "attribute_score": 73,
                        "attribute_description": (
                            "TrustID is scored on a scale between -100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "humanity",
                        "attribute_name": "Humanity",
                        "attribute_score": 65,
                        "attribute_description": (
                            "Humanity is demonstrating empathy and kindness "
                            "towards customers, and treating everyone fairly. "
                            "It is scored on a scale between -100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "transparency",
                        "attribute_name": "Transparency",
                        "attribute_score": 78,
                        "attribute_description": (
                            "Transparency is openly sharing all information, "
                            "motives, and choices in straightforward and plain"
                            " language. It is scored on a scale between "
                            "-100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "capability",
                        "attribute_name": "Capability",
                        "attribute_score": 73,
                        "attribute_description": (
                            "Capability is creating quality products, "
                            "services, and/or experiences. It is scored "
                            "on a scale between -100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "reliability",
                        "attribute_name": "Reliability",
                        "attribute_score": -14,
                        "attribute_description": (
                            "Reliability is consistently and dependably "
                            "delivering on promises. It is scored on a "
                            "scale between -100 to 100"
                        ),
                    },
                ],
            },
        ],
    },
    {
        "segment_type": "capability attributes",
        "segments": [
            {
                "segment_name": "Segment 1",
                "segment_filters": [],
                "attributes": [
                    {
                        "attribute_type": "capability",
                        "attribute_name": "Capability",
                        "attribute_score": 78,
                        "attribute_description": (
                            "Capability is creating quality products, "
                            "services, and/or experiences. It is scored "
                            "on a scale between -100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "product_quality",
                        "attribute_name": "Product quality",
                        "attribute_score": 78,
                        "attribute_description": (
                            "Products are good quality, accessible "
                            "and safe to use"
                        ),
                    },
                    {
                        "attribute_type": "good_value",
                        "attribute_name": "Good value",
                        "attribute_score": 71,
                        "attribute_description": (
                            "Prices of products, services, and "
                            "experiences are good value for money"
                        ),
                    },
                    {
                        "attribute_type": "competent_leaders_employees",
                        "attribute_name": "Competent leaders & employees",
                        "attribute_score": 71,
                        "attribute_description": (
                            "Employees and leadership are competent "
                            "and understand how to respond to needs"
                        ),
                    },
                    {
                        "attribute_type": "long_term_solutions_improvements",
                        "attribute_name": "Long-term solutions & improvements",
                        "attribute_score": 71,
                        "attribute_description": (
                            "Creates long-term solutions and improvements "
                            "that work well for me"
                        ),
                    },
                ],
            },
            {
                "segment_name": "Segment 2",
                "segment_filters": [
                    {
                        "type": "age",
                        "description": "Age",
                        "values": [
                            "18-20 years",
                            "21-24 years",
                            "50-54 years",
                            "55-59 years",
                        ],
                    },
                    {
                        "type": "gender",
                        "description": "Gender",
                        "values": ["Female"],
                    },
                ],
                "attributes": [
                    {
                        "attribute_type": "capability",
                        "attribute_name": "Capability",
                        "attribute_score": 73,
                        "attribute_description": (
                            "Capability is creating quality products, "
                            "services, and/or experiences. It is scored "
                            "on a scale between -100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "product_quality",
                        "attribute_name": "Product quality",
                        "attribute_score": 88,
                        "attribute_description": (
                            "Products are good quality, accessible "
                            "and safe to use"
                        ),
                    },
                    {
                        "attribute_type": "good_value",
                        "attribute_name": "Good value",
                        "attribute_score": 78,
                        "attribute_description": (
                            "Prices of products, services, and "
                            "experiences are good value for money"
                        ),
                    },
                    {
                        "attribute_type": "competent_leaders_employess",
                        "attribute_name": "Competent leaders & employees",
                        "attribute_score": 84,
                        "attribute_description": (
                            "Employees and leadership are competent and "
                            "understand how to respond to needs"
                        ),
                    },
                    {
                        "attribute_type": "long_term_solutions_improvements",
                        "attribute_name": "Long-term solutions & improvements",
                        "attribute_score": 48,
                        "attribute_description": (
                            "Creates long-term solutions and improvements "
                            "that work well for me"
                        ),
                    },
                ],
            },
        ],
    },
    {
        "segment_type": "humanity attributes",
        "segments": [
            {
                "segment_name": "Segment 1",
                "segment_filters": [],
                "attributes": [
                    {
                        "attribute_type": "humanity",
                        "attribute_name": "Humanity",
                        "attribute_score": 71,
                        "attribute_description": (
                            "Humanity is demonstrating empathy and kindness "
                            "towards customers, and treating everyone fairly. "
                            "It is scored on a scale between -100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "quickly_resolves_issues",
                        "attribute_name": "Quickly Resolves Issues",
                        "attribute_score": 71,
                        "attribute_description": (
                            "Quickly resolves issues with safety, security "
                            "and satisfaction top of mind"
                        ),
                    },
                    {
                        "attribute_type": "values_respects_everyone",
                        "attribute_name": "Values & respects everyone",
                        "attribute_score": 67,
                        "attribute_description": (
                            "Values and respects everyone, regardless of "
                            "background, identity or beliefs"
                        ),
                    },
                    {
                        "attribute_type": "values_society_environment",
                        "attribute_name": "Values society & environment",
                        "attribute_score": 50,
                        "attribute_description": (
                            "Values the good of society and the "
                            "environment, not just profit"
                        ),
                    },
                    {
                        "attribute_type": "takes_care_of_employees",
                        "attribute_name": "Takes care of employees",
                        "attribute_score": 89,
                        "attribute_description": "Takes care of employees",
                    },
                ],
            },
            {
                "segment_name": "Segment 2",
                "segment_filters": [
                    {
                        "type": "age",
                        "description": "Age",
                        "values": [
                            "18-20 years",
                            "21-24 years",
                            "50-54 years",
                            "55-59 years",
                        ],
                    },
                    {
                        "type": "gender",
                        "description": "Gender",
                        "values": ["Female"],
                    },
                ],
                "attributes": [
                    {
                        "attribute_type": "humanity",
                        "attribute_name": "Humanity",
                        "attribute_score": 65,
                        "attribute_description": (
                            "Humanity is demonstrating empathy and kindness "
                            "towards customers, and treating everyone fairly. "
                            "It is scored on a scale between -100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "quickly_resolves_issues",
                        "attribute_name": "Quickly Resolves Issues",
                        "attribute_score": 74,
                        "attribute_description": (
                            "Quickly resolves issues with safety, security "
                            "and satisfaction top of mind"
                        ),
                    },
                    {
                        "attribute_type": "values_respects_everyone",
                        "attribute_name": "Values & respects everyone",
                        "attribute_score": 64,
                        "attribute_description": (
                            "Values and respects everyone, regardless of "
                            "background, identity or beliefs"
                        ),
                    },
                    {
                        "attribute_type": "values_society_environment",
                        "attribute_name": "Values society & environment",
                        "attribute_score": -10,
                        "attribute_description": (
                            "Values the good of society and the environment, "
                            "not just profit"
                        ),
                    },
                    {
                        "attribute_type": "takes_care_of_employees",
                        "attribute_name": "Takes care of employees",
                        "attribute_score": 89,
                        "attribute_description": "Takes care of employees",
                    },
                ],
            },
        ],
    },
    {
        "segment_type": "transparency attributes",
        "segments": [
            {
                "segment_name": "Segment 1",
                "segment_filters": [],
                "attributes": [
                    {
                        "attribute_type": "transparency",
                        "attribute_name": "Transparency",
                        "attribute_score": 71,
                        "attribute_description": (
                            "Transparency is openly sharing all information, "
                            "motives, and choices in straightforward and plain"
                            " language. It is scored on a scale between "
                            "-100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "honesty_marketing_comms",
                        "attribute_name": "Honesty marketing & comms",
                        "attribute_score": 71,
                        "attribute_description": (
                            "Marketing and communications are accurate "
                            "and honest"
                        ),
                    },
                    {
                        "attribute_type": "upfront_on_how_they_make_money",
                        "attribute_name": "Upfront on how they make money",
                        "attribute_score": 67,
                        "attribute_description": (
                            "Upfront about how they make and spend money "
                            "from interactions"
                        ),
                    },
                    {
                        "attribute_type": "plain_language_data_policy",
                        "attribute_name": "Plain language data policy",
                        "attribute_score": 50,
                        "attribute_description": (
                            "How and why my data is used is communicated "
                            "in plain and easy to understand language"
                        ),
                    },
                    {
                        "attribute_type": "clear_fees_costs",
                        "attribute_name": "Clear fees & costs",
                        "attribute_score": 89,
                        "attribute_description": (
                            "Clear and upfront about fees and costs of "
                            "products, services and experiences"
                        ),
                    },
                ],
            },
            {
                "segment_name": "Segment 2",
                "segment_filters": [
                    {
                        "type": "age",
                        "description": "Age",
                        "values": [
                            "18-20 years",
                            "21-24 years",
                            "50-54 years",
                            "55-59 years",
                        ],
                    },
                    {
                        "type": "gender",
                        "description": "Gender",
                        "values": ["Female"],
                    },
                ],
                "attributes": [
                    {
                        "attribute_type": "transparency",
                        "attribute_name": "Transparency",
                        "attribute_score": 78,
                        "attribute_description": (
                            "Transparency is openly sharing all information, "
                            "motives, and choices in straightforward and plain"
                            " language. It is scored on a scale between "
                            "-100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "honesty_marketing_comms",
                        "attribute_name": "Honesty marketing & comms",
                        "attribute_score": 78,
                        "attribute_description": (
                            "Marketing and communications are accurate "
                            "and honest"
                        ),
                    },
                    {
                        "attribute_type": "upfront_on_how_they_make_money",
                        "attribute_name": "Upfront on how they make money",
                        "attribute_score": 68,
                        "attribute_description": (
                            "Upfront about how they make and spend money "
                            "from interactions"
                        ),
                    },
                    {
                        "attribute_type": "plain_language_data_policy",
                        "attribute_name": "Plain language data policy",
                        "attribute_score": 88,
                        "attribute_description": (
                            "How and why my data is used is communicated in "
                            "plain and easy to understand language"
                        ),
                    },
                    {
                        "attribute_type": "clear_fees_costs",
                        "attribute_name": "Clear fees & costs",
                        "attribute_score": 78,
                        "attribute_description": (
                            "Clear and upfront about fees and costs of "
                            "products, services and experiences"
                        ),
                    },
                ],
            },
        ],
    },
    {
        "segment_type": "reliability attributes",
        "segments": [
            {
                "segment_name": "Segment 1",
                "segment_filters": [],
                "attributes": [
                    {
                        "attribute_type": "reliability",
                        "attribute_name": "Reliability",
                        "attribute_score": 71,
                        "attribute_description": (
                            "Reliability is consistently and dependably "
                            "delivering on promises. It is scored on a "
                            "scale between -100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "continuous_product_improvement",
                        "attribute_name": "Continuous product improvement",
                        "attribute_score": 71,
                        "attribute_description": (
                            "Can be counted on to improve the quality "
                            "of products and services"
                        ),
                    },
                    {
                        "attribute_type": "consistent_quality",
                        "attribute_name": "Consistent quality",
                        "attribute_score": 67,
                        "attribute_description": (
                            "Consistently delivers products, services "
                            "and experiences with quality"
                        ),
                    },
                    {
                        "attribute_type": "smooth_digital_interactions",
                        "attribute_name": "Smooth digital interactions",
                        "attribute_score": 50,
                        "attribute_description": (
                            "Facilitates digital interactions that "
                            "run smoothly and work when needed"
                        ),
                    },
                    {
                        "attribute_type": "timely_issue_resolution",
                        "attribute_name": "Timely issue resolution",
                        "attribute_score": 89,
                        "attribute_description": (
                            "Resolves issues in an adequate and timely manner"
                        ),
                    },
                ],
            },
            {
                "segment_name": "Segment 2",
                "segment_filters": [
                    {
                        "type": "age",
                        "description": "Age",
                        "values": [
                            "18-20 years",
                            "21-24 years",
                            "50-54 years",
                            "55-59 years",
                        ],
                    },
                    {
                        "type": "gender",
                        "description": "Gender",
                        "values": ["Female"],
                    },
                ],
                "attributes": [
                    {
                        "attribute_type": "reliability",
                        "attribute_name": "Reliability",
                        "attribute_score": 34,
                        "attribute_description": (
                            "Reliability is consistently and dependably "
                            "delivering on promises. It is scored on a "
                            "scale between -100 to 100"
                        ),
                    },
                    {
                        "attribute_type": "continuous_product_improvement",
                        "attribute_name": "Continuous product improvement",
                        "attribute_score": 42,
                        "attribute_description": (
                            "Can be counted on to improve the quality "
                            "of products and services"
                        ),
                    },
                    {
                        "attribute_type": "consistent_quality",
                        "attribute_name": "Consistent quality",
                        "attribute_score": 79,
                        "attribute_description": (
                            "Consistently delivers products, services "
                            "and experiences with quality"
                        ),
                    },
                    {
                        "attribute_type": "smooth_digital_interactions",
                        "attribute_name": "Smooth digital interactions",
                        "attribute_score": 8,
                        "attribute_description": (
                            "Facilitates digital interactions that run "
                            "smoothly and work when needed"
                        ),
                    },
                    {
                        "attribute_type": "timely_issue_resolution",
                        "attribute_name": "Timely issue resolution",
                        "attribute_score": -18,
                        "attribute_description": (
                            "Resolves issues in an adequate and timely manner"
                        ),
                    },
                ],
            },
        ],
    },
]

trust_id_attribute_stub_data = [
    {
        "signal_name": "capability",
        "attribute_score": -31,
        "attribute_description": (
            "Products are good quality, accessible and safe to use"
        ),
        "overall_customer_rating": {
            "total_customers": 134036,
            "rating": {
                "agree": {"percentage": 0.0581, "count": 7793},
                "neutral": {"percentage": 0.5689, "count": 76250},
                "disagree": {"percentage": 0.373, "count": 49993},
            },
        },
    },
    {
        "signal_name": "capability",
        "attribute_score": 16,
        "attribute_description": (
            "Prices of products, services, and "
            "experiences are good value for money"
        ),
        "overall_customer_rating": {
            "total_customers": 225426,
            "rating": {
                "agree": {"percentage": 0.367, "count": 82722},
                "neutral": {"percentage": 0.4347, "count": 97987},
                "disagree": {"percentage": 0.1984, "count": 44717},
            },
        },
    },
    {
        "signal_name": "capability",
        "attribute_score": 3,
        "attribute_description": (
            "Employees and leadership are competent and "
            "understand how to respond to needs"
        ),
        "overall_customer_rating": {
            "total_customers": 115498,
            "rating": {
                "agree": {"percentage": 0.4207, "count": 48592},
                "neutral": {"percentage": 0.1925, "count": 22233},
                "disagree": {"percentage": 0.3868, "count": 44673},
            },
        },
    },
    {
        "signal_name": "capability",
        "attribute_score": 6,
        "attribute_description": (
            "Creates long-term solutions and improvements that "
            "work well for me"
        ),
        "overall_customer_rating": {
            "total_customers": 177435,
            "rating": {
                "agree": {"percentage": 0.2644, "count": 46906},
                "neutral": {"percentage": 0.5354, "count": 95007},
                "disagree": {"percentage": 0.2002, "count": 35522},
            },
        },
    },
    {
        "signal_name": "humanity",
        "attribute_score": 14,
        "attribute_description": (
            "Quickly resolves issues with safety, security and satisfaction "
            "top of mind"
        ),
        "overall_customer_rating": {
            "total_customers": 168740,
            "rating": {
                "agree": {"percentage": 0.3453, "count": 58273},
                "neutral": {"percentage": 0.4583, "count": 77340},
                "disagree": {"percentage": 0.1963, "count": 33127},
            },
        },
    },
    {
        "signal_name": "humanity",
        "attribute_score": 23,
        "attribute_description": (
            "Values and respects everyone, regardless of background, "
            "identity or beliefs"
        ),
        "overall_customer_rating": {
            "total_customers": 195412,
            "rating": {
                "agree": {"percentage": 0.3631, "count": 70950},
                "neutral": {"percentage": 0.5088, "count": 99423},
                "disagree": {"percentage": 0.1281, "count": 25039},
            },
        },
    },
    {
        "signal_name": "humanity",
        "attribute_score": 43,
        "attribute_description": (
            "Values the good of society and the environment, not just profit"
        ),
        "overall_customer_rating": {
            "total_customers": 76687,
            "rating": {
                "agree": {"percentage": 0.6877, "count": 52736},
                "neutral": {"percentage": 0.056, "count": 4295},
                "disagree": {"percentage": 0.2563, "count": 19656},
            },
        },
    },
    {
        "signal_name": "humanity",
        "attribute_score": 6,
        "attribute_description": "Takes care of employees",
        "overall_customer_rating": {
            "total_customers": 166498,
            "rating": {
                "agree": {"percentage": 0.5172, "count": 86106},
                "neutral": {"percentage": 0.0278, "count": 4622},
                "disagree": {"percentage": 0.4551, "count": 75770},
            },
        },
    },
    {
        "signal_name": "transparency",
        "attribute_score": -14,
        "attribute_description": (
            "Marketing and communications are accurate and honest"
        ),
        "overall_customer_rating": {
            "total_customers": 88798,
            "rating": {
                "agree": {"percentage": 0.1131, "count": 10044},
                "neutral": {"percentage": 0.6302, "count": 55962},
                "disagree": {"percentage": 0.2567, "count": 22792},
            },
        },
    },
    {
        "signal_name": "transparency",
        "attribute_score": 41,
        "attribute_description": (
            "Upfront about how they make and spend money from interactions"
        ),
        "overall_customer_rating": {
            "total_customers": 165955,
            "rating": {
                "agree": {"percentage": 0.4787, "count": 79442},
                "neutral": {"percentage": 0.4573, "count": 75894},
                "disagree": {"percentage": 0.064, "count": 10619},
            },
        },
    },
    {
        "signal_name": "transparency",
        "attribute_score": -23,
        "attribute_description": (
            "How and why my data is used is communicated in plain "
            "and easy to understand language"
        ),
        "overall_customer_rating": {
            "total_customers": 176300,
            "rating": {
                "agree": {"percentage": 0.1466, "count": 25839},
                "neutral": {"percentage": 0.4696, "count": 82786},
                "disagree": {"percentage": 0.3839, "count": 67675},
            },
        },
    },
    {
        "signal_name": "transparency",
        "attribute_score": 6,
        "attribute_description": (
            "Clear and upfront about fees and costs of products, "
            "services and experiences"
        ),
        "overall_customer_rating": {
            "total_customers": 257410,
            "rating": {
                "agree": {"percentage": 0.3463, "count": 89150},
                "neutral": {"percentage": 0.3715, "count": 95631},
                "disagree": {"percentage": 0.2822, "count": 72629},
            },
        },
    },
    {
        "signal_name": "reliability",
        "attribute_score": -9,
        "attribute_description": (
            "Can be counted on to improve the quality of products and services"
        ),
        "overall_customer_rating": {
            "total_customers": 178742,
            "rating": {
                "agree": {"percentage": 0.3828, "count": 68423},
                "neutral": {"percentage": 0.1416, "count": 25318},
                "disagree": {"percentage": 0.4756, "count": 85001},
            },
        },
    },
    {
        "signal_name": "reliability",
        "attribute_score": 7,
        "attribute_description": (
            "Consistently delivers products, services and experiences "
            "with quality"
        ),
        "overall_customer_rating": {
            "total_customers": 116304,
            "rating": {
                "agree": {"percentage": 0.526, "count": 61172},
                "neutral": {"percentage": 0.0203, "count": 2356},
                "disagree": {"percentage": 0.4538, "count": 52776},
            },
        },
    },
    {
        "signal_name": "reliability",
        "attribute_score": -33,
        "attribute_description": (
            "Facilitates digital interactions that run smoothly and "
            "work when needed"
        ),
        "overall_customer_rating": {
            "total_customers": 203131,
            "rating": {
                "agree": {"percentage": 0.1329, "count": 26998},
                "neutral": {"percentage": 0.4041, "count": 82085},
                "disagree": {"percentage": 0.463, "count": 94048},
            },
        },
    },
    {
        "signal_name": "reliability",
        "attribute_score": 16,
        "attribute_description": (
            "Resolves issues in an adequate and timely manner"
        ),
        "overall_customer_rating": {
            "total_customers": 209956,
            "rating": {
                "agree": {"percentage": 0.4059, "count": 85230},
                "neutral": {"percentage": 0.3555, "count": 74629},
                "disagree": {"percentage": 0.2386, "count": 50097},
            },
        },
    },
]

trust_id_filters_stub = [
    {
        "type": "households_with_children_under_18",
        "description": "Households with children under 18",
        "values": ["true"],
    },
    {
        "type": "households_with_seniors_over_65",
        "description": "Households with seniors over 65",
        "values": ["true"],
    },
    {
        "type": "age",
        "description": "Age",
        "values": [
            "18-20 years",
            "21-24 years",
            "25-29 years",
            "30-34 years",
            "35-39 years",
            "40-44 years",
            "45-49 years",
            "50-54 years",
            "55-59 years",
            "60-64 years",
            "65-69 years",
            "70-79 years",
            "80-89 years",
            "Other",
            "Prefer not to say",
        ],
    },
    {
        "type": "children_count",
        "description": "Children count",
        "values": ["1", "2", "3", "4", "5+"],
    },
    {
        "type": "employment_status",
        "description": "Employment status",
        "values": [
            "Employed full-time",
            "Employed part-time",
            "Employed on temporary, contract, gig basis",
            "Full-time homemaker",
            "Retired",
            "Unemployed",
            "Other",
        ],
    },
    {
        "type": "gender",
        "description": "Gender",
        "values": ["Male", "Female", "Gender-fluid/ Non-binary", "Other"],
    },
    {
        "type": "highest_level_of_education",
        "description": "Highest level of education",
        "values": [
            "Some high-school diploma",
            "High-school diploma",
            "Vocational school",
            "Undergraduate degree",
            "Graduate degree",
            "Post-graduate degree",
        ],
    },
    {
        "type": "lgbtq_identified",
        "description": "LGBTQ identified",
        "values": ["Yes", "No", "Not sure what to say", "Prefer not to say"],
    },
    {
        "type": "living_situation",
        "description": "Living situation",
        "values": [
            "Unmarried and living alone",
            "Unmarried and living roommates / family",
            "Unmarried and living with significant other",
            "Married",
            "Divorced, separated",
            "Other",
            "Prefer not to answer",
        ],
    },
    {
        "type": "physical_mental_condition",
        "description": "Physical & mental condition",
        "values": [
            "Blindness / partial sight",
            "Deafness / partial hearing",
            "Mobility impairment",
            (
                "Dexterity impairment (e.g. lifting or carrying objects, "
                "using a keyboard"
            ),
            "Learning, understanding or concentrating difficulty or disability",
            "Memory difficulty or disability",
            "Memory health condition",
            "Stamina, breathing or fatigue difficulty or disability",
            (
                "Social or behavioral difficulty or disability "
                "(e.g. associated with autism, attention deficit disorder "
                "or Asperger's syndrome)"
            ),
            "Other",
            "Prefer not to say",
        ],
    },
    {
        "type": "political_outlook",
        "description": "Political outlook",
        "values": [
            "Very liberal",
            "Liberal",
            "Centrist / Moderate",
            "Conservative",
            "Very conservative",
            "Prefer not to answer",
        ],
    },
    {
        "type": "race_ethnicity",
        "description": "Race & ethnicity",
        "values": [
            "Alaska Native or Native American",
            "Asian",
            "Black, African-American, Caribbean",
            "Hispanic, Latino, Spanish",
            "Native Hawaiian or Other Pacific Islander",
            "White",
            "Other",
            "Prefer not to say",
        ],
    },
    {
        "type": "residential_area",
        "description": "Residential area",
        "values": ["Urban", "Suburban", "Rural"],
    },
]
