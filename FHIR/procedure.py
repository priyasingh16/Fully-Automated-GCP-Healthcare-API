from client import client

class Procedure:
    """
    Description
    -----------
    Procedures perfromed in a particular patient.
    """
    def __init__(self):
        """
        Description
        -----------
        Initializes google cloud big query client to query FHIR data.
        """
        self.cl = client()

    def get_procedure(self, id):
        """
        Description
        -----------
        Extracts Information about all procedure performed of a patient in the hospital.
        Parameters
        ----------
        id : Integer
            Subject id of the patient to fetch prescription record.
        Returns
        ----------
        procedures_res : list
            list of procedures performed on a patient in all visits to the hospital.
        """

        query_string = """SELECT SUBJECT_ID, HADM_ID, STARTTIME, ENDTIME, ITEMID, LOCATION, STATUSDESCRIPTION,
            ORDERCATEGORYNAME, ICUSTAY_ID FROM `green-gasket-256323.mimiciii_fullyautomated.PROCEDUREEVENTS_MV` 
            where SUBJECT_ID = {};"""

        query_string = query_string.format(id)
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
        procedures_res = []
        for res in r:
            procedure_json = {
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
                procedure_json["status"] = "stopped"
            elif res['STATUSDESCRIPTION'] == "FinishedRunning":
                procedure_json["status"] = "completed"
            elif res['STATUSDESCRIPTION'] == "Paused":
                procedure_json["status"] = "on-hold"
            elif res['STATUSDESCRIPTION'] == "Rewritten":
                procedure_json["status"] = "not-done"

            procedures_res.append(procedure_json)
        return procedures_res
