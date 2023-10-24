import sounddevice as sd
import numpy as np
import time

# Initialize parameters
A = 1  # Amplitude
frequency1 = 390  # First frequency
frequency2 = 490  # Second frequency
frequency3 = 590  # Third frequency
phi = 0  # Phase
sr = 44100  # Sample rate

chords_list = [[260,330,390],[290,370,440],[330,420,490],[370,470,550],[390,490,590]]

# Start the sound stream
sd_stream = sd.OutputStream(callback=None, channels=1, samplerate=sr, dtype='float32')
sd_stream.start()

# Define the time interval for changing the frequency (0.1 seconds)
change_interval = 0.1  # seconds
next_change_time = time.time() + change_interval

while True:
    # Check if it's time to change the frequencies
    if time.time() >= next_change_time:
        # frequency1 -= 10
        # frequency3 += 10
        print(f"F1: {frequency1} | F2: {frequency2} | F3: {frequency3}")
        next_change_time += change_interval

    try:
        t = np.arange(int(sr * change_interval)) / sr  # Generate a time vector for the specified duration
        # Generate audio signals for all three frequencies
        y1 = A * np.sin(2 * np.pi * frequency1 * t + phi).astype('float32')
        y2 = A * np.sin(2 * np.pi * frequency2 * t + phi).astype('float32')
        y3 = A * np.sin(2 * np.pi * frequency3 * t + phi).astype('float32')
        # Add the three signals together
        y = (y1 + y2 + y3) / 3  # Adjust the scaling factor for desired volume balance

        sd_stream.write(y)
    except KeyboardInterrupt:
        break

# Stop and close the sound stream
sd_stream.stop()
sd_stream.close()