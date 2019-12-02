
import json
from sklearn.model_selection import train_test_split
from SurvivalGenerator import  DataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Input 
from utils import f1_m, precision_m, recall_m

def SurvivalPrediction():
    model = Sequential()
    model.add(Input(shape=(7, 814)))
    model.add(LSTM(200))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc',f1_m,precision_m, recall_m])
    return model

    
def main():
    batch_size = 32                 # Batch size for training.
    epochs = 10                     # Number of epochs to train for.

    with open("data/final_merge_with_len.json") as fp:
        model_data = json.load(fp)
        
    ids = list(model_data.keys())
    del model_data

    X_train, X_test = train_test_split(ids, test_size=0.20, random_state=42)
    model = SurvivalPrediction()
    training_generator = DataGenerator(X_train, batch_size=batch_size, ModelName = 'Survival')
    validation_generator = DataGenerator(X_test, batch_size=batch_size, ModelName = 'Survival')
    model.fit_generator(generator=training_generator, validation_data=validation_generator, epochs=epochs)


if __name__ == "__main__":
    main()