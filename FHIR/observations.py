from client import client
from pprint import pprint


class Observations:
    """
    Description
    -----------
    Observation for a patient's visit to the hospital.
    """
    def __init__(self):
        """
        Description
        -----------
        Initializes google cloud big query client to query FHIR data.
        """
        self.cl = client()

    def get_observations(self, id):
        """
        Description
        -----------
        Extracts observation of a patient in the hospital visits.
        Parameters
        ----------
        id : Integer
            Subject id of the patient to fetch prescription record.
        Returns
        ----------
        procedures_res : list
            list of all the observation for a patient in all visit to the hospital.
        """

        query_string = """SELECT L.SUBJECT_ID, L.HADM_ID, L.ITEMID, COUNT(L.ITEMID) as TOTAL_ITEMCOUNT, COUNT(L.FLAG) AS TOTAL_ABNORMAL, 
            MAX(DL.LABEL) AS LABEL, MAX(DL.FLUID) AS SPECIMEN, MAX(DL.CATEGORY) AS CATEGORY FROM `green-gasket-256323.mimiciii_fullyautomated.LABEVENTS` AS L 
            JOIN `green-gasket-256323.mimiciii_fullyautomated.D_LABITEMS` AS DL ON L.ITEMID = DL.ITEMID WHERE HADM_ID IS NOT NULL AND SUBJECT_ID = {} 
            GROUP BY SUBJECT_ID, HADM_ID, ITEMID;"""
        query_string = query_string.format(id)
        results = self.cl.queryRecords(query_string)

        patient_observation = []
        for row in results:
            res = {}
            for i in row.keys():
                if i not in res:
                    res[i] = None
                if i in res and res[i] == None:
                    res[i] = row[i]
            patient_observation.append(res)
        
        patient_observation_res = []

        for res in patient_observation:
            observation_json = {
                "resourceType" : "Observation",
                # from Resource: id, meta, implicitRules, and language
                # from DomainResource: text, contained, extension, and modifierExtension
                "identifier" : None, # Business Identifier for observation
                "basedOn" : None, # Fulfills plan, proposal or order
                "partOf" : None, # Part of referenced event
                "status" : "registered", # R!  registered | preliminary | final | amended +
                "category" : res["CATEGORY"], # Classification of  type of observation
                "code" : res["ITEMID"], # R!  Type of observation (code / type)
                "subject" : res["SUBJECT_ID"], # Who and/or what the observation is about
                "focus" : res["LABEL"], # What the observation is about, when it is not about the subject of record
                "encounter" : res["HADM_ID"], # Healthcare event during which this observation is made
                # effective[x]: Clinically relevant time/time-period for observation. One of these 4:
                "effectiveDateTime" : None,
                "effectivePeriod" : None,
                "effectiveTiming" : None,
                "effectiveInstant" : None,
                "issued" : None, # Date/Time this version was made available
                "performer" : None, # Who is responsible for the observation
                # value[x]: Actual result. One of these 11:
                "valueQuantity" : res["TOTAL_ITEMCOUNT"],
                "valueCodeableConcept" : None,
                "valueString" : None,
                "valueBoolean" : None,
                "valueInteger" : res["TOTAL_ABNORMAL"],
                "valueRange" : None,
                "valueRatio" : None,
                "valueSampledData" : None,
                "valueTime" : None,
                "valueDateTime" : None,
                "valuePeriod" : None,
                "dataAbsentReason" : None, # C? Why the result is missing
                "interpretation" : None, # High, low, normal, etc.
                "note" : None, # Comments about the observation
                "bodySite" : None, # Observed body part
                "method" : None, # How it was done
                "specimen" : res["SPECIMEN"], # Specimen used for this observation
                "device" : None, # (Measurement) Device
                "referenceRange" : [{ # Provides guide for interpretation
                    "low" : None, # C? Low Range, if relevant
                    "high" : None, # C? High Range, if relevant
                    "type" : None, # Reference range qualifier
                    "appliesTo" :None, # Reference range population
                    "age" : None, # Applicable age range, if relevant
                    "text" : None # Text based reference range in an observation
                }],
                "hasMember" : None, # Related resource that belongs to the Observation group
                "derivedFrom" :None, # Related measurements the observation is made from
                "component" : [{ # Component results
                    "code" : res["ITEMID"], # R!  Type of component observation (code / type)
                    # value[x]: Actual component result. One of these 11:
                    "valueQuantity" : None,
                    "valueCodeableConcept" : None,
                    "valueString" : None,
                    "valueBoolean" : None,
                    "valueInteger" : None,
                    "valueRange" : None,
                    "valueRatio" : None,
                    "valueSampledData" : None,
                    "valueTime" : None,
                    "valueDateTime" : None,
                    "valuePeriod" : None,
                    "dataAbsentReason" : None, # C? Why the component result is missing
                    "interpretation" : None, # High, low, normal, etc.
                    "referenceRange" : None # Provides guide for interpretation of component result
                }]
            }
            patient_observation_res.append(observation_json)
        return patient_observation_res