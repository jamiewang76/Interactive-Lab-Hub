import numpy as np
import sounddevice as sd
import time

# Initialize parameters
A = 1
f = 1000
phi = 0
sr = 44100

# Main loop
while True:
    # Create a sine wave
    T = 1  # Time duration for each frequency step
    t = np.linspace(0, T, int(sr * T), endpoint=False)
    y = A * np.sin(2 * np.pi * f * t + phi)

    # Play the sine wave
    sd.play(y, sr)
    sd.wait()

    # Increase the frequency
    f += 100  # You can adjust the frequency increment as needed
    
    # Add a small delay before the next iteration (optional)
    time.sleep(0.5)  # Adjust the delay time as needed