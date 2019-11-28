import datetime
import glob
import json
import re
import ast
from utils import getvalue
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from AutoEncoder import Autoencoder
from scipy.sparse import csr_matrix

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

        medication_auto_encoder_data = {}
        for subject_id in medication_info_row_mapping:
            medication_auto_encoder_data[subject_id] = {}
            for hospital_id in medication_info_row_mapping[subject_id]:
                index = medication_info_row_mapping[subject_id][hospital_id]
                medication_auto_encoder_data[subject_id][hospital_id] = encoder.predict(sparse_matrix[index])

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
                encoded_ouput = encoder.predict(model_inp)
                diagnostics_transformed_info[subject_id][hadm_id] = list(encoded_ouput)

                
        return diagnostics_transformed_info


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
                    observation_info[subject_id][hospital_id]["abnormal_test_count"] += data["valueInteger"]
                    observation_info[subject_id][hospital_id]["all_test_count"] += data["valueQuantity"]

        return observation_info

    @staticmethod
    def encounter_processor(paths, num_epochs, num_embedding=500, batch_size=256):
        stop_words = set(stopwords.words('english'))
        encounter_info = {}
        text = []
        for path in paths:
            with open(path, 'r') as fl:
                js_data = ast.literal_eval(fl.read())
                for data in js_data["data"]:
                    date1 = datetime.datetime.strptime(data["period"].split(" - ")[0], "%Y-%m-%d %H:%M:%S") 
                    date2 = datetime.datetime.strptime(data["period"].split(" - ")[1], "%Y-%m-%d %H:%M:%S") 
                    length = (date2 - date1)
                    length = length.days*24 + length.seconds/3600
                    subject_id = data["subject"]
                    hospital_id = data["identifier"]
                    if subject_id not in encounter_info:
                        encounter_info[subject_id] = {}
                    if hospital_id not in encounter_info[subject_id]:
                        encounter_info[subject_id][hospital_id] = {}
                    encounter_info[subject_id][hospital_id]["length"] = length
                    encounter_info[subject_id][hospital_id]["reason_code"] = data["reasonCode"]
                    diag = " ".join([i["condition"] for i in ast.literal_eval(data["diagnosis"]) if i["condition"] != None]).lower()
                    encounter_info[subject_id][hospital_id]["encounter_diagnosis"] = diag
                    words = [w for w in diag.split() if not w in stop_words]
                    text.append(" ".join(words))
            
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
                        validation_data=(X_test, X_test))

        for subject_id in encounter_info:
            for hospital_id in encounter_info[subject_id]:
                words = encounter_info[subject_id][hospital_id]["encounter_diagnosis"].lower()
                words = [w for w in words.split() if not w in stop_words]
                model_inp = vectorizer.transform([" ".join(words)])
                encoded_output = encoder.predict(model_inp)
                encounter_info[subject_id][hospital_id]["autoencoded_diagnosis"] = list(encoded_output)
        
        return encounter_info

