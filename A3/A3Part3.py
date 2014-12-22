import numpy as np
from scipy.fftpack import fft, fftshift
import math

import matplotlib.pylab as plt

"""
A3-Part-3: Symmetry properties of the DFT

Write a function to check if the input signal is real and even using the symmetry properties of its DFT. 
The function will return the result of this test, the zerophase windowed version of the input signal 
(dftbuffer), and the DFT of the dftbuffer. 

Given an input signal x of length M, do a zero phase windowing of x without any zero-padding (a dftbuffer, 
on the same lines as the fftbuffer in sms-tools). Then compute the M point DFT of the zero phase windowed 
signal and use the symmetry of the computed DFT to test if the input signal x is real and even. Return 
the result of the test, the dftbuffer computed, and the DFT of the dftbuffer. 

The input argument is a signal x of length M. The output is a tuple with three elements 
(isRealEven, dftbuffer, X), where 'isRealEven' is a boolean variable which is True if x is real 
and even, else False. dftbuffer is the M length zero phase windowed version of x. X is the M point 
DFT of the dftbuffer. 

To make the problem easier, we will use odd length input sequence in this question (M is odd). 

Due to the precision of the FFT computation, the zero values of the DFT are not zero but very small
values < 1e-12 (or -240 dB) in magnitude. For practical purposes, all values with absolute value less 
than 1e-6 (or -120 dB) can be considered to be zero. Use an error tolerance of 1e-6 on the linear 
scale to compare if two floating point arrays are equal. 

EXAMPLE: If x = np.array([ 2, 3, 4, 3, 2 ]), which is a real and even signal, the function returns 
(True, array([ 4., 3., 2., 2., 3.]), array([14.0000+0.j, 2.6180+0.j, 0.3820+0.j, 0.3820+0.j, 2.6180+0.j]))
(values are approximate)

"""
def testRealEven(x):
    """
    Inputs:
        x (numpy array)= input signal of length M (M is odd)
    Output:
        The function should return a tuple (isRealEven, dftbuffer, X)
        isRealEven (boolean) = True if the input x is real and even, and False otherwise
        dftbuffer (numpy array, possibly complex) = The M point zero phase windowed version of x 
        X (numpy array, possibly complex) = The M point DFT of dftbuffer 
    """
    ## Your code here
    M = len(x)

    fftbuffer = np.zeros(M)
    fftbuffer[:M/2+1] = x[M/2:]
    fftbuffer[M/2+1:] = x[:M/2]

    X = fft(fftbuffer)
    mX = abs(X)
    pX = np.angle(X)

    isReal = True

    for i in range(len(X)):
        if i > 0 and i <= len(X)/2:
            if mX[i] != mX[len(X)-i]:
                isReal = False
                break
        if abs(X.imag[i]) >= 1e-6 and abs(X.imag[i]) >= np.pi * 10**-6:
            isReal = False
            break

    """print len(x)
    print x"""
    
    #print pX
    
    return (isReal, fftbuffer, X)



"""x = [ 0.01960784,  0.03921569,  0.05882353,  0.07843137,  0.09803922,  0.11764706,
  0.1372549,   0.15686275,  0.17647059,  0.19607843,  0.21568627,  0.23529412,
  0.25490196,  0.2745098,   0.29411765,  0.31372549,  0.33333333,  0.35294118,
  0.37254902,  0.39215686,  0.41176471,  0.43137255,  0.45098039,  0.47058824,
  0.49019608,  0.50980392,  0.52941176,  0.54901961,  0.56862745,  0.58823529,
  0.60784314,  0.62745098,  0.64705882,  0.66666667,  0.68627451,  0.70588235,
  0.7254902,   0.74509804,  0.76470588,  0.78431373,  0.80392157,  0.82352941,
  0.84313725,  0.8627451,   0.88235294,  0.90196078,  0.92156863,  0.94117647,
  0.96078431,  0.98039216,  1.,          0.98039216,  0.96078431,  0.94117647,
  0.92156863,  0.90196078,  0.88235294,  0.8627451,   0.84313725,  0.82352941,
  0.80392157,  0.78431373,  0.76470588,  0.74509804,  0.7254902,   0.70588235,
  0.68627451,  0.66666667,  0.64705882,  0.62745098,  0.60784314,  0.58823529,
  0.56862745,  0.54901961,  0.52941176,  0.50980392, 0.49019608,  0.47058824,
  0.45098039,  0.43137255,  0.41176471,  0.39215686,  0.37254902,  0.35294118,
  0.33333333,  0.31372549,  0.29411765,  0.2745098,   0.25490196,  0.23529412,
  0.21568627,  0.19607843,  0.17647059,  0.15686275,  0.1372549,   0.11764706,
  0.09803922,  0.07843137,  0.05882353,  0.03921569,  0.01960784]"""

"""x = [ 0.,  0.,  0., 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., 0.,  0.,  0.,  0.,  0.,  0.,  0.,
  0.,  0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
  1.,  1.,  1., 1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
  0.]"""

"""x = [0.00000000e+00, 2.46719817e-04, 9.86635786e-04, 2.21901770e-03,
   3.94264934e-03,   6.15582970e-03,   8.85637464e-03,   1.20416190e-02,
   1.57084194e-02,   1.98531572e-02,   2.44717419e-02,   2.95596155e-02,
   3.51117571e-02,   4.11226872e-02,   4.75864738e-02,   5.44967379e-02,
   6.18466600e-02,   6.96289865e-02,   7.78360372e-02,   8.64597129e-02,
   9.54915028e-02,   1.04922494e-01,   1.14743379e-01,   1.24944465e-01,
   1.35515686e-01,   1.46446609e-01,   1.57726447e-01,   1.69344067e-01,
   1.81288005e-01,   1.93546473e-01,   2.06107374e-01,   2.18958311e-01,
   2.32086603e-01,   2.45479292e-01,   2.59123163e-01,   2.73004750e-01,
   2.87110354e-01,   3.01426055e-01,   3.15937724e-01,   3.30631040e-01,
   3.45491503e-01,   3.60504447e-01,   3.75655056e-01,   3.90928379e-01,
   4.06309343e-01,   4.21782767e-01,   4.37333383e-01,   4.52945843e-01,
   4.68604740e-01,   4.84294620e-01,   5.00000000e-01,   5.15705380e-01,
   5.31395260e-01,   5.47054157e-01,   5.62666617e-01,   5.78217233e-01,
   5.93690657e-01,   6.09071621e-01,   6.24344944e-01,   6.39495553e-01,
   6.54508497e-01,   6.69368960e-01,   6.84062276e-01,   6.98573945e-01,
   7.12889646e-01,   7.26995250e-01,   7.40876837e-01,   7.54520708e-01,
   7.67913397e-01,   7.81041689e-01,   7.93892626e-01,   8.06453527e-01,
   8.18711995e-01,   8.30655933e-01,   8.42273553e-01,   8.53553391e-01,
   8.64484314e-01,   8.75055535e-01,   8.85256621e-01,   8.95077506e-01,
   9.04508497e-01,   9.13540287e-01,   9.22163963e-01,   9.30371014e-01,
   9.38153340e-01,   9.45503262e-01,   9.52413526e-01,   9.58877313e-01,
   9.64888243e-01,   9.70440384e-01,   9.75528258e-01,   9.80146843e-01,
   9.84291581e-01,   9.87958381e-01,   9.91143625e-01,   9.93844170e-01,
   9.96057351e-01,   9.97780982e-01,   9.99013364e-01,   9.99753280e-01,
   1.00000000e+00,   9.99753280e-01,   9.99013364e-01,   9.97780982e-01,
   9.96057351e-01,   9.93844170e-01,   9.91143625e-01,   9.87958381e-01,
   9.84291581e-01,   9.80146843e-01,   9.75528258e-01,   9.70440384e-01,
   9.64888243e-01,   9.58877313e-01,   9.52413526e-01,   9.45503262e-01,
   9.38153340e-01,   9.30371014e-01,   9.22163963e-01,   9.13540287e-01,
   9.04508497e-01,   8.95077506e-01,   8.85256621e-01,   8.75055535e-01,
   8.64484314e-01,   8.53553391e-01,   8.42273553e-01,   8.30655933e-01,
   8.18711995e-01,   8.06453527e-01,   7.93892626e-01,   7.81041689e-01,
   7.67913397e-01,   7.54520708e-01,   7.40876837e-01,   7.26995250e-01,
   7.12889646e-01,   6.98573945e-01,   6.84062276e-01,   6.69368960e-01,
   6.54508497e-01,   6.39495553e-01,   6.24344944e-01,   6.09071621e-01,
   5.93690657e-01,   5.78217233e-01,   5.62666617e-01,   5.47054157e-01,
   5.31395260e-01,   5.15705380e-01,   5.00000000e-01,   4.84294620e-01,
   4.68604740e-01,   4.52945843e-01,   4.37333383e-01,   4.21782767e-01,
   4.06309343e-01,   3.90928379e-01,   3.75655056e-01,   3.60504447e-01,
   3.45491503e-01,   3.30631040e-01,   3.15937724e-01,   3.01426055e-01,
   2.87110354e-01,   2.73004750e-01,   2.59123163e-01,   2.45479292e-01,
   2.32086603e-01,   2.18958311e-01,   2.06107374e-01,   1.93546473e-01,
   1.81288005e-01,   1.69344067e-01,   1.57726447e-01,   1.46446609e-01,
   1.35515686e-01,   1.24944465e-01,   1.14743379e-01,   1.04922494e-01,
   9.54915028e-02,   8.64597129e-02,   7.78360372e-02,   6.96289865e-02,
   6.18466600e-02,   5.44967379e-02,   4.75864738e-02,   4.11226872e-02,
   3.51117571e-02,   2.95596155e-02,   2.44717419e-02,   1.98531572e-02,
   1.57084194e-02,   1.20416190e-02,   8.85637464e-03,   6.15582970e-03,
   3.94264934e-03,   2.21901770e-03,   9.86635786e-04,   2.46719817e-04,
   0.00000000e+00]"""


"""(isReal, fftbuffer, X) = testRealEven(x)

print isReal
print fftbuffer
print X"""


