from client import client
from pprint import pprint


class Medication:
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

    def get_medication(self, id):
        query_string = """SELECT DRUG_NAME_GENERIC, FORMULARY_DRUG_CD, NDC, PROD_STRENGTH, 
        DOSE_VAL_RX, FORM_UNIT_DISP FROM `green-gasket-256323.mimiciii_fullyautomated.PRESCRIPTIONS`
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
          "resourceType" : "Medication",
          "identifier" : res['NDC'],
          "code" : res['FORMULARY_DRUG_CD'],
          "status" : None,
          "manufacturer" : None,
          "form" : res['FORM_UNIT_DISP'],
          "amount" : res['DOSE_VAL_RX'],
          "ingredient" : [{
            "itemCodeableConcept" : res['FORMULARY_DRUG_CD'],
            "itemReference" : res['DRUG_NAME_GENERIC'],
            "isActive" : None,
            "strength" : res['PROD_STRENGTH']
          }],
          "batch" : None
        }

            medication_res.append(p_json)
        return medication_res


if __name__ == "__main__":
#
    p = Medication()
    for id in p.all_patient():
        pprint(p.get_medication(id))