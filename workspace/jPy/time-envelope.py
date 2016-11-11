import seaborn
import numpy as np, scipy, matplotlib.pyplot as plt, pandas, librosa, IPython.display as ipd, urllib, os.path
import sys

x, fs = librosa.load(sys.argv[1], sr=44100)

plt.subplot(211)
librosa.display.waveplot(x, fs, alpha=0.5)
#print x.size

size = x.size
subsize = 300
a = []
k = 0
while k < size/subsize:
    b = x[(k*subsize):(k+1)*subsize]
    max_bi = np.argmax(b)
    a.append(x[max_bi + k*subsize])
    k = k + 1
#print len(a)

time = 1.0*size/fs
subtime = (1.0*subsize/size)*time
#print time
#print subtime
#print time/(subtime*1.0)
t = np.arange(0,len(a))*subtime
plt.subplot(212)
plt.plot(t, a)
plt.show()
