from client import client

class Medication:
    """
    Description
    -----------
    Get relevent information about a paticular medicine
    """

    def __init__(self):
        """
        Description
        -----------
        Initializes google cloud big query client to query FHIR data.
        """
        self.cl = client()

    def get_medication(self, id):
        """
        Description
        -----------
        Extracts Information about all medication in the mimic catalog
        from prescription table.
        Parameters
        ----------
        id : Integer
            Subject id of the patient to fetch prescription record.
        Returns
        ----------
        medicine_res : list
            list of dicts which contains information about a particular drug
        """

        query_string = """SELECT DRUG_NAME_GENERIC, FORMULARY_DRUG_CD, NDC, PROD_STRENGTH, 
            DOSE_VAL_RX, FORM_UNIT_DISP FROM `green-gasket-256323.mimiciii_fullyautomated.PRESCRIPTIONS`
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


        medicine_res = []
        for res in r:
            medicine_info = {
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

            medicine_res.append(medicine_info)
        return medicine_res
