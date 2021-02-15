import snowflake.connector
from os import getenv


WAREHOUSE = "COMPUTE_WH"
DATABASE = "CDP_ADMIN"
SCHEMA = "CTRL"
TABLE_DATA_FEED_CATALOG = "DATA_FEED_CATALOG"
TABLE_PII_REQUIRED_FIELDS_LOOKUP = "PII_REQUIRED_FIELDS_LOOKUP"

# establish connection...
connection = snowflake.connector.connect(
    user=getenv("CDM_SNOWFLAKE_USER"),
    password=getenv("CDM_SNOWFLAKE_PASSWORD"),
    account=getenv("CDM_SNOWFLAKE_ACCOUNT"),
)

# set up...
cursor = connection.cursor()
cursor.execute(f"USE WAREHOUSE {WAREHOUSE}")
cursor.execute(f"USE DATABASE {DATABASE}")
cursor.execute(f"USE SCHEMA {SCHEMA}")


def read_datafeeds():
    """Reads the data feed catalog table, returning a list of data feeds.
    """
    try:
        cursor = connection.cursor()

        cursor.execute(f"SELECT FEED_ID, FEED_TYPE, DATA_SOURCE, DATA_TYPE, FILE_EXTENSION, IS_PII, FIELD_SEPRATOR, MODIFIED FROM {TABLE_DATA_FEED_CATALOG} ORDER BY MODIFIED")

        results = []

        for (
            FEED_ID, FEED_TYPE, DATA_SOURCE, DATA_TYPE,
            FILE_EXTENSION, FIELD_SEPRATOR, IS_PII, MODIFIED,
        ) in cursor:
            result = {
                "data_source": DATA_SOURCE,
                "data_type": DATA_TYPE,
                "feed_id": FEED_ID,
                "feed_type": FEED_TYPE,
                "file_extension": FILE_EXTENSION,
                "is_pii": True if IS_PII == "Y" else False,
                "modified": MODIFIED,
            }
            results.append(result)

        return results
    except Exception as exc:
        raise Exception(f"Something went wrong. Details {exc}")
    finally:
        cursor.close()


def read_datafeed_by_id(feed_id: int):
    """Finds a data feed in the data feed catalog table and returns it.
    """
    try:
        cursor = connection.cursor()

        cursor.execute(f"SELECT FEED_ID, FEED_TYPE, DATA_SOURCE, DATA_TYPE, FILE_EXTENSION, IS_PII, FIELD_SEPRATOR, MODIFIED FROM {TABLE_DATA_FEED_CATALOG} WHERE FEED_ID = %s", (int(feed_id)))

        row = cursor.fetchone()

        if not row:
            return None

        (
            FEED_ID, FEED_TYPE, DATA_SOURCE, DATA_TYPE,
            FILE_EXTENSION, FIELD_SEPRATOR, IS_PII, MODIFIED,
        ) = row

        result = {
            "data_source": DATA_SOURCE,
            "data_type": DATA_TYPE,
            "feed_id": FEED_ID,
            "feed_type": FEED_TYPE,
            "file_extension": FILE_EXTENSION,
            "is_pii": True if IS_PII == "Y" else False,
            "modified": MODIFIED,
        }

        return result
    except Exception as exc:
        raise Exception(f"Something went wrong. Details {exc}")
    finally:
        cursor.close()


def read_fieldmappings():
    """Reads the PII required fields lookup table, returning a list of fieldmappings.
    """
    try:
        cursor = connection.cursor()

        cursor.execute(f"SELECT ID, FIELD_NAME, FIELD_VARIATION, MODIFIED FROM {TABLE_PII_REQUIRED_FIELDS_LOOKUP} ORDER BY MODIFIED")

        results = []

        for (ID, FIELD_NAME, FIELD_VARIATION, MODIFIED) in cursor:
            result = {
                "id": ID,
                "field_name": FIELD_NAME,
                "field_variation": FIELD_VARIATION,
                "modified": MODIFIED,
            }
            results.append(result)

        return results
    except Exception as exc:
        raise Exception(f"Something went wrong. Details {exc}")
    finally:
        cursor.close()

def read_fieldmapping_by_id(id: int):
    """Finds a fieldmapping in the PII required fields lookup table and returns it.
    """
    try:
        cursor = connection.cursor()

        cursor.execute(f"SELECT ID, FIELD_NAME, FIELD_VARIATION, MODIFIED FROM {TABLE_PII_REQUIRED_FIELDS_LOOKUP} WHERE ID = %s", (int(id)))

        row = cursor.fetchone()

        if not row:
            return None

        ID, FIELD_NAME, FIELD_VARIATION, MODIFIED = row

        result = {
            "id": ID,
            "field_name": FIELD_NAME,
            "field_variation": FIELD_VARIATION,
            "modified": MODIFIED,
        }

        return result
    except Exception as exc:
        raise Exception(f"Something went wrong. Details {exc}")
    finally:
        cursor.close()


# Close the connection...
# connection.close()
