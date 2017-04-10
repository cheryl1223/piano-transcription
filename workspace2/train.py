import numpy as np
import json
import h5py
import os
from keras.models import load_model, Sequential
from keras.layers import Dense, Activation, Dropout

class MetaModel(type):

    method_to_model = {}

    def __init__(self, name, bases, attrs):
        if self._name is not None:
            self.method_to_model[self._name] = self

    def __new__(meta, name, bases, attrs):
        return type.__new__(meta, name, bases, attrs)

class Model(object):

    __metaclass__ = MetaModel
    _name = None
    _description = None

    def __init__(self):
        self.model = None
        self.parameters = {}

    def fit(self, X, y):
        pass

    def save(self, filename):
        pass

    def _save_metadata(self, filename):
        filename, ext = os.path.splitext(filename)

        with open(filename + '.meta', 'w') as f:
            json.dump(self.parameters, f, indent=4)

    def predict(self, inp):
        return self.model.predict(inp)

    def load(self, filename):
        pass

    def _load_metadata(self, filename):
        filename, ext = os.path.splitext(filename)

        with open(filename + '.meta', 'r') as f:
            self.parameters = json.load(f)

class NeuralNetwork(Model):
    def __init__(self):
        super(NeuralNetwork, self).__init__()

        self.parameters = {
            'layer': 3,
            'unit': 150,
            'dropout': 0.0,
            'activation': 'relu',
            'optimizer': 'sgd',
            'threshold': 0.5,
            'epoch': 100,
        }

    def fit(self, X, y):
        if self.model is None:
            self._build_model(X.shape[1], y.shape[1])

        self.model.fit(X, y, epochs=self.parameters['epoch'])

    def fit_generator(self, generator):
        X, y = generator().next()
        self._build_model(X.shape[1], y.shape[1])

        self.model.fit_generator(generator(), samples_per_epoch=50000, epochs=self.parameters['epoch'])

    def save(self, output):
        self.model.save(output)

        self._save_metadata(output)

    def predict(self, X):
        y = self.model.predict(X)

        y[y > self.parameters['threshold']] = 1
        y[y <= self.parameters['threshold']] = 0

        return y.astype(int)

    def load(self, filename):
        self.model = load_model(filename)
        self._load_metadata(filename)

    def _build_model(self, n_input, n_output):
        self.model = Sequential()

        self.model.add(
            Dense(
                self.parameters['unit'],
                input_dim=n_input, activation=self.parameters['activation']))

        for i in range(self.parameters['layer'] - 1):
            self.model.add(
                Dense(
                    self.parameters['unit'],
                    activation=self.parameters['activation']))
            if self.parameters['dropout'] > 0.0001:
                self.model.add(
                    Dropout(self.parameters['dropout']))

        self.model.add(
            Dense(n_output, activation='sigmoid'))

        self.model.compile(
            loss='binary_crossentropy',
            optimizer=self.parameters['optimizer'],
            metrics=[])



def main():
    
    X = np.loadtxt("train.txt")
    y = np.loadtxt("labels.txt", dtype = int)
    print (X.shape)
    print (y.shape)
    nn = NeuralNetwork()
    nn.fit(X,y)
    nn.save('nn')

if __name__ == '__main__':
    main()
