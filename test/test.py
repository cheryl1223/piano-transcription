
import sys, csv
from essentia import *
from essentia.standard import *
from pylab import *
from numpy import *


# we're going to work with a file specified as an argument in the command line
try:
    filename = sys.argv[1]
except:
    print "usage:", sys.argv[0], "<audiofile>"
    sys.exit()

# don't forget, we can actually instantiate and call an algorithm on the same line!
print 'Loading audio file...'
audio = MonoLoader(filename = filename)()

od2 = OnsetDetection(method = 'complex')



w = Windowing(type = 'hann')
fft = FFT() # this gives us a complex FFT
c2p = CartesianToPolar() # and this turns it into a pair (magnitude, phase)

pool = Pool()

# let's get down to business
print 'Computing onset detection functions...'
for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
    mag, phase, = c2p(fft(w(frame)))

    pool.add('features.complex', od2(mag, phase))


# Phase 2: compute the actual onsets locations
onsets = Onsets()

print 'Computing onset times...'

onsets_complex = onsets(array([ pool['features.complex'] ]), [ 1 ])

print onsets_complex






# We will use a composite algorithm PredominantMelody, which combines a number of 
# required steps for us. Let's declare and configure it first: 
hopSize = 128
frameSize = 2048
sampleRate = 44100
guessUnvoiced = True # read the algorithm's reference for more details
run_predominant_melody = PitchMelodia(guessUnvoiced=guessUnvoiced,
                                      frameSize=frameSize,
                                      hopSize=hopSize);

# Load audio file, apply equal loudness filter, and compute predominant melody
audio = MonoLoader(filename = filename, sampleRate=sampleRate)()
audio = EqualLoudness()(audio)
pitch, confidence = run_predominant_melody(audio)


n_frames = len(pitch)
print "number of frames:", n_frames
# Visualize output pitch values
fig = plt.figure()
plot(range(n_frames), pitch, 'b')
n_ticks = 10
xtick_locs = [i * (n_frames / 10.0) for i in range(n_ticks)]
xtick_lbls = [i * (n_frames / 10.0) * hopSize / sampleRate for i in range(n_ticks)]
xtick_lbls = ["%.2f" % round(x,2) for x in xtick_lbls]
plt.xticks(xtick_locs, xtick_lbls)
ax = fig.add_subplot(111)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Pitch (Hz)')
suptitle("Predominant melody pitch")
show()
