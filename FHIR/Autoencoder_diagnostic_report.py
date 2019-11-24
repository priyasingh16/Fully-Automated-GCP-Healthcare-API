#!/usr/bin/env python
# coding: utf-8

# In[141]:


import pandas as pd 
import numpy as np
import os
import re
import keras
import nltk
from keras.layers import Input
from keras.layers import Embedding
from keras.layers import GRU
from keras.layers import RepeatVector
from keras.layers import Dense
from keras import optimizers
from keras.models import Model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


# In[48]:


with open("data/labels.txt") as f:
    data = f.read() 


# In[54]:


data = data.split("\n")


# In[70]:


X = [i.split("|")[0] for i in data if len(i.split("|")) == 2]
y = [i.split("|")[1] for i in data if len(i.split("|")) == 2]


# In[139]:


vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)
X_vec.shape


# In[81]:


X_ind = [i for i in range(len(X))]
X_train, X_test, y_train, y_test = train_test_split(X_ind, X_ind, test_size=0.33, random_state=42)


# In[140]:


lr = LogisticRegression().fit((X_vec)[X_train,],np.array(y)[y_train])
print("Score from tf-idf: ", lr.score((X_vec)[X_test,],np.array(y)[y_test]))


# In[142]:


# this is the size of our encoded representations
encoding_dim = 2000  
shape = (X_vec.shape[1],)
# this is our input placeholder
input_img = Input(shape)
# "encoded" is the encoded representation of the input
encoded = Dense(encoding_dim, activation='relu')(input_img)
# "decoded" is the lossy reconstruction of the input
decoded = Dense(shape, activation='sigmoid')(encoded)
# this model maps an input to its reconstruction
autoencoder = Model(input_img, decoded)
# this model maps an input to its encoded representation
encoder = Model(input_img, encoded)
# create a placeholder for an encoded (32-dimensional) input
encoded_input = Input(shape=(encoding_dim,))
# retrieve the last layer of the autoencoder model
decoder_layer = autoencoder.layers[-1]
# create the decoder model
decoder = Model(encoded_input, decoder_layer(encoded_input))
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
autoencoder.fit((X_vec)[X_train,], (X_vec)[X_train,],
                epochs=50,
                batch_size=256,
                shuffle=True,
                validation_data=((X_vec)[X_test,], (X_vec)[X_test,]))


# In[143]:


new_X_train = encoder.predict((X_vec)[X_train,])
new_X_test = encoder.predict((X_vec)[X_test,])

lr = LogisticRegression().fit(new_X_train, np.array(y)[y_train])
print("Score from encoded: ", lr.score(new_X_test,np.array(y)[y_test]))


# In[157]:


sample_example = """
Admission Date:  [**2128-1-25**]              Discharge Date:   [**2128-2-3**]


Service: MEDICINE

Allergies:
Patient recorded as having No Known Allergies to Drugs

Attending:[**First Name3 (LF) 338**]
Chief Complaint:
slow responses, right sided weakness

Major Surgical or Invasive Procedure:
thoracentesis
nasogastric tube placement

History of Present Illness:
86yo right handed man with PMH significant for uncontrolled HTN
and hyperlipidemia who was in his USOH the night of presentation
when he walked to the restroom at 8:30pm. He then sat on the
couch but when his wife called to him to come to dinner, he was
slow to respond, stood but could not walk due to right-sided
weakness and his speech was slurred. She gave him a series of
commands which he performed but his response time was
significantly slowed and she had difficulty understanding his
speech. At this point, she called EMS. He is now transferred
here after CT of the head at OSH showed a 2.5cm x 2.4cm left
thalamic ICH with slight rupture into the
"""


# In[158]:


sample_example.split("Service:")[1].replace("\n", " ").replace("  ", "")


# In[ ]:




