import logging
import time
from storageClient import DatastoreClient
from patient import Patient
from encounter import Encounter
from medication import Medication
from medication_dispense import MedicationDispense
from report import DiagnosticReport
from procedure import Procedure
from observations import Observations
import json
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/app.log',level=logging.INFO)

if __name__ == "__main__":
    d = DatastoreClient()
    
    p = Patient()
    e = Encounter()
    m = Medication()
    o = Observations()
    dr = DiagnosticReport()
    md = MedicationDispense()
    pr = Procedure()

    all_patient = sorted(p.all_patient())
    for id in all_patient:
        start = time.time()
        logger.info('Extracting Data For Id: ' + str(id) + ', time : ' + str(start))
        patient_info = p.get_patient(id)
        encounter_info = e.get_encounter(id)
        medicine_info = m.get_medication(id)
        observation_info = o.get_observations(id)
        medication_info = md.get_medication_dispense(id)
        diagnostic_info = dr.get_diagnostic_report(id)
        procedure_info = pr.get_procedure(id)

        d.insertData("patient", str(id), patient_info)
        d.insertData("encounter", str(id), {"data" : encounter_info})
        d.insertData("medicine", str(id), {"data" : medicine_info})
        d.insertData("obsevation", str(id), {"data" : observation_info})
        d.insertData("medication", str(id), {"data" : medication_info})
        d.insertData("diagnostics", str(id), {"data" : diagnostic_info})
        d.insertData("procedure", str(id), {"data" : procedure_info})

        end = time.time()

        logger.info('Extracting Data For Id: ' + str(id) + ', time : ' + str(end))
        logger.info('Rime taken for Id: ' + str(id) + ', time : ' + str(end-start))

