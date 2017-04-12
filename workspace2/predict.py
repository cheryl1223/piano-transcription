from train import NeuralNetwork
import numpy as np
import sys,os
filename = sys.argv[1].split(".")[0]
os.system("python3 transform.py %s.wav"%filename)
nn = NeuralNetwork()
nn.load('nn')
print(nn.model.summary())
X = np.loadtxt("%s_transform.txt"%filename)
for i in range(len(X)):
    X[i] = X[i].reshape(-1,180)
print(nn.predict(X).shape)

y = nn.model.predict(X)
y[y > 0.4] = 1
y[y <= 0.4] = 0
y.astype(int)
np.savetxt("result.txt", y, fmt = "%d")