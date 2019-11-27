
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model

class Autoencoder:
    
    def __init__(self, inputshape, encoding_dim=100):
        self.inputshape = inputshape
        self.encoding_dim = encoding_dim


    def Model(self):
        input_img = Input(shape=(self.inputshape,))
        encoded = Dense(self.encoding_dim, activation='relu')(input_img)
        decoded = Dense(self.inputshape, activation='sigmoid')(encoded)
        
        autoencoder = Model(input_img, decoded)
        encoder = Model(input_img, encoded)
        encoded_input = Input(shape=(self.encoding_dim,))
        decoder_layer = autoencoder.layers[-1]
        decoder = Model(encoded_input, decoder_layer(encoded_input))

        autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=["acc"])
        return autoencoder , encoder, decoder

