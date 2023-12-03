# SPDX-FileCopyrightText: 2021 John Park
# SPDX-License-Identifier: MIT

# I2C rotary encoder multiple test example.
# solder the A0 jumper on the second QT Rotary Encoder board
username = 'ziyingwang76@gmail.com' # Your ClickSend username 
api_key = '0592FD37-2D0D-150E-7A56-000E6821998B' # Your Secure Unique API key 
msg_to = '+19178259760' # Recipient Mobile Number in international format (+61411111111 test number). 
msg_from = '' # Custom sender ID (leave blank to accept replies). 
msg_body = 'This message is from PI' # The message to be sent. 

# from __future__ import print_function
import json, subprocess 
import digitalio as digi
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import time
import threading
from adafruit_seesaw import seesaw, digitalio, rotaryio, neopixel

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digi.DigitalInOut(board.CE0)
# cs_seesaw = seesaw.Seesaw(i2c, addr=0x36)
# cs_pin = digitalio.DigitalIO(cs_seesaw, 22)
dc_pin = digi.DigitalInOut(board.D25)
# ds_seesaw = seesaw.Seesaw(i2c, addr=0x36)
# ds_pin = digitalio.DigitalIO(ds_seesaw, 22)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

buttonA = digi.DigitalInOut(board.D23)
buttonB = digi.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
# disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digi.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

#Init all stove timer
draw.text((0.02*width, 0.1*height), "Stove 1", font=font, fill=(255, 255, 255))
draw.text((0.02*width, 0.3*height), "Stove 2", font=font, fill=(255, 255, 255))
draw.text((0.02*width, 0.5*height), "Stove 3", font=font, fill=(255, 255, 255))
draw.text((0.02*width, 0.7*height), "Stove 4", font=font, fill=(255, 255, 255))
disp.image(image, rotation)


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

# def countdown_timer1(seconds):
#     while seconds:
#         mins, secs = divmod(seconds, 60)
#         timeformat = "{:02d}:{:02d}".format(mins, secs)
#         print(timeformat, end="\r")
#         time.sleep(1)
#         seconds -= 1

#     print("Time's up!")

def countdown_timer1(timer_name, initial_time):
    global draw, image, disp
    height_var = 0.1
    rect_height = 0.1
    while initial_time > 0:
        
        print(f"{timer_name}: {initial_time} seconds")
        time.sleep(1)
        initial_time -= 1
        if timer_name == "Stove 1":
            height_var = 0.1
            rect_height = 0
        if timer_name == "Stove 2":
            height_var = 0.3
            rect_height = 0.26
        if timer_name == "Stove 3":
            height_var = 0.5
            rect_height = 0.53
        if timer_name == "Stove 4":
            height_var = 0.7
            rect_height = 0.8
        # draw.rectangle((0.4*width, rect_height*height, width, 0.25*height), outline=0, fill=(0, 0, 0))
        draw.text((0.5*width, height_var*height), str(initial_time), font=font, fill=(255, 255, 255))
        disp.image(image, rotation)

    print(f"{timer_name}: Time's up!")
    msg_body = f"{timer_name} Done!"
    request = { "messages" : [ { "source":"rpi", "from":msg_from, "to":msg_to, "body":msg_body } ] } 
    request = json.dumps(request) 
    cmd = "curl https://rest.clicksend.com/v3/sms/send -u " + username + ":" + api_key + " -H \"Content-Type: application/json\" -X POST --data-raw '" + request + "'" 
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True) 
    (output,err) = p.communicate() 
    print 
    output

while True:
    # negate the position to make clockwise rotation positive
    # print("hiiiiii")
    position1 = -encoder1.position
    position2 = -encoder2.position
    position3 = -encoder3.position
    position4 = -encoder4.position

    # positions = [position1, position2, position3, position4]

    # if any(pos > 120 for pos in positions):
    #     for i, pos in enumerate(positions):
    #         if pos > 120:
    #             positions[i] = 120
    #             # print(f"Position {i + 1} is greater than 120: {pos}")
    #         if pos < 1:
    #             positions[i] = 1

    if position1 >= 120:
        position1 = 120
        encoder1.position = -120
    if position1 <= 1:
        position1 = 1
        encoder1.position = -1

    if position2 >= 120:
        position2 = 120
        encoder2.position = -120
    if position2 <= 1:
        position2 = 1
        encoder2.position = -1

    if position3 >= 120:
        position3 = 120
        encoder3.position = -120
    if position3 <= 1:
        position3 = 1
        encoder3.position = -1

    if position4 >= 120:
        position4 = 120
        encoder4.position = -120
    if position4 <= 1:
        position4 = 1
        encoder4.position = -1

    

    draw.rectangle((0.35*width, 0, width, height), outline=0, fill=(0, 0, 0))
    # disp.image(image, rotation)
    draw.text((0.35*width, 0.1*height), str(position1), font=font, fill=(255, 255, 255))
    draw.text((0.45*width, 0.1*height), " total", font=font, fill=(255, 255, 255))
    draw.text((0.35*width, 0.3*height), str(position2), font=font, fill=(255, 255, 255))
    draw.text((0.45*width, 0.3*height), " total", font=font, fill=(255, 255, 255))
    draw.text((0.35*width, 0.5*height), str(position3), font=font, fill=(255, 255, 255))
    draw.text((0.45*width, 0.5*height), " total", font=font, fill=(255, 255, 255))
    draw.text((0.35*width, 0.7*height), str(position4), font=font, fill=(255, 255, 255))
    draw.text((0.45*width, 0.7*height), " total", font=font, fill=(255, 255, 255))
    disp.image(image, rotation)

    # # print("hiiiiii")
    # position1 = -encoder1.position
    # position2 = -encoder2.position
    # position3 = -encoder3.position
    # position4 = -encoder4.position

    if position1 != last_position1:
        last_position1 = position1
        if position1 >= 120:
            position1 = 120
        if position1 <= 1:
            position1 = 1
        print("Position 1: {}".format(position1))
        # draw.text((0.4*width, 0.1*height), str(position1), font=font, fill=(255, 255, 255))
        # disp.image(image, rotation)
        # settime_text = draw.text((0.3*width, 0.1*height), position1, font=font, fill=(255, 255, 255))
        # print("hiiiiiii")

    if not button1.value and not button_held1:
        if position1 >= 120:
            position1 = 120
        if position1 <= 1:
            position1 = 1
        time1 = position1
        timer_thread1 = threading.Thread(target=countdown_timer1, args=("Stove 1", time1))
        timer_thread1.start()
        button_held1 = True
        pixel1.brightness = 0.5
        print("Button 1 pressed")

    if button1.value and button_held1:
        button_held1 = False
        pixel1.brightness = 0.2
        print("Button 1 released")

    if position2 != last_position2:
        last_position2 = position2
        if position2 >= 120:
            position2 = 120
        if position2 <= 1:
            position2 = 1
        print("Position 2: {}".format(position2))
        # draw.text((0.4*width, 0.3*height), str(position2), font=font, fill=(255, 255, 255))
        # disp.image(image, rotation)

    if not button2.value and not button_held2:
        if position2 >= 120:
            position2 = 120
        if position2 <= 1:
            position2 = 1
        time2 = position2
        timer_thread2 = threading.Thread(target=countdown_timer1, args=("Stove 2", time2))
        timer_thread2.start()
        button_held2 = True
        pixel2.brightness = 0.5
        print("Button 2 pressed")

    if button2.value and button_held2:
        button_held2 = False
        pixel2.brightness = 0.2
        print("Button 2 released")

    if position3 != last_position3:
        last_position3 = position3
        if position3 >= 120:
            position3 = 120
        if position3 <= 1:
            position3 = 1
        print("Position 3: {}".format(position3))
        # draw.text((0.4*width, 0.5*height), str(position3), font=font, fill=(255, 255, 255))
        # disp.image(image, rotation)

    if not button3.value and not button_held2:
        button_held3 = True
        if position3 >= 120:
            position3 = 120
        if position3 <= 1:
            position3 = 1
        time3 = position3
        timer_thread3 = threading.Thread(target=countdown_timer1, args=("Stove 3", time3))
        timer_thread3.start()
        pixel3.brightness = 0.5
        print("Button 3 pressed")
        
    if button3.value and button_held3:
        button_held3 = False
        pixel3.brightness = 0.2
        print("Button 3 released")

    if position4 != last_position4:
        last_position4 = position4
        if position4 >= 120:
            position4 = 120
        if position4 <= 1:
            position4 = 1
        print("Position 4: {}".format(position4))
        # draw.text((0.4*width, 0.7*height), str(position4), font=font, fill=(255, 255, 255))
        # disp.image(image, rotation)

    if not button4.value and not button_held4:
        button_held4 = True
        if position4 >= 120:
            position4 = 120
        if position4 <= 1:
            position4 = 1
        time4 = position4
        timer_thread4 = threading.Thread(target=countdown_timer1, args=("Stove 4", time4))
        timer_thread4.start()
        pixel4.brightness = 0.5
        print("Button 4 pressed")
        # msg_body = "Stove 4 Done!"
        # request = { "messages" : [ { "source":"rpi", "from":msg_from, "to":msg_to, "body":msg_body } ] } 
        # request = json.dumps(request) 
        # cmd = "curl https://rest.clicksend.com/v3/sms/send -u " + username + ":" + api_key + " -H \"Content-Type: application/json\" -X POST --data-raw '" + request + "'" 
        # p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True) 
        # (output,err) = p.communicate() 
        # print 
        # output
        

    if button4.value and button_held4:
        button_held4 = False
        pixel4.brightness = 0.2
        print("Button 4 released")

    # # Set the countdown time (in seconds)
    # countdown_time = 300  # 5 minutes

    # countdown_timer(countdown_time)