"""Database client user management tests."""

import unittest
import mongomock
from bson import ObjectId
from hypothesis import given, strategies as st

import huxunifylib.database.user_management as um
import huxunifylib.database.orchestration_management as am
import huxunifylib.database.engagement_management as em
import huxunifylib.database.delivery_platform_management as dpm
import huxunifylib.database.constants as db_c
from huxunifylib.database import collection_management

from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.db_exceptions import (
    DuplicateName,
    DuplicateFieldType,
)


# pylint: disable=too-many-instance-attributes,too-many-public-methods
class TestUserManagement(unittest.TestCase):
    """Test user management module."""

    def setUp(self) -> None:
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # Connect
        self.database = DatabaseClient(host="localhost", port=27017).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        # user to be created
        self.sample_user = {
            db_c.OKTA_ID: "00ub0oNGTSWTBKOLGLNR",
            db_c.S_TYPE_EMAIL: "joe@deloitte.com",
            db_c.USER_ORGANIZATION: "deloitte",
            db_c.USER_DISPLAY_NAME: "joe smith",
            db_c.USER_ROLE: db_c.USER_ROLE_ADMIN,
            db_c.USER_PROFILE_PHOTO: "https://s3/unififed/3.png",
            db_c.USER_SUBSCRIPTION: [],
        }

        # set a user document
        self.user_doc = um.set_user(
            database=self.database,
            okta_id=self.sample_user[db_c.OKTA_ID],
            email_address=self.sample_user[db_c.S_TYPE_EMAIL],
            role=self.sample_user[db_c.USER_ROLE],
            organization=self.sample_user[db_c.USER_ORGANIZATION],
            subscriptions=self.sample_user[db_c.USER_SUBSCRIPTION],
            display_name=self.sample_user[db_c.USER_DISPLAY_NAME],
            profile_photo=self.sample_user[db_c.USER_PROFILE_PHOTO],
        )

        self.auth_details_facebook = {
            "facebook_access_token": "path1",
            "facebook_app_secret": "path2",
            "facebook_app_id": "path3",
            "facebook_ad_account_id": "path4",
        }

        self.delivery_platform_doc = dpm.set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform for Facebook",
            self.auth_details_facebook,
        )

        self.audience = am.create_audience(
            self.database,
            "Test Audience",
            [],
            self.sample_user.get(db_c.USER_DISPLAY_NAME),
        )
        self.lookalike_audience_doc = (
            dpm.create_delivery_platform_lookalike_audience(
                self.database,
                self.delivery_platform_doc[db_c.ID],
                self.audience,
                "Lookalike audience",
                0.01,
                "US",
                "Kam Chancellor",
                31,
            )
        )

        # setting id to set engagement
        self.audience[db_c.OBJECT_ID] = self.audience[db_c.ID]

        self.engagement_id = em.set_engagement(
            self.database,
            "Engagement",
            "Engagement Description",
            [self.audience],
            "user1",
        )
        self.component_ids = {
            db_c.ENGAGEMENTS: self.engagement_id,
            db_c.AUDIENCES: self.audience[db_c.OBJECT_ID],
            db_c.LOOKALIKE: self.lookalike_audience_doc[db_c.ID],
        }

    def test_set_user(self) -> None:
        """Test set_user routine."""

        # set a user document, use a duplicate okta id
        user_doc = um.set_user(
            database=self.database,
            okta_id="hf7hr43f7hfr7h7",
            email_address="dave@deloitte.com",
            role=self.sample_user[db_c.USER_ROLE],
            organization=self.sample_user[db_c.USER_ORGANIZATION],
            subscriptions=self.sample_user[db_c.USER_SUBSCRIPTION],
            display_name=self.sample_user[db_c.USER_DISPLAY_NAME],
            profile_photo=self.sample_user[db_c.USER_PROFILE_PHOTO],
        )

        self.assertIsNotNone(user_doc)

    def test_duplicate_set_user(self) -> None:
        """Test duplicate set_user routine based on okta id."""

        # set a user document, use a different okta id and email
        um.set_user(
            database=self.database,
            okta_id="hf7hr43f7hfr7h7",
            email_address="dave@deloitte.com",
            role=self.sample_user[db_c.USER_ROLE],
            organization=self.sample_user[db_c.USER_ORGANIZATION],
            subscriptions=self.sample_user[db_c.USER_SUBSCRIPTION],
            display_name=self.sample_user[db_c.USER_DISPLAY_NAME],
            profile_photo=self.sample_user[db_c.USER_PROFILE_PHOTO],
        )

        with self.assertRaises(DuplicateName):
            um.set_user(
                database=self.database,
                okta_id="hf7hr43f7hfr7h7",
                email_address="joesmith@deloitte.com",
                role=self.sample_user[db_c.USER_ROLE],
                organization=self.sample_user[db_c.USER_ORGANIZATION],
                subscriptions=self.sample_user[db_c.USER_SUBSCRIPTION],
                display_name=self.sample_user[db_c.USER_DISPLAY_NAME],
                profile_photo=self.sample_user[db_c.USER_PROFILE_PHOTO],
            )

    def test_get_user(self) -> None:
        """Test get_user routine."""

        user_doc = um.get_user(self.database, self.user_doc[db_c.OKTA_ID])

        self.assertIsNotNone(user_doc)
        self.assertEqual(
            user_doc[db_c.USER_DISPLAY_NAME],
            self.user_doc[db_c.USER_DISPLAY_NAME],
        )

    def test_get_users(self) -> None:
        """Test get all users function."""

        user_docs = um.get_all_users(database=self.database)

        self.assertIsNotNone(user_docs)

    def test_get_users_filter_and_projection(self) -> None:
        """Test get all users function with filter and projection."""

        # pylint: disable=too-many-function-args
        user_docs = um.get_all_users(
            database=self.database,
            filter_dict={
                db_c.USER_DISPLAY_NAME: self.user_doc[db_c.USER_DISPLAY_NAME]
            },
            project_dict={
                db_c.OKTA_ID: 1,
                db_c.USER_DISPLAY_NAME: 1,
            },
        )

        self.assertTrue(user_docs)
        # check length of one
        self.assertEqual(1, len(user_docs))
        self.assertEqual(
            self.user_doc[db_c.USER_DISPLAY_NAME],
            user_docs[0][db_c.USER_DISPLAY_NAME],
        )
        for project_field in user_docs[0].keys():
            self.assertIn(
                project_field, [db_c.ID, db_c.OKTA_ID, db_c.USER_DISPLAY_NAME]
            )

    @given(login_count=st.integers(min_value=0, max_value=9))
    def test_update_user_success(self, login_count: int) -> None:
        """Test update_user routine success.

        Args:
            login_count (int): login_count value to be updated in the user
                record.
        """

        # set update_doc dict to update the user_doc
        update_doc = {db_c.USER_LOGIN_COUNT: login_count + 1}
        user_doc = um.update_user(
            self.database, self.user_doc[db_c.OKTA_ID], update_doc
        )

        self.assertIsNotNone(user_doc)
        self.assertIn(db_c.USER_LOGIN_COUNT, user_doc)
        self.assertEqual(login_count + 1, user_doc[db_c.USER_LOGIN_COUNT])

    def test_update_all_users(self) -> None:
        """Test update_all_users.

        Args:

        """

        # set update_doc dict to update the user_doc\
        um.update_all_users(
            database=self.database, update_doc={db_c.SEEN_NOTIFICATIONS: True}
        )

        for user in um.get_all_users(database=self.database):
            self.assertTrue(user.get(db_c.SEEN_NOTIFICATIONS))

    def test_update_user_failure_disallowed_field(self) -> None:
        """Test update_user routine failure with disallowed field."""

        # set update_doc dict to update the user_doc
        update_doc = {db_c.OKTA_ID: "jd63bsfd884bdsff7348"}

        with self.assertRaises(DuplicateFieldType):
            um.update_user(
                self.database, self.user_doc[db_c.OKTA_ID], update_doc
            )

    def test_delete_user(self) -> None:
        """Test delete_user routine."""

        # create a user first
        user_doc = um.set_user(
            database=self.database,
            okta_id="hgf7hf8hdfgh7",
            email_address="russellw@deloitte.com",
            role=self.sample_user[db_c.USER_ROLE],
            organization=self.sample_user[db_c.USER_ORGANIZATION],
            subscriptions=self.sample_user[db_c.USER_SUBSCRIPTION],
            display_name=self.sample_user[db_c.USER_DISPLAY_NAME],
            profile_photo=self.sample_user[db_c.USER_PROFILE_PHOTO],
        )
        # validate user was created
        self.assertTrue(db_c.ID in user_doc)

        # remove the user
        success_flag = um.delete_user(self.database, user_doc[db_c.OKTA_ID])
        self.assertTrue(success_flag)

        # ensure user does not exist anymore
        user_doc = um.get_user(self.database, user_doc[db_c.OKTA_ID])
        self.assertIsNone(user_doc)

    def test_add_favorite(self) -> None:
        """Test function for adding manage_user_favorites routine."""

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[db_c.OKTA_ID])

        # test each component
        for component in db_c.FAVORITE_COMPONENTS:
            component_id = self.component_ids[component]

            # add favorite component
            update_doc = um.manage_user_favorites(
                self.database, user_doc[db_c.OKTA_ID], component, component_id
            )

            # test non empty list first
            self.assertTrue(update_doc[db_c.USER_FAVORITES][component])

            # test to ensure the ID we added exists
            self.assertTrue(
                component_id in update_doc[db_c.USER_FAVORITES][component]
            )

    def test_delete_favorite(self) -> None:
        """Test function for deleting via manage_user_favorites routine"""

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[db_c.OKTA_ID])

        # test all the components
        for component in db_c.FAVORITE_COMPONENTS:
            component_id = self.component_ids[component]

            # add favorite component
            um.manage_user_favorites(
                self.database, user_doc[db_c.OKTA_ID], component, component_id
            )

            # now remove the favorite
            removed_doc = um.manage_user_favorites(
                self.database,
                user_doc[db_c.OKTA_ID],
                component,
                component_id,
                delete_flag=True,
            )

            # test empty list first
            self.assertFalse(removed_doc[db_c.USER_FAVORITES][component])

    def test_duplicate_add_favorite(self) -> None:
        """Test function for duplicate adding manage_user_favorites routine."""

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[db_c.OKTA_ID])

        # test all the components
        for component in db_c.FAVORITE_COMPONENTS:
            component_id = self.component_ids[component]

            # add favorite component x2
            for _ in range(2):
                um.manage_user_favorites(
                    self.database,
                    user_doc[db_c.OKTA_ID],
                    component,
                    component_id,
                )

            # get user doc
            update_doc = um.get_user(self.database, user_doc[db_c.OKTA_ID])

            # test non empty list first
            self.assertTrue(update_doc[db_c.USER_FAVORITES][component])

            # test to ensure the ID we added exists
            self.assertTrue(
                component_id in update_doc[db_c.USER_FAVORITES][component]
            )

            # test to ensure the ID we added exists, only once!
            self.assertEqual(
                update_doc[db_c.USER_FAVORITES][component].count(component_id),
                1,
            )

    def test_set_dashboard_config(self) -> None:
        """Test function for manage_user_dashboard_config routine."""

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[db_c.OKTA_ID])

        # simulate a dashboard config
        pinned_key = "pin_key_perf_insights"
        pinned_value = True

        # set the config setting for a user
        updated_doc = um.manage_user_dashboard_config(
            self.database, user_doc[db_c.OKTA_ID], pinned_key, pinned_value
        )

        # test pinned value key exists
        self.assertIn(
            pinned_key, updated_doc[db_c.USER_DASHBOARD_CONFIGURATION]
        )

        # test pinned value is set correctly
        self.assertEqual(
            updated_doc[db_c.USER_DASHBOARD_CONFIGURATION][pinned_key],
            pinned_value,
        )

    def test_unset_dashboard_config(self) -> None:
        """Test delete_flag for manage_user_dashboard_config routine."""

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[db_c.OKTA_ID])

        # simulate a dashboard config
        pinned_key = "pin_customer_insights"
        pinned_value = True

        # set the config setting for a user first
        user_doc = um.manage_user_dashboard_config(
            self.database, user_doc[db_c.OKTA_ID], pinned_key, pinned_value
        )

        # test pinned value key exists
        self.assertIn(pinned_key, user_doc[db_c.USER_DASHBOARD_CONFIGURATION])

        # test pinned value is set correctly
        self.assertEqual(
            user_doc[db_c.USER_DASHBOARD_CONFIGURATION][pinned_key],
            pinned_value,
        )

        # delete the config setting for a user
        updated_doc = um.manage_user_dashboard_config(
            self.database,
            user_doc[db_c.OKTA_ID],
            pinned_key,
            None,
            delete_flag=True,
        )

        # test pinned value key does not exist
        self.assertNotIn(
            pinned_key, updated_doc[db_c.USER_DASHBOARD_CONFIGURATION]
        )

    def test_add_applications_to_users(self):
        """Test add user applications"""
        application_id = ObjectId()
        url = "https://www.test1.com"

        updated_user_doc = um.add_applications_to_users(
            database=self.database,
            okta_id=self.user_doc[db_c.OKTA_ID],
            application_id=application_id,
            url=url,
        )
        self.assertTrue(updated_user_doc)
        self.assertEqual(
            url,
            updated_user_doc.get(db_c.USER_APPLICATIONS, [{}])[0].get(
                db_c.URL
            ),
        )
        self.assertEqual(
            application_id,
            updated_user_doc.get(db_c.USER_APPLICATIONS, [{}])[0].get(
                db_c.OBJECT_ID
            ),
        )

    def test_update_user_applications(self):
        """Test update user applications"""
        application_id = ObjectId()
        updated_url = "https://www.test2.com"

        um.add_applications_to_users(
            database=self.database,
            okta_id=self.user_doc[db_c.OKTA_ID],
            application_id=application_id,
            url="https://www.test1.com",
        )
        updated_user_doc = um.update_user_applications(
            database=self.database,
            okta_id=self.user_doc[db_c.OKTA_ID],
            application_id=application_id,
            url=updated_url,
        )

        self.assertTrue(updated_user_doc)
        self.assertEqual(
            updated_url,
            updated_user_doc.get(db_c.USER_APPLICATIONS, [{}])[0].get(
                db_c.URL
            ),
        )
        self.assertEqual(
            application_id,
            updated_user_doc.get(db_c.USER_APPLICATIONS, [{}])[0].get(
                db_c.OBJECT_ID
            ),
        )

    def test_get_user_applications(self):
        """Test for get user applications."""

        # Create an application.
        new_application = {
            db_c.CATEGORY: "Uncategorized",
            db_c.NAME: "Custom",
            db_c.ENABLED: True,
        }

        application = collection_management.create_document(
            database=self.database,
            collection=db_c.APPLICATIONS_COLLECTION,
            new_doc=new_application,
            username=self.user_doc[db_c.USER_DISPLAY_NAME],
        )

        # Add the application to the user.
        um.add_applications_to_users(
            database=self.database,
            okta_id=self.user_doc[db_c.OKTA_ID],
            application_id=application.get(db_c.ID),
            url="https://www.test1.com",
        )

        user_applications = um.get_user_applications(
            database=self.database, okta_id=self.user_doc[db_c.OKTA_ID]
        )

        self.assertIsInstance(user_applications, list)
        self.assertEqual(
            new_application[db_c.CATEGORY],
            user_applications[0].get(db_c.CATEGORY),
        )
        self.assertEqual(
            new_application[db_c.NAME], user_applications[0].get(db_c.NAME)
        )
        self.assertTrue(user_applications[0].get("is_added"))

    def test_soft_delete_user_applications(self):
        """Test soft delete user applications"""

        application_id = ObjectId()

        um.add_applications_to_users(
            database=self.database,
            okta_id=self.user_doc[db_c.OKTA_ID],
            application_id=application_id,
            url="https://www.test1.com",
        )

        # Soft Delete.
        um.update_user_applications(
            database=self.database,
            okta_id=self.user_doc[db_c.OKTA_ID],
            application_id=application_id,
            is_added=False,
        )

        user_applications = um.get_user_applications(
            database=self.database, okta_id=self.user_doc[db_c.OKTA_ID]
        )

        # Ensure user applications are empty.
        self.assertFalse(user_applications)

    def test_add_user_trust_id_segments(self):
        """Test add trust id segment to user"""
        segment = {"segment_name": "Test Segment", "segment_filters": []}

        updated_user_doc = um.add_user_trust_id_segments(
            database=self.database,
            okta_id=self.user_doc[db_c.OKTA_ID],
            segment=segment,
        )
        self.assertTrue(updated_user_doc)
        self.assertIn(segment, updated_user_doc[db_c.TRUST_ID_SEGMENTS])

    def test_remove_user_trust_id_segments(self):
        """Test remove trust id segment to user"""
        segment = {"segment_name": "Test Segment", "segment_filters": []}

        updated_user_doc = um.add_user_trust_id_segments(
            database=self.database,
            okta_id=self.user_doc[db_c.OKTA_ID],
            segment=segment,
        )
        self.assertTrue(updated_user_doc)
        self.assertIn(segment, updated_user_doc[db_c.TRUST_ID_SEGMENTS])

        updated_user_doc = um.remove_user_trust_id_segments(
            database=self.database,
            okta_id=self.user_doc[db_c.OKTA_ID],
            segment_name=segment["segment_name"],
        )
        self.assertTrue(updated_user_doc)
        self.assertNotIn(segment, updated_user_doc[db_c.TRUST_ID_SEGMENTS])

    def test_get_user_trust_id_segments(self):
        """Test fetch trust id segments"""
        segment = {"segment_name": "Test Segment", "segment_filters": []}

        updated_user_doc = um.add_user_trust_id_segments(
            database=self.database,
            okta_id=self.user_doc[db_c.OKTA_ID],
            segment=segment,
        )
        self.assertTrue(updated_user_doc)

        trust_id_segments = um.get_user_trust_id_segments(
            database=self.database, okta_id=self.user_doc[db_c.OKTA_ID]
        )

        self.assertTrue(trust_id_segments)
        self.assertEqual([segment], trust_id_segments)
