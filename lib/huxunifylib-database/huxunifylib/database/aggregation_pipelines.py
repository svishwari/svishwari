# pylint:disable=too-many-lines
"""This module houses all aggregation pipelines."""

trust_id_overview_pipeline = [
    {"$project": {"factors": "$responses.factors"}},
    {
        "$group": {
            "_id": None,
            "total_customers": {"$sum": 1},
            "humanity_agree": {
                "$sum": {
                    "$cond": [{"$eq": ["$factors.HUMANITY.rating", 1]}, 1, 0]
                }
            },
            "humanity_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$factors.HUMANITY.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "humanity_neutral": {
                "$sum": {
                    "$cond": [{"$eq": ["$factors.HUMANITY.rating", 0]}, 1, 0]
                }
            },
            "reliability_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$factors.RELIABILITY.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$factors.RELIABILITY.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$factors.RELIABILITY.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "capability_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$factors.CAPABILITY.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "capability_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$factors.CAPABILITY.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "capability_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$factors.CAPABILITY.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$factors.TRANSPARENCY.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$factors.TRANSPARENCY.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$factors.TRANSPARENCY.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
        }
    },
    {
        "$addFields": {
            "humanity": {
                "total_customers": "$total_customers",
                "rating": {
                    "agree": {
                        "count": "$humanity_agree",
                        "percentage": {
                            "$divide": ["$humanity_agree", "$total_customers"]
                        },
                    },
                    "disagree": {
                        "count": "$humanity_disagree",
                        "percentage": {
                            "$divide": [
                                "$humanity_disagree",
                                "$total_customers",
                            ]
                        },
                    },
                    "neutral": {
                        "count": "$humanity_neutral",
                        "percentage": {
                            "$divide": [
                                "$humanity_neutral",
                                "$total_customers",
                            ]
                        },
                    },
                },
            },
            "reliability": {
                "total_customers": "$total_customers",
                "rating": {
                    "agree": {
                        "count": "$reliability_agree",
                        "percentage": {
                            "$divide": [
                                "$reliability_agree",
                                "$total_customers",
                            ]
                        },
                    },
                    "disagree": {
                        "count": "$reliability_disagree",
                        "percentage": {
                            "$divide": [
                                "$reliability_disagree",
                                "$total_customers",
                            ]
                        },
                    },
                    "neutral": {
                        "count": "$reliability_neutral",
                        "percentage": {
                            "$divide": [
                                "$reliability_neutral",
                                "$total_customers",
                            ]
                        },
                    },
                },
            },
            "capability": {
                "total_customers": "$total_customers",
                "rating": {
                    "agree": {
                        "count": "$capability_agree",
                        "percentage": {
                            "$divide": [
                                "$capability_agree",
                                "$total_customers",
                            ]
                        },
                    },
                    "disagree": {
                        "count": "$capability_disagree",
                        "percentage": {
                            "$divide": [
                                "$capability_disagree",
                                "$total_customers",
                            ]
                        },
                    },
                    "neutral": {
                        "count": "$capability_neutral",
                        "percentage": {
                            "$divide": [
                                "$capability_neutral",
                                "$total_customers",
                            ]
                        },
                    },
                },
            },
            "transparency": {
                "total_customers": "$total_customers",
                "rating": {
                    "agree": {
                        "count": "$transparency_agree",
                        "percentage": {
                            "$divide": [
                                "$transparency_agree",
                                "$total_customers",
                            ]
                        },
                    },
                    "disagree": {
                        "count": "$transparency_disagree",
                        "percentage": {
                            "$divide": [
                                "$transparency_disagree",
                                "$total_customers",
                            ]
                        },
                    },
                    "neutral": {
                        "count": "$transparency_neutral",
                        "percentage": {
                            "$divide": [
                                "$transparency_neutral",
                                "$total_customers",
                            ]
                        },
                    },
                },
            },
        }
    },
    {
        "$project": {
            "humanity": 1,
            "reliability": 1,
            "capability": 1,
            "transparency": 1,
        }
    },
]

trust_id_attribute_ratings_pipeline = [
    {
        "$project": {
            "humanity": "$responses.factors.HUMANITY.attributes",
            "reliability": "$responses.factors.RELIABILITY.attributes",
            "capability": "$responses.factors.CAPABILITY.attributes",
            "transparency": "$responses.factors.TRANSPARENCY.attributes",
        }
    },
    {
        "$addFields": {
            "humanity_attribute1": {"$arrayElemAt": ["$humanity", 0]},
            "humanity_attribute2": {"$arrayElemAt": ["$humanity", 1]},
            "humanity_attribute3": {"$arrayElemAt": ["$humanity", 2]},
            "humanity_attribute4": {"$arrayElemAt": ["$humanity", 3]},
            "reliability_attribute1": {"$arrayElemAt": ["$reliability", 0]},
            "reliability_attribute2": {"$arrayElemAt": ["$reliability", 1]},
            "reliability_attribute3": {"$arrayElemAt": ["$reliability", 2]},
            "reliability_attribute4": {"$arrayElemAt": ["$reliability", 3]},
            "capability_attribute1": {"$arrayElemAt": ["$capability", 0]},
            "capability_attribute2": {"$arrayElemAt": ["$capability", 1]},
            "capability_attribute3": {"$arrayElemAt": ["$capability", 2]},
            "capability_attribute4": {"$arrayElemAt": ["$capability", 3]},
            "transparency_attribute1": {"$arrayElemAt": ["$transparency", 0]},
            "transparency_attribute2": {"$arrayElemAt": ["$transparency", 1]},
            "transparency_attribute3": {"$arrayElemAt": ["$transparency", 2]},
            "transparency_attribute4": {"$arrayElemAt": ["$transparency", 3]},
        }
    },
    {
        "$group": {
            "_id": None,
            "total_customers": {"$sum": 1},
            "humanity_attribute1_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$humanity_attribute1.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "humanity_attribute1_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$humanity_attribute1.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "humanity_attribute1_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$humanity_attribute1.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "humanity_attribute2_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$humanity_attribute2.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "humanity_attribute2_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$humanity_attribute2.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "humanity_attribute2_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$humanity_attribute2.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "humanity_attribute3_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$humanity_attribute3.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "humanity_attribute3_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$humanity_attribute3.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "humanity_attribute3_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$humanity_attribute3.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "humanity_attribute4_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$humanity_attribute4.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "humanity_attribute4_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$humanity_attribute4.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "humanity_attribute4_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$humanity_attribute4.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_attribute1_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$reliability_attribute1.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_attribute1_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$reliability_attribute1.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_attribute1_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$reliability_attribute1.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_attribute2_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$reliability_attribute2.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_attribute2_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$reliability_attribute2.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_attribute2_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$reliability_attribute2.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_attribute3_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$reliability_attribute3.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_attribute3_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$reliability_attribute3.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_attribute3_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$reliability_attribute3.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_attribute4_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$reliability_attribute4.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_attribute4_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$reliability_attribute4.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "reliability_attribute4_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$reliability_attribute4.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "capability_attribute1_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$capability_attribute1.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "capability_attribute1_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$capability_attribute1.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "capability_attribute1_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$capability_attribute1.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "capability_attribute2_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$capability_attribute2.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "capability_attribute2_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$capability_attribute2.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "capability_attribute2_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$capability_attribute2.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "capability_attribute3_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$capability_attribute3.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "capability_attribute3_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$capability_attribute3.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "capability_attribute3_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$capability_attribute3.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "capability_attribute4_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$capability_attribute4.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "capability_attribute4_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$capability_attribute4.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "capability_attribute4_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$capability_attribute4.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_attribute1_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$transparency_attribute1.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_attribute1_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$transparency_attribute1.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_attribute1_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$transparency_attribute1.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_attribute2_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$transparency_attribute2.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_attribute2_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$transparency_attribute2.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_attribute2_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$transparency_attribute2.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_attribute3_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$transparency_attribute3.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_attribute3_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$transparency_attribute3.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_attribute3_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$transparency_attribute3.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_attribute4_agree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$transparency_attribute4.rating", 1]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_attribute4_disagree": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$transparency_attribute4.rating", -1]},
                        1,
                        0,
                    ]
                }
            },
            "transparency_attribute4_neutral": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$transparency_attribute4.rating", 0]},
                        1,
                        0,
                    ]
                }
            },
        }
    },
    {
        "$addFields": {
            "attributes": {
                "humanity": [
                    {
                        "agree": {
                            "count": "$humanity_attribute1_agree",
                            "percentage": {
                                "$divide": [
                                    "$humanity_attribute1_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$humanity_attribute1_disagree",
                            "percentage": {
                                "$divide": [
                                    "$humanity_attribute1_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$humanity_attribute1_neutral",
                            "percentage": {
                                "$divide": [
                                    "$humanity_attribute1_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                    {
                        "agree": {
                            "count": "$humanity_attribute2_agree",
                            "percentage": {
                                "$divide": [
                                    "$humanity_attribute2_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$humanity_attribute2_disagree",
                            "percentage": {
                                "$divide": [
                                    "$humanity_attribute2_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$humanity_attribute2_neutral",
                            "percentage": {
                                "$divide": [
                                    "$humanity_attribute2_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                    {
                        "agree": {
                            "count": "$humanity_attribute3_agree",
                            "percentage": {
                                "$divide": [
                                    "$humanity_attribute3_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$humanity_attribute3_disagree",
                            "percentage": {
                                "$divide": [
                                    "$humanity_attribute3_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$humanity_attribute3_neutral",
                            "percentage": {
                                "$divide": [
                                    "$humanity_attribute3_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                    {
                        "agree": {
                            "count": "$humanity_attribute4_agree",
                            "percentage": {
                                "$divide": [
                                    "$humanity_attribute4_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$humanity_attribute4_disagree",
                            "percentage": {
                                "$divide": [
                                    "$humanity_attribute4_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$humanity_attribute4_neutral",
                            "percentage": {
                                "$divide": [
                                    "$humanity_attribute4_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                ],
                "reliability": [
                    {
                        "agree": {
                            "count": "$reliability_attribute1_agree",
                            "percentage": {
                                "$divide": [
                                    "$reliability_attribute1_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$reliability_attribute1_disagree",
                            "percentage": {
                                "$divide": [
                                    "$reliability_attribute1_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$reliability_attribute1_neutral",
                            "percentage": {
                                "$divide": [
                                    "$reliability_attribute1_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                    {
                        "agree": {
                            "count": "$reliability_attribute2_agree",
                            "percentage": {
                                "$divide": [
                                    "$reliability_attribute2_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$reliability_attribute2_disagree",
                            "percentage": {
                                "$divide": [
                                    "$reliability_attribute2_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$reliability_attribute2_neutral",
                            "percentage": {
                                "$divide": [
                                    "$reliability_attribute2_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                    {
                        "agree": {
                            "count": "$reliability_attribute3_agree",
                            "percentage": {
                                "$divide": [
                                    "$reliability_attribute3_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$reliability_attribute3_disagree",
                            "percentage": {
                                "$divide": [
                                    "$reliability_attribute3_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$reliability_attribute3_neutral",
                            "percentage": {
                                "$divide": [
                                    "$reliability_attribute3_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                    {
                        "agree": {
                            "count": "$reliability_attribute4_agree",
                            "percentage": {
                                "$divide": [
                                    "$reliability_attribute4_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$reliability_attribute4_disagree",
                            "percentage": {
                                "$divide": [
                                    "$reliability_attribute4_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$reliability_attribute4_neutral",
                            "percentage": {
                                "$divide": [
                                    "$reliability_attribute4_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                ],
                "capability": [
                    {
                        "agree": {
                            "count": "$capability_attribute1_agree",
                            "percentage": {
                                "$divide": [
                                    "$capability_attribute1_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$capability_attribute1_disagree",
                            "percentage": {
                                "$divide": [
                                    "$capability_attribute1_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$capability_attribute1_neutral",
                            "percentage": {
                                "$divide": [
                                    "$capability_attribute1_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                    {
                        "agree": {
                            "count": "$capability_attribute2_agree",
                            "percentage": {
                                "$divide": [
                                    "$capability_attribute2_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$capability_attribute2_disagree",
                            "percentage": {
                                "$divide": [
                                    "$capability_attribute2_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$capability_attribute2_neutral",
                            "percentage": {
                                "$divide": [
                                    "$capability_attribute2_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                    {
                        "agree": {
                            "count": "$capability_attribute3_agree",
                            "percentage": {
                                "$divide": [
                                    "$capability_attribute3_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$capability_attribute3_disagree",
                            "percentage": {
                                "$divide": [
                                    "$capability_attribute3_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$capability_attribute3_neutral",
                            "percentage": {
                                "$divide": [
                                    "$capability_attribute3_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                    {
                        "agree": {
                            "count": "$capability_attribute4_agree",
                            "percentage": {
                                "$divide": [
                                    "$capability_attribute4_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$capability_attribute4_disagree",
                            "percentage": {
                                "$divide": [
                                    "$capability_attribute4_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$capability_attribute4_neutral",
                            "percentage": {
                                "$divide": [
                                    "$capability_attribute4_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                ],
                "transparency": [
                    {
                        "agree": {
                            "count": "$transparency_attribute1_agree",
                            "percentage": {
                                "$divide": [
                                    "$transparency_attribute1_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$transparency_attribute1_disagree",
                            "percentage": {
                                "$divide": [
                                    "$transparency_attribute1_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$transparency_attribute1_neutral",
                            "percentage": {
                                "$divide": [
                                    "$transparency_attribute1_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                    {
                        "agree": {
                            "count": "$transparency_attribute2_agree",
                            "percentage": {
                                "$divide": [
                                    "$transparency_attribute2_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$transparency_attribute2_disagree",
                            "percentage": {
                                "$divide": [
                                    "$transparency_attribute2_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$transparency_attribute2_neutral",
                            "percentage": {
                                "$divide": [
                                    "$transparency_attribute2_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                    {
                        "agree": {
                            "count": "$transparency_attribute3_agree",
                            "percentage": {
                                "$divide": [
                                    "$transparency_attribute3_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$transparency_attribute3_disagree",
                            "percentage": {
                                "$divide": [
                                    "$transparency_attribute3_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$transparency_attribute3_neutral",
                            "percentage": {
                                "$divide": [
                                    "$transparency_attribute3_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                    {
                        "agree": {
                            "count": "$transparency_attribute4_agree",
                            "percentage": {
                                "$divide": [
                                    "$transparency_attribute4_agree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "disagree": {
                            "count": "$transparency_attribute4_disagree",
                            "percentage": {
                                "$divide": [
                                    "$transparency_attribute4_disagree",
                                    "$total_customers",
                                ]
                            },
                        },
                        "neutral": {
                            "count": "$transparency_attribute4_neutral",
                            "percentage": {
                                "$divide": [
                                    "$transparency_attribute4_neutral",
                                    "$total_customers",
                                ]
                            },
                        },
                    },
                ],
            }
        }
    },
    {"$project": {"attributes": 1, "total_customers": 1}},
]
