#execute: python determineNote.py example.wav

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
        if X_mag[i] > 0.28*maxAmp and f[i] > 120:
            check_f0 = f[i]
            break

file = open("f0.txt",'r')
f0_Arr = []
note_Arr = []
MidiNumArr = []
for line in file:
    x = line.split('\n')
    info = x[0].split(' ')
    f0_Arr.append(float(info[0]))
    note_Arr.append(info[1])
    MidiNumArr.append(float(info[2]))


for j in range(len(f0_Arr)):
    if check_f0 < f0_Arr[j]+4 and check_f0 > f0_Arr[j]-4:	
	print check_f0, note_Arr[j], MidiNumArr[j]
