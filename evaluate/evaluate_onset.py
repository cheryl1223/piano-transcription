import numpy as np 
import math
import sys, os
from math import floor
from mir_eval import multipitch, onset
def onset_eval(ref_onsets, est_onsets):
    
    #print(onset.f_measure(ref_onsets, est_onsets, window=0.05))
    print(onset.evaluate(ref_onsets, est_onsets, window=0.1))
def main():
    os.system("CNNOnsetDetector single %s -o onsets.txt"%sys.argv[1])
    filename = sys.argv[1].split(".")[0]
    labels = np.loadtxt('%s_labels.txt'%filename, dtype = int) #.txt    
    f = open('%s.txt'%filename)
    ref_onsets = []
    ref_offsets = []
    ref_midinotes = []
    n = 0
    for line in f:
        if line.strip():
            if n != 0:
                x = line.strip()
                info = x.split('\t')
                ref_onsets.append(float(info[0]))
                ref_offsets.append(float(info[1]))
                ref_midinotes.append(int(info[2]))
        n = n + 1

    est_onsets = np.loadtxt("onsets.txt")

    ref_onsets = np.unique(np.array(ref_onsets))
    est_onsets = np.unique(est_onsets)
    print(est_onsets.shape)
    print( ref_onsets.shape)

    onset_eval(ref_onsets, est_onsets)
if __name__ == '__main__':
    main() 