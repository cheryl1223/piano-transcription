import sys, csv
from essentia import *
from essentia.standard import *
from pylab import *
from numpy import *

try:
    filename = sys.argv[1]
except:
    print "usage:", sys.argv[0], "<audiofile>"
    sys.exit()

print 'Loading audio file...'
audio = MonoLoader(filename = filename)()
od = OnsetDetection(method = 'complex')
w = Windowing(type = 'hann')
fft = FFT()
c2p = CartesianToPolar()
pool = Pool()


for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
    mag, phase, = c2p(fft(w(frame)))
    pool.add('features.complex', od(mag, phase))

onsets = Onsets()
onsets_complex = onsets(array([ pool['features.complex'] ]), [ 1 ])

f = open('onsets.txt','w')
for i in range(len(onsets_complex)):
    temp = onsets_complex[i]
    f.write("%s\n"%str(temp))
f.close()



