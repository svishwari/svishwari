"""
The purpose of this file is for housing the Customer Data Management (CDM) related API models
"""
import logging
from huxunify.api.data_connectors.snowflake_client import SnowflakeClient

# CDM DATABASE CONSTANTS - we can move these after
PROCESSED_DATABASE = "CDP_LTD"
ADMIN_DATABASE = "CDP_ADMIN"
SCHEMA = "CTRL"
TABLE_DATA_FEED_CATALOG = "DATA_FEED_CATALOG"
TABLE_PII_REQUIRED_FIELDS_LOOKUP = "PII_REQUIRED_FIELDS_LOOKUP"


class CdmModel:
    """
    cdm model class
    """

    def __init__(self):
        self.message = "Hello cdm"
        self.db = SnowflakeClient()
        self.ctx = self.db.connect()

    def get_data_sources(self):
        """A function to get all CDM processed files.

        Returns:
            list(dict): processed client data sources
        """
        data_sources = []
        if self.ctx is None:
            return data_sources, 200

        # setup the cursor object
        cs = self.ctx.cursor()

        try:
            # execute the fetch all query
            cs.execute(
                f"""
                select data_source, filename, count(*) as record_count
                from {PROCESSED_DATABASE}.LTD.NETSUITE_ITEMS_205FD81AFAAB9B858EDA8E503BE224AC_LTD
                group by data_source, filename 
            """
            )
            results = cs.fetchall()

            # port the data back into the list
            data_sources = [
                {"src": rec[0], "filename": rec[1], "record_count": rec[2]}
                for rec in results
            ]
        finally:
            cs.close()
        return data_sources

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

            results = []

            for (
                feed_id,
                feed_type,
                data_source,
                data_type,
                file_extension,
                is_pii,
                modified,
            ) in cursor:
                result = {
                    "data_source": data_source,
                    "data_type": data_type,
                    "feed_id": feed_id,
                    "feed_type": feed_type,
                    "file_extension": file_extension,
                    "is_pii": is_pii == "Y",
                    "modified": modified.__str__(),
                }
                results.append(result)

            return results

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
                (int(datafeed_id)),
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
                "modified": modified.__str__(),
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

            results = []

            for field_id, field_name, field_variation, modified in cursor:
                result = {
                    "field_id": field_id,
                    "field_name": field_name,
                    "field_variation": field_variation,
                    "modified": modified,
                }
                results.append(result)

            return results

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
