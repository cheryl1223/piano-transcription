from __future__ import absolute_import, division, print_function

import numpy as np

from madmom.features.onsets import peak_picking, PeakPickingProcessor
from madmom.processors import SequentialProcessor, ParallelProcessor
from madmom.utils import suppress_warnings, combine_events

class PianoNoteProcessor(SequentialProcessor):
    """
    Processor to get a (piano) note activation function from a RNN.

    Examples
    --------
    Create a RNNPianoNoteProcessor and pass a file through the processor to
    obtain a note onset activation function (sampled with 100 frames per
    second).

    >>> proc = RNNPianoNoteProcessor()
    >>> proc  # doctest: +ELLIPSIS
    <madmom.features.notes.RNNPianoNoteProcessor object at 0x...>
    >>> act = proc('tests/data/audio/sample.wav')
    >>> act.shape
    (281, 88)
    >>> act  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    array([[-0.00014,  0.0002 , ..., -0.     ,  0.     ],
           [ 0.00008,  0.0001 , ...,  0.00006, -0.00001],
           ...,
           [-0.00005, -0.00011, ...,  0.00005, -0.00001],
           [-0.00017,  0.00002, ...,  0.00009, -0.00009]], dtype=float32)

    """

    def __init__(self, **kwargs):
        # pylint: disable=unused-argument
        from madmom.audio.signal import SignalProcessor, FramedSignalProcessor
        from madmom.audio.stft import ShortTimeFourierTransformProcessor
        from madmom.audio.spectrogram import (
            FilteredSpectrogramProcessor, LogarithmicSpectrogramProcessor,
            SpectrogramDifferenceProcessor)
        from madmom.models import NOTES_BRNN
        from madmom.ml.nn import NeuralNetwork

        # define pre-processing chain
        sig = SignalProcessor(num_channels=1, sample_rate=44100)
        # process the multi-resolution spec & diff in parallel
        multi = ParallelProcessor([])
        for frame_size in [1024, 2048, 4096]:
            frames = FramedSignalProcessor(frame_size=frame_size, fps=100)
            stft = ShortTimeFourierTransformProcessor()  # caching FFT window
            filt = FilteredSpectrogramProcessor(
                num_bands=12, fmin=30, fmax=17000, norm_filters=True)
            spec = LogarithmicSpectrogramProcessor(mul=5, add=1)
            diff = SpectrogramDifferenceProcessor(
                diff_ratio=0.5, positive_diffs=True, stack_diffs=np.hstack)
            # process each frame size with spec and diff sequentially
            multi.append(SequentialProcessor((frames, stft, filt, spec, diff)))
        # stack the features and processes everything sequentially
        pre_processor = SequentialProcessor((sig, multi, np.hstack))
	print (pre_processor.shape)
	"""
        # process the pre-processed signal with a NN
        nn = NeuralNetwork.load(NOTES_BRNN[0])

        # instantiate a SequentialProcessor
        super(RNNPianoNoteProcessor, self).__init__((pre_processor, nn))
	"""
