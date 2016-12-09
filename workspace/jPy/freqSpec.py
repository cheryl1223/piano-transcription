import numpy, scipy, matplotlib.pyplot as plt
import librosa
import sys

x,fs = librosa.load(sys.argv[1], sr=44100)
X = scipy.fft(x[0:4096])
X_mag = numpy.absolute(X)
f = numpy.linspace(0, fs, 4096)
plt.plot(f[:1000], X_mag[:1000]) 
plt.xlabel('Frequency (Hz)')
plt.show()


