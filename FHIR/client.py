from google.cloud import bigquery

class client:
    """
    Description
    -----------
    The class deals with client connection to google big query resource to get record form mimic table.
    """

    def __init__(self):
        """
        Description
        -----------
        Create connection to bigquery using GOOGLE_APPLICATION_CREDENTIALS 
        """
        self.client = bigquery.Client()

    def closeConnection(self):
        """
        Description
        -----------
        Close connection to big query server.
        """

        if self.client:
            self.client.close()

    def queryRecords(self, query):
        """
        Description
        -----------
        Query big query database which contains mimic records
        ----------
        query : String
            Valid sql like query to query record from the mimic tables.
        Returns
        ----------
        query_job : Record:
            list of dictionary like record for they query or false if client not initialized
        """

        if self.client:
            query_job = self.client.query(query)
            return query_job.result()
        else:
            return False
