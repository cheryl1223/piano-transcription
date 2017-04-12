import numpy as np
import os
from math import floor
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD,Adagrad
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

batch_size = 200
epochs = 5
unit = 500
dropout = 0.001
activation = 'relu'
optimizer = SGD(lr=0.9, decay=1e-5, momentum=0.9, nesterov=True)

X = np.loadtxt("train.txt")
n = floor(X.shape[0]/5)
X_dim = X.shape[1]
X_train = X[0:5*n].reshape(n,5,X_dim,1)
del X
y = np.loadtxt("labels.txt", dtype = int)
y_train = []
for i in range(n):
    y_train.append(y[5*i+2,:])
y_train = np.asarray(y_train)
del y
print ("training shape: ", X_train.shape)
print ("label shape: ", y_train.shape)
input_shape = ( 5, 180,1)


model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(1, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(88, activation='softmax'))
model.compile(loss='binary_crossentropy',optimizer=optimizer,metrics=['accuracy'])
print (model.summary())
hist = model.fit(X_train, y_train,batch_size=batch_size,epochs=epochs,validation_split = 0.1)

model.save('cnn.h5')


