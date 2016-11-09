from mido import Message, MidiFile, MidiTrack
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
for frame in FrameGenerator(filtered_audio, frameSize, hopSize):
    spec = spectrum(w(frame))
    pitch, pitchConfidence = pitch_detect(spec)
    filtered_pitch_array.append(pitch)
onset,duration,MIDIpitch = run_pitchContourSegmentation(filtered_pitch_array, audio) # Extracts onset,duration,MIDIpitch parameters

for i in range(len(onset)):
    print "onset", i, ":", onset[i], "duration:", duration[i], "MIDIpitch", MIDIpitch[i]
outfile = MidiFile()

track = MidiTrack()
outfile.tracks.append(track)

track.append(Message('program_change', program=12))
note = MIDIpitch
delta = 200
for i in range(len(note)):
    track.append(Message('note_on', note=int(note[i]), velocity=100, time=delta))
    track.append(Message('note_off', note=int(note[i]), velocity=100, time=delta))
    
outfile.save('test.mid')
