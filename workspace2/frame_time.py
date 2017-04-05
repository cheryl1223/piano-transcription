from madmom.audio.signal import FramedSignalProcessor
import sys
import numpy as np

class frame_time:
    def __init__(self,wav):
        self.wav = wav


    def frame(self):	
        proc = FramedSignalProcessor(frame_size = 4096, fps = 100)
        frames = proc(self.wav)
        frame_time = []
        for i in range(frames.num_frames):
     	    frame_time.append(0.01*i)
        frame_time = np.array(frame_time)
        return frame_time
