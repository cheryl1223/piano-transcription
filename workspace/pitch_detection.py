import sys
import wave
import os
import sys, csv
from essentia import *
from essentia.standard import *
from pylab import *
from numpy import *

class Pitch(object):
    """
        A class to analyze onset frame pitch.
    """

    def __init__(self, music_file, output_directory):
        self.music_file = music_file
        self.output_directory = output_directory
        self.verbose = False

    def onset_frames_pitch(self):
        """
            Analyze pitches for an onset frame.
        """

        onsets_output_file = "pitches.txt"

        audio = MonoLoader(filename = self.music_file)()
        w = Windowing(type = 'hann')
        fft = FFT() 
        c2p = CartesianToPolar()
        peaks = PeakDetection() 
        pool = Pool()

        for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
            mag, phase, = c2p(fft(w(frame)))
            pool.add('peaks', peaks(mag))

        onsets = Onsets()
        onsets_complex = onsets(array([ pool['peaks'] ]), [ 1 ])
        onsets_complex = onsets_complex.tolist()

        if self.verbose:
            print 'onsets: '
            for o in onsets_complex:
                print o
        f = open('onsets.txt','w')
        for i in range(len(onsets_complex)):
            temp = onsets_complex[i]
            f.write("%s\n"%str(temp))
        f.close()


        # Reading in the music wave and getting parameters.
        input_music_wave = wave.open(self.music_file, "rb")
        nframes = input_music_wave.getnframes()
        params = input_music_wave.getparams()
        framerate = input_music_wave.getframerate()
        duration = nframes / float(framerate)

        if self.verbose:
            print "nframes: %d" % (nframes,)
            print "frame rate: %d " % (framerate,)
            print "duration: %f seconds" % (duration,)

        onsets_complex.append(duration)
        onsets_complex[0] = 0.0

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        # Splitting the music file into onset frames.
        for i in range(len(onsets_complex) - 1):
            frame = int(framerate * (onsets_complex[i + 1] - onsets_complex[i]))
            sound = input_music_wave.readframes(frame)
            music_wave = wave.open(self.output_directory + "/note%d.wav" % (i, ), "wb")
            music_wave.setparams(params)
            music_wave.setnframes(frame)
            music_wave.writeframes(sound)
            music_wave.close()
        print 'Done.'


if __name__ == '__main__':
    music_file = sys.argv[1]
    directory = 'frames'
    splitter = OnsetFrameSplitter(music_file, directory)
    splitter.onset_frames_split()
