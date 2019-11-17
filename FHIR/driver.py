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
import sys
from multiprocessing import Pool

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# first file logger
logger = setup_logger('Info_Logger', 'logs/app.log')

# error file logger
error_logger = setup_logger('Error_Logger', 'logs/error.log')


def getPatientRecords( d, p, e, m, o, dr, md, pr, id):
    start = time.time()
    logger.info('Extracting Data For Id: ' + str(id) + ', time : ' + str(start))
    try:
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
        logger.info('Time taken for Id: ' + str(id) + ', time : ' + str(end-start))

    except Exception as e:
        error_logger.error('Extracting Data For ' +str(id)+ ' failed !')
        error_logger.error(str(e))


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
        if i >= len(all_patient):
            break
        id = all_patient[i]
        getPatientRecords( d, p, e, m, o, dr, md, pr, id)
    
    return True





if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.stderr.write("Invalid Argument required offset")
        exit(-1)

    offset = int(sys.argv[1])


    if (offset == 0 or offset == 10 or offset == 20) == False:
        sys.stderr.write("Invalid argument offset can be 0, 10 or 20 only, for 0-20000, 20000-40000, 40000- respectively")
        exit(-1)


    start = time.time()
    indexes = []
    r = 2000
    for i in range(10):
        indexes.append(((offset + i) * r, (offset + i + 1) *r))

    with Pool(10) as p:
        print(p.map(processBatch, indexes))
    print("Done")
    end = time.time()
    print(end-start)

