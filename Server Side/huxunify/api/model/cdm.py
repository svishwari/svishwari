"""
The purpose of this file is for housing the Customer Data Management (CDM) related API models
"""
import logging
from huxunify.api.data_connectors.snowflake_client import SnowflakeClient, PROCESSED_DATABASE


class CdmModel:
    """
    cdm model class
    """
    def __init__(self):
        self.message = "Hello cdm"
        self.db = SnowflakeClient(username='', password='')
        self.ctx = self.db.connect()

    def get_data_sources(self):
        """A function to get all CDM processed files.
        Args:
            client_table: name of the snowflake client table
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
            cs.execute(f"""
                select data_source, filename, count(*) as record_count
                from {PROCESSED_DATABASE}.LTD.NETSUITE_ITEMS_205FD81AFAAB9B858EDA8E503BE224AC_LTD
                group by data_source, filename 
            """)
            results = cs.fetchall()

            # port the data back into the list
            data_sources = [{'src': rec[0], 'filename': rec[1], 'record_count': rec[2]}
                            for rec in results]
        finally:
            cs.close()
        return data_sources


if __name__ == '__main__':
    pass
