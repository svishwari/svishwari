"""
Models for the CDM API
"""
from typing import Union, List, Optional, Any
from snowflake.connector import DictCursor, SnowflakeConnection
from huxunify.api.data_connectors.snowflake_client import SnowflakeClient


# CDM DATABASE CONSTANTS - we can move these after
PROCESSED_DATABASE: str = "CDP_LTD"
ADMIN_DATABASE: str = "CDP_ADMIN"
SCHEMA: str = "CTRL"
PROCESSED_SCHEMA: str = "LTD"
INFORMATION_SCHEMA: str = "INFORMATION_SCHEMA"
TABLE_DATA_FEED_CATALOG: str = "DATA_FEED_CATALOG"
TABLE_PII_REQUIRED_FIELDS_LOOKUP: str = "PII_REQUIRED_FIELDS_LOOKUP"


class CdmModel:
    """
    cdm model class
    """

    def __init__(self, database: Union[SnowflakeClient, None] = None) -> None:
        self.message: str = "Hello cdm"
        if database is None:
            self.database: SnowflakeClient = SnowflakeClient()
        else:
            self.database: None = database
        self.ctx: SnowflakeConnection = self.database.connect()

    def table_exists(self, database: str, schema: str, table_name: str) -> dict:
        """A function to check if a table exists

        Args:
            database (str): name of the database.
            schema (str): name of the schema.
            table_name (str): name of the table.

        Returns:
            dict: return dict
        """
        # setup the cursor object to return list of dict objects
        cursor: DictCursor = self.ctx.cursor(DictCursor)

        try:
            # get all data sources and order by date created desc
            cursor.execute(f"use database {database}")
            cursor.execute(f"use schema {INFORMATION_SCHEMA}")
            cursor.execute(
                f"""
                        select table_name as source_name,
                               created,
                               last_altered as modified
                        from {database}.{INFORMATION_SCHEMA}.tables
                        where table_type = 'BASE TABLE' and table_name = '{table_name}'
                        and table_schema = '{schema}'
                        order by last_altered desc;
            """
            )
            return cursor.fetchone()

        except Exception as exc:
            raise Exception(f"Something went wrong. Details {exc}") from exc

        finally:
            cursor.close()

    def read_processed_sources(self) -> List[dict]:
        """A function to get all CDM processed sources.

        Returns:
            list(dict): processed client data sources
        """
        # setup the cursor object to return list of dict objects
        cursor: DictCursor = self.ctx.cursor(DictCursor)

        try:
            # get all data sources and order by date created desc
            cursor.execute(f"use database {PROCESSED_DATABASE}")
            cursor.execute(f"use schema {INFORMATION_SCHEMA}")
            cursor.execute(
                f"""
                        select table_name as source_name,
                               created,
                               last_altered as modified
                        from {PROCESSED_DATABASE}.{INFORMATION_SCHEMA}.tables
                        where table_type = 'BASE TABLE' and table_name like '%ITEMS_SCHEMA%'
                        order by last_altered desc;
            """
            )
            return cursor.fetchall()

        except Exception as exc:
            raise Exception(f"Something went wrong. Details {exc}") from exc

        finally:
            cursor.close()

    def read_processed_source_by_name(self, processed_data_source: str) -> dict:
        """Finds a processed client data source in the CDP_LTD database table.

        Args:
            processed_data_source (str): name of the processed data source.

        Returns:
            list(dict): processed client data source
        """
        # check if table source exists first
        if not self.table_exists(
            PROCESSED_DATABASE, PROCESSED_SCHEMA, processed_data_source
        ):
            return {}

        # setup the cursor object to return list of dict objects
        cursor: DictCursor = self.ctx.cursor(DictCursor)

        try:
            # get all data sources and order by date created desc
            cursor.execute(f"use database {PROCESSED_DATABASE}")
            cursor.execute(f"use schema {PROCESSED_SCHEMA}")
            cursor.execute(
                f"""
                        select data_source as source_name,
                                filename,
                                "ITEM SOURCE" as item_source,
                                itemcost as item_cost,
                               created as created,
                               updated as modified
                        from {PROCESSED_DATABASE}.{PROCESSED_SCHEMA}.{processed_data_source}
                        order by updated desc;
            """
            )
            return cursor.fetchone()

        except Exception as exc:
            raise Exception(f"Something went wrong. Details {exc}") from exc

        finally:
            cursor.close()

    def read_datafeeds(self) -> List[dict]:
        """Reads the data feed catalog table.

        Returns:
            list(dict): The list of data feeds in the database.
        """
        cursor: DictCursor = self.ctx.cursor()

        try:
            cursor.execute(f"use database {ADMIN_DATABASE}")
            cursor.execute(f"use schema {SCHEMA}")
            cursor.execute(
                f"""
                select
                    feed_id, feed_type, data_source, data_type, file_extension,
                    is_pii, modified
                from {TABLE_DATA_FEED_CATALOG}
                order by modified
            """
            )

            results: List[Optional[Any]] = cursor.fetchall()
            datafeeds: List[dict] = []

            for (
                feed_id,
                feed_type,
                data_source,
                data_type,
                file_extension,
                is_pii,
                modified,
            ) in results:
                result = {
                    "data_source": data_source,
                    "data_type": data_type,
                    "feed_id": feed_id,
                    "feed_type": feed_type,
                    "file_extension": file_extension,
                    "is_pii": is_pii == "Y",
                    "modified": modified,
                }
                datafeeds.append(result)

            return datafeeds

        except Exception as exc:
            raise Exception(f"Something went wrong. Details {exc}") from exc

        finally:
            cursor.close()

    def read_datafeed_by_id(self, datafeed_id: int) -> Union[dict, None]:
        """Finds a data feed in the data feed catalog table.

        Args:
            datafeed_id (int): id of the datafeed

        Returns:
            dict: The data feed in the database
        """
        cursor: DictCursor = self.ctx.cursor()

        try:
            cursor.execute(f"use database {ADMIN_DATABASE}")
            cursor.execute(f"use schema {SCHEMA}")
            cursor.execute(
                f"""
                select
                    feed_id, feed_type, data_source, data_type, file_extension,
                    is_pii, modified
                from {TABLE_DATA_FEED_CATALOG}
                where feed_id = %s""",
                int(datafeed_id),
            )

            row: Optional[Any] = cursor.fetchone()

            if not row:
                return None

            (
                feed_id,
                feed_type,
                data_source,
                data_type,
                file_extension,
                is_pii,
                modified,
            ) = row

            result: dict = {
                "data_source": data_source,
                "data_type": data_type,
                "feed_id": feed_id,
                "feed_type": feed_type,
                "file_extension": file_extension,
                "is_pii": is_pii == "Y",
                "modified": modified,
            }

            return result

        except Exception as exc:
            raise Exception(f"Something went wrong. Details {exc}") from exc

        finally:
            cursor.close()

    def read_fieldmappings(self) -> List[dict]:
        """Reads the fieldmappings table.

        Returns:
            list(dict): The list of fieldmappings in the database.
        """
        cursor: DictCursor = self.ctx.cursor()

        try:
            cursor.execute(f"use database {ADMIN_DATABASE}")
            cursor.execute(f"use schema {SCHEMA}")
            cursor.execute(
                f"""
                select id as field_id, field_name, field_variation, modified
                from {TABLE_PII_REQUIRED_FIELDS_LOOKUP}
                order by modified
            """
            )
            results: List[Optional[Any]] = cursor.fetchall()
            fieldmappings: List[dict] = []

            for field_id, field_name, field_variation, modified in results:
                result = {
                    "field_id": field_id,
                    "field_name": field_name,
                    "field_variation": field_variation,
                    "modified": modified,
                }
                fieldmappings.append(result)

            return fieldmappings

        except Exception as exc:
            raise Exception(f"Something went wrong. Details {exc}") from exc

        finally:
            cursor.close()

    def read_fieldmapping_by_id(self, fieldmapping_id: int) -> Union[dict, None]:
        """Finds a fieldmapping in the fieldmapping table.

        Args:
            fieldmapping_id (int): id of the fieldmapping

        Returns:
            dict: The fieldmapping in the database
        """
        cursor: DictCursor = self.ctx.cursor()

        try:
            cursor.execute(f"use database {ADMIN_DATABASE}")
            cursor.execute(f"use schema {SCHEMA}")
            cursor.execute(
                f"""
                select id as field_id, field_name, field_variation, modified
                from {TABLE_PII_REQUIRED_FIELDS_LOOKUP}
                where id = %s""",
                (int(fieldmapping_id)),
            )

            row: Optional[Any] = cursor.fetchone()

            if not row:
                return None

            field_id, field_name, field_variation, modified = row

            result: dict = {
                "field_id": field_id,
                "field_name": field_name,
                "field_variation": field_variation,
                "modified": modified,
            }

            return result

        except Exception as exc:
            raise Exception(f"Something went wrong. Details {exc}") from exc

        finally:
            cursor.close()
