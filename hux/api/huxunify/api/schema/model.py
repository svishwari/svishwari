"""
Schemas for the Model Object
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, Float, Nested

from huxunify.api.schema.custom_schemas import DateTimeWithZ


class ModelSchema(Schema):
    """Model Schema"""

    id = Int()
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

    name = Str(required=True)
    description = Str()
    status = Str()
    trained_date = DateTimeWithZ()
    version = Str()


class FeatureSchema(Schema):
    """Feature Schema"""

    # TODO - Update as it becomes available.
    name = Str(required=True)
    feature_service = Str()
    data_source = Str()
    status = Str()
    popularity = Int()
    owner = Str()


class LiftSchema(Schema):
    """Lift Schema"""

    # TODO - Update as it becomes available.
    bucket = Int(example=10)
    predicted_value = Float(example=693.69)
    actual_value = Float(example=797.81)
    profile_count = Int(example=22)
    predicted_rate = Float(example=0.31)
    actual_rate = Float(example=0.29)
    predicted_lift = Float(example=1.03)
    actual_lift = Float(example=1.53)
    profile_size_percent = Float(example=97.16)


class FeatureImportance(Schema):
    """Feature Importance Schema"""

    # TODO - Update as it becomes available.
    name = Str(example="Feature Name")
    description = Str(example="Description of Feature ")
    score = Float(example=0.20)


class DriftSchema(Schema):
    """Drift Schema"""

    # TODO - Update as it becomes available.
    drift = Float()
    run_date = DateTimeWithZ()


class PerformanceMetricSchema(Schema):
    """Performance Metric Schema"""

    # TODO - Update as it becomes available.
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
    feature_importance = Nested(FeatureImportance, many=True)
    lift_data = Nested(LiftSchema, many=True)
