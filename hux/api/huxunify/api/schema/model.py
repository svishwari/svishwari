"""
Schemas for the Model Object
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, Float, DateTime, Nested, List


class ModelSchema(Schema):
    """Model Schema"""

    id = Int()
    name = Str(required=True)
    description = Str()
    status = Str()
    latest_version = Str()
    past_version_count = Int()
    last_trained = DateTime()
    owner = Str()
    lookback_window = Int()
    prediction_window = Int()
    fulcrum_date = DateTime()
    type = Str()


class ModelVersionSchema(Schema):
    """Model Version Schema"""

    name = Str(required=True)
    description = Str()
    status = Str()
    trained_date = DateTime()
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
    run_date = DateTime()


class PerformanceMetricSchema(Schema):
    """Performance Metric Schema"""

    # TODO - Update as it becomes available.
    rmse = Float()
    auc = Float()
    precision = Float()
    recall = Float()
    current_version = Str()


class ModelDashboardSchema(Schema):
    """Model Dashboard Schema"""

    model_type = Str()
    model_name = Str()
    description = Str()
    performance_metric = Nested(PerformanceMetricSchema)
    feature_importance = List(Nested(FeatureImportance))
    lift_data = List(Nested(LiftSchema))
