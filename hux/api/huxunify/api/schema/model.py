"""Schemas for the Model Object"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, Float, Nested
from marshmallow.validate import OneOf

from huxunify.api.schema.custom_schemas import DateTimeWithZ
from huxunify.api import constants as c


class ModelSchema(Schema):
    """Model Schema"""

    id = Str()
    name = Str(required=True)
    description = Str()
    status = Str()
    latest_version = Str()
    past_version_count = Int()
    last_trained = DateTimeWithZ()
    owner = Str()
    lookback_window = Int()
    prediction_window = Int()
    fulcrum_date = DateTimeWithZ()
    type = Str()


class ModelVersionSchema(Schema):
    """Model Version Schema"""

    id = Int()
    name = Str(required=True)
    description = Str()
    status = Str()
    version = Str(attribute=c.CURRENT_VERSION)
    trained_date = DateTimeWithZ(attribute=c.LAST_TRAINED)
    owner = Str()
    lookback_window = Int()
    prediction_window = Int()
    fulcrum_date = DateTimeWithZ()


class FeatureSchema(Schema):
    """Feature Schema"""

    id = Str()
    version = Str()
    feature_service = Str()
    data_source = Str()
    created_by = Str()
    description = Str(default="")
    name = Str(required=True)
    status = Str()
    score = Float()
    popularity = Int()


class ModelLiftSchema(Schema):
    """Lift Schema"""

    bucket = Int(example=10)
    predicted_value = Float(example=693.69)
    actual_value = Float(example=797.81)
    profile_count = Int(example=22)
    predicted_rate = Float(example=0.31)
    actual_rate = Float(example=0.29)
    predicted_lift = Float(example=1.03)
    actual_lift = Float(example=1.53)
    profile_size_percent = Float(example=1.16)


class ModelDriftSchema(Schema):
    """Drift Schema"""

    drift = Float(required=True)
    run_date = DateTimeWithZ(required=True)


class PerformanceMetricSchema(Schema):
    """Performance Metric Schema"""

    class Meta:
        """Meta class to handle ordering of schema"""

        ordered = True

    rmse = Float(example=350)
    auc = Float(example=0.79)
    precision = Float(example=0.82)
    recall = Float(example=0.65)
    current_version = Str(example="3.1.2")


class ModelDashboardSchema(Schema):
    """Model Dashboard Schema"""

    model_type = Str()
    model_name = Str()
    description = Str()
    performance_metric = Nested(PerformanceMetricSchema)


class ModelRequestPOSTSchema(Schema):
    """Model Request Post Schema"""

    id = Str(required=True)
    name = Str(required=True)
    status = Str(
        validate=[
            OneOf(
                choices=[
                    c.REQUESTED,
                ]
            )
        ],
        required=True,
    )
    type = Str(required=True)
