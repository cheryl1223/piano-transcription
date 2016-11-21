import numpy,matplotlib.pyplot as plt, librosa, IPython.display as ipd, urllib, os.path
import scipy
import sys

f0_arr = []
for ai in range(1, len(sys.argv)):
	x,fs = librosa.load(sys.argv[ai], sr=44100)

	X = scipy.fft(x[10000:14096])
	X_mag = numpy.absolute(X)
	f = numpy.linspace(0, fs, 4096)

	maxAmp = X_mag.max()   #max amplitude value
	for i in range(2,4095):
	    if X_mag[i] > X_mag[i-1] and X_mag[i] > X_mag[i+1]:
		if X_mag[i] > 0.28*maxAmp and f[i] > 120:		 		      		 
                    f0_arr.append(f[i])
                    break

l = ['C3','C#3','D3','D#3','E3','F3','F#3','G3','G#3','A3','A#3','B3',
     'C4','C#4','D4','D#4','E4','F4','F#4','G4','G#4','A4','A#4','B4',
     'C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','B5',
     'C6','C#6','D6','D#6','E6','F6','F#6','G6','G#6','A6','A#6','B6']

f = open("f0.txt", "w")
for j in range(len(l)):
  f.write(str(f0_arr[j])+' '+l[j]+' '+str(j+48))
  f.write("\n")
f.close()

