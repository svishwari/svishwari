"""
purpose of this script is for housing the advertising routes for the API
"""
import json
from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from
from api.model.marketing import MarketingModel
import api.schema.marketing as schema


marketing_bp = Blueprint('marketing_bp', __name__)


@marketing_bp.route('/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'marketing api',
            'schema': schema.MarketingSchema
        }
    }
})
def index():
    """
    marketing api landing
    ---
    """
    result = MarketingModel()
    return schema.MarketingSchema().dump(result), 200


@marketing_bp.route('/segments/count', methods=['GET'])
@swag_from({
    "parameters": [
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'list all segments',
            'schema': schema.SegmentCountSchema
        }
    }
})
def segment_runs_count():
    """
    get count of segment runs
    ---
    """
    result = MarketingModel()
    result.get_number_of_segment_runs()
    return schema.SegmentCountSchema().dump(result), 200


@marketing_bp.route('/segments', methods=['GET'])
@swag_from({
    "summary": "get all data sources",
    "parameters": [],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get all data sources',
            'schema': schema.MarketingSchema
        }
    }
})
def get_all_segments():
    """
    get all segment runs
    ---
    """
    result = MarketingModel()
    segments = result.get_all_segment_runs()
    return json.dumps(segments), 200


@marketing_bp.route('/segments', methods=['POST'])
@swag_from({
    "parameters": [
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'create new segment',
            'schema': schema.MarketingSchema
        }
    }
})
def segment_create():
    """
    creates a new segment
    ---
    """
    result = MarketingModel()
    segment = result.create_segment()
    return json.dumps(segment), 200


@marketing_bp.route('/segments/<segment_id>', methods=['GET'])
@swag_from({
    "parameters": [
        {
            "name": "segment_id",
            "in": "path",
            "type": "string",
            "required": "true",
            "description": "segment id",
            "default": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0"
        },
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'segment details',
            'schema': schema.MarketingSchema
        }
    }
})
def segment_run(segment_id):
    """
    get all segment runs
    ---
    """
    result = MarketingModel()
    segment_info = result.get_segment_run(segment_id)
    return json.dumps(segment_info), 200


@marketing_bp.route('/segments/<segment_id>/customers', methods=['GET'])
@swag_from({
    "parameters": [
        {
            "name": "segment_id",
            "in": "path",
            "type": "string",
            "required": "true",
            "description": "segment id",
            "default": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0"
        },
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'list all customers for a segment',
            'schema': schema.MarketingSchema,
        }
    }
})
def segment_run_customers(segment_id):
    """
    get all customers for a segment run
    ---
    """
    result = MarketingModel()
    customers = result.get_segment_customers(segment_id)
    return json.dumps(customers), 200


@marketing_bp.route('/segments', methods=['PUT'])
@swag_from({
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": "true",
            "schema": {
                "id": "updateSegment",
                "example":
                    {
                        "TransactionID": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
                        "Scales": {
                            "Propensity": {
                                "Segments": {
                                    "0.0-0.2": "Unlikely",
                                    "0.21-0.5": "Likely",
                                    "0.51-0.8": "Most likely",
                                    "0.81-1.0": "Very likely"
                                },
                                "Values": {
                                    "Min": "0.0",
                                    "Max": "1.0"
                                }
                            }
                        },
                    }
            },
        },
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'update a specific segment',
            'schema': schema.MarketingSchema
        }
    }
})
def segment_update():
    """
    updates an existing segment
    ---
    """
    segment = request.json
    result = MarketingModel()
    result = result.update_segment(segment)
    return json.dumps(result), 200


@marketing_bp.route('/models/<category>', methods=['POST'])
@swag_from({
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": "true",
            "schema": {
                "id": "getModels",
                "example":
                    {
                        "Category": "Audience/ Marketing/ Commerce"
                    }
            },
        },
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'list all models',
            'schema': schema.ModelSchema
        }
    }
})
def fetch_models(category):
    """
    get all models
    ---
    """
    result = MarketingModel()
    result.get_models(category)
    return schema.ModelSchema().dump(result), 200


@marketing_bp.route('/segmentation', methods=['POST'])
@swag_from({
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": "true",
            "schema": {
                "id": "segments",
                "required": [
                    "s3_url",
                    "models"
                ],
                "example":
                {
                   "url": "s3://XXXXXXXX/customers.csv",
                   "models": [
                      "Churn",
                      "Propensity"
                   ]
                },
            },
        },
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Fetch Scores API helps you retrieve the the result values for the customers from the '
                           'machine learning models chosen, the output further can be utilized to categorize in one '
                           'or many segments. The campaigning strategy can be defined and executed as next steps.',
            'schema': schema.SegmentSchema
        }
    }
})
def fetch_scores():
    """
    get all scores
    ---
    """
    s3_url = request.json['url']
    models = request.json['models']
    result = MarketingModel()
    result.get_scores(s3_url, models)
    return schema.SegmentSchema().dump(result), 200


@marketing_bp.route('/segmentation/fly', methods=['POST'])
@swag_from({
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": "true",
            "example": {
               "TransactionID": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
               "Scales": {
                  "Propensity": {
                        "Segments": {
                           "0.0-0.2": "Unlikely",
                           "0.21-0.5": "Likely",
                           "0.51-0.8": "Most likely",
                           "0.81-1.0": "Very likely"
                        },
                        "Values": {
                           "Min": "0.0",
                           "Max": "1.0"
                        }
                  }
               },
               "Rules": [
                  {
                        "Rule": [
                           {
                              "Transaction": {
                                    "all": [
                                       {
                                          "all": [
                                                {
                                                   "fact": "Propensity",
                                                   "operator": "greaterThanInclusive",
                                                   "value": 0.6
                                                },
                                                {
                                                   "fact": "Propensity",
                                                   "operator": "lessThanInclusive",
                                                   "value": 1
                                                }
                                          ]
                                       }
                                    ]
                              }
                           },
                           {
                              "Values": {
                                    "Segment": "Most Likely"
                              }
                           }
                        ]
                  }
               ]
            },
        },
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': """Segmentation on the fly API helps you apply the group of segments with the defined
             criteria, this API will segregate each customer into the segment as per the criteria defined. This 
             output is the key input to execute the campaign workflow with the help of Orchestration tools.""",
            'schema': schema.SegmentFlySchema
        }
    }
})
def fetch_scores_on_the_fly():
    """
    get all scores
    ---
    """
    result = MarketingModel()
    result.get_scores_on_the_fly(request.json)
    return schema.SegmentFlySchema().dump(result), 200


@marketing_bp.route('/segmentation/deliver', methods=['POST'])
@swag_from({
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": "true",
            "schema": {
                "id": "segments_deliver",
                "required": [
                    "s3_url",
                    "models"
                ],
                "example":
                    {
                        "fileURL": "filepath",
                        "TransactionID": "ID",
                        "PredictionData": [
                            {
                                "User": "Customer1",
                                "Segment": "Likely"
                            },
                            {
                                "User": "Customer2",
                                "Segment": "Neutral"
                            },
                            {
                                "User": "Customer3",
                                "Segment": "Very likely"
                            }
                        ]
                    },
            },
        },
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': """This DeliverACS API will help you to deliver the segmented customers data(CSV format)
             to S3 location, the same file would be used by the custom ACS workflow to start the campaign.""",
             'schema': schema.SegmentDeliverSchema
        }
    }
})
def deliver_segments():
    """
    deliver segment
    ---
    """
    result = MarketingModel()
    result.deliver_segment(request.json)
    return schema.SegmentDeliverSchema().dump(result), 200