from client import client

class DiagnosticReport:
    """
    Description
    -----------
    Get relevent Diagnostics information about a particular patient.
    """

    def __init__(self):
        """
        Description
        -----------
        Initializes google cloud big query client to query FHIR data.
        """
        self.cl = client()

    def get_diagnostic_report(self, id):
        """
        Description
        -----------
        Extracts Information about all daignosis patient in the hospital.
        Parameters
        ----------
        id : Integer
            Subject id all of the patient to fetch prescription record.
        Returns
        ----------
        procedures_res : list
            list of all diagnostic information of a patient in all visits to the hospital.
        """

        query_string = """SELECT ROW_ID, SUBJECT_ID, HADM_ID, CHARTDATE, CHARTTIME, STORETIME, 
            CATEGORY, DESCRIPTION, CGID, ISERROR, TEXT  FROM `green-gasket-256323.mimiciii_fullyautomated.NOTEEVENTS` 
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
        
        report_res = []

        for res in r:
            report_json = {
                    "resourceType" : "DiagnosticReport",
                    "identifier" : res["ROW_ID"], # Business identifier for report
                    "basedOn" : None, # What was requested [{ Reference(CarePlan|ImmunizationRecommendation|MedicationRequest|NutritionOrder|ServiceRequest) }]
                    "status" : "registered", # R!  registered | partial | preliminary | final +
                    "category" : res["CATEGORY"], # Service category
                    "code" :  res["DESCRIPTION"], # R!  Name/Code for this diagnostic report
                    "subject" : res["SUBJECT_ID"], # The subject of the report - usually, but not always, the patient
                    "encounter" : res["HADM_ID"], # Health care event when test ordered
                    # effective[x]: Clinically relevant time/time-period for report. One of these 2:
                    "effectiveDateTime" : None,
                    "effectivePeriod" : None,
                    "issued" : res["CHARTDATE"], # DateTime this version was made
                    "performer" : None, # Responsible Diagnostic Service
                    "resultsInterpreter" : None, # Primary result interpreter
                    "specimen" : None, # Specimens this report is based on
                    "result" : None, # Observations
                    "imagingStudy" : None, # Reference to full details of imaging associated with the diagnostic report
                    "media" : [{ # Key images associated with this report
                        "comment" : None, # Comment about the image (e.g. explanation)
                        "link" : None # R!  Reference to the image source
                    }],
                    "conclusion" : None, # Clinical conclusion (interpretation) of test results
                    "conclusionCode" : None, # Codes for the clinical conclusion of test results
                    "presentedForm" : res["TEXT"] # Entire report as issued
            }

            report_res.append(report_json)
        return report_res