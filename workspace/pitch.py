# first, we need to import our essentia module. It is aptly named 'essentia'!

# as there are 2 operating modes in essentia which have the same algorithms,
# these latter are dispatched into 2 submodules:

import essentia.standard
import essentia.streaming

# pylab contains the plot() function, as well as figure, etc... (same names as Matlab)
from pylab import plot, show, figure, imshow
import matplotlib.pyplot as plt

import sys
filename = sys.argv[1]
# let's have a look at what is in there

# print dir(essentia.standard)

# you can also do it by using autocompletion in IPython, typing "essentia.standard." and pressing Tab

# Essentia has a selection of audio loaders:
#
#  - AudioLoader: the basic one, returns the audio samples, sampling rate and number of channels
#  - MonoLoader: which returns audio, down-mixed and resampled to a given sampling rate
#  - EasyLoader: a MonoLoader which can optionally trim start/end slices and rescale according
#                to a ReplayGain value
#  - EqloudLoader: an EasyLoader that applies an equal-loudness filtering on the audio
#

# we start by instantiating the audio loader:
loader = essentia.standard.MonoLoader(filename=filename)

# and then we actually perform the loading:
audio = loader()
# audio = audio[1*44100:10*44100]

# by default, the MonoLoader will output audio with 44100Hz samplerate

window = essentia.standard.Windowing(type = 'hann')
spectrum = essentia.standard.Spectrum()  # FFT() would return the complex FFT, here we just want the magnitude spectrum
pitch_yin_fft = essentia.standard.PitchYinFFT()

# help(essentia.standard.FFT)
index = 0
pitches = []

for frame in essentia.standard.FrameGenerator(audio, frameSize = 2048, hopSize = 512):
	# mfcc_bands, mfcc_coeffs = mfcc(spectrum(window(frame)))
	# mfccs.append(mfcc_coeffs)
	pitch, pitch_confidence = pitch_yin_fft(spectrum(window(frame)))
	
	if pitch < 800:
		pitches.append(pitch)

	index = index + 1

print pitches

# transpose to have it in a better shape
# we need to convert the list to an essentia.array first (== numpy.array of floats)

# mfccs = essentia.array(mfccs).T

# and plot
# imshow(mfccs[1:,:], aspect = 'auto')

# show() # unnecessary if you started "ipython --pylab"
