"""
purpose of this script is for housing the decision routes for the API
"""
from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from
from api.model.decision import DecisionModel
from api.schema.decision import DecisionSchema

decision_bp = Blueprint('decision_bp', __name__)


@decision_bp.route('/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'decision api',
            'schema': DecisionSchema
        }
    }
})
def index():
    """
    decision api landing
    ---
    """
    result = DecisionModel()
    return DecisionSchema().dump(result), 200
