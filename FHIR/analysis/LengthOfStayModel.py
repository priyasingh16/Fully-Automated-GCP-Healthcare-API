import json
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input 
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


def process_model_data():
    with open("data/final_merge.json") as fp:
        model_data = json.load(fp)
    with open("data/encounter_output.json") as fp:
        encounter_output = json.load(fp)

    X = []
    Y = []
    for subject_id in encounter_output:
        for hospital_id in encounter_output[subject_id]:
            X.append(model_data[subject_id][hospital_id])
            Y.append(encounter_output[subject_id][hospital_id][0])
    return np.array(X), np.array(Y)


def length_of_stay_model():
    model = Sequential()
    model.add(Dense(500, kernel_initializer='normal', activation='relu'))
    model.add(Dense(100, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


def main():
    X,Y = process_model_data()
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
    
    model = length_of_stay_model()
    model.fit(X_train, y_train,
              batch_size=64, epochs=150,
              validation_data=(X_test, y_test),
              verbose=True)
    
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    print("Mean Square Error train :", mean_squared_error(y_train, y_pred_train))
    print("Mean Square Error test :", mean_squared_error(y_test, y_pred_test))

    print("R2 score train :", r2_score(y_train, y_pred_train))
    print("R2 score test :", r2_score(y_test, y_pred_test))

    print("Mean Square Error train :", mean_absolute_error(y_train, y_pred_train))
    print("Mean Square Error test :", mean_absolute_error(y_test, y_pred_test))


if __name__ == "__main__":
    main()
