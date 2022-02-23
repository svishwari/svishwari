"""Module for loading users to test database"""
from huxunifylib.database import constants as db_c
from huxunifylib.database.client import DatabaseClient

from huxunifylib.database.user_management import set_user


def load_users(database: DatabaseClient) -> None:
    """Load users into the test database

    Args:
        database: database instance to load data into

    Returns:
        None
    """

    users = [
        {
            db_c.OKTA_ID: "00u7acrr5pEmJ09lc2p7",
            db_c.S_TYPE_EMAIL: "user1_admin@deloitte.com",
            db_c.USER_ROLE: db_c.USER_ROLE_ADMIN,
            db_c.USER_ORGANIZATION: "Deloitte",
            db_c.USER_SUBSCRIPTION: [],
            db_c.USER_DISPLAY_NAME: "USER 1",
            db_c.USER_PROFILE_PHOTO: "",
            db_c.USER_PII_ACCESS: True,
        },
        {
            db_c.OKTA_ID: "00u7acrr5pEmA32lc2p8",
            db_c.S_TYPE_EMAIL: "user2_editor@deloitte.com",
            db_c.USER_ROLE: db_c.USER_ROLE_EDITOR,
            db_c.USER_ORGANIZATION: "Deloitte",
            db_c.USER_SUBSCRIPTION: [],
            db_c.USER_DISPLAY_NAME: "USER 2",
            db_c.USER_PROFILE_PHOTO: "",
            db_c.USER_PII_ACCESS: False,
        },
        {
            db_c.OKTA_ID: "00u7acrr5pEmJ78lc2p9",
            db_c.S_TYPE_EMAIL: "user1_editor@deloitte.com",
            db_c.USER_ROLE: db_c.USER_ROLE_VIEWER,
            db_c.USER_ORGANIZATION: "Deloitte",
            db_c.USER_SUBSCRIPTION: [],
            db_c.USER_DISPLAY_NAME: "USER 3",
            db_c.USER_PROFILE_PHOTO: "",
            db_c.USER_PII_ACCESS: True,
        },
    ]

    for user in users:
        set_user(
            database,
            okta_id=user[db_c.OKTA_ID],
            email_address=user[db_c.S_TYPE_EMAIL],
            role=user[db_c.USER_ROLE],
            organization=user[db_c.USER_ORGANIZATION],
            subscriptions=user[db_c.USER_SUBSCRIPTION],
            display_name=user[db_c.USER_DISPLAY_NAME],
            profile_photo=user[db_c.USER_PROFILE_PHOTO],
            pii_access=user[db_c.USER_PII_ACCESS],
        )
