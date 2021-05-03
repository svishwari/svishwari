"""
Schemas for the Model Object
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, Float, DateTime


class ModelSchema(Schema):
    """Model Schema"""

    name = Str(required=True)
    description = Str()
    status = Str()
    latest_version = Str()
    past_version_count = Int()
    last_trained = DateTime()
    owner = Str()
    lookback_window = Str()
    prediction_window = Str()
    fulcrum_date = DateTime()


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
