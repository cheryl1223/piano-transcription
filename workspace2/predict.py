from train import NeuralNetwork
import numpy as np
import sys,os
filename = sys.argv[1]
os.system("python3 transform.py %s"%filename)
nn = NeuralNetwork()
nn.load('nn.save')
X = np.loadtxt("piano_mono.txt")
for i in range(len(X)):
    X[i] = X[i].reshape(-1,180)
print(nn.predict(X).shape)
np.savetxt("result.txt", nn.predict(X), fmt = "%d")