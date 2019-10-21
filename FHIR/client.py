from google.cloud import bigquery
import os

class client:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/parth/Downloads/1c476b5a2f39.json"
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
