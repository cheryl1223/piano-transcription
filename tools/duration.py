from midiutil.MidiFile import MIDIFile
from method1 import *
from method2 import *
import math
#get duration and tempo from onsets file
f = open("onsets.txt","r")
onsets = list()

for line in f:
    line = line.rstrip('\n')
    onsets.append(float(line))
f.close()

duration = list()
for i in range(len(onsets)-2):
    duration.append(onsets[i+1]-onsets[i])

min_duration = min(duration)
tempo = round(1.0/min_duration * 60)

for i in range(len(duration)):
    temp = duration[i]
    duration[i] = math.ceil(temp/min_duration)
duration.append(0.5)
output = MIDIFile(1)
track = 0
channel = 0
volume = 100
output.addTrackName(track,0,"Track 0")
output.addTempo(track,0,tempo)
import os,sys
# Now add the note.
cur_time = 0

for i in range(len(duration)):
    detector1 = Highest_Peaks_MIDI_Detector('frames/note%s.wav'%i)
    notes1 = detector1.detect_MIDI_notes()
    detector2 = MIDI_Detector('frames/note%s.wav'%i)
    notes2 = detector2.detect_MIDI_notes()
    midi_notes = set(notes1).intersection(notes2)
    print midi_notes
    if len (midi_notes) == 0:
        output.addNote(track,channel,0,cur_time,duration[i],0) 
    else:
		for note in midi_notes:
		    if note <90 and note > 72:
		        output.addNote(track,channel,note,cur_time,duration[i],volume)
		    else:
		        output.addNote(track,channel,note,cur_time,duration[i],volume-20) 

    cur_time += duration[i]
# And write it to disk.
f = open("output.mid", 'wb')
output.writeFile(f)
f.close()
