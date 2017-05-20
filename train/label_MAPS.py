"""
    Get labels from MAPS dataset.
    python3 label.py wav/
"""


import numpy as np 
import sys,os
from math import floor
from madmom.audio.signal import FramedSignalProcessor


def frame(wav):    
    proc = FramedSignalProcessor(frame_size = 4096, fps = 100)
    frames = proc(wav)
    frame_time = []
    for i in range(frames.num_frames):
        frame_time.append(0.01*i)
    frame_time = np.array(frame_time)
    return frame_time

def label(filename):
    #filename = sys.argv[1].split(".")[0]
    frames = frame(wav = "%s.wav"%filename)#wav
    labels = np.zeros((frames.shape[0],88),dtype = int)
    with open("%s.txt"%filename,'r') as f:
        n = 0
        for line in f:
            if line.strip():
                if n != 0:
                    x = line.split('\n')
                    info = x[0].split('\t')
                    onset = float(info[0])
                    offset = float(info[1])
                    midinote = int(info[2])
                    on_frame = floor(onset/0.01)
                    off_frame = floor(offset/0.01)
                    note = midinote-21
                    for i in range(on_frame,off_frame):
                        labels[i][note] = 1
            n=n+1
        np.savetxt('%s_labels.txt'%filename, labels, fmt = '%s')

def main():
    MAPS_directory = sys.argv[1]
    n = 0
    for root, dirs, files in os.walk(MAPS_directory):
        for file in files:
            if file.endswith(".txt"):
                filename, suffix = file.split(".")
                print("labelling %s..."%filename)
                label(filename = '%s%s'%(MAPS_directory,filename))
                n = n + 1
    print("labeled %d files" %n)


    


if __name__ == '__main__':
    main()
