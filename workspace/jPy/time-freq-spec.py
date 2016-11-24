import seaborn
import numpy, scipy, matplotlib.pyplot as plt, pandas, librosa, IPython.display as ipd, urllib, os.path

x, fs = librosa.load('CE4.wav', sr=44100)

#librosa.display.waveplot(x,fs,alpha=0.5)
#S = librosa.feature.melspectrogram(x,sr=fs,n_fft=1024)
#logS=librosa.logamplitude(S)
#librosa.display.specshow(logS, sr=fs,x_axis='time',y_axis='mel')

#S,freqs,bins,im = plt.specgram(x,NFFT=1024,noverlap=512,Fs=44100)

S = librosa.stft(x)
logX = librosa.logamplitude(S)
librosa.display.specshow(logX, sr=fs, x_axis='time', y_axis='log')
plt.show()

