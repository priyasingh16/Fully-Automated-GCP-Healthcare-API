from client import client
from pprint import pprint

class Encounter:
    def __init__(self):
        self.cl = client()

    def allPatient(self):
        query_string = """SELECT SUBJECT_ID from `green-gasket-256323.mimiciii_fullyautomated.PATIENTS`;"""
        results = self.cl.queryRecords(query_string)
        SUBJECT_IDS = []
        for row in results:
            SUBJECT_IDS.append(row["SUBJECT_ID"]) 
        return SUBJECT_IDS

    def getEncounter(self, id):
        query_string = """
            SELECT A.ADMITTIME, A.DISCHTIME, A.SUBJECT_ID, A.HADM_ID, A.DIAGNOSIS, A.ADMISSION_LOCATION, A.ADMISSION_TYPE, 
            D.SEQ_NUM, D.ICD9_CODE, D_ICD.SHORT_TITLE, D_ICD.LONG_TITLE  
            FROM `green-gasket-256323.mimiciii_fullyautomated.ADMISSIONS` as A  
            left join `green-gasket-256323.mimiciii_fullyautomated.DIAGNOSES_ICD` as D on D.HADM_ID = A.HADM_ID
            left join `green-gasket-256323.mimiciii_fullyautomated.D_ICD_DIAGNOSES` as D_ICD on D_ICD.ICD9_CODE = D.ICD9_CODE
            where A.SUBJECT_ID = {}
            ORDER BY HADM_ID, SEQ_NUM
            """
        query_string = query_string.format(id)
        results = self.cl.queryRecords(query_string)
        rec = {}

        for row in results:
            h_id = row["HADM_ID"]
            if h_id not in rec:
                r = {}
                r["SUBJECT_ID"] = row["SUBJECT_ID"]
                r["HADM_ID"] = row["HADM_ID"]
                r["DIAGNOSIS"] = row["DIAGNOSIS"]
                r["ADMISSION_LOCATION"] = row["ADMISSION_LOCATION"]
                r["ADMITTIME"] = row["ADMITTIME"]
                r["DISCHTIME"] = row["DISCHTIME"]
                if row["ADMISSION_TYPE"] == "ELECTIVE":
                    row["ADMISSION_TYPE"] == "PRENC"
                elif row["ADMISSION_TYPE"] == "EMERGENCY":
                    row["ADMISSION_TYPE"] == "EMER"
                else:
                    row["ADMISSION_TYPE"] == "NONAC"

                r["ADMISSION_TYPE"] = row["ADMISSION_TYPE"]
                r["DIAGNOSES_ICD"] = []
                r["TRANSFERS"] = []
                rec[h_id] = r
            d = {}
            d["SEQ_NUM"] = row["SEQ_NUM"]
            d["ICD9_CODE"] = row["ICD9_CODE"]
            d["SHORT_TITLE"] = row["SHORT_TITLE"]
            d["LONG_TITLE"] = row["LONG_TITLE"]
            rec[h_id]["DIAGNOSES_ICD"].append(d)

        for h_id in rec.keys():
            query_string = """
            SELECT *  FROM `green-gasket-256323.mimiciii_fullyautomated.TRANSFERS`
            where HADM_ID = {}
            order by INTIME
            """
            query_string = query_string.format(h_id)
            results = self.cl.queryRecords(query_string)

            for row in results:
                t = {}
                t["ICUSTAY_ID"] = row["ICUSTAY_ID"]
                t["DBSOURCE"] = row["DBSOURCE"]
                t["EVENTTYPE"] = row["EVENTTYPE"]
                t["PREV_CAREUNIT"] = row["PREV_CAREUNIT"]
                t["PREV_WARDID"] = row["PREV_WARDID"]
                t["CURR_WARDID"] = row["CURR_WARDID"]
                t["CURR_CAREUNIT"] = row["CURR_CAREUNIT"]
                t["INTIME"] = row["INTIME"]
                t["LOS"] = row["LOS"]
                t["OUTTIME"] = row["OUTTIME"]
                rec[h_id]["TRANSFERS"].append(t)
        pprint(rec)
        encounter = []
        for h_id in rec:
            row = rec[h_id]

            e_json = {
                "resourceType" : "Encounter",
                "identifier" : row["HADM_ID"],
                "class" : row["ADMISSION_TYPE"],
                "type" : row["ADMISSION_TYPE"],
                "subject" : row["SUBJECT_ID"],
                "period" : str(row["ADMITTIME"]) + " - " + str(row["DISCHTIME"]),
                "length" : (row["DISCHTIME"] - row["ADMITTIME"]).seconds/3600,
                "reasonCode" : row["DIAGNOSIS"],
            }

            e_json["diagnosis"] = []
            for i in row["DIAGNOSES_ICD"]:
                d = {}
                d["condition"] = i["SHORT_TITLE"]
                d["rank"] = i["SEQ_NUM"]
                e_json["diagnosis"].append(d)

            e_json["location"] = []
            for i in row["TRANSFERS"]:
                t = {}
                t["location"] = i["CURR_WARDID"]
                t["status"] = i["EVENTTYPE"]
                t["physicalType"] = i["CURR_CAREUNIT"]
                t["period"] = str(i["INTIME"]) + " - " + str(i["OUTTIME"])
                e_json["location"].append(t)

            encounter.append(e_json)

        return encounter




if __name__ == "__main__":

    p = Encounter()
    for id in p.all_patient():
        pprint(p.getEncounter(id))
