from google.cloud import firestore
class DatastoreClient:
    def __init__(self):
        """
        Description
        -----------
        Create connection to firestore server using GOOGLE_APPLICATION_CREDENTIALS 
        """

        self.db = firestore.Client()

    def closeConnection(self):
        """
        Description
        -----------
        Close connection to fire store server.
        """

        if self.db:
            self.db.close()

    def insertData(self, kind, name, data):
        """
        Description
        -----------
        Inserts data into firestore NOSQL db 
        ----------
        Kind : String
            name of the collection to store data into.
        name : String
            unique identifier for that document.
        data : dict
            document in dictionary key value pair format.
        Returns
        ----------
        _ : Boolean
            if success true else false
        """
        if self.db:
            doc_ref = self.db.collection(kind).document(name)
            doc_ref.set(data)
            return True
        else:
            return False    
