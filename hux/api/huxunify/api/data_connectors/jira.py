"""Purpose of this file is for holding methods to query and push data to JIRA
"""
from typing import Tuple

from jira import JIRA, JIRAError

from huxunifylib.util.general.logging import logger

from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.exceptions.integration_api_exceptions import (
    FailedAPIDependencyError,
)
from huxunify.api.prometheus import record_health_status_metric


class JiraConnection:
    """JIRA Connection class"""

    def __init__(self):
        """Initialize Jira Connection"""
        config = get_config()

        # get JIRA client
        self.jira_client = JIRA(
            server=config.JIRA_SERVER,
            options={
                "headers": {
                    **JIRA.DEFAULT_OPTIONS["headers"],
                    api_c.AUTHORIZATION: f"Bearer {config.JIRA_API_KEY}",
                }
            },
        )
        self.project_key = config.JIRA_PROJECT_KEY

    @staticmethod
    def check_jira_connection() -> Tuple[bool, str]:
        """Validates JIRA connection.

        Returns:
            Tuple[bool, str]: Flag if connection is valid and message.
        """
        config = get_config()
        try:
            JIRA(
                server=config.JIRA_SERVER,
                validate=True,
                options={
                    "headers": {
                        **JIRA.DEFAULT_OPTIONS["headers"],
                        api_c.AUTHORIZATION: f"Bearer {config.JIRA_API_KEY}",
                    }
                },
            )
            record_health_status_metric(api_c.JIRA_CONNECTION_HEALTH, 200)
            return True, "Jira available"

        except JIRAError as jira_error:
            logger.error(
                "Encountered Error: %s while connecting to JIRA and %s Status "
                "code.",
                jira_error.text,
                jira_error.status_code,
            )
            record_health_status_metric(api_c.JIRA_CONNECTION_HEALTH, False)
            return False, jira_error.text

        except AttributeError as attribute_error:
            logger.error(
                "Could not connect to JIRA %s",
                getattr(attribute_error, "message", repr(attribute_error)),
            )
            record_health_status_metric(api_c.JIRA_CONNECTION_HEALTH, False)
            return (
                False,
                getattr(attribute_error, "message", repr(attribute_error)),
            )

        except Exception as exception:  # pylint: disable=broad-except
            logger.error(
                "Could not connect to JIRA %s",
                getattr(exception, "message", repr(exception)),
            )
            record_health_status_metric(api_c.JIRA_CONNECTION_HEALTH, False)
            return False, getattr(exception, "message", repr(exception))

    def create_jira_issue(
        self, issue_type: str, summary: str, description: str
    ):
        """Create a new issue in JIRA

        Args:
            issue_type (str): Type of issue
            summary (str): Summary of issue
            description (str): Description of issue

        Returns:
            dict: Object of new issue created

        Raises:
            FailedAPIDependencyError: Any exception raised during endpoint execution.
        """

        try:
            new_issue = self.jira_client.create_issue(
                {
                    "project": {api_c.KEY: self.project_key},
                    "components": [{api_c.NAME: self.project_key}],
                    "issuetype": {api_c.NAME: issue_type},
                    "summary": summary,
                    "description": description,
                },
                False,
            )
        except JIRAError as jira_error:
            raise FailedAPIDependencyError(
                "Failed to connect to JIRA.",
                jira_error.status_code,
            ) from jira_error

        return {
            api_c.ID: new_issue.id,
            api_c.KEY: new_issue.key,
            api_c.TYPE: issue_type,
            api_c.SUMMARY: summary,
            api_c.DESCRIPTION: description,
        }
