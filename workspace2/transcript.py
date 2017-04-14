from midiutil.MidiFile import MIDIFile
import math
import numpy as np
import sys, os
import matplotlib.pyplot as plt
from operator import itemgetter, attrgetter  



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
    notes = []
    for i in range(onsets.shape[0]):
        onsets[i] = int(onsets[i]*100)
        #plt.axvline(x=onsets[i],color = 'r')

    for i in range(frames.shape[0]):
        for j in range(frames.shape[1]):
            if frames[i][j] < 0.5:
                frames[i][j] = 0
            else:
                frames[i][j] =1

    for i in onsets:
        i = int(i)
        for n in range(88):
            if (frames[i][n] == 1 or frames[i-1][n]==1 or frames[i+1][n]==1 or frames[i+2][n]==1 or frames[i-2][n]==1): 
                x = i
                while(frames[x][n] == 1):
                    x = x+1
                if (x-i>5):
                    on_time = float(i/100)
                    off_time = float(x/100)

                    notes.append((n+21, on_time, off_time))

    '''
    plt.imshow(frames.transpose())
    plt.show()
    '''


    #notes = notes[np.argsort(notes[:,2])]
    notes = sorted(notes, key=itemgetter(2,0))

    notes_new = []
    for i in range(len(notes)-2):
        if i == 0:
            notes_new.append(notes[i])
        if notes[i+1][0] != notes[i][0]:
            notes_new.append(notes[i+1])

    print (len(notes_new))



    output = MIDIFile(1)
    track = 0
    channel = 0
    volume = 100
    output.addTrackName(track,0,"Track 0")
    for note in notes_new:
        output.addNote(track,channel,note[0],note[1],note[2]-note[1],volume)
    midi = open("output.mid", 'wb')
    output.writeFile(midi)
    midi.close()
if __name__ == '__main__':
    main()
