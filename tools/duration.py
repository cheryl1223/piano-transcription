from midiutil.MidiFile import MIDIFile

#get duration and tempo from onsets file
f = open("onsets.txt","r")
onsets = list()

for line in f:
    line = line.rstrip('\n')
    onsets.append(float(line))
f.close()

duration = list()
for i in range(len(onsets)-1):
    duration.append(onsets[i+1]-onsets[i])

min_duration = min(duration)
tempo = round(1.0/min_duration * 60)

for i in range(len(duration)):
    temp = duration[i]
    duration[i] = int(temp/min_duration)

output = MIDIFile(1)
track = 0
channel = 0
volume = 100
output.addTrackName(track,0,"Track 0")
output.addTempo(track,0,tempo)

# Now add the note.
cur_time = 0
for i in range(len(duration)):
    output.addNote(track,channel,60,cur_time,duration[i],volume)
    
    cur_time += duration[i]
# And write it to disk.
f = open("output.mid", 'wb')
output.writeFile(f)
f.close()
