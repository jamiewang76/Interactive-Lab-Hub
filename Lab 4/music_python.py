import sounddevice as sd
import numpy as np

# Initialize parameters
A = 1  # Amplitude
frequency = 440  # Fixed frequency
phi = 0  # Phase
sr = 44100  # Sample rate

# Start the sound stream
sd_stream = sd.OutputStream(callback=None, channels=1, samplerate=sr, dtype='float32')
sd_stream.start()

while True:
    try:
        t = np.arange(sr) / sr  # Generate a time vector for one second
        y = A * np.sin(2 * np.pi * frequency * t + phi).astype('float32')
        sd_stream.write(y)
    except KeyboardInterrupt:
        break

# Stop and close the sound stream
sd_stream.stop()
sd_stream.close()