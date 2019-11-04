from client import client
from pprint import pprint


class MedicationDispense:
    # Procedure start and stop times recorded for MetaVision patients.
    def __init__(self):
        self.cl = client()

    def all_patient(self):
        query_string = """SELECT SUBJECT_ID from `green-gasket-256323.mimiciii_fullyautomated.PATIENTS`;"""
        results = self.cl.queryRecords(query_string)
        SUBJECT_IDS = []
        for row in results:
            SUBJECT_IDS.append(row["SUBJECT_ID"])
        return SUBJECT_IDS

    def get_medication_dispense(self, id):
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
            p_json = {
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

            medication_res.append(p_json)
        return medication_res


if __name__ == "__main__":
#
    p = MedicationDispense()
    # for id in p.all_patient():
    pprint(p.get_medication_dispense(61))