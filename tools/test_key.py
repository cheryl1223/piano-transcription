import numpy
import librosa
import scipy
import sys, os.path
import operator
peaks = dict()
sample_rate = 44100
frame_size = 4096
noise_threshold = 0.2
max_frequency = 2000
f = open("test_key.txt","w")
for ai in range(1, len(sys.argv)):
    x,fs = librosa.load(sys.argv[ai], sr=44100)
    X = scipy.fft(x[0:4096])
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

