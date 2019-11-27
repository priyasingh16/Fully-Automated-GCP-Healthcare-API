
import glob
import json
import re
import ast
from utils import getvalue
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from AutoEncoder import Autoencoder

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


