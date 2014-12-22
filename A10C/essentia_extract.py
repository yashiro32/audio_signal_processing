import os

import essentia
import essentia.standard as ess
import essentia.streaming

import numpy as np

fpaths = []
labels = []
spoken = []
folders = []
for f in os.listdir('testDownload'):
    for w in os.listdir('testDownload/' + f):
        if os.path.isdir('testDownload/' + f + '/' + w):
            folders.append(w)
            for music in os.listdir('testDownload/' + f + '/' + w):
                if music.endswith('.mp3'):
                    fpaths.append('testDownload/' + f + '/' + w + '/' + music)  
                    labels.append(f)
                    if f not in spoken:
                        spoken.append(f)

#print 'Words spoken:',spoken
#print len(fpaths)
#print len(labels)
#print len(folders)


M = 1024
N = 1024
H = 512
fs = 44100
spectrum = ess.Spectrum(size=N)
window = ess.Windowing(size=M, type='hann')
mfcc = ess.MFCC(numberCoefficients = 40, inputSize = N/2+1)
lpc = ess.LPC()
extractor = ess.Extractor()

c = 0

for n,file in enumerate(fpaths):
    x = ess.MonoLoader(filename=file, sampleRate = fs)()
    
    """pool = essentia.Pool()

    mfccs = np.array([])
    
    for frame in ess.FrameGenerator(x, frameSize=M, hopSize=H, startFromZero=True):
        mX = spectrum(window(frame))
        mfcc_bands, mfcc_coeffs = mfcc(mX)
        
        #if len(mfccs) == 0:
            #mfccs = mfcc_coeffs
        #else:
            #mfccs = np.vstack((mfccs, mfcc_coeffs))

        pool.add('lowlevel.mfcc', mfcc_coeffs)
        #pool.add('lowlevel.mfcc_bands', mfcc_bands)

        #lpcs, reflections = lpc(frame)
        #pool.add('lowlevel.lpc', lpcs) """

    pool = extractor(x)
    
    #mfccs_mean = np.mean(mfccs, axis=0)
    # Compute mean and variance of the frames
    aggrPool = ess.PoolAggregator(defaultStats = ['mean'])(pool)

    """print 'Original pool descriptor names:'
    print pool.descriptorNames()
    print
    print 'Aggregated pool descriptor names:'
    print aggrPool.descriptorNames()"""

    # And output those results in a file
    start_folder = 'essentiaDownload2/'
    if not os.path.exists(start_folder + labels[c]):
        os.makedirs(start_folder + labels[c])
    if not os.path.exists(start_folder + labels[c] + '/' + folders[c]):
        os.makedirs(start_folder + labels[c] + '/' + folders[c])
    #ess.YamlOutput(filename = start_folder + labels[c] + '/' + folders[c] + '/' + folders[c] + '.json', format='json')(aggrPool)

    c += 1
    
        

    
