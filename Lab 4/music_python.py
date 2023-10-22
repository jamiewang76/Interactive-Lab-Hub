import sounddevice as sd
import numpy as np

# Define the constant frequency
frequency = 440  # Change this to your desired frequency

# Create a time vector
fs = 44100  # Sample rate
t = np.arange(0, 10, 1/fs)  # This generates a 1-second time vector, but the sound will play indefinitely

while True:
    # Generate a sine wave with the constant frequency
    y = np.sin(2 * np.pi * frequency * t)

    # Play the sine wave
    sd.play(y, fs, blocking=False)  # Use blocking=False to play the sound without blocking the loop

    # Wait for the sound to finish (optional, add a delay to avoid excessive CPU usage)
    sd.wait()