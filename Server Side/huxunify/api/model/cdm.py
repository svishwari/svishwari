"""
Models for the CDM API
"""
from snowflake.connector import DictCursor
from huxunify.api.data_connectors.snowflake_client import SnowflakeClient


# CDM DATABASE CONSTANTS - we can move these after
PROCESSED_DATABASE = "CDP_LTD"
ADMIN_DATABASE = "CDP_ADMIN"
SCHEMA = "CTRL"
PROCESSED_SCHEMA = "LTD"
INFORMATION_SCHEMA = "INFORMATION_SCHEMA"
TABLE_DATA_FEED_CATALOG = "DATA_FEED_CATALOG"
TABLE_PII_REQUIRED_FIELDS_LOOKUP = "PII_REQUIRED_FIELDS_LOOKUP"


class CdmModel:
    """
    cdm model class
    """

    def __init__(self, database=None):
        self.message = "Hello cdm"
        if database is None:
            self.database = SnowflakeClient()
        else:
            self.database = database
        self.ctx = self.database.connect()

    def table_exists(self, database, schema, table_name):
        """A function to check if a table exists

        Returns:
            bool: return boolean if table exists
        """
        # setup the cursor object to return list of dict objects
        cursor = self.ctx.cursor(DictCursor)

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

    def read_processed_sources(self):
        """A function to get all CDM processed sources.

        Returns:
            list(dict): processed client data sources
        """
        # setup the cursor object to return list of dict objects
        cursor = self.ctx.cursor(DictCursor)

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
            raise Exception(f"Something went wrong. Details: {exc}") from exc

        finally:
            cursor.close()

    def read_processed_source_by_name(self, processed_data_source: str):
        """Finds a processed client data source in the CDP_LTD database table.

        Returns:
            list(dict): processed client data source
        """
        # check if table source exists first
        if not self.table_exists(
            PROCESSED_DATABASE, PROCESSED_SCHEMA, processed_data_source
        ):
            return {}

        # setup the cursor object to return list of dict objects
        cursor = self.ctx.cursor(DictCursor)

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
            raise Exception(f"Something went wrong. Details: {exc}") from exc

        finally:
            cursor.close()

    def read_datafeeds(self):
        """Reads the data feed catalog table.

        Returns:
            list(dict): The list of data feeds in the database.
        """
        cursor = self.ctx.cursor()

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

            results = cursor.fetchall()
            datafeeds = []

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

    def read_datafeed_by_id(self, datafeed_id: int):
        """Finds a data feed in the data feed catalog table.

        Returns:
            dict: The data feed in the database
        """
        cursor = self.ctx.cursor()

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

            row = cursor.fetchone()

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

            result = {
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

    def read_fieldmappings(self):
        """Reads the fieldmappings table.

        Returns:
            list(dict): The list of fieldmappings in the database.
        """
        cursor = self.ctx.cursor()

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
            results = cursor.fetchall()
            fieldmappings = []

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

    def read_fieldmapping_by_id(self, fieldmapping_id: int):
        """Finds a fieldmapping in the fieldmapping table.

        Returns:
            dict: The fieldmapping in the database
        """
        cursor = self.ctx.cursor()

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

            row = cursor.fetchone()

            if not row:
                return None

            field_id, field_name, field_variation, modified = row

            result = {
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
