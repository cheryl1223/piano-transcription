import numpy as np 
import sys
import os
from math import floor
from frame_time import *
f = open(sys.argv[1])
frames = frame_time(wav = sys.argv[2]).frame()
labels = np.zeros((frames.shape[0],88),dtype = int)
def set_note(onset,offset,midinote):
    on_frame = floor(onset/0.01)
    off_frame = floor(offset/0.01)
    note = midinote-21
    for i in range(on_frame,off_frame):
    	labels[i][note] = 1
n = 0
for line in f:
    if n != 0:
    	x = line.split('\n')
    	info = x[0].split('\t')
    	onset = float(info[0])
    	offset = float(info[1])
    	midinote = int(info[2])
    	set_note(onset,offset,midinote)
    n=n+1

np.savetxt('labels.txt', labels, fmt = '%s')
