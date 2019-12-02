import numpy as np
from tensorflow import keras
import json

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, batch_size=32, ModelName ="Survival", shuffle=True):
        'Initialization'
        self.batch_size = batch_size
        self.list_IDs = list_IDs
        self.shuffle = shuffle
        self.ModelName = ModelName
        self.on_epoch_end()

        with open("data/final_merge_with_len.json") as fp:
            self.model_data = json.load(fp)

        with open("data/patient_output.json") as fp:
            self.patient_output = json.load(fp)

        with open("data/readmission_output.json") as fp:
            self.readmission_output = json.load(fp)

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]
        # Generate data
        if self.ModelName == "Survival":
            X,y = self.__data_generation_patient(list_IDs_temp)
        elif self.ModelName == "Readmission":
            X,y = self.__data_generation_readmission(list_IDs_temp)
        else:
            X,y = self.__data_generation_patient(list_IDs_temp)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation_readmission(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        X = []
        Y = []
        for subject_id in list_IDs_temp:
            xseq = []
            oldseq = []
            newseq = []
            count = 0
            for hospital_id in self.model_data[subject_id]:
                count = count + 1
                xseq = (self.model_data[subject_id][hospital_id])
                newseq.append(xseq)
                oldseq.append(xseq)
                for _ in range(count, 7):
                    newseq.append([0] * 814)
                if count == 7:
                    break
                X.append(newseq)
                Y.append(int(self.readmission_output[subject_id][hospital_id]))
                newseq = oldseq[:]

        return np.array(X), np.array(Y)
    
    def __data_generation_re_one_peid(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        X = []
        Y = []
        for subject_id in list_IDs_temp:
            seq = []
            count = 0
            for hospital_id in self.model_data[subject_id]:
                count = count + 1
                seq.append(self.model_data[subject_id][hospital_id])
                if count == 7:
                    break
            for _ in range(count, 7):
                seq.append([0] * 814)
            X.append(seq)
            val = 0
            if len(self.readmission_output[subject_id]) > 1:
                val = 1
            Y.append(val)

        return np.array(X), np.array(Y)

    def __data_generation_patient(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        X = []
        Y = []
        for subject_id in list_IDs_temp:
            seq = []
            count = 0
            for hospital_id in self.model_data[subject_id]:
                count = count + 1
                seq.append(self.model_data[subject_id][hospital_id])
                if count == 7:
                    break
            for _ in range(count, 7):
                seq.append([0] * 814)
            X.append(seq)
            Y.append(int(self.patient_output[subject_id]["survived"]))

        return np.array(X), np.array(Y)