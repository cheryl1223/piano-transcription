#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from common import analyze_channels
from common import parabolic as parabolic
from numpy.fft import rfft
from numpy import argmax, mean, diff, log, copy, arange
from matplotlib.mlab import find
from scipy.signal import fftconvolve, kaiser, decimate
from time import time
import operator
import numpy
from pylab import*


def freq_from_autocorr(signal, fs):
    """Estimate frequency using autocorrelation

    Pros: Best method for finding the true fundamental of any repeating wave,
    even with strong harmonics or completely missing fundamental

    Cons: Not as accurate, doesn't work for inharmonic things like musical
    instruments, this implementation has trouble with finding the true peak

    """
    # Calculate autocorrelation (same thing as convolution, but with one input
    # reversed in time), and throw away the negative lags

    signal -= mean(signal)  # Remove DC offset
    signal = signal[0:1024]
    corr = fftconvolve(signal, signal[::-1], mode='full')
    corr = corr[len(corr)/2:]
    print corr[0:1024]
    # Find the first low point
    d = diff(corr)
    start = find(d > 0.001)[0]

    f = numpy.linspace(0, len(corr),len(corr))
    plot(f,corr)
    show()
    # Find the next peak after the low point (other than 0 lag).  This bit is
    # not reliable for long signals, due to the desired peak occurring between
    # samples, and other peaks appearing higher.

    i_peak = argmax(corr[start:]) + start
    i_interp = parabolic(corr, i_peak)[0]

    max_peak = max(corr[start:])
    print max_peak
    peaks= dict()
    for i in range(2,1023):
        if corr[i] > corr[i-1] and corr[i]>corr[i+1] :
            peaks[i]=corr[i]
    
    sorted_peaks = sorted(peaks.items(), key=operator.itemgetter(1),reverse = 1)
    sorted_peaks = [(i[0],fs/i[0]) for i in sorted_peaks][0:4]
    print sorted_peaks
    return fs / i_interp




if __name__ == '__main__':
    try:
        import sys

        def freq_wrapper(signal, fs):
            freq = freq_from_autocorr(signal, fs)
            print '%f Hz' % freq

        files = sys.argv[1:]
        if files:
            for filename in files:
                try:
                    start_time = time()
                    analyze_channels(filename, freq_wrapper)
                    print '\nTime elapsed: %.3f s\n' % (time() - start_time)

                except IOError:
                    print 'Couldn\'t analyze "' + filename + '"\n'
                print ''
        else:
            sys.exit("You must provide at least one file to analyze")
    except BaseException as e:
        print('Error:')
        print(e)
        raise
    finally:
        # Otherwise Windows closes the window too quickly to read
        raw_input('(Press <Enter> to close)')
