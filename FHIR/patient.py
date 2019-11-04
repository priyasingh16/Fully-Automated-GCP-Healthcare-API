from client import client

class Patient:
    """
    Description
    -----------
    The class deals with etl script transforming patient data
    from mimic3 tables to FHIR accepted format.
    """

    def __init__(self):
        """
        Description
        -----------
        Initializes google cloud big query client to query FHIR data.
        """
        self.cl = client()

    def all_patient(self):
        """
        Description
        -----------
        Extract all the unique ids given to patient and return a list of all those ids.
        Returns
        ----------
        SUJECTS_IDS : list
            list of all subjects_ids in integer format.
        """

        query_string = """SELECT SUBJECT_ID from `green-gasket-256323.mimiciii_fullyautomated.PATIENTS`;"""
        results = self.cl.queryRecords(query_string)
        SUBJECT_IDS = []
        for row in results:
            SUBJECT_IDS.append(row["SUBJECT_ID"]) 
        return SUBJECT_IDS

    def get_patient(self, id):
        """
        Description
        -----------
        Extracts Information about as a single patient given subject id.
        Parameters
        ----------
        id : Integer
            Subject id of the coresponding patient.
        Returns
        ----------
        patient_json : dict
            key value pair of information relevant to the given patient id.
        """

        query_string = """SELECT P.*, A.HADM_ID,  A.INSURANCE, A.LANGUAGE, A.RELIGION, A.MARITAL_STATUS, A.ETHNICITY, A.DEATHTIME from 
        `green-gasket-256323.mimiciii_fullyautomated.PATIENTS` as P 
        left join `green-gasket-256323.mimiciii_fullyautomated.ADMISSIONS` as A on P.SUBJECT_ID=A.SUBJECT_ID
        where P.SUBJECT_ID = {};"""

        query_string = query_string.format(id)        
        results = self.cl.queryRecords(query_string)
        res = {}
        for row in results:
            for i in row.keys():
                if i not in res:
                    res[i] = None
                
                if i in res and res[i] == None:
                    res[i] = row[i]
        patient_json = {
            "resourceType" : "Patient",
            "identifier" : res["SUBJECT_ID"],
            "active" : None,
            "name" : res["SUBJECT_ID"],
            "telecom" : None,
            "gender" : res['GENDER'],
            "birthDate" : res["DOB"],
            "address" : None,
            "maritalStatus" : res["MARITAL_STATUS"],
            "multipleBirthBoolean" : None,
            "multipleBirthInteger" : None,
            "photo" : None,
            "contact" : [],
            "communication" : [{ 
                "language" : res["LANGUAGE"],
                "preferred" : res["LANGUAGE"]
            }],
            "generalPractitioner" : None,
            "managingOrganization" : res["HADM_ID"],
            "link" : []
        }

        if res["GENDER"].lower() == "m":
            patient_json["gender"] = "male"
        elif res["GENDER"].lower() == "f":
            patient_json["gender"] = "female"


        patient_json["deceasedBoolean"] = 0
        patient_json["deceasedDateTime"] = None 
        if res["DOD"] != None:
            patient_json["deceasedBoolean"] = 1
            patient_json["deceasedDateTime"] = res["DEATHTIME"]

        return patient_json