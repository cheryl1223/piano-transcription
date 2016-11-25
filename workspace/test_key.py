import numpy 
from numpy import fft
from scipy.io.wavfile import read
from pylab import *
import scipy
import sys, os.path
import operator

sample_rate = 44100
frame_size = 4096
noise_threshold = 0.1
max_frequency = 2000
f = open("test_key.txt","w")
for ai in range(1, len(sys.argv)):
    peaks = dict()
    fs, x = read(sys.argv[1]) 
    print x[0:44100]
    print fs
    X = numpy.fft.fft(x[0:4096])
    X_mag = numpy.absolute(X)

    f = numpy.linspace(0, fs, 4096)

    maxAmp = X_mag.max()   #max amplitude value
    for i in range(2,4095):
        if f[i] < max_frequency:
            if X_mag[i] > X_mag[i-1] and X_mag[i] > X_mag[i+1] :
                if X_mag[i] > noise_threshold*maxAmp:
                    peaks[f[i]] = X_mag[i]
        else:
            break    
    
    sorted_peaks = sorted(peaks.items(), key=operator.itemgetter(0))
    print sorted_peaks

