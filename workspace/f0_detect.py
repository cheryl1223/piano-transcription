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
		if X_mag[i] > 0.28*maxAmp:
	          f0_arr.append(f[i])
        	  break

f = open("f0.txt", "w");
for f0_i in f0_arr:
  f.write(str(f0_i))
  f.write("\n");
f.close()

#	plt.plot(f[:1000], X_mag[:1000])
#	plt.xlabel('Frequency (Hz)')
#	plt.show()
#print f0_arr



