import sys
import math
import scipy
import pylab
import scipy.io.wavfile as wav
import wave
from scipy import signal
from itertools import product
import numpy
import operator

def getDuration(sound_file):
    """
        Returns the duration of a given sound file.
    """

    wr = wave.open(sound_file, 'r')
    nchannels, sampwidth, framerate, nframes, comptype, compname =  wr.getparams()
    return nframes / float(framerate)

def get_channels_no(sound_file):
    """
        Returns number of channels of a given sound file.
    """

    wr = wave.open(sound_file, 'r')
    nchannels, sampwidth, framerate, nframes, comptype, compname = wr.getparams()
    return nchannels

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


class MIDI_Detector(object):
    """
        Class for MIDI notes detection given a .wav file.
    """

    def __init__(self, wav_file):
        self.wav_file = wav_file
        self.minFreqConsidered = 20
        self.maxFreqConsidered = 2000
        self.low_f0s = [27.5, 29.135, 30.868, 32.703, 34.648, 37.708, 38.891,
                        41.203, 43.654, 46.249, 48.999, 51.913, 55.0, 58.27,
                        61.735, 65.406, 69.296, 73.416, 77.782, 82.407]

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
            FFT, filteredFreqs, maxFreq, magnitudes, significant_freq = self.calculateFFT(duration, framerate, sample)
            
            peaks = dict()
            for i in range(len(filteredFreqs)):
                peaks[filteredFreqs[i]]=magnitudes[i]
            sorted_peaks = sorted(peaks.items(), key=operator.itemgetter(1),reverse = 1)[0:10]
            sorted_freq = sorted(sorted_peaks)
            print sorted_peaks           
            clusters = self.clusterFrequencies(sorted_freq)
            averagedClusters_w = self.getClustersMeans(clusters)
            print averagedClusters_w
            averagedClusters = [i[0] for i in averagedClusters_w]

            f0_candidates = self.getF0Candidates(averagedClusters)
            max_f0_weight = 0
   
            
            def is_multiple(f, f0):
                return abs(round(f / f0))  
         
            for w in averagedClusters_w:
                for f0 in f0_candidates:
                    if w[0] == f0 and w[1]>max_f0_weight:
                        max_f0_weight = w[1]
            for w in averagedClusters_w:
                for f0 in f0_candidates:
                    if w[1] >  0.5*max_f0_weight and is_multiple(w[0],f0) and w[0] not in f0_candidates:
                        
                        f0_candidates.append(w[0])   
            
            midi_notes = self.matchWithMIDINotes(f0_candidates)


        return midi_notes

    def remove_lower_octave(self, upper_octave, midi_notes):
        lower_octave = upper_octave - 12
        if lower_octave in midi_notes:
            midi_notes.remove(lower_octave)
        return midi_notes



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
        for i in range(len(FFT)/2):
            power_spectrum = scipy.absolute(FFT[i]) * scipy.absolute(FFT[i])
            if power_spectrum > threshold:
                frequency_bin_with_max_spectrum = i
            power_spectra.append(power_spectrum)
        max_power_spectrum = max(power_spectra)
        threshold =0.05*max_power_spectrum

        binFrequencies = []
        magnitudes = []
        binResolution = float(framerate) / float(fft_length)
        sum_of_significant_spectra = 0
        # For each bin calculate the corresponding frequency.
        for k in range(len(FFT)):
            binFreq = k * binResolution

            # Truncating the FFT so we consider only hearable frequencies.
            if binFreq > self.maxFreqConsidered:
                FFT = FFT[:k]
                break
            elif binFreq > self.minFreqConsidered:
                # Consider only the frequencies
                # with magnitudes higher than the threshold.
                power_spectrum = power_spectra[k]
                if power_spectrum > threshold:
                    magnitudes.append(power_spectrum)
                    binFrequencies.append(binFreq)

                    # Sum all significant power spectra
                    # except the max power spectrum.
                    if power_spectrum != max_power_spectrum:
                        sum_of_significant_spectra += power_spectrum

        significant_freq = 0.0

        if max_power_spectrum > sum_of_significant_spectra:
            significant_freq = frequency_bin_with_max_spectrum * binResolution

        # Max. frequency considered after truncating.
        # maxFreq = rate without truncating.
        maxFreq = len(FFT) / duration

        return (FFT, binFrequencies, maxFreq, magnitudes, significant_freq)


    def clusterFrequencies(self, freqs):
        """
            Clusters frequencies.
        """

        if len(freqs) == 0:
            return {}
        clusteredFreqs = {}
        bin = 0
        clusteredFreqs[0] = [freqs[0]]
        for i in range(len(freqs) - 1):
            dist = self.calcDistance(freqs[i][0], freqs[i + 1][0])
            if dist < 2.0:
                clusteredFreqs[bin].append(freqs[i + 1])
            else:
                bin += 1
                clusteredFreqs[bin] = [freqs[i + 1]]

        return clusteredFreqs

    def getClustersMeans(self, clusters):
        """
            Given clustered frequencies finds a mean of each cluster.
        """

        means = []
        for bin, freqs in clusters.iteritems():
            freq_sum = 0
            power_sum = 0
            for i in range(len(freqs)):
                freq_sum+=freqs[i][0]
                power_sum+=freqs[i][1]
            means.append((freq_sum / len(freqs),power_sum/len(freqs)))
        return means

    def getDistances(self, freqs):
        """
            Returns a list of distances between each frequency.
        """

        distances =  {(freqs[i], freqs[j]): self.calcDistance(freqs[i], freqs[j])
                        for (i, j) in product(range(len(freqs)), repeat=2)}
        distances = {freq_pair: dist for freq_pair, dist in distances.iteritems() if dist < 2.0}
        return distances

    def calcDistance(self, freq1, freq2):
        """
            Calculates distance between frequencies taking into account that
            the frequencies of pitches increase logarithmically.
        """

        difference = abs(freq1 - freq2)
        log = math.log((freq1 + freq2) / 2)
        return difference / log

    def getF0Candidates(self, frequencies):
        """
            Given frequencies finds possible F0 candidates
            by discarding potential harmonic frequencies.
        """

        f0_candidates = []

        '''
        MODIFICATION: CONSIDER ONLY MIDDLE RANGE FREQUENCIES
        '''
        '''

        if len(frequencies) > 0 and frequencies[0] < 83.0:
            low_freq_candidate = self.find_low_freq_candidate(frequencies)
            if low_freq_candidate > 0.0:
                f0_candidates.append(low_freq_candidate)
                #frequencies = self.filterOutHarmonics(
                    frequencies, low_freq_candidate)
        '''

        while len(frequencies) > 0:
            f0_candidate = frequencies[0]
            f0_candidates.append(f0_candidate)
            frequencies.remove(f0_candidate)
            frequencies = self.filterOutHarmonics(frequencies, f0_candidate)
        return f0_candidates

    def filterOutHarmonics(self, frequencies, f0_candidate):
        """
            Given frequencies and an f0 candidate remove
            all possible harmonics of this f0 candidate.
        """

        # If an integer frequency is a multiple of another frequency
        # then it is its harmonic. This constant was found empirically.
        REMAINDER_THRESHOLD = 0.2

        def is_multiple(f, f0):
            return abs(round(f / f0) - f / f0) < REMAINDER_THRESHOLD

        return [f for f in frequencies if not is_multiple(f, f0_candidate)]

    def find_low_freq_candidate(self, frequencies):
        REMAINDER_THRESHOLD = 0.05
        f0_candidates = []

        def is_multiple(f, f0):
            return abs(round(f / f0) - f / f0) < REMAINDER_THRESHOLD

        best_candidate = -1
        max_no_partials = 0
        for low_f0 in self.low_f0s:
            num_of_partials = 0
            for f in frequencies:
                if is_multiple(f, low_f0):
                    num_of_partials += 1
            if num_of_partials > max_no_partials:
                max_no_partials = num_of_partials
                best_candidate = low_f0
        return best_candidate

    def matchWithMIDINotes(self, f0_candidates):
        midi_notes = []
        for freq in f0_candidates:
            # Formula for calculating MIDI note number.
            midi_notes.append(int(
                round(69 + 12 * math.log(freq / 440) / math.log(2))))
        return midi_notes

if __name__ == '__main__':

    MIDI_detector = MIDI_Detector(sys.argv[1])
    midi_notes = MIDI_detector.detect_MIDI_notes()

