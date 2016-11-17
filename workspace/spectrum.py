import numpy,matplotlib.pyplot as plt, librosa, IPython.display as ipd, urllib, os.path
import scipy
import sys

filename = sys.argv[1]
x,fs = librosa.load(filename,sr=44100)

#ipd.Audio(x, rate=fs)
#print x.shape

X = scipy.fft(x[10000:14096])
X_mag = numpy.absolute(X)
f = numpy.linspace(0, fs, 4096)
plt.plot(f[:1000], X_mag[:1000])
plt.xlabel('Frequency (Hz)')
plt.show()


