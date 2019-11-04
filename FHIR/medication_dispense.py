from client import client
from pprint import pprint


class MedicationDispense:
    """
    Description
    -----------
    Get relevent medication information about a particular patient.
    """
    def __init__(self):
        """
        Description
        -----------
        Initializes google cloud big query client to query FHIR data.
        """
        self.cl = client()

    def get_medication_dispense(self, id):
        """
        Description
        -----------
        Extracts Information about all medication information of a patient given subject id.
        Parameters
        ----------
        id : Integer
            Subject id of the coresponding patient.
        Returns
        ----------
        encounter : list
            list of dicts which contains Medication information about patients for every visit to the hospital.
        """

        query_string = """SELECT ROW_ID, SUBJECT_ID, HADM_ID, ICUSTAY_ID, STARTDATE, ENDDATE, DRUG_TYPE, DRUG, 
        DRUG_NAME_GENERIC, NDC, PROD_STRENGTH, FORM_VAL_DISP, FORM_UNIT_DISP, ROUTE
        FROM `green-gasket-256323.mimiciii_fullyautomated.PRESCRIPTIONS`
        where SUBJECT_ID = {};"""

        query_string = query_string.format(id)
        print(query_string)
        results = self.cl.queryRecords(query_string)

        r = []
        for row in results:
            res = {}
            for i in row.keys():
                if i not in res:
                    res[i] = None

                if i in res and res[i] == None:
                    res[i] = row[i]

            r.append(res)


        medication_res = []
        for res in r:
            medication_info = {
                "resourceType" : "MedicationDispense",

                "identifier" : res['ROW_ID'],
                "partOf" : res['ICUSTAY_ID'],
                "status" : None,

                "statusReasonCodeableConcept" : None,
                "statusReasonReference" : None,
                "category" : res['DRUG_TYPE'],
                "medicationCodeableConcept" :res['DRUG_NAME_GENERIC'],
                "medicationReference" : res['NDC'],
                "subject" : res['SUBJECT_ID'],
                "context" : res['HADM_ID'],
                "supportingInformation" : None,
                "performer" : [{
                    "function" : None,
                    "actor" : res['HADM_ID']
                }],
                "location" : None,
                "authorizingPrescription" : None,
                "type" : None,
                "quantity" : res['FORM_VAL_DISP'],
                "daysSupply" : round(abs(res['ENDDATE'] - res['STARTDATE']).seconds/86400, 2),
                "whenPrepared" : str(res['STARTDATE']),
                "whenHandedOver" : None,
                "destination" : None,
                "receiver" : None,
                "note" : res['DRUG'] + " " + res['FORM_VAL_DISP']	+ " " + res['FORM_UNIT_DISP'],
                "dosageInstruction" : res['ROUTE'],
                "substitution" : None,
                "detectedIssue" : None,
                "eventHistory" : None
            }

            medication_res.append(medication_info)
        return medication_res
