import os
import sys
import numpy as np
import math
from scipy.signal import get_window
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import utilFunctions as UF
import harmonicModel as HM
import stft

eps = np.finfo(float).eps

"""
A6Part2 - Segmentation of stable note regions in an audio signal

Complete the function segmentStableNotesRegions() to identify the stable regions of notes in a specific 
monophonic audio signal. The function returns an array of segments where each segment contains the 
starting and the ending frame index of a stable note.

The input argument to the function are the wav file name including the path (inputFile), threshold to 
be used for deciding stable notes (stdThsld), minimum allowed duration of a stable note (minNoteDur), 
number of samples to be considered for computing standard deviation (winStable), analysis window (window), 
window size (M), FFT size (N), hop size (H), error threshold used in the f0 detection (f0et), magnitude 
threshold for spectral peak picking (t), minimum allowed f0 (minf0) and maximum allowed f0 (maxf0). 
The function returns a numpy array of shape (k,2), where k is the total number of detected segments. 
The two columns in each row contains the starting and the ending frame indices of a stable note segment. 
The segments must be returned in the increasing order of their start times. 

In order to facilitate the assignment we have configured the input parameters to work with a particular 
sound, '../../sounds/sax-phrase-short.wav'. The code and parameters to estimate the fundamental frequency 
is completed. Thus you start from an f0 curve obtained using the f0Detection() function and you will use 
that to obtain the note segments. 

All the steps to be implemented in order to solve this question are indicated in segmentStableNotesRegions() 
as comments. These are the steps:

1. In order to make the processing musically relevant, the f0 values should be converted first from 
Hertz to Cents, which is a logarithmic scale. 
2. At each time frame (for each f0 value) you should compute the standard deviation of the past winStable 
number of f0 samples (including the f0 sample at the current audio frame). 
3. You should then apply a deviation threshold, stdThsld, to determine if the current frame belongs 
to a stable note region or not. Since we are interested in the stable note regions, the standard 
deviation of the previous winStable number of f0 samples (including the current sample) should be less 
than stdThsld. 
4. All the consecutive frames belonging to the stable note regions should be grouped together into 
segments. For example, if the indices of the frames corresponding to the stable note regions are 
3,4,5,6,12,13,14, we get two segments, first 3-6 and second 12-14. 
5. After grouping frame indices into segments filter/remove the segments which are smaller in duration 
than minNoteDur. Return the segment indexes.

Using '../../sounds/sax-phrase-short.wav', if you use all the default values of the input arguments in 
segmentStableNotesRegions(), then the resulting segment array should be 
array([[  8,  83],
       [ 93, 119],
       [128, 202],
       [207, 326],
       [360, 464],
       [471, 502]])

if you use all the default values except stdThsld = 30.0, then the resulting segment array should be 
array([[  8,  85],
       [ 88, 120],
       [123, 203],
       [206, 326],
       [360, 466],
       [469, 506]])
If you use all the default values except minNoteDur = 0.3, then the resulting segment array should be
array([[  8,  83],
       [128, 202],
       [207, 326],
       [360, 464]])

We also provide the function plotSpectogramF0Segments() to plot the f0 contour and the detected segments 
on the top of the spectrogram of the audio signal in order to visually analyse the outcome of your function. 

"""

def segmentStableNotesRegions(inputFile = '../../sounds/sax-phrase-short.wav', stdThsld=10, minNoteDur=0.1, 
                              winStable = 3, window='hamming', M=1024, N=2048, H=256, f0et=5.0, t=-100, 
                              minf0=310, maxf0=650):
    """
    Function to segment the stable note regions in an audio signal
    Input:
        inputFile (string): wav file including the path
        stdThsld (float): threshold for detecting stable regions in the f0 contour
        minNoteDur (float): minimum allowed segment length (note duration)  
        winStable (integer): number of samples used for computing standard deviation
        window (string): analysis window
        M (integer): window size used for computing f0 contour
        N (integer): FFT size used for computing f0 contour
        H (integer): Hop size used for computing f0 contour
        f0et (float): error threshold used for the f0 computation
        t (float): magnitude threshold in dB used in spectral peak picking
        minf0 (float): minimum fundamental frequency in Hz
        maxf0 (float): maximum fundamental frequency in Hz
    Output:
        segments (np.ndarray): Numpy array containing starting and ending frame indices of every 
                               segment.
    """
    fs, x = UF.wavread(inputFile)                               #reading inputFile
    w  = get_window(window, M)                                  #obtaining analysis window    
    f0 = HM.f0Detection(x, fs, w, N, H, t, minf0, maxf0, f0et)  #estimating F0

    ### Your code here
    
    # 1. convert f0 values from Hz to Cents (as described in pdf document)
    f0_mod = f0[f0 > 0.0]
    
    """f0c = np.zeros(len(f0)) 
    for i in range(len(f0)):
        if f0[i] > 0.0:
            f0c[i] = 1200.0 * np.log2(f0[i]/55.0)
        else:
            f0c[i] = 0.0"""

    epsilon = 10**-17 # Add epsilon to f0 values to prevent log(0) errors
    f0c = 1200.0 * np.log2((f0+epsilon)/55.0)
    
    # 2. create an array containing standard deviation of last winStable samples
    sd = np.zeros(len(f0c))
    
    for i in range(len(f0c)):
        #samples = f0c[i-winStable:i+1]
        samples = []
        #samples.append(f0c[i])
        for j in range(winStable):
            if i-j >= 0:
                samples.append(f0c[i-j])
        
        sd[i] = np.std(samples)
    
    # 3. apply threshold on standard deviation values to find indices of the stable points in melody
    thres = np.where(sd<stdThsld)[0]
    
    # 4. create segments of continuous stable points such that concequtive stable points belong to 
    #    same segment
    thres_array = thres
    
    segs = []
    seg = np.array([])
    
    for i in range(len(thres_array)):
        if len(seg) == 0:
            seg = np.append(seg, thres_array[i])
            
        if i+1 < len(thres_array):
            if thres_array[i+1] - thres_array[i] == 1:
                seg = np.append(seg, thres_array[i+1])
            else:
                segs.append(seg)
                
                seg = np.array([])

    # 5. apply segment filtering, i.e. remove segments with are < minNoteDur in length
    minTrackLength = round(fs*minNoteDur/H)
    
    segs2 = []
    for i in range(len(segs)):
        if len(segs[i]) > minTrackLength:
            segs2.append(segs[i])

    segments = np.zeros((len(segs2), 2))
    #segments = np.array([])
    for i in range(len(segs2)):
        #ind = np.array((seg[0], seg[len(seg)-1]))
        segments[i][0] = segs2[i][0]
        segments[i][1] = segs2[i][len(segs2[i])-1]
        
    #plotSpectogramF0Segments(x, fs, w, N, H, f0, segments)
    
    return segments

## Use this function to plot the f0 contour and the estimated segments on the spectrogram
def plotSpectogramF0Segments(x, fs, w, N, H, f0, segments):
    """
    Code for plotting the f0 contour on top of the spectrogram
    """
    # frequency range to plot
    maxplotfreq = 1000.0    
    fontSize = 16

    fig = plt.figure()
    ax = fig.add_subplot(111)

    mX, pX = stft.stftAnal(x, fs, w, N, H)                      #using same params as used for analysis
    mX = np.transpose(mX[:,:int(N*(maxplotfreq/fs))+1])
    
    timeStamps = np.arange(mX.shape[1])*H/float(fs)                             
    binFreqs = np.arange(mX.shape[0])*fs/float(N)
    
    plt.pcolormesh(timeStamps, binFreqs, mX)
    plt.plot(timeStamps, f0, color = 'k', linewidth=5)

    for ii in range(segments.shape[0]):
        plt.plot(timeStamps[segments[ii,0]:segments[ii,1]], f0[segments[ii,0]:segments[ii,1]], color = '#A9E2F3', linewidth=1.5)        
    
    plt.autoscale(tight=True)
    plt.ylabel('Frequency (Hz)', fontsize = fontSize)
    plt.xlabel('Time (s)', fontsize = fontSize)
    plt.legend(('f0','segments'))
    
    xLim = ax.get_xlim()
    yLim = ax.get_ylim()
    ax.set_aspect((xLim[1]-xLim[0])/(2.0*(yLim[1]-yLim[0])))    
    plt.autoscale(tight=True) 
    plt.show()
    

#segments = segmentStableNotesRegions()
#segments = segmentStableNotesRegions(stdThsld=30.0)
#segments = segmentStableNotesRegions(minNoteDur=0.3)
#print segments
