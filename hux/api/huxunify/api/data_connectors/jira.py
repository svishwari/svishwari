"""Purpose of this file is for holding methods to query and push data to JIRA
"""
from jira import JIRA, JIRAError
from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.exceptions.integration_api_exceptions import (
    FailedAPIDependencyError,
)


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

        self.jira_user_email = config.JIRA_USER_EMAIL

    def create_jira_issue(
        self, issue_type: str, summary: str, description: str
    ) -> dict:
        """Create a new issue in JIRA.

        Args:
            issue_type (str): Type of issue
            summary (str): Summary of issue
            description (str): Description of issue

        Returns:
            dict: Object of new issue created

        Raises:
            FailedAPIDependencyError: Any exception raised during endpoint
                execution.
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

    def search_jira_issues(
        self,
        jql_suffix: str,
        return_fields: list,
        order_by_field: str = None,
        sort_order: str = None,
    ) -> list:
        """Searches for issues in the configured project on Jira that matches
        jql_suffix in the ticket ordered by order_by_field and returns the
        return_fields.

        Args:
            jql_suffix (str): Suffix to append to the pre-cooked jql string.
            return_fields (list): List of fields that are to be returned.
            order_by_field (str): field based on which the results are to be
                ordered.
            sort_order (str): Order by value (ASC or DESC).

        Returns:
            list: List of matching issues returned via search api.

        Raises:
            FailedAPIDependencyError: Any exception raised during endpoint
                execution.
        """

        jql = f"project={self.project_key} AND reporter={self.jira_user_email} AND {jql_suffix}"
        if order_by_field:
            sort_order = sort_order if sort_order else "ASC"
            jql = f"{jql} ORDER BY {order_by_field} {sort_order}"

        try:
            matched_issues = self.jira_client.search_issues(
                jql_str=jql,
                json_result=True,
                fields=",".join(x for x in return_fields),
            )
        except JIRAError as jira_error:
            raise FailedAPIDependencyError(
                "Failed to connect to JIRA.",
                jira_error.status_code,
            ) from jira_error

        return matched_issues
