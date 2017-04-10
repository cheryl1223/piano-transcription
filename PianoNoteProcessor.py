from madmom.processors import SequentialProcessor
import numpy as np
class PianoNoteProcessor(SequentialProcessor):

    def __init__(self, **kwargs):
        # pylint: disable=unused-argument
        from madmom.audio.signal import SignalProcessor, FramedSignalProcessor
        from madmom.audio.stft import ShortTimeFourierTransformProcessor
        from madmom.audio.spectrogram import (
            FilteredSpectrogramProcessor, LogarithmicSpectrogramProcessor,
            SpectrogramDifferenceProcessor)
        from madmom.models import NOTES_BRNN
        from madmom.ml.nn import NeuralNetwork

        from madmom.features.onsets import peak_picking, PeakPickingProcessor
        from madmom.processors import SequentialProcessor, ParallelProcessor
        from madmom.utils import suppress_warnings, combine_events

        # define pre-processing chain
        sig = SignalProcessor(num_channels=1, sample_rate=44100)
        # process the multi-resolution spec & diff in parallel
        multi = ParallelProcessor([])
        for frame_size in [4096]:
            frames = FramedSignalProcessor(frame_size=frame_size, fps=100)
            stft = ShortTimeFourierTransformProcessor(window = np.hamming(frame_size))  # caching FFT window
            filt = FilteredSpectrogramProcessor(
                num_bands=12, fmin=30, fmax=16000, norm_filters=True)
            spec = LogarithmicSpectrogramProcessor(mul=5, add=1)
            diff = SpectrogramDifferenceProcessor(diff_ratio=0.5, positive_diffs=True, stack_diffs=np.hstack)
            # process each frame size with spec and diff sequentially
            multi.append(SequentialProcessor((frames, stft, filt, spec,diff)))
        # stack the features and processes everything sequentially
        pre_processor = SequentialProcessor((sig, multi, np.hstack))
        super(PianoNoteProcessor,self).__init__(pre_processor)

