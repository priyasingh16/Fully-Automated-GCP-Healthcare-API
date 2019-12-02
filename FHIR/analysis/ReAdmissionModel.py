import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import json
from sklearn.model_selection import train_test_split
from Generator import DataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Input 
from utils import f1_m, precision_m, recall_m


def SurvivalPrediction():
    model = Sequential()
    model.add(Input(shape=(7, 814)))
    model.add(LSTM(20))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc',f1_m,precision_m, recall_m])

    return model

    
def main():
    batch_size = 32                 # Batch size for training.
    epochs = 30                     # Number of epochs to train for.

    with open("data/final_merge_with_len.json") as fp:
        model_data = json.load(fp)
        
    # ids = list(model_data.keys())
    # del model_data

    with open("data/readmission_output.json") as fl:
        data = json.load(fl)

    ids = []
    for s in data:
        if len(data[s]) > 1:
            ids.append(s)
    
    len_ids = len(ids)

    c = 0
    for s in data:
        if len(data[s]) == 1:
            ids.append(s)
            c = c + 1
        if c > len_ids:
            break


    del data

    X_train, X_test = train_test_split(ids, test_size=0.20, random_state=42)
    model = SurvivalPrediction()

    training_generator = DataGenerator(X_train, batch_size=batch_size, ModelName = 'Readmission')
    validation_generator = DataGenerator(X_test, batch_size=batch_size, ModelName = 'Readmission')
    model.fit_generator(generator=training_generator, validation_data=validation_generator, epochs=epochs)



if __name__ == "__main__":
    main()


# 28/492 [>.............................] - ETA: 2:15 - loss: 0.5034 - acc: 0.77752019-12-01 
# 23:51:53.662380: W tensorflow/core/grappler/optimizers/implementation_selector.cc:199] Skipping optimization due to error while loading function 
# libraries: Invalid argument: Functions '__inference___backward_standard_lstm_785_1287_specialized_for_Adam_gradients_lstm_StatefulPartitioned
# Call_grad_StatefulPartitionedCall_at___inference_keras_scratch_graph_1857' and '__inference___backward_cudnn_lstm_344_520' both implement '
# lstm_c6a0dc0f-9b04-4bd0-96e8-1b21f023b0a9' but their signatures do not match.
