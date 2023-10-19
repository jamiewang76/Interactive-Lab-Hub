# To begin using librosa we need to import it, and other tools such as matplotlib and numpy
from pylab import *
import librosa             # The librosa library
import librosa.display     # librosa's display module (for plotting features)
# import IPython.display     # IPython's display module (for in-line audio)
import matplotlib.pyplot as plt # matplotlib plotting functions
import matplotlib.style as ms   # plotting style
import numpy as np              # numpy numerical functions
ms.use('seaborn-muted')         # fancy plot designs

# create a sine wave from scratch 
# try to modify some parameters
A = 1;
f = 440;
# f = 440 * 11
phi = 0;
sr = 44100;
# sr = 4410
T = 2;
y = [A * sin(2*pi*f*t + phi) for t in arange(0.,T,1./sr)]
IPython.display.Audio(data=y, rate=sr) # press the "play" button to hear audio