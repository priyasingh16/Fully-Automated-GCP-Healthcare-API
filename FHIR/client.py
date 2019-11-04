from google.cloud import bigquery

class client:
    def __init__(self):
        self.client = bigquery.Client()

    def closeConnection(self):
        if self.client:
            self.client.close()

    def queryRecords(self, query):
        if self.client:
            query_job = self.client.query(query)
            return query_job.result()
        else:
            return False
