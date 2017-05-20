from keras.models import load_model
import numpy as np
import sys,os
import matplotlib.pyplot as plt
from math import floor
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

filename = sys.argv[1].split(".")[0]
os.system("python3 transform.py %s.wav"%filename)
nn = load_model('../models/cnn.h5')
#print(nn.summary())

X = np.loadtxt("%s_transform.txt"%filename)

n = floor(X.shape[0]/5)
X_dim = X.shape[1]
X_train = X[0:5*n].reshape(n,5,X_dim,1)
#print(nn.predict(X_train).shape)

y = nn.predict(X_train)
#print (y[0])


'''
y[y > 0.95] = 1
y[y <= 0.95] = 0
y.astype(int)
'''
np.savetxt("result.txt", y, fmt = "%4f")