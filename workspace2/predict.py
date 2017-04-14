from keras.models import load_model
import numpy as np
import sys,os
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

filename = sys.argv[1].split(".")[0]
os.system("python3 transform.py %s.wav"%filename)
nn = load_model('nn.h5')
print(nn.summary())

X = np.loadtxt("%s_transform.txt"%filename)
for i in range(len(X)):
    X[i] = X[i].reshape(-1,180)
print(nn.predict(X).shape)

y = nn.predict(X)
print (y[0])


'''
y[y > 0.95] = 1
y[y <= 0.95] = 0
y.astype(int)
'''
np.savetxt("result.txt", y, fmt = "%4f")