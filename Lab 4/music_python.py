import numpy as np
import sounddevice as sd

# Create a sine wave
A = 1
f = 1000
phi = 0
sr = 44100
T = 2
t = np.linspace(0, T, int(sr * T), endpoint=False)
y = A * np.sin(2 * np.pi * f * t + phi)

# Play the sine wave
sd.play(y, sr)
sd.wait()