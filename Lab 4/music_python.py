import sounddevice as sd
import numpy as np
import keyboard

# Define the constant frequency
frequency = 440  # Change this to your desired frequency

# Create a time vector
fs = 44100  # Sample rate
t = np.arange(0, 10, 1/fs)  # This generates a 10-second time vector

# Initialize a flag to indicate if the sound is playing
sound_playing = True

# Function to toggle the sound state
def toggle_sound_state(e):
    global sound_playing
    sound_playing = not sound_playing

# Register the spacebar key event
keyboard.on_press_key('space', toggle_sound_state)

while True:
    if sound_playing:
        # Generate a sine wave with the constant frequency
        y = np.sin(2 * np.pi * frequency * t)

        # Play the sine wave
        sd.play(y, fs, blocking=False)  # Use blocking=False to play the sound without blocking the loop
    else:
        sd.stop()  # Stop the sound if the spacebar is held down

keyboard.wait('esc')  # Wait for the 'esc' key to exit the program