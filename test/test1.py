from essentia.standard import *
from pylab import *
from numpy import *
import numpy as np

from matplotlib.pylab import *

loader = MonoLoader(filename = 'piano.wav')
audio = loader()
w = Windowing(type = 'hann')
spectrum = Spectrum()
i = 0
pitch_array = [] # Stores the pitch values in a list
filtered_pitch_array = []

hopSize = 512
frameSize = 2048
sampleRate = 44100.
time = np.linspace(0, len(audio)/sampleRate, num = len(audio))
frame_to_time_2 = []
local_time = 0


run_equal_loudness = EqualLoudness(sampleRate=sampleRate)
run_pitchContourSegmentation = PitchContourSegmentation (hopSize=hopSize)
pitch_detect = PitchYinFFT(frameSize = frameSize, sampleRate = sampleRate)
filtered_audio = run_equal_loudness(audio)

for frame in FrameGenerator(audio, frameSize, hopSize):
    spec = spectrum(w(frame))
    pitch, pitchConfidence = pitch_detect(spec)
    pitch_array.append(pitch)
    frame_to_time_2.append(local_time)
    local_time += hopSize / sampleRate # Obtaining the time array

#Prints pitch and pitch confidece values for each frame
for i in range(1024):
    print "pitch", i, ":", pitch_array [i], "pitch confidence:", pitchConfidence

#Original Audio
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(221)
ax1.plot(time,audio)
grid()
xlabel('time')
title('Original Audio')

#Filtered Audio through EqualLoudness
fig2 = plt.figure(1)
ax2 = fig2.add_subplot(222)
ax2.plot(time,filtered_audio)
grid()
xlabel('time')
title('Filtered Signal')

#Pitch Values
fig3 = plt.figure(1)
ax3 = fig3.add_subplot(223)
ax3.plot(frame_to_time_2,pitch_array)
grid()
xlabel('time')
ylabel('frequency(Hz)')
title('Detected Pitch Values')

for frame in FrameGenerator(filtered_audio, frameSize, hopSize):
    spec = spectrum(w(frame))
    pitch, pitchConfidence = pitch_detect(spec)
    filtered_pitch_array.append(pitch)

#Pitch Contour Segmentation
onset,duration,MIDIpitch = run_pitchContourSegmentation(filtered_pitch_array, audio) # Extracts onset,duration,MIDIpitch parameters

for i in range(len(onset)):
    print "onset", i, ":", onset[i], "duration:", duration[i], "MIDIpitch", MIDIpitch[i]

#Pitch Values of Filtered Audio
fig4 = plt.figure(1)
ax4 = fig4.add_subplot(224)
ax4.plot(frame_to_time_2,filtered_pitch_array)
grid()
xlabel('time')
ylabel('frequency(Hz)')
title('Detected Pitch Values of Filtered Signal')

show()

