# SPDX-FileCopyrightText: 2021 John Park
# SPDX-License-Identifier: MIT

# I2C rotary encoder multiple test example.
# solder the A0 jumper on the second QT Rotary Encoder board

import board
import time
from adafruit_seesaw import seesaw, rotaryio, digitalio, neopixel

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

qt_enc1 = seesaw.Seesaw(i2c, addr=0x36)  # 1
qt_enc2 = seesaw.Seesaw(i2c, addr=0x3C)  # 2
qt_enc3 = seesaw.Seesaw(i2c, addr=0x3A)  # 3
qt_enc4 = seesaw.Seesaw(i2c, addr=0x38)  # 4

qt_enc1.pin_mode(24, qt_enc1.INPUT_PULLUP)
button1 = digitalio.DigitalIO(qt_enc1, 24)
button_held1 = False

qt_enc2.pin_mode(24, qt_enc2.INPUT_PULLUP)
button2 = digitalio.DigitalIO(qt_enc2, 24)
button_held2 = False

qt_enc3.pin_mode(24, qt_enc3.INPUT_PULLUP)
button3 = digitalio.DigitalIO(qt_enc3, 24)
button_held3 = False

qt_enc4.pin_mode(24, qt_enc4.INPUT_PULLUP)
button4 = digitalio.DigitalIO(qt_enc4, 24)
button_held4 = False

encoder1 = rotaryio.IncrementalEncoder(qt_enc1)
last_position1 = None

encoder2 = rotaryio.IncrementalEncoder(qt_enc2)
last_position2 = None

encoder3 = rotaryio.IncrementalEncoder(qt_enc3)
last_position3 = None

encoder4 = rotaryio.IncrementalEncoder(qt_enc4)
last_position4 = None

pixel1 = neopixel.NeoPixel(qt_enc1, 6, 1)
pixel1.brightness = 0.2
pixel1.fill(0xFF0000)

pixel2 = neopixel.NeoPixel(qt_enc2, 6, 1)
pixel2.brightness = 0.2
pixel2.fill(0x0000FF)

pixel3 = neopixel.NeoPixel(qt_enc3, 6, 1)
pixel3.brightness = 0.2
pixel3.fill(0x00FF00)

pixel4 = neopixel.NeoPixel(qt_enc4, 6, 1)
pixel4.brightness = 0.2
pixel4.fill(0x00FF00)

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = "{:02d}:{:02d}".format(mins, secs)
        print(timeformat, end="\r")
        time.sleep(1)
        seconds -= 1

    print("Time's up!")


while True:
    # negate the position to make clockwise rotation positive
    position1 = -encoder1.position
    position2 = -encoder2.position
    position3 = -encoder3.position
    position4 = -encoder4.position

    if position1 != last_position1:
        last_position1 = position1
        print("Position 1: {}".format(position1))

    if not button1.value and not button_held1:
        button_held1 = True
        pixel1.brightness = 0.5
        print("Button 1 pressed")
        countdown_timer(position1)

    if button1.value and button_held1:
        button_held1 = False
        pixel1.brightness = 0.2
        print("Button 1 released")

    if position2 != last_position2:
        last_position2 = position2
        print("Position 2: {}".format(position2))

    if not button2.value and not button_held2:
        button_held2 = True
        pixel2.brightness = 0.5
        print("Button 2 pressed")

    if button2.value and button_held2:
        button_held2 = False
        pixel2.brightness = 0.2
        print("Button 2 released")

    if position3 != last_position3:
        last_position3 = position3
        print("Position 3: {}".format(position3))

    if not button3.value and not button_held2:
        button_held3 = True
        pixel3.brightness = 0.5
        print("Button 3 pressed")

    if button3.value and button_held3:
        button_held3 = False
        pixel3.brightness = 0.2
        print("Button 3 released")

    if position4 != last_position4:
        last_position4 = position4
        print("Position 4: {}".format(position4))

    if not button4.value and not button_held4:
        button_held4 = True
        pixel4.brightness = 0.5
        print("Button 4 pressed")

    if button4.value and button_held4:
        button_held4 = False
        pixel4.brightness = 0.2
        print("Button 4 released")

    # Set the countdown time (in seconds)
    countdown_time = 300  # 5 minutes

    countdown_timer(countdown_time)