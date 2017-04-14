from midiutil.MidiFile import MIDIFile
import math
import numpy as np
import sys, os



def getDuration(onsets):
    #get duration and tempo from onsets file
    duration = list()
    for i in range(onsets.shape[0]-2):
        duration.append(onsets[i+1]-onsets[i])
    min_duration = min(duration)
    bpm = round(1.0/min_duration * 60)
    for i in range(len(duration)):
        temp = duration[i]
        duration[i] = math.ceil(temp/min_duration)
    duration.append(0.5)
    return duration,bpm


def main():
    os.system("OnsetDetector single %s -o onsets.txt"%sys.argv[1])
    onsets = np.loadtxt("onsets.txt")
    frames = np.loadtxt("result.txt")
    duration,bpm = getDuration(onsets = onsets)
    output = MIDIFile(1)
    track = 0
    channel = 0
    volume = 100
    output.addTrackName(track,0,"Track 0")
    output.addTempo(track,0,bpm)

    # Now add the note.
    cur_time = 0
    for i in range(len(duration)):
        midi_notes = []
        frame = int(onsets[i]*100)
        if frame > frames.shape[0]:
            break
        for j in range(frames.shape[1]):
            if frames[frame][j] == 1:
                midi_notes.append(j+21)
        for note in midi_notes:
            if note <90 and note > 72:
                output.addNote(track,channel,note,cur_time,duration[i],volume)
            else:
                output.addNote(track,channel,note,cur_time,duration[i],volume-20)
        print (midi_notes)
        cur_time += duration[i]

    # And write it to disk.
    midi = open("output.mid", 'wb')
    output.writeFile(midi)
    midi.close()

if __name__ == '__main__':
    main()
