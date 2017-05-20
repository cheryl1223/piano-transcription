from midiutil.MidiFile import MIDIFile
import math
import numpy as np
import sys, os
import matplotlib.pyplot as plt
from operator import itemgetter, attrgetter  
from math import floor
import warnings
warnings.filterwarnings("ignore")

p_onset = 0.7
p_offset = 0.3



def main():
    os.system("python3 predict_cnn.py %s"%sys.argv[1])
    os.system("CNNOnsetDetector single %s -o onsets.txt"%sys.argv[1])
    onsets = np.loadtxt("onsets.txt")
    frames = np.loadtxt("result.txt")
    notes = []
    
    for i in range(onsets.shape[0]):
        onsets[i] = int(onsets[i]*20)
        #plt.axvline(x=onsets[i],color = 'r')
    
    frames = np.loadtxt("result.txt")
    notes = []


    ''' 
    for i in range(frames.shape[0]):
        for j in range(frames.shape[1]):
            if frames[i][j] >= p_onset:
                frames[i][j] = 1

    for i in range(frames.shape[0]):
        for n in range(88):
            if frames[i][n] == 1 and frames[i-1][n]!= 1:
                x = i
                while(x < frames.shape[0] and frames[x][n] >p_offset):
                    x = x+1
                if (x-i>2):
                    on_time = float(i/20)
                    off_time = float(x/20)

                    notes.append((n+21, on_time, off_time))
                    for p in range(i,x):
                        frames[p][n]=1000
    '''

    for i in onsets:
        i = int(i)
        for n in range(88):
            if i+2 < frames.shape[0]:
                if (frames[i][n] >p_onset or frames[i-1][n]>p_onset \
                    or frames[i+1][n]>p_onset or frames[i+2][n]>p_onset or frames[i-2][n]>p_onset\
                    or frames[i+3][n]>p_onset or frames[i-3][n]>p_onset): 
                    x = i
                    while(x < frames.shape[0] and frames[x][n] >p_offset):
                        x = x+1
                    if (x-i>1):
                        on_time = float(i/20)
                        off_time = float(x/20)

                        notes.append((n+21, on_time, off_time))
                        for p in range(i,x):
                            frames[p][n]=1000
        
    plt.imshow(np.transpose(frames)[:,200:400])
    plt.title("final transcription")
    plt.show()
    

    #notes = notes[np.argsort(notes[:,2])]
    notes = sorted(notes, key=itemgetter(2,0))

    notes_new = []
    for i in range(len(notes)-2):
        if i == 0:
            notes_new.append(notes[i])
        if notes[i+1][0] != notes[i][0]:
            notes_new.append(notes[i+1])

    print (notes_new)



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
