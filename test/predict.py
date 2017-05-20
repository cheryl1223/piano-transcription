from keras.models import load_model
import numpy as np
import sys,os
import matplotlib.pyplot as plt

#os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

filename = sys.argv[1].split(".")[0]
os.system("python3 transform.py %s.wav"%filename)
nn = load_model('../models/nn.h5')
#print(nn.summary())
from keras.utils import plot_model
plot_model(nn, to_file='nn.png')
X = np.loadtxt("%s_transform.txt"%filename)

#print(nn.predict(X).shape)

y = nn.predict(X)
#print (y[0])



y[y > 0.5] = 1
y[y <= 0.5] = 0
y.astype(int)

np.savetxt("result.txt", y, fmt = "%4f")