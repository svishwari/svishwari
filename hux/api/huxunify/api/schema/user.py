"""Schemas for the User API"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, validate, List, Nested, Dict, Bool
from marshmallow.validate import OneOf

from huxunifylib.database import constants as db_c
from huxunify.api.schema.utils import validate_object_id
from huxunify.api.schema.custom_schemas import DateTimeWithZ
from huxunify.api import constants as api_c


class Favorites(Schema):
    """Favorites Schema"""

    campaigns = List(Str(), default=[])
    audiences = List(Str(), default=[])
    destinations = List(Str(), default=[])
    engagements = List(Str(), default=[])


class UserPatchSchema(Schema):
    """User patch schema"""

    id = Str(validate=validate_object_id)
    role = Str(required=False)
    display_name = Str(required=False)
    dashboard_configuration = Dict(required=False)
    pii_access = Bool(required=False)


class TicketSchema(Schema):
    """Ticket schema"""

    issue_type = Str(required=True, validate=OneOf([api_c.TICKET_TYPE_BUG]))
    summary = Str(required=True)
    description = Str(required=False)


class TicketGetSchema(Schema):
    """Ticket get schema"""

    id = Int(example=1)
    key = Str(example="ABC-123")
    issue_type = Str(required=False, example=api_c.TICKET_TYPE_BUG)
    summary = Str(example="Summary of the issue")
    description = Str(required=False, example="Description of the issue.")
    status = Str(required=False, example="To Do")
    create_time = DateTimeWithZ(
        attribute="created",
        required=False,
        example="2021-08-05T14:44:42.694Z",
    )


class NewUserRequest(Schema):
    """New User Request Schema"""

    first_name = Str(required=True, example="Sarah")
    last_name = Str(required=True, example="Huxley")
    email = Str(required=True)
    access_level = Str(required=True, validate=validate.OneOf(db_c.USER_ROLES))
    pii_access = Bool(required=True, default=False)
    reason_for_request = Str(required=True)


class UserAlertSchema(Schema):
    """User alert schema"""

    class Meta:
        """Meta class to handle ordering of schema"""

        ordered = True

    critical = Bool(default=False, load_default=False)
    success = Bool(default=False, load_default=False)
    informational = Bool(default=False, load_default=False)


class UserAlertDataManagementSchema(Schema):
    """User alert data management schema"""

    class Meta:
        """Meta class to handle ordering of schema"""

        ordered = True

    data_sources = Nested(UserAlertSchema, required=False)


class UserAlertDecisioningSchema(Schema):
    """User alert decisioning schema"""

    class Meta:
        """Meta class to handle ordering of schema"""

        ordered = True

    models = Nested(UserAlertSchema, required=False)


class UserAlertOrchestrationSchema(Schema):
    """User alert orchestration schema"""

    class Meta:
        """Meta class to handle ordering of schema"""

        ordered = True

    destinations = Nested(UserAlertSchema, required=False)
    delivery = Nested(UserAlertSchema, required=False)
    audiences = Nested(UserAlertSchema, required=False)
    engagements = Nested(UserAlertSchema, required=False)


class UserAlertCategorySchema(Schema):
    """User alert category schema"""

    class Meta:
        """Meta class to handle ordering of schema"""

        ordered = True

    data_management = Nested(UserAlertDataManagementSchema)
    decisioning = Nested(UserAlertDecisioningSchema)
    orchestration = Nested(UserAlertOrchestrationSchema)


class UserPreferencesSchema(Schema):
    """User preferences schema"""

    alerts = Nested(UserAlertCategorySchema)


class UserSchema(Schema):
    """User Schema"""

    _id = Str(
        data_key=api_c.ID,
        example="5f5f7262997acad4bac4373b",
        required=True,
        validate=validate_object_id,
    )
    email = Str(required=True, attribute=api_c.USER_EMAIL_ADDRESS)
    display_name = Str(example="Joe M")
    first_name = Str()
    last_name = Str()
    phone_number = Str()
    access_level = Str()
    role = Str(required=True, validate=validate.OneOf(db_c.USER_ROLES))
    pii_access = Bool(default=False)
    organization = Str()
    subscriptions = List(Str())
    dashboard_configuration = Dict()
    favorites = Nested(Favorites, required=True)
    profile_photo = Str()
    login_count = Int(required=True, default=0, example=10)
    last_login = DateTimeWithZ(required=True, attribute=db_c.UPDATE_TIME)
    modified = DateTimeWithZ(required=True)
    alerts = Nested(UserAlertCategorySchema)


class RequestedUserSchema(Schema):
    """Requested User Schema"""

    email = Str(required=True, exmaple="sh@fake.com")
    pii_access = Bool(default=False)
    display_name = Str(example="Sarah, Huxley")
    access_level = Str(default=db_c.USER_ROLE_VIEWER)
    status = Str(
        required=True,
        validate=validate.OneOf(
            [
                api_c.STATE_TO_DO,
                api_c.STATE_IN_PROGRESS,
                api_c.STATE_IN_REVIEW,
                api_c.STATE_DONE,
            ]
        ),
    )
    created = DateTimeWithZ(required=True)
    updated = DateTimeWithZ(required=True)
    key = Str(example="ABC-123", required=True)
