import scipy.io.wavfile as wf 
import scipy.signal as sig
import numpy as np
import sys
#import pyaudio
import scipy.signal as sig
from scipy.io.wavfile import read
#AUTOCORRELATION FUNCTION
#(1/N)Sigma{n=0, N-1}(x(n), x(x+m))
def pitchByACF(wavFile, mmin=50, mmax=260, N=1024):
	rate = wavFile[0]
	soundArr = np.mean(wavFile[1])
	# convert mmin and mmax from hertz to samples
	tempMin = mmin
	tempMax = mmax
	mmin = int((1./tempMax) * rate)
	mmax = int((1./tempMin) * rate)
	#print mmin, mmax

	# amount of windows that can be fit into the audio file
	# can also be seen as the starting points of window
	numPitchPts = (len(soundArr) - mmax)/N
	pitchArr = np.zeros(numPitchPts)
	for i in range(0,numPitchPts):
		window = soundArr[i*N:(i+1)*N]
		maxDm = float('-inf')
		pitchPt = 0	

		for m in range(mmin, mmax):
			slidedWindow = soundArr[i*N+m:(i+1)*N+m]
			AC = np.sum( np.multiply(window, slidedWindow)) / N
			if AC > maxDm:
				maxDm = AC
				pitchPt = m

		pitchArr[i] = 1/(float(pitchPt)/rate)

	return pitchArr


# AMDF (Average Magnitude Difference Function)
# D(m) = 1/N Sigma{n=0 -> N-1}( abs( x(n) - x(n+m) ) )
# N = window size
# pitch = MIN(D(m)), for m= mmin to mmax (range of expected pitches)
# mmin and mmax in hertz
def pitchByAMDF(wavFile, mmin=50, mmax=260, N=1024, threshold=150):
	rate = wavFile[0]
	soundArr = np.mean(wavFile[1])
	# convert mmin and mmax from hertz to samples
	tempMin = mmin
	tempMax = mmax
	mmin = int((1./tempMax) * rate)
	mmax = int((1./tempMin) * rate)

	# amount of windows that can be fit into the audio file
	# can also be seen as the starting points of window
	numPitchPts = (len(soundArr) - mmax)/N
	pitchArr = np.zeros(numPitchPts)
	for i in range(0,numPitchPts):
		window = soundArr[i*N:(i+1)*N]
		minDm = sys.maxint
		pitchPt = 0

		for m in range(mmin, mmax):
			slidedWindow = soundArr[i*N+m:(i+1)*N+m]
			AMD = np.sum( (np.absolute(window - slidedWindow)) ) / N

			if AMD < minDm:
				#print AMD
				minDm = AMD
				# convert pitch from samples back to hertz
				if AMD > threshold:
					pitchArr[i] = 1/(float(m)/rate)
				else:
					pitchPt = None

	return pitchArr


# WEIGHTED AUTOCORRELATION FUNCTION
# combination of ACF and AMDF 
def pitchByWACF(wavFile, mmin=50, mmax=260, N=1024, threshold=1500):
	rate = wavFile[0]
	soundArr = np.mean(wavFile[1])
	# convert mmin and mmax from hertz to samples
	tempMin = mmin
	tempMax = mmax
	mmin = int((1./tempMax) * rate)
	mmax = int((1./tempMin) * rate)

	# amount of windows that can be fit into the audio file
	# can also be seen as the starting points of window
	numPitchPts = (len(soundArr) - mmax)/N
	pitchArr = np.zeros(numPitchPts)
	for i in range(0,numPitchPts):
		window = soundArr[i*N:(i+1)*N]
		maxDm = float('-inf')
		pitchPt = 0

		for m in range(mmin, mmax):
			slidedWindow = soundArr[i*N+m:(i+1)*N+m]
			AC = np.sum( np.multiply(window, slidedWindow)) / N
			AMD = np.sum( (np.absolute(window - slidedWindow)) ) / N
			WAC = AC/(AMD+1)
			if WAC > maxDm:
				
				maxDm = WAC
				if WAC > threshold:
					pitchArr[i] = 1/(float(m)/rate)
				else:
					pitchPt = None

	pitchArr = sig.medfilt(pitchArr, kernel_size=7)
	pitchArr = sig.medfilt(pitchArr, kernel_size=5)
	return pitchArr



sample_rate = 44100
frame_size = 4096
noise_threshold = 0.1
max_frequency = 2000


N = 1024
rate,x = read(sys.argv[1]) 
soundArr = x[0:1024]
# convert mmin and mmax from hertz to samples
tempMin = 50
tempMax = 300
mmin = int((1./tempMax) * rate)
mmax = int((1./tempMin) * rate)

# amount of windows that can be fit into the audio file
# can also be seen as the starting points of window
numPitchPts = (len(x) - mmax)/N
pitchArr = np.zeros(numPitchPts)
print numPitchPts

window = soundArr
maxDm = float('-inf')
pitchPt = 0

for m in range(mmin, mmax):
	slidedWindow = soundArr[m:N+m]
	AC = np.sum( np.multiply(window, slidedWindow)) / N
	AMD = np.sum( (np.absolute(window - slidedWindow)) ) / N
	WAC = AC/(AMD+1)
	if WAC > maxDm:
				
		maxDm = WAC
		if WAC > threshold:
				pitchArr[i] = 1/(float(m)/rate)
			else:
				pitchPt = None

pitchArr = sig.medfilt(pitchArr, kernel_size=7)
pitchArr = sig.medfilt(pitchArr, kernel_size=5)
time=np.arange(0,len(WACFpitchArr),1);

    
f = plt.figure(1)
plt.subplot(211)
plt.scatter(time, WACFpitchArr)
plt.xlabel('time (s)')
#plt.yscale('log')
plt.ylabel('frequency(Hz)')
plt.xlim([-20,140])
plt.title('pitch contour')
plt.grid(True)
#plt.subplot(212)
#plt.plot(soundArr)
plt.show()

