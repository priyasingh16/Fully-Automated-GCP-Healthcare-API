import datetime
import glob
import json
import re
import ast
from utils import getvalue, periodToHours
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from AutoEncoder import Autoencoder
from scipy.sparse import csr_matrix
from sklearn.preprocessing import OneHotEncoder

class FHIRprocessor:  
    @staticmethod
    def medication_processor(paths, num_epochs, num_embedding=500, batch_size=256):
        medication_info = {}
        for path in paths:
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
                    elif len(re.findall("\d*\.?\d*-\d*\.?\d*", quantity)) > 0:
                        quantity = re.findall("\d*\.?\d*-\d*\.?\d*", quantity)[0]
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

        feature_dict = {}
        row = []
        columns = []
        data = []
        feature_index = 0
        row_index = 0
        medication_info_row_mapping = {}

        for subject_id in medication_info:
            medication_info_row_mapping[subject_id] = {}
            for hospital_id in medication_info[subject_id]:
                for feature in medication_info[subject_id][hospital_id]:

                    if feature not in feature_dict:
                        feature_dict[feature] = feature_index
                        feature_index = feature_index + 1
                        
                    row.append(row_index)
                    columns.append(feature_dict[feature])
                    data.append(medication_info[subject_id][hospital_id][feature])

                medication_info_row_mapping[subject_id][hospital_id] = row_index
                row_index += 1

        sparse_matrix = csr_matrix((data, (row, columns)), shape=(row_index, feature_index))


        inp_shape = sparse_matrix.shape[1]
        textAutoEncoder = Autoencoder(inputshape = inp_shape, encoding_dim = num_embedding)
        autoencoder, encoder, decoder = textAutoEncoder.Model()


        print("training model")
        X_train, X_test = train_test_split( sparse_matrix , test_size=0.33, random_state=42)
        autoencoder.fit(X_train, X_train,
                        epochs=num_epochs,
                        batch_size=batch_size,
                        shuffle=True,
                        validation_data=(X_test, X_test),
                        verbose = False)

        print("model fit finished")

        medication_auto_encoder_data = {}
        for subject_id in medication_info_row_mapping:
            medication_auto_encoder_data[subject_id] = {}
            for hospital_id in medication_info_row_mapping[subject_id]:
                index = medication_info_row_mapping[subject_id][hospital_id]
                encoded_ouput = encoder.predict(sparse_matrix[index])[0]
                encoded_ouput = [float(a) for a in encoded_ouput]
                medication_auto_encoder_data[subject_id][hospital_id] = encoded_ouput
        print("saving model data")

        return medication_auto_encoder_data

    @staticmethod
    def diagnostics_processor(paths, num_epochs, num_embedding=500, batch_size=256):
        stop_words = set(stopwords.words('english'))
        diagnostics_info = {}
        for path in paths:        
            with open(path, 'r') as fl:
                js_data = json.load(fl)
                js_data = js_data["data"]
                
                for data in js_data:
                    subject_id = data["subject"]
                    hospital_id = data["encounter"]
                    if hospital_id == 'None':
                        continue
                    if subject_id not in diagnostics_info:
                        diagnostics_info[subject_id] = {}
                    if hospital_id not in diagnostics_info[subject_id]:
                        diagnostics_info[subject_id][hospital_id] = ""
                    feature_name = data["category"].lower()
                    diagnostics_info[subject_id][hospital_id] += (feature_name + " " + data["presentedForm"].lower())
                    
        print("text parsing")
        text = []
        for subject_id in diagnostics_info:
            for hadm_id in diagnostics_info[subject_id]:
                words = diagnostics_info[subject_id][hadm_id].lower()
                words = [w for w in words.split() if not w in stop_words]
                text.append(" ".join(words))

        print("text clean up")

        vectorizer = TfidfVectorizer(max_df=0.95, min_df=0.05)
        vector = vectorizer.fit_transform(text)

        print("text tokenization")
        
        inp_shape = vector.shape[1]
        textAutoEncoder = Autoencoder(inputshape = inp_shape, encoding_dim = num_embedding)
        autoencoder, encoder, decoder = textAutoEncoder.Model()


        print("training model")
        X_train, X_test = train_test_split( vector , test_size=0.33, random_state=42)
        autoencoder.fit(X_train, X_train,
                        epochs=num_epochs,
                        batch_size=batch_size,
                        shuffle=True,
                        validation_data=(X_test, X_test))



        diagnostics_transformed_info = {}

        for subject_id in diagnostics_info:
            diagnostics_transformed_info[subject_id] = {}
            for hadm_id in diagnostics_info[subject_id]:
                words = diagnostics_info[subject_id][hadm_id].lower()
                words = [w for w in words.split() if not w in stop_words]
                model_inp = vectorizer.transform([" ".join(words)])
                encoded_ouput = encoder.predict(model_inp)[0]
                encoded_ouput = [float(a) for a in encoded_ouput]
                diagnostics_transformed_info[subject_id][hadm_id] = encoded_ouput
                
        return diagnostics_transformed_info


    @staticmethod
    def observation_processor(paths):
        observation_info_output = {}
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
                        observation_info_output[subject_id] = {}
                    if hospital_id not in observation_info[subject_id]:
                        observation_info[subject_id][hospital_id] = {"abnormal_test_count" : 0, "all_test_count":0}
                    observation_info[subject_id][hospital_id]["abnormal_test_count"] += data["valueInteger"]
                    observation_info[subject_id][hospital_id]["all_test_count"] += data["valueQuantity"]

        for subject_id in observation_info:
            for hospital_id in observation_info[subject_id]:
                abnormal_tc = observation_info[subject_id][hospital_id]["abnormal_test_count"] 
                total_tc = observation_info[subject_id][hospital_id]["all_test_count"] 
                observation_info_output[subject_id][hospital_id] = [abnormal_tc, total_tc]
        return observation_info_output

    @staticmethod
    def procedure_processor(paths):
        procedure_info = {}

        for path in paths:
            with open(path, 'r') as fl:
                js_data = ast.literal_eval(fl.read())
                js_data = ast.literal_eval(js_data['data'].replace("'", "\""))

                if len(js_data) == 0:
                    continue

                for data in js_data:
                    subject_id = data["subject"]
                    hospital_id = data["encounter"]
                    if subject_id not in procedure_info:
                        procedure_info[subject_id] = {}
                    if hospital_id not in procedure_info[subject_id]:
                        procedure_info[subject_id][hospital_id] = {}
                    feature_name = data["performedString"].lower()
                    quantity = periodToHours(data["performedRange"])

                    if feature_name not in procedure_info[subject_id][hospital_id]:
                        procedure_info[subject_id][hospital_id][feature_name] = 0
                    procedure_info[subject_id][hospital_id][feature_name] += quantity

        feature_dict = {}
        row = []
        columns = []
        data = []
        feature_index = 0
        row_index = 0
        procedure_info_row_mapping = {}

        for subject_id in procedure_info:
            procedure_info_row_mapping[subject_id] = {}
            for hospital_id in procedure_info[subject_id]:
                for feature in procedure_info[subject_id][hospital_id]:

                    if feature not in feature_dict:
                        feature_dict[feature] = feature_index
                        feature_index = feature_index + 1

                    row.append(row_index)
                    columns.append(feature_dict[feature])
                    data.append(procedure_info[subject_id][hospital_id][feature])

                procedure_info_row_mapping[subject_id][hospital_id] = row_index
                row_index += 1

        sparse_matrix = csr_matrix((data, (row, columns)), shape=(row_index, feature_index))

        procedure_auto_encoder_data = {}
        for subject_id in procedure_info_row_mapping:
            procedure_auto_encoder_data[subject_id] = {}
            for hospital_id in procedure_info_row_mapping[subject_id]:
                index = procedure_info_row_mapping[subject_id][hospital_id]
                procedure_auto_encoder_data[subject_id][hospital_id] = list(sparse_matrix[index].toarray()[0])

        return procedure_auto_encoder_data

    @staticmethod
    def encounter_processor(paths, num_epochs, num_embedding=500, batch_size=256):
        stop_words = set(stopwords.words('english'))
        encounter_info = {}
        text = []
        code_list = []
        for path in paths:
            with open(path, 'r') as fl:
                js_data = ast.literal_eval(fl.read())
                if len(js_data) == 0:
                    continue
                for data in js_data["data"]:
                    length = periodToHours(data["period"])
                    subject_id = int(data["subject"])
                    hospital_id = int(data["identifier"])
                    if subject_id not in encounter_info:
                        encounter_info[subject_id] = {}
                    if hospital_id not in encounter_info[subject_id]:
                        encounter_info[subject_id][hospital_id] = {}
                    encounter_info[subject_id][hospital_id]["length"] = length
                    # encounter_info[subject_id][hospital_id]["reason_code"] = data["reasonCode"]
                    code_list.append([data["reasonCode"]])
                    diag = " ".join([i["condition"] for i in ast.literal_eval(data["diagnosis"]) if i["condition"] != None]).lower()
                    encounter_info[subject_id][hospital_id]["encounter_diagnosis"] = diag
                    words = [w for w in diag.split() if not w in stop_words]
                    text.append(" ".join(words))
            
        # enc = OneHotEncoder(handle_unknown='ignore')
        # categorical_diagnosis = enc.fit_transform(code_list)

        vectorizer = TfidfVectorizer(max_df=0.95, min_df=0.05)
        vector = vectorizer.fit_transform(text)
        inp_shape = vector.shape[1]

        textAutoEncoder = Autoencoder(inputshape = inp_shape, encoding_dim = num_embedding)
        autoencoder, encoder, decoder = textAutoEncoder.Model()

        X_train, X_test = train_test_split(vector, test_size=0.33, random_state=42)
        autoencoder.fit(X_train, X_train,
                        epochs=num_epochs,
                        batch_size=batch_size,
                        shuffle=True,
                        validation_data=(X_test, X_test),
                        verbose=True)

        ind = 0
        encounter_auto_encoded = {}
        for subject_id in encounter_info:
            for hospital_id in encounter_info[subject_id]:
                words = encounter_info[subject_id][hospital_id]["encounter_diagnosis"].lower()
                words = [w for w in words.split() if not w in stop_words]
                model_inp = vectorizer.transform([" ".join(words)])
                encoded_output = encoder.predict(model_inp)
                encoded_output = [float(i) for i in encoded_output[0]]
                output = [encounter_info[subject_id][hospital_id]["length"]] + encoded_output
                ind += 1
                if subject_id not in encounter_auto_encoded:
                    encounter_auto_encoded[subject_id] = {}
                encounter_auto_encoded[subject_id][hospital_id] = output

        return encounter_auto_encoded

    @staticmethod
    def patient_processor(paths):
        patient_info = {}

        for path in paths:
            with open(path, 'r') as fl:
                js_data = ast.literal_eval(fl.read())
                subject_id = js_data["identifier"]
                if subject_id not in patient_info:
                    patient_info[subject_id] = {}
                patient_info[subject_id]['gender'] = js_data["gender"]
                if js_data["deceasedBoolean"] == '1':
                    patient_info[subject_id]['survived'] = False
                else:
                    patient_info[subject_id]['survived'] = True
        return patient_info

    @staticmethod
    def get_data(subject_id, hospital_id, procedure_output, medication_output, diagnostics_output, observation_output, encounter_output):
        default_medication_len = 100
        default_procedure_len = 11
        default_diagnostics_len = 500
        default_observation_len = 2
        default_encounter_len = 201

        output = []
        medication_data = [0] * default_medication_len
        if subject_id in medication_output and hospital_id in medication_output[subject_id]:
            medication_data = medication_output[subject_id][hospital_id]
        output = output + medication_data

        procedure_data = [0] * default_procedure_len
        if subject_id in procedure_output and hospital_id in procedure_output[subject_id]:
            procedure_data = procedure_output[subject_id][hospital_id]
        output = output + procedure_data

        diagnostics_data = [0] * default_diagnostics_len
        if subject_id in diagnostics_output and hospital_id in diagnostics_output[subject_id]:
            diagnostics_data = diagnostics_output[subject_id][hospital_id]
        output = output + diagnostics_data

        observation_data = [0] * default_observation_len
        if subject_id in observation_output and hospital_id in observation_output[subject_id]:
            observation_data = observation_output[subject_id][hospital_id]
        output = output + observation_data

        encounter_data = [0] * default_encounter_len
        if subject_id in encounter_output and hospital_id in encounter_output[subject_id]:
            encounter_data = encounter_output[subject_id][hospital_id]
        output = output + encounter_data

        return output
