import numpy as np
import pickle
import h5py
import os
from keras.optimizers import SGD, Adagrad
from keras.models import load_model, Sequential
from keras.layers import Dense, Activation, Dropout
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

batch_size = 200
epochs = 20
unit = 500
dropout = 0.001
activation = 'relu'
optimizer = SGD(lr=0.9, decay=1e-5, momentum=0.9, nesterov=True)
#optimizer = 'Adagrad'


X = np.loadtxt("train.txt")
y = np.loadtxt("labels.txt", dtype = int)
print ("training dataset shape: ", X.shape)
print ("label shape: ", y.shape)


n_input = X.shape[1]
n_output = y.shape[1]


model = Sequential()
model.add(Dense(unit,input_dim=n_input, activation=activation))
model.add(Dense(unit,input_dim=n_input, activation=activation))
model.add(Dropout(dropout))
model.add(Dense(n_output, activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer=optimizer,metrics=['accuracy'])
print (model.summary())


hist = model.fit(X, y,batch_size=batch_size,epochs=epochs,validation_split = 0.1)

model.save('nn.h5')

