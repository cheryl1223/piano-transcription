import sys
import wave
import math
import scipy
import pylab
import scipy.io.wavfile as wav
import numpy
from scipy import signal

def getDuration(sound_file):
    """
        Returns the duration of a given sound file.
    """

    wr = wave.open(sound_file, 'r')
    nchannels, sampwidth, framerate, nframes, comptype, compname =  wr.getparams()
    return nframes / float(framerate)


def getFrameRate(sound_file):
    wr = wave.open(sound_file, 'r')
    nchannels, sampwidth, framerate, nframes, comptype, compname = wr.getparams()
    return framerate



def get_next_power_2(n):
    """
        Returns the closest number that is smaller than n that is a power of 2.
    """

    power = 1
    while (power < n):
        power *= 2
    if power > 1:
        return power / 2
    else:
        return 1

def get_channels_no(sound_file):
    """
        Returns number of channels of a given sound file.
    """

    wr = wave.open(sound_file, 'r')
    nchannels, sampwidth, framerate, nframes, comptype, compname = wr.getparams()
    return nchannels
class Highest_Peaks_MIDI_Detector(object):
    """
        Class for MIDI notes detection given a .wav file.
    """

    def __init__(self, wav_file):
        self.wav_file = wav_file
        # before: 0.005e+13  twinkle: 0.002e+14 scale: 0.005e+16
        self.THRESHOLD = 0.005e+13
        self.HAN_WINDOW = 0.093
        self.HOP_SIZE = 0.00928
        self.minFreqConsidered = 27.0
        self.maxFreqConsidered = 2093

    def detect_MIDI_notes(self):
        """
            The algorithm for calculating midi notes from a given wav file.
        """

        (framerate, sample) = wav.read(self.wav_file)
        if get_channels_no(self.wav_file) > 1:
            sample = sample.mean(axis=1)
        duration = getDuration(self.wav_file)
        midi_notes = []


        if duration > 0.1:
            frequency_power = self.calculateFFT(duration, framerate, sample)
            sorted_frequency_power = sorted(frequency_power, key=lambda power: power[1], reverse=True)

            filtered_frequencies = [f for (f, p) in sorted_frequency_power]
            #self.plot_power_spectrum(frequency_power)
            #self.plot_power_spectrum_dB(frequency_power)
            f0_candidates = self.get_pitch_candidates_remove_highest_peak(sorted_frequency_power)
            def is_multiple(f, f0):
                return abs(round(f / f0)-f/f0) <= 0.2 
            max_f0_weight = 0

            for w in sorted_frequency_power:
                for f0 in f0_candidates:
                    if w[0] == f0 and w[1]>max_f0_weight:
                        max_f0_weight = w[1]

            for w in sorted_frequency_power:
                for f0 in f0_candidates:
                    if w[1] >  0.4*max_f0_weight and is_multiple(w[0],f0) and w[0] not in f0_candidates:
                        print "add"
                        f0_candidates.append(w[0])   
            midi_notes = self.matchWithMIDINotes(f0_candidates)
        return midi_notes

    def get_pitch_candidates_remove_highest_peak(self, frequency_power):
        peak_frequencies = []
        while len(frequency_power) > 0:
            # sort the frequency_power by power (highest power first)
            sorted_frequency_power = sorted(frequency_power, key=lambda power: power[1], reverse=True)
            peak_frequency = sorted_frequency_power[0][0]
            peak_frequencies.append(peak_frequency)
            frequency_power = self.filterOutHarmonics(sorted_frequency_power, peak_frequency)
        return peak_frequencies

    def calculateFFT(self, duration, framerate, sample):
        """
            Calculates FFT for a given sound wave.
            Considers only frequencies with the magnitudes higher than
            a given threshold.
        """
        fft_length = int(duration * framerate)
        # For the FFT to work much faster take the length that is a power of 2.
        fft_length = get_next_power_2(fft_length)

        w = signal.hamming(fft_length)
        FFT = numpy.fft.fft(sample[0:fft_length]*w, n=fft_length)

        threshold = 0
        power_spectra = []
        frequency_bin_with_max_spectrum = 0 
        for i in range(len(FFT) / 2):
            power_spectrum = scipy.absolute(FFT[i]) * scipy.absolute(FFT[i])
            if power_spectrum > threshold:
                threshold = power_spectrum
            power_spectra.append(power_spectrum)
        threshold *= 0.04

        binResolution = float(framerate) / float(fft_length)
        frequency_power = []
        # For each bin calculate the corresponding frequency.
        for k in range(len(FFT) / 2):
            binFreq = k * binResolution

            if binFreq > self.minFreqConsidered and binFreq < self.maxFreqConsidered:
                power_spectrum = power_spectra[k]
                #dB = 10*math.log10(power_spectrum)
                if power_spectrum > threshold:
                    frequency_power.append((binFreq, power_spectrum))

        return frequency_power

    def filterOutHarmonics(self, frequency_power, f0_candidate):
        """
            Given frequency_power pairs and an f0 candidate remove
            all possible harmonics of this f0 candidate.
        """

        # If an integer frequency is a multiple of another frequency
        # then it is its harmonic. This constant was found empirically.
        # TODO: This constant may change for inharmonic frequencies!!!
        REMAINDER_THRESHOLD = 0.2

        def is_multiple(f, f0):
            return abs(round(f / f0) - f / f0) < REMAINDER_THRESHOLD

        return [(f, p) for (f, p) in frequency_power if not is_multiple(f, f0_candidate)]

    def matchWithMIDINotes(self, f0_candidates):
        midi_notes = []
        for freq in f0_candidates:
            #print 'FREQUENCY: ' + str(freq)
            midi_notes.append(int(round(69 + 12 * math.log(freq / 440) / math.log(2))))  # Formula for calculating MIDI note number.
        return midi_notes


if __name__ == '__main__':
    MIDI_detector = Highest_Peaks_MIDI_Detector(sys.argv[1])
    midi_notes = MIDI_detector.detect_MIDI_notes()
    print midi_notes
