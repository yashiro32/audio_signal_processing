import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../software/models/'))
import dftModel as DFT
import utilFunctions as UF

(fs, x) = UF.wavread('../sounds/sine-440.wav')
M = 501
N = 2048
t = -20
w = get_window('hamming', M)
x1 = x[.8*fs:.8*fs+M]
mX, pX = DFT.dftAnal(x1, w, N)
ploc = UF.peakDetection(mX, t)
iploc, ipmag, ipphase = UF.peakInterp(mX, pX, ploc)
pmag = mX[ploc]

freqaxis = fs*np.arange(N/2+1)/float(N)
print mX.shape
print freqaxis.shape

plt.plot(freqaxis, mX)
plt.plot(fs * iploc / float(N), ipmag, marker='x', linestyle='')

plt.show()
