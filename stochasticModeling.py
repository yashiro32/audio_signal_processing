import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../software/models/'))
import utilFunctions as UF
import stochasticModel as STM

# Read input sound
(fs, x) = UF.wavread('../sounds/ocean.wav')

# Compute stochastic model
H = 128
stocf = .2
stocEnv = STM.stochasticModelAnal(x, H, H*2, stocf)

# Synthesize sound from stochastic model
y = STM.stochasticModelSynth(stocEnv, H, N)
