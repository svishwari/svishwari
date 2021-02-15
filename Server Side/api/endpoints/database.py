import snowflake.connector
from os import getenv

connection = snowflake.connector.connect(
    user=getenv("CDM_SNOWFLAKE_USER"),
    password=getenv("CDM_SNOWFLAKE_PASSWORD"),
    account=getenv("CDM_SNOWFLAKE_ACCOUNT"),
)

WAREHOUSE = "COMPUTE_WH"
DATABASE = "CDP_ADMIN"
SCHEMA = "CTRL"
DATA_FEED_CATALOG_TABLE = "DATA_FEED_CATALOG"

# setup
cursor = connection.cursor()
cursor.execute(f"USE WAREHOUSE {WAREHOUSE}")
cursor.execute(f"USE DATABASE {DATABASE}")
cursor.execute(f"USE SCHEMA {SCHEMA}")

def read_data_feed_catalog():
    try:
        cursor = connection.cursor()

        cursor.execute(f"SELECT FEED_ID, FEED_TYPE, DATA_SOURCE, DATA_TYPE, FILE_EXTENSION, IS_PII, FIELD_SEPRATOR, MODIFIED FROM {DATA_FEED_CATALOG_TABLE} ORDER BY MODIFIED")

        data_feeds = []

        for (
            FEED_ID, FEED_TYPE, DATA_SOURCE, DATA_TYPE,
            FILE_EXTENSION, FIELD_SEPRATOR, IS_PII, MODIFIED,
        ) in cursor:
            data_feed = {
                "data_source": DATA_SOURCE,
                "data_type": DATA_TYPE,
                "feed_id": FEED_ID,
                "feed_type": FEED_TYPE,
                "file_extension": FILE_EXTENSION,
                "is_pii": True if IS_PII == "Y" else False,
                "modified": MODIFIED,
            }
            data_feeds.append(data_feed)

        return data_feeds
    except Exception as exc:
        raise Exception(f"Something went wrong. Details {exc}")
    finally:
        cursor.close()


def read_data_feed_catalog_by_id(feed_id: int):
    try:
        cursor = connection.cursor()

        cursor.execute(f"SELECT FEED_ID, FEED_TYPE, DATA_SOURCE, DATA_TYPE, FILE_EXTENSION, IS_PII, FIELD_SEPRATOR, MODIFIED FROM {DATA_FEED_CATALOG_TABLE} WHERE FEED_ID = %s", (feed_id))

        row = cursor.fetchone()

        if not row:
            return None

        (
            FEED_ID, FEED_TYPE, DATA_SOURCE, DATA_TYPE,
            FILE_EXTENSION, FIELD_SEPRATOR, IS_PII, MODIFIED,
        ) = row

        data_feed = {
            "data_source": DATA_SOURCE,
            "data_type": DATA_TYPE,
            "feed_id": FEED_ID,
            "feed_type": FEED_TYPE,
            "file_extension": FILE_EXTENSION,
            "is_pii": True if IS_PII == "Y" else False,
            "modified": MODIFIED,
        }

        return data_feed
    except Exception as exc:
        raise Exception(f"Something went wrong. Details {exc}")
    finally:
        cursor.close()


# Close the connection...
# connection.close()
