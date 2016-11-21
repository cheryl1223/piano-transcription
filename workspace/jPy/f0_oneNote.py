import numpy,matplotlib.pyplot as plt
import librosa, IPython.display as ipd, urllib, os.path
import scipy
import sys

#f0_arr = []
#for ai in range(1, len(sys.argv)):

x,fs = librosa.load(sys.argv[1], sr=44100)

X = scipy.fft(x[10000:14096])
X_mag = numpy.absolute(X)
f = numpy.linspace(0, fs, 4096)

maxAmp = X_mag.max()   #max amplitude value
for i in range(2,4095):
    if X_mag[i] > X_mag[i-1] and X_mag[i] > X_mag[i+1]:
        if X_mag[i] > 0.28*maxAmp:
            check_f0 = f[i]
            break

print check_f0
print f[0:40]
