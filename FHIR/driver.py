import logging
import time
from storageClient import DatastoreClient
from patient import Patient
from encounter import Encounter
from medication import Medication
from medication_dispense import MedicationDispense
from report import DiagnosticReport
from procedure import Procedure
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/app.log',level=logging.INFO)

if __name__ == "__main__":
    d = DatastoreClient()
    
    p = Patient()
    e = Encounter()
    m = Medication()
    dr = DiagnosticReport()
    md = MedicationDispense()
    pr = Procedure()

    all_patient = sorted(p.all_patient())
    for id in all_patient:
        start = time.time()
        logger.info('Extracting Data For Id: ' + str(id) + ', time : ' + str(start))
        print(p.get_patient(id))
        print(e.get_encounter(id))
        print(m.get_medication(id))
        print(md.get_medication_dispense(id))
        print(dr.get_diagnostic_report(id))
        print(pr.get_procedure(id))


        end = time.time()

        logger.info('Extracting Data For Id: ' + str(id) + ', time : ' + str(end))
        logger.info('Rime taken for Id: ' + str(id) + ', time : ' + str(end-start))

        break
