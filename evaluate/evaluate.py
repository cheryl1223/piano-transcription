'''
python3 evaluate.py *.wav
'''

import numpy as np 
import math
import sys, os
from math import floor
from mir_eval import multipitch, onset
def midi2freq(notes):
    return [2**((i-69)/12)*440 for i in notes]

def evaluation(labels, preds):
    ## session 1
    TP = np.zeros(labels.shape[0]) # true positive
    FP = np.zeros(labels.shape[0]) # false positive
    FN = np.zeros(labels.shape[0]) # true negative
    
    n_ref = np.zeros(labels.shape[0]) # Array for the num of ref freqes at each frame
    n_est = np.zeros(labels.shape[0]) # Array for the num of est freqes at each frame
    
    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):
            if (labels[i][j] == 1 and preds[i][j] == 1):
                TP[i] += 1
            elif (labels[i][j] == 0 and preds[i][j] == 1):
                FP[i] += 1
            elif (labels[i][j] == 1 and preds[i][j] == 0):
                FN[i] += 1

        n_ref[i] = np.sum(labels[i])
        n_est[i] = np.sum(preds[i])

    ## session 2
    ref_time = np.arange(labels.shape[0]) #Time of each ref freq value
    est_time = np.arange(labels.shape[0]) #Time of each est freq value
    ref_notes = [] # List of np.ndarrays of ref freq values
    est_notes = [] # List of np.ndarrays of est freq values
    
    for i in range(labels.shape[0]):
        ref_i = np.zeros(int(np.sum(labels[i])))
        est_i = np.zeros(int(np.sum(preds[i])))
        r = 0
        e = 0
        for j in range(labels.shape[1]):
            if (labels[i][j] == 1):
                ref_i[r] = j + 21
                r = r + 1
            if (preds[i][j] == 1):
                est_i[e] = j + 21
                e = e + 1           
        ref_notes.append(ref_i)
        est_notes.append(est_i)
    ref_notes = midi2freq(ref_notes)
    est_notes = midi2freq(est_notes)
    # Evaluate multipitch (multi-f0) transcriptions
    Dict = multipitch.evaluate(ref_time, ref_notes, est_time, est_notes)
    for key in Dict:
        print(key, " ", Dict[key])    
    


def main():
    filename = sys.argv[1].split(".")[0]
    labels = np.loadtxt('%s_labels.txt'%filename, dtype = int) #.txt
    os.system('python3 predict.py %s'%sys.argv[1])

    preds = np.loadtxt("result.txt")
    for i in range(preds.shape[0]):
        for j in range(preds.shape[1]):
            if preds[i][j] < 0.5:
                preds[i][j] = 0
            else:
                preds[i][j] = 1

    print(labels.shape,preds.shape)
    evaluation(labels, preds)



if __name__ == '__main__':
    main() 
