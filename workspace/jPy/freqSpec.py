import seaborn
import numpy, scipy, matplotlib.pyplot as plt, pandas, librosa, IPython.display as ipd, urllib, os.path
import sys

x,fs = librosa.load(sys.argv[1], sr=44100)
#ipd.Audio(x, rate=fs)
#print x.shape

X = scipy.fft(x[20000:24096])
X_mag = numpy.absolute(X)
f = numpy.linspace(0, fs, 4096)
plt.plot(f[:1000], X_mag[:1000]) 
plt.xlabel('Frequency (Hz)')
plt.show()


