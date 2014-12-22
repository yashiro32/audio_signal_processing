import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../software/models/'))
import dftModel as DFT
import utilFunctions as UF
import stft as STFT
import harmonicModel as HM
import sineModel as SM

(fs, x) = UF.wavread('../sounds/sawtooth-440.wav')
N = 2048
M = 1001
t = -50
minf0 = 300
maxf0 = 500
f0et = 1
H = 1000

hN = N/2
hM = (M+1)/2

w = get_window('blackman', M)
start = .8*fs

"""x1 = x[start:start+M]
mX, pX = DFT.dftAnal(x1, w, N)
ploc = UF.peakDetection(mX, t)
iploc, ipmag, ipphase = UF.peakInterp(mX, pX, ploc)
ipfreq = fs * iploc/N
f0c = np.argwhere((ipfreq>minf0) & (ipfreq<maxf0))[:,0]
f0cf = ipfreq[f0c]
f0Errors = UF.TWM_Errors (ipfreq, ipmag, f0cf)

freqaxis = fs*np.arange(N/2)/float(N)
plt.plot(freqaxis, mX)
plt.plot(ipfreq, ipmag, marker='x', linestyle='')
plt.show()"""

f0 = HM.f0Detection(x, fs, w, N, H, t, minf0, maxf0, f0et)
