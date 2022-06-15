"""Schemas for the Model Object."""
import re
from flask_marshmallow import Schema
from marshmallow import post_dump
from marshmallow.fields import Str, Int, Float, Nested, Bool, List

from huxunifylib.database import constants as db_c
from huxunify.api.schema.custom_schemas import DateTimeWithZ, RoundedFloat
from huxunify.api import constants as api_c


class ModelTagsSchema(Schema):
    """Model tags schema class"""

    industry = List(Str)


class ModelSchema(Schema):
    """Model Schema"""

    id = Str()
    name = Str(required=True)
    description = Str()
    status = Str()
    latest_version = Str()
    past_version_count = Int()
    last_trained = DateTimeWithZ(allow_none=True)
    owner = Str()
    lookback_window = Int()
    prediction_window = Int()
    fulcrum_date = DateTimeWithZ(allow_none=True)
    type = Str()
    category = Str()
    is_enabled = Bool(attribute=db_c.ENABLED, required=False)
    is_added = Bool(attribute=db_c.ADDED, required=False)
    tags = Nested(ModelTagsSchema, required=False)

    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    @post_dump
    def post_serialize(self, model: dict, many: bool = False) -> dict:
        """Process the schema before serializing.

        Args:
            model (dict): The model object.
            many (bool): If there are many to process.

        Returns:
            dict: Returns model object.
        """

        replaced_dict = replace_customer_in_model_data(
            model.get(api_c.NAME), model.get(api_c.DESCRIPTION)
        )

        model[api_c.NAME] = replaced_dict.get(
            api_c.NAME, model.get(api_c.NAME)
        )
        model[api_c.DESCRIPTION] = replaced_dict.get(
            api_c.DESCRIPTION, model.get(api_c.DESCRIPTION)
        )

        return model


class ModelVersionSchema(Schema):
    """Model Version Schema"""

    id = Str()
    name = Str(required=True)
    description = Str()
    status = Str()
    version = Str(attribute=api_c.CURRENT_VERSION)
    trained_date = DateTimeWithZ(attribute=api_c.LAST_TRAINED)
    owner = Str()
    lookback_window = Int()
    prediction_window = Int()
    fulcrum_date = DateTimeWithZ()

    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    @post_dump
    def post_serialize(self, model: dict, many: bool = False) -> dict:
        """Process the schema before serializing.

        Args:
            model (dict): The model object.
            many (bool): If there are many to process.

        Returns:
            dict: Returns model object.
        """

        replaced_dict = replace_customer_in_model_data(
            model.get(api_c.NAME), model.get(api_c.DESCRIPTION)
        )

        model[api_c.NAME] = replaced_dict.get(
            api_c.NAME, model.get(api_c.NAME)
        )
        model[api_c.DESCRIPTION] = replaced_dict.get(
            api_c.DESCRIPTION, model.get(api_c.DESCRIPTION)
        )

        return model


class FeatureSchema(Schema):
    """Feature Schema"""

    id = Str()
    name = Str(required=True)
    description = Str(default="")
    feature_type = Str()
    records_not_null = Str()
    feature_importance = Int()
    mean = Float()
    min = Float()
    max = Float()
    unique_values = Int()
    lcuv = Str()
    mcuv = Str()
    score = RoundedFloat(default=None)


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


class ModelOverviewSchema(Schema):
    """Model Dashboard Schema"""

    model_type = Str()
    model_name = Str()
    description = Str()
    performance_metric = Nested(PerformanceMetricSchema)

    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    @post_dump
    def post_serialize(self, model: dict, many: bool = False) -> dict:
        """Process the schema before serializing.

        Args:
            model (dict): The model object.
            many (bool): If there are many to process.

        Returns:
            dict: Returns model object.
        """

        replaced_dict = replace_customer_in_model_data(
            model.get(api_c.MODEL_NAME), model.get(api_c.DESCRIPTION)
        )

        model[api_c.MODEL_NAME] = replaced_dict.get(
            api_c.NAME, model.get(api_c.MODEL_NAME)
        )
        model[api_c.DESCRIPTION] = replaced_dict.get(
            api_c.DESCRIPTION, model.get(api_c.DESCRIPTION)
        )

        return model


class ModelRequestPostSchema(Schema):
    """Model Request Post Schema"""

    id = Str(required=True)
    name = Str(required=True)
    type = Str(required=True)
    status = Str(
        validate=lambda x: x.lower() in [api_c.REQUESTED.lower()],
        required=True,
    )


class ModelPipelineRunDurationSchema(Schema):
    """Model Pipeline Run Duration Schema"""

    status = Str()
    timestamp = DateTimeWithZ()
    duration = Str()


class ModelPipelineRunDataSchema(Schema):
    """Model Pipeline Run Data Schema"""

    frequency = Str()
    last_run = DateTimeWithZ()
    most_recent_run_duration = Str()
    run_duration = List(Nested(ModelPipelineRunDurationSchema))
    total_runs = Int()


class ModelPipelinePerformanceSchema(Schema):
    """Model Pipeline Performance Schema"""

    training = Nested(ModelPipelineRunDataSchema)
    scoring = Nested(ModelPipelineRunDataSchema)


def replace_customer_in_model_data(
    model_name: str, model_description: str
) -> dict:
    """Function to replace the words "customer" and "customers" to "consumer"
    and "consumers" respectively regardless of case sensitivity in a model name
    and description.

    Args:
        model_name (str): The model name.
        model_description (str): The model description.

    Returns:
        dict: Returns the replaced model name and description as a dict.
    """

    # replace all occurrences of word "customer" to "consumer" in name and
    # description field regardless of case sensitiveness
    match_replacements = {"customer": "consumer", "Customer": "Consumer"}
    pattern_regex = re.compile("|".join(match_replacements.keys()))

    return_dict = {}

    if model_name:
        return_dict[api_c.NAME] = pattern_regex.sub(
            lambda x: match_replacements[x.group(0)], model_name
        )
    if model_description:
        return_dict[api_c.DESCRIPTION] = pattern_regex.sub(
            lambda x: match_replacements[x.group(0)], model_description
        )

    return return_dict
