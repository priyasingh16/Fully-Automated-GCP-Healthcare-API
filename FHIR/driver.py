import logging
from storageClient import DatastoreClient
from patient import patient

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/app.log',level=logging.INFO)

if __name__ == "__main__":
    p = patient()
    d = DatastoreClient()
    all_patient = sorted(p.all_patient())
    for id in all_patient:
        print(p.get_patient(id))
        break
        # logger.info('Extracting Data For Id: ' + str(id))
