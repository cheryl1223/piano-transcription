from pylab import *
import scipy.signal.signaltools as sigtool
import numpy, matplotlib.pyplot as plt,  librosa, IPython.display as ipd, urllib, os.path

x = linspace(0,5,1e4)
s, fs = librosa.load('C4.wav', sr=44100)
env = numpy.abs(sigtool.hilbert(s)) # hilbert(s) actually returns the analytical signal

plot(x,s,label='Time Signal')
plot(x,env,label='Envelope')
legend()
show()
