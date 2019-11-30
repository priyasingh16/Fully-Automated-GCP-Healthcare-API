import numpy as np
from tensorflow import keras
import json

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, batch_size=32, shuffle=True):
        'Initialization'
        self.batch_size = batch_size
        self.list_IDs = list_IDs
        self.shuffle = shuffle
        self.on_epoch_end()
        with open("data/final_merge_with_len.json") as fp:
            self.model_data = json.load(fp)

        with open("data/patient_output.json") as fp:
            self.patient_output = json.load(fp)


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
        X, y = self.__data_generation(list_IDs_temp)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_IDs_temp):
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
            for i in range(count, 7):
                seq.append([0] * 814)
            X.append(seq)
            Y.append(int(self.patient_output[subject_id]["survived"]))

        return np.array(X), np.array(Y)