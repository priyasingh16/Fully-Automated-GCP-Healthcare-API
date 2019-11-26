
import glob
import json
import re
import ast
from utils import getvalue

class FHIRprocessor:
    @staticmethod
    def medication_processor(paths):
        medication_info = {}
        # count = 0
        for path in paths:
            # count = count + 1
            # if count % 10 == 0:
            #     print(count)
                
            with open(path, 'r') as fl:
                js_data = ast.literal_eval(fl.read())
                js_data = ast.literal_eval(js_data['data'].replace("'" , "\""))
                
                for data in js_data:
                    subject_id = data["subject"]
                    hospital_id = data["context"]
                    if subject_id not in medication_info:
                        medication_info[subject_id] = {}
                    if hospital_id not in medication_info[subject_id]:
                        medication_info[subject_id][hospital_id] = {}
                    drug = str(data["medicationCodeableConcept"]).lower()
                    quantity = "".join(data["quantity"].split())
                    quantity_value = getvalue(quantity)
                    
                    # equating to string false because 0 is a valid value but is considered false
                    if quantity_value != "false": 
                        quantity = quantity_value
                    elif re.findall("\d*\.?\d*-\d*\.?\d*", quantity):
                        quantity = quantity.split("-")
                        quantity = list(map(getvalue, quantity))
                        quantity = sum(quantity) / len(quantity)
                    else:
                        quantity = 1
                    unit = ""
                    if data["note"] is not None:
                        unit = str(data["note"].split()[-1]).lower()
                    feature_name = drug + "_" + unit
                    if feature_name not in medication_info[subject_id][hospital_id]:
                        medication_info[subject_id][hospital_id][feature_name] = 0
                    medication_info[subject_id][hospital_id][feature_name] += quantity
        return medication_info

    @staticmethod
    def observation_processor(paths):
        observation_info = {}

        for path in paths:
            with open(path, 'r') as fl:
                js_data = ast.literal_eval(fl.read())
                js_data = ast.literal_eval(js_data['data'].replace("'" , "\""))
                for data in js_data:
                    subject_id = data["subject"]
                    hospital_id = data["encounter"]
                    if subject_id not in observation_info:
                        observation_info[subject_id] = {}
                    if hospital_id not in observation_info[subject_id]:
                        observation_info[subject_id][hospital_id] = {"abnormal_test_count" : 0, "all_test_count":0}
                    else:
                        observation_info[subject_id][hospital_id]["abnormal_test_count"] += data["valueInteger"]
                        observation_info[subject_id][hospital_id]["all_test_count"] += data["valueQuantity"]

        return observation_info

    # @staticmethod
    # def diagnostics_processor(paths):
        



