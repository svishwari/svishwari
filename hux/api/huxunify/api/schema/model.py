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
    bucket = Int()
    predicted_value = Float()
    actual_value = Float()
    profile_count = Int()
    predicted_rate = Float()
    actual_rate = Float()
    predicted_lift = Float()
    actual_lift = Float()
    profile_size_percent = Float()


class FeatureImportance(Schema):
    """Feature Importance Schema"""

    # TODO - Update as it becomes available.
    name = Str()
    description = Str()
    score = Float()


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


class ModelDashboardSchema(Schema):
    """Model Dashboard Schema"""

    model_type = Str()
    model_name = Str()
    description = Str()
    performance_metrics = Nested(PerformanceMetricSchema)
    feature_importance = List(Nested(FeatureImportance))
    lift_data = List(Nested(LiftSchema))
