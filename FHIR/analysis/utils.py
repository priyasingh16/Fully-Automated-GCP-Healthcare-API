import datetime

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


def getvalue(s):
    try:
        return float(s)
    except ValueError:
        return "false" # because 0 is also false but here in this case 0 is a valid value

def periodToHours(s):
    date1 = datetime.datetime.strptime(s.split(" - ")[0], "%Y-%m-%d %H:%M:%S") 
    date2 = datetime.datetime.strptime(s.split(" - ")[1], "%Y-%m-%d %H:%M:%S") 
    length = (date2 - date1)
    length = length.days*24 + length.seconds/3600
    return float(length)

