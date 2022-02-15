"""Module for loading data sources to test database"""
from huxunifylib.database import constants as db_c
from huxunifylib.database.cdp_data_source_management import create_data_source
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.data.data_sources import DATA_SOURCES_LIST


def load_data_sources(database: DatabaseClient) -> None:
    """Loads data sources into the test database

    Args:
        database: database instance to load data into

    Returns:
        None
    """

    for data_source in DATA_SOURCES_LIST:
        create_data_source(
            database,
            name=data_source[db_c.DATA_SOURCE_NAME],
            source_type=data_source[db_c.DATA_SOURCE_TYPE],
            category=data_source[db_c.CATEGORY],
            status=data_source[db_c.STATUS],
            enabled=data_source[db_c.ENABLED],
            added=data_source[db_c.ADDED],
        )
