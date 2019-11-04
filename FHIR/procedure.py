from client import client
from pprint import pprint


class Procedure:
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

    def get_procedure(self, id):
        query_string = """SELECT SUBJECT_ID, HADM_ID, STARTTIME, ENDTIME, ITEMID, LOCATION, STATUSDESCRIPTION,
        ORDERCATEGORYNAME FROM `green-gasket-256323.mimiciii_fullyautomated.PROCEDUREEVENTS_MV` 
        where SUBJECT_ID = {};"""

        query_string = query_string.format(id)
        print(query_string)
        results = self.cl.queryRecords(query_string)
        pprint(results)

        r = []
        for row in results:
            res = {}
            for i in row.keys():
                if i not in res:
                    res[i] = None

                if i in res and res[i] == None:
                    res[i] = row[i]

            r.append(res)
        pprint(r)

        procedures_res = []
        for res in r:
            p_json = {
                "resourceType": "Procedure",
                "instantiatesCanonical" : None,
                "instantiatesUri": None,
                "basedOn": None,
                "partOf": res['ICUSTAY_ID'],
                "statusReason": None,
                "category" : None,
                "code" : None,
                "subject" : res['SUBJECT_ID'],
                "encounter" : res['HADM_ID'],
                "performedDateTime" : str(res['STARTTIME']),
                "performedPeriod" : round(abs(res['ENDTIME'] - res['STARTTIME']).seconds/3600, 2),
                "performedString": res['ORDERCATEGORYNAME'],
                "performedAge": None,
                "performedRange": str(res['STARTTIME']) + " - " + str(res['ENDTIME']),
                "recorder": None,
                "asserter": None,
                "performer":[],
                "location" : None, # TODO
                "reasonCode" : None,
                "reasonReference": None,
                "bodySite": res['LOCATION'],
                "outcome" : None,
                "report" : None,
                "complication" : None,
                "complicationDetail" : None,
                "followUp" : None,
                "note" : None,
                "focalDevice" : None,
                "action" :None,
                "manipulated" : None,
                "usedReference" : res['ITEMID'] ,
                "usedCode" : None
            }

            if res['STATUSDESCRIPTION']== "Stopped":
                p_json["status"] = "stopped"
            elif res['STATUSDESCRIPTION'] == "FinishedRunning":
                p_json["status"] = "completed"
            elif res['STATUSDESCRIPTION'] == "Paused":
                p_json["status"] = "on-hold"
            elif res['STATUSDESCRIPTION'] == "Rewritten":
                p_json["status"] = "not-done"

            procedures_res.append(p_json)
        return procedures_res


if __name__ == "__main__":
#
    p = Procedure()
    for id in p.all_patient():
        p.get_procedure(id)