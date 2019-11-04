from google.cloud import firestore


class DatastoreClient:
    def __init__(self):
        self.db = firestore.Client()

    def closeConnection(self):
        if self.db:
            self.db.close()

    def insertData(self, kind, name, data):
        print(name)
        if self.db:
            doc_ref = self.db.collection(kind).document(name)
            doc_ref.set(data)
        else:
            return False    
