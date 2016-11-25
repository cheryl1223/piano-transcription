import numpy as np
from scipy.fftpack import rfft, irfft, fftfreq
from scipy.io.wavfile import read
sample_rate = 44100
frame_size = 4096
noise_threshold = 0.1
d = 1.0/sample_rate * frame_size
import sys

fs, signal = read(sys.argv[1])
time   = np.linspace(0,d,frame_size)

W = fftfreq(signal.size, d=time[1]-time[0])
print W
f_signal = rfft(signal)

# If our original signal time was in seconds, this is now in Hz    
cut_f_signal = f_signal.copy()
cut_f_signal_upper[(W< 280)] = 0
cut_signal = irfft(cut_f_signal)

cut_f_signal = cut_signal.copy()
cut_f_signal_lower[(W< 250)] = 0
cut_signal = irfft(cut_f_signal)

import pylab as plt
plt.subplot(221)
plt.plot(time,signal)
plt.subplot(222)
plt.plot(W,f_signal)
plt.xlim(0,10)
plt.subplot(223)
plt.plot(W,cut_f_signal)
plt.xlim(0,10)
plt.subplot(224)
plt.plot(time,cut_signal)
plt.show()
