import os
import sys
import numpy as np
from scipy.signal import get_window
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import stft
import utilFunctions as UF

import math

eps = np.finfo(float).eps

"""
A4-Part-3: Computing band-wise energy envelopes of a signal

Write a function that computes band-wise energy envelopes of a given audio signal by using the STFT.
Consider two frequency bands for this question, low and high. The low frequency band is the set of all the 
frequencies from 0 - 3000 Hz and the high frequency band is the set of all the frequencies from 
3000 - 10000 Hz. At a given frame, the value of the energy envelope of a band can be computed as the 
sum of squared values of all the frequency coefficients in that band. Compute the energy envelopes in 
decibels. 

Refer to "A4-STFT.pdf" document for further details on computing bandwise energy.

The input arguments to the function are the wav file name including the path (inputFile), window 
type (window), window length (M), FFT size (N) and hop size (H). The function should return a numpy 
array with two columns, where the first column is the energy envelope of the low frequency band and 
the second column is that of the high frequency band.

Use stft.stftAnal() to obtain the STFT magnitude spectrum for all the audio frames. Then compute two 
energy values for each frequency band specified. While calculating frequency bins for each frequency 
band, consider only the bins that are within the specified frequency range. For example, for the low 
frequency band consider only the bins with frequency > 0 Hz and < 3000 Hz. This way we also remove the 
DC offset in the signal in energy envelope computation.

To get a better understanding of the energy envelope and its characteristics you can plot the envelopes 
together with the spectrogram of the signal. You can use matplotlib plotting library for this purpose. 
To visualize the spectrogram of a signal, a good option is to use colormesh. You can reuse the code in
sms-tools/lectures/4-STFT/plots-code/spectrogram.py. Either overlay the envelopes on the spectrogram 
or plot them in a different subplot. Make sure you use the same range of the x-axis for both the 
spectrogram and the energy envelopes.

EXAMPLE: Running your code on piano.wav file with window = 'blackman', M = 513, N = 1024, H = 128, in 
the plots you can clearly notice the sharp attacks and decay of the piano notes (See figure in the 
accompanying pdf). In addition, you can also visually analyse which of the two energy envelopes is better 
for detecting onsets of the piano notes.
"""
def computeEngEnv(inputFile, window, M, N, H):
    """
    Inputs:
            inputFile (string): input sound file (monophonic with sampling rate of 44100)
            window (string): analysis window type (choice of rectangular, triangular, hanning, hamming, 
                blackman, blackmanharris)
            M (integer): analysis window size (odd positive integer)
            N (integer): FFT size (power of 2, such that N > M)
            H (integer): hop size for the stft computation
    Output:
            The function should return a numpy array engEnv with shape Kx2, K = Number of frames
            containing energy envelop of the signal in decibles (dB) scale
            engEnv[:,0]: Energy envelope in band 0 < f < 3000 Hz (in dB)
            engEnv[:,1]: Energy envelope in band 3000 < f < 10000 Hz (in dB)
    """
    
    ### your code here
    windowing = get_window(window, M)

    (fs, x) = UF.wavread(inputFile)
    
    mX, pX = stft.stftAnal(x, fs, windowing, N, H)
    
    bin0 = 0
    bin3000 = np.floor(3000.0*N/fs)
    bin10000 = np.floor(10000.0*N/fs)
    bin3000up = np.ceil(3000.0*N/fs)
    
    engEnv = np.zeros((mX.shape[0], 2))
    
    """
    hM1 = int(math.floor((M+1)/2))                 # half analysis window size by rounding
    hM2 = int(math.floor(M/2)) 
    
    pin = hM1                                      # initialize sound pointer in middle of analysis window       
    pend = x.size-hM1 
    
    while pin <= pend: 
        x1 = x[pin-hM1:pin+hM2]                      # select one frame of input sound
        mX, pX = STFT.stftAnal(x1, fs, windowing, N, H)

        print mX.shape

        env3000 = np.sum(np.square(mX[bin0:bin3000]))
        env10000 = np.sum(np.square(mX[bin3000:bin10000]))
        engEnv = np.append(engEnv, [env3000, env10000], axis=1)

        pin += H"""

    """for i in range(mX.shape[0]):
        env3000 = np.sum(np.square(10**(mX[i,1:bin3000+1] / 20)))
        engEnv[i,0] = 10 * np.log10(env3000)
        env10000 = np.sum(np.square(10**(mX[i,bin3000up:bin10000+1] / 20)))
        engEnv[i,1] = 10 * np.log10(env10000)"""

    env3000 = np.sum(np.square(10**(mX[:,1:bin3000+1] / 20)), axis=1)
    engEnv[:,0] = 10 * np.log10(env3000)
    env10000 = np.sum(np.square(10**(mX[:,bin3000up:bin10000+1] / 20)), axis=1)
    engEnv[:,1] = 10 * np.log10(env10000)
    
    return engEnv

"""input_file = "../../sounds/piano.wav"
engEnv = computeEngEnv(input_file, 'blackman', 513, 1024, 128)
#print engEnv
plt.plot(engEnv[:,0])
plt.plot(engEnv[:,1])
plt.show()"""



