import sys
sys.path.append('../../software/models/')
from dftModel import dftAnal, dftSynth
from scipy.signal import get_window
import matplotlib.pyplot as plt
import numpy as np

import math
import copy

"""
A3-Part-4: Suppressing frequency components using DFT model

Given a frame of the signal, write a function that uses the dftModel functions to suppress all the frequency 
components till the first bin >= 70Hz in the signal and returns the output of the dftModel with and without filtering. 

You will use the DFT model to implement a very basic form of filtering to suppress frequency components. 
When working close to mains power lines, there is a 50/60 Hz hum that can get introduced into the 
audio signal. You will try to remove that using a basic DFT model based filter. You will work on just 
one frame of a synthetic audio signal to see the effect of filtering. 

You can use the functions dftAnal and dftSynth provided by the dftModel file of sms-tools. Use dftAnal 
to obtain the magnitude spectrum (in dB) and phase spectrum of the audio signal. Set the values of 
the magnitude spectrum that correspond to frequencies <= 70 Hz to -120dB (there may not be a bin 
corresponding exactly to 70 Hz, choose the nearest bin of equal or higher frequency). Use dftSynth 
to synthesize the filtered output signal and return the output. The function should also return the 
output of dftSynth without any filtering (without altering the magnitude spectrum in any way). 
You will use a hamming window to smooth the signal. Hence, do not forget to scale the output signals 
by the sum of the window values (as done in sms-tools/software/models_interface/dftModel_function.py).
To understand the effect of filtering, you can plot both the filtered output and non-filtered output of the dftModel. 

Please note that this question is just for illustrative purposes and filtering is not usually done 
this way - such sharp cutoffs introduce artifacts in the output. 

The input is a M length input signal x that contains undesired frequencies below 70 Hz, sampling 
frequency fs and the FFT size N. The output is a tuple with two elements (y, yfilt), where y is the 
output of dftModel with the unaltered original signal and yfilt is the filtered output of the dftModel.

EXAMPLE: For an input signal with 40 Hz, 100 Hz, 200 Hz, 1000 Hz components, yfilt will only contain
100 Hz, 200 Hz and 1000 Hz components. 

"""
def suppressFreqDFTmodel(x, fs, N):
    """
    Inputs:
        x (numpy array) = input signal of length M (odd)
        fs (float) = sampling frequency (Hz)
        N (positive integer) = FFT size
    Outputs:
        The function should return a tuple (y, yfilt)
        y (numpy array) = Output of the dftSynth() without filtering (M samples long)
        yfilt (numpy array) = Output of the dftSynth() with filtering (M samples long)
    The first few lines of the code have been written for you, do not modify it. 
    """
    ## Your code here
    M = len(x)

    bin70 = int(math.ceil(70.0*N/fs))
    
    w = get_window("hamming", M)

    mX, pX = dftAnal(x, w, N)
    
    mX2 = mX.copy()
    
    mX2[:bin70 + 1] = -120
    
    """z = 0
    while True:
        if( z <= bin70):
            mX2[z] = -120
	    z= z + 1
	else:
            mX2[z] = -120
            break"""
    
    print M
    print fs
    print N
    print bin70
    
    """plt.plot(mX)
    plt.plot(mX2)
    plt.show()"""

    y = dftSynth(mX, pX, M) * sum(w)
    yfilt = dftSynth(mX2, pX, M) * sum(w)
    
    return (y, yfilt)

"""A = 1.
f0 = 1000
phi = np.pi/2
fs = 10000

N = 1024
ty = (N * (1.0/fs)) / 2

t = np.arange(-ty, ty, 1.0/fs)

x1 = A * np.cos(2 * np.pi * 40 * t +phi)
x2 = A * np.cos(2 * np.pi * 70 * t +phi)
x3 = A * np.cos(2 * np.pi * 100 * t +phi)
x = x1 + x2 + x3

plt.plot(x)
plt.show()

(y, yfilt) = suppressFreqDFTmodel(x, fs, 1024)

plt.plot(y)
plt.plot(yfilt)
plt.show()"""


