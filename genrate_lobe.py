import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../software/models/'))
import utilFunctions as UF

bins = np.array([-4.0,-3.0,-2.0,-1.0,0.0,1.0,2.0,3.0]) +.5
X = UF.genBhLobe(bins)
