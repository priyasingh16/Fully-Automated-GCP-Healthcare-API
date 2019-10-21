from client import client
from pprint import pprint

class patient:
    def __init__(self):
        self.cl = client()

    def allPatient(self):
        query_string = """SELECT SUBJECT_ID from `green-gasket-256323.mimiciii_fullyautomated.PATIENTS`;"""
        results = self.cl.queryRecords(query_string)
        SUBJECT_IDS = []
        for row in results:
            SUBJECT_IDS.append(row["SUBJECT_ID"]) 
        return SUBJECT_IDS

    def getPatient(self, id):
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
        p_json = {
            "resourceType" : "Patient",
            "identifier" : res["SUBJECT_ID"],
            "active" : None,
            "name" : res["SUBJECT_ID"],
            "telecom" : None,
            "gender" : "unknown",
            "birthDate" : res["DOB"],
            "address" : None,
            "maritalStatus" : res["MARITAL_STATUS"],
            "multipleBirthBoolean" : None,
            "multipleBirthInteger" : None,
            "photo" : None,
            "contact" : [
            #     {
            #     # "relationship" : None
            #     # "name" : { HumanName }, // A name associated with the contact person
            #     # "telecom" : [{ ContactPoint }], // A contact detail for the person
            #     # "address" : { Address }, // Address for the contact person
            #     # "gender" : "<code>", // male | female | other | unknown
            #     # "organization" : { Reference(Organization) }, // C? Organization that is associated with the contact
            #     # "period" : { Period } // The period during which this contact person or organization is valid to be contacted relating to this patient
            # }
            ],
            "communication" : [{ 
                "language" : res["LANGUAGE"],
                "preferred" : res["LANGUAGE"]
            }],
            "generalPractitioner" : None,
            "managingOrganization" : res["HADM_ID"],
            "link" : [
                # { // Link to another patient resource that concerns the same actual person
                # "other" : { Reference(Patient|RelatedPerson) }, // R!  The other patient or related person resource that the link refers to
                # "type" : "<code>" // R!  replaced-by | replaces | refer | seealso
                # }
            ]
        }

        if res["GENDER"].lower() == "m":
            p_json["gender"] = "male"
        elif res["GENDER"].lower() == "f":
            p_json["gender"] = "female"


        p_json["deceasedBoolean"] = 0
        p_json["deceasedDateTime"] = None 
        if res["DOD"] != None:
            p_json["deceasedBoolean"] : 1
            p_json["deceasedDateTime"] : res["DEATHTIME"]

        return p_json




if __name__ == "__main__":

    p = patient()
    all_patient = p.allPatient()
    for id in all_patient:
        pprint(p.getPatient(id))
