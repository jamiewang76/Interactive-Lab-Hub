import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

# Parameters
duration = 3  # Duration in seconds
sample_rate = 44100  # Sample rate (samples per second)
frequency = 1000  # Frequency of the sine wave (Hz)
amplitude = 0.5  # Amplitude of the sine wave (between -1 and 1)

# Generate the time values
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate the sine wave
sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)

# Visualize the waveform (optional)
plt.plot(t, sine_wave)
plt.title("Sine Wave")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()

# Play the sound
sd.play(sine_wave, sample_rate)
sd.wait()