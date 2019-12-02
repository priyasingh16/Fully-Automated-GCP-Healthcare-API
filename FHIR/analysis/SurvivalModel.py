
import json
from sklearn.model_selection import train_test_split
from SurvivalGenerator import  DataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Input 
from tensorflow.keras import backend as K

def recall_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

def precision_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))


def SurvivalPrediction():
    model = Sequential()
    model.add(Input(shape=(7, 814)))
    model.add(LSTM(200))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc',f1_m,precision_m, recall_m])
    return model

    
def main():
    batch_size = 32                 # Batch size for training.
    epochs = 100                    # Number of epochs to train for.
    hidden_state_dim = 200          # dimensionality of the hidden space.
    data_path = 'data/fra.txt'      # data Path "question'\t'answer" format

    with open("/home/monica/Documents/NEU/DataViz/data/final_merge_with_len.json") as fp:
        model_data = json.load(fp)

    ids = list(model_data.keys())
    del model_data

    X_train, X_test = train_test_split(ids, test_size=0.20, random_state=42)
    model = SurvivalPrediction()
    training_generator = DataGenerator(X_train, batch_size=batch_size)
    print("training_generator", training_generator)
    validation_generator = DataGenerator(X_test, batch_size=batch_size)
    model.fit_generator(generator=training_generator, validation_data=validation_generator, epochs=epochs)


if __name__ == "__main__":
    main()