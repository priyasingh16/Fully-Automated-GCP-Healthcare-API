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
from multiprocessing import Pool

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/app.log',level=logging.INFO)



def getPatientRecords( d, p, e, m, o,dr,md,pr, id):
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

def processBatch(a_b):
    a,b = a_b
    d = DatastoreClient()
    p = Patient()
    e = Encounter()
    m = Medication()
    o = Observations()
    dr = DiagnosticReport()
    md = MedicationDispense()
    pr = Procedure()


    all_patient = sorted(p.all_patient())

    for i in range(a,b):
        id = all_patient[i]
        getPatientRecords( d, p, e, m, o,dr,md,pr, id)
    
    return True





if __name__ == "__main__":

    start = time.time()
    with Pool(10) as p:
        print(p.map(processBatch, [(0,5), (5,10), (10,15), (15,20), (20,25), (25,30), (30,35), (35,40), (40,45), (45,50)]))
    print("Done")
    end = time.time()
    print(end-start)

