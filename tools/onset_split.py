import sys
import wave
import os

class OnsetFrameSplitter(object):
    """
        A class for splitting a file into onset frames.
    """

    def __init__(self, music_file, output_directory):
        self.music_file = music_file
        self.output_directory = output_directory
        self.verbose = False

    def onset_frames_split(self):
        """
            Splits a music file into onset frames.
        """
        print 'Start to detect onsets...'
        os.system("OnsetDetector single %s -o onsets.txt"%music_file)
        f = open("onsets.txt","r")
        onsets_complex = []
        for line in f:
            line = line.rstrip('\n')
            onsets_complex.append(float(line))
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
