from __future__ import print_function
import qwiic_joystick
import time
import sys
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
import tkinter as tk

import ssl
import paho.mqtt.client as mqtt
import uuid

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/your/topic/here'

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
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

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90
state = 0
Jiao_run = False
event_num = 0
myJoystick = qwiic_joystick.QwiicJoystick()
timeTravel = False

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
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
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


current_year = 2023
# year_bk_1 = 1983
start_year = 2023
current_year = 2023
pictures = {2093: "2093.png",
            2083: "2083.png",
            2073: "mars.png",
            2063: "2063.png",
            2053: "2053.png",
            2043: "2043.png",
            2033: "2033.png",
            2023: "Hawaii.png",
            2013: "Obama.png", 
            2003: "Shenzhou.png", 
            1993: "Schindler.png", 
            1983: "MarioBros.png", 
            1973: "Viet.png", 
            1963: "JFK.png", 
            1953: "Queen.png", 
            1943: "1943.png",
            1933: "Depression.png", 
            1923: "Turkey.png", 
            1913: "Wilson.png",
            1903: "wright.png"}

initial_time = int(time.time()) #frame of reference in seconds

def editImage(filename):
    image = Image.open(filename).convert("RGB")
    
    
     # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2 - (scaled_height - height) // 2
    image = image.crop((x, y, x + width, y + height - 40))

    
    return image


def delta_sleep(s):
    """
    Parameters:
        s: seconds since elapsed to sleep until
    """
    if int(time.time()) > initial_time + s:
        # check if the delta time has already passed
        return
    else:
        # find time needed to sleep to reach the specified param 's'
        needed_sleep = (initial_time+s) - int(time.time())
        time.sleep(needed_sleep)

def main_screen():
    time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)

    x1 = 0.3*width
    y1 = 0.05*height
    x2 = 0.35*width
    y2 = 0.17*height

    x3 = 0.1*width
    y3 = 0.33*height
    x4 = 0.4*width
    y4 = 0.46*height

    x5 = 0.1*width
    y5 = 0.65*height
    x6 = 0.1*width
    y6 = 0.80*height

    display_date = strftime("%m/%d/%Y")
    display_hour = strftime("%H:%M:%S")
    display_title = "ARE YOU READY"
    display_title2 = "FOR TIME TRAVEL?"
    display_option1 = "Steer Left to the back"
    display_option2 = "Steer Right to the future"

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")
    draw.text((x2, y2), display_hour, font=time_font, fill="#FFFFFF")
    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")
    draw.text((x4, y4), display_title2, font=text_font, fill="#20E200")
    draw.text((x5, y5), display_option1, font=text_font, fill="#FFFFFF")
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")


# def Jiao():
#     print("Jiao")
#     global Jiao_run
#     Jiao_run = True

#     x = 0.4*width
#     y = 0.46*height
    
#     if current_year > 1983:
#         draw.text((x, y), str(current_year), font=font, fill="#FFFFFF")
#         print(current_year)
#         disp.image(image, rotation)
#         current_year -= 10
#     elif current_year == 1983:
#         delta_sleep(5)
#         disp.image(image, rotation)
#         draw.text((x, y),'<<1983>>', font=font, fill="#FFFFFF")
    
#     global event_num
#     if event_num == 0:
#         event_num += 1

def JiaoPast():
    print("Jiao")
    global Jiao_run
    Jiao_run = True

    x = 0.4*width
    y = 0.46*height
    
    global current_year

    if current_year > 1983:
        draw.text((x, y), str(current_year), font=font, fill="#FFFFFF")
        print(current_year)
        disp.image(image, rotation)
        current_year -= 10
    elif current_year == 1983:
        delta_sleep(5)
        disp.image(image, rotation)
        draw.text((x, y),'<<1983>>', font=font, fill="#FFFFFF")
    
    global event_num
    if current_year == 1983:
        event_num += 1

def PastCarousel():
    global state
    if event_num == 1:
        Internet()
    if event_num == 2:
        Moon()
    if event_num == 3:
        WWII()
    if event_num == 4:
        Wright()
    if event_num == 5:
        state = 0
        global current_year
        current_year = 2023


def Internet():
    image.paste(editImage("dns.png"), (0,0))
    time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)

    x1 = 0.3*width
    y1 = 0.05*height

    display_date = "01/01/1983"

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")

    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    x6 = 0.1*width
    y6 = 0.80*height
    display_option2 = "> Continue"
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")

    x3 = 0.27*width
    y3 = 0.4*height
    display_title = "Advent of DNS"
    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")

    # disp.image(editImage("dns.png"), rotation)
    delta_sleep(1)

    print("internet")

def Moon():
    image.paste(editImage("moon.png"),(0,0))

    time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)

    x1 = 0.3*width
    y1 = 0.05*height

    display_date = "07/21/1969"

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")

    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    x6 = 0.1*width
    y6 = 0.80*height
    display_option2 = "> Continue"
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")

    x3 = 0.3*width
    y3 = 0.4*height
    display_title = "Land on Moon"
    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")


    # disp.image(editImage("moon.png"), rotation)
    delta_sleep(1)

    print("moon")

def WWII():
    image.paste(editImage("ww2.png"),(0,0))

    time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)

    x1 = 0.3*width
    y1 = 0.05*height

    display_date = "09/01/1939"

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")

    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    x6 = 0.1*width
    y6 = 0.80*height
    display_option2 = "> Continue"
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")

    x3 = 0.25*width
    y3 = 0.4*height
    display_title = "Beginning of WWII"
    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")

    # disp.image(editImage("ww2.png"), rotation)
    delta_sleep(1)

    print("wwii")

def Wright():
    image.paste(editImage("wright.png"),(0,0))

    time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

    x1 = 0.3*width
    y1 = 0.05*height
    x2 = 0.35*width
    y2 = 0.17*height

    display_date = "12/17/1903"
    display_hour = strftime("%H:%M:%S")

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")
    draw.text((x2, y2), display_hour, font=time_font, fill="#FFFFFF")

    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    x6 = 0.1*width
    y6 = 0.80*height
    display_option2 = "> Back to Present"
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")

    x3 = 0.15*width
    y3 = 0.4*height
    display_title = "Invention of Wright Flyer"
    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")

    # disp.image(editImage("wright.png"), rotation)
    delta_sleep(1)

    print("wright")
    print("past finished")

# def ToPast():
#     # print("to past")
#     if Jiao_run == False:
#         Jiao()
#     PastCarousel()
#     print("past finished")

def ToPastTest():
    # print("to past")
    if event_num >= 1:
        PastCarousel()
    # print("past finished")

def JiaoFuture():
    print("Jiao")
    global Jiao_run
    Jiao_run = True

    x = 0.4*width
    y = 0.46*height
    
    global current_year

    if current_year < 2053:
        draw.text((x, y), str(current_year), font=font, fill="#FFFFFF")
        print(current_year)
        disp.image(image, rotation)
        current_year += 10
    elif current_year == 2053:
        delta_sleep(5)
        disp.image(image, rotation)
        draw.text((x, y),'<<2050>>', font=font, fill="#FFFFFF")
    
    global event_num
    if current_year == 2053:
        event_num += 1

def FutureCarousel():
    global state
    if event_num == 1:
        Maldives()
    if event_num == 2:
        Flight()
    if event_num == 3:
        Mars()
    if event_num == 4:
        Cyborg()
    if event_num == 5:
        state = 0
        global current_year
        current_year = 2023
        
def Maldives():
    image.paste(editImage("maldives.png"),(0,0))

    time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)

    x1 = 0.3*width
    y1 = 0.05*height

    display_date = "07/05/2050"

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")

    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    x6 = 0.1*width
    y6 = 0.80*height
    display_option2 = "> Continue"
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")

    x3 = 0.3*width
    y3 = 0.4*height
    display_title = "Maldives Sinks"
    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")

    # disp.image(editImage("maldives.png"), rotation)
    delta_sleep(1)

    print("Maldives")

def Flight():
    image.paste(editImage("flight.png"),(0,0))

    time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)

    x1 = 0.3*width
    y1 = 0.05*height

    display_date = "10/01/2099"

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")

    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    x6 = 0.1*width
    y6 = 0.80*height
    display_option2 = "> Continue"
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")

    x3 = 0.2*width
    y3 = 0.4*height
    display_title = "Low Cost Private Jet"
    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")

    # disp.image(editImage("flight.png"), rotation)
    delta_sleep(1)

    print("flight")

def Mars():
    image.paste(editImage("mars.png"),(0,0))

    time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)

    x1 = 0.3*width
    y1 = 0.05*height

    display_date = "01/01/2192"

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")

    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    x6 = 0.1*width
    y6 = 0.80*height
    display_option2 = "> Continue"
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")

    x3 = 0.30*width
    y3 = 0.4*height
    display_title = "Colonize Mars"
    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")

    # disp.image(editImage("mars.png"), rotation)
    delta_sleep(1)

    print("Mars")

def Cyborg():
    image.paste(editImage("cyborg.png"),(0,0))

    time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

    x1 = 0.3*width
    y1 = 0.05*height
    x2 = 0.35*width
    y2 = 0.17*height

    display_date = "02/10/2258"
    display_hour = strftime("%H:%M:%S")

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")
    draw.text((x2, y2), display_hour, font=time_font, fill="#FFFFFF")

    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    x6 = 0.1*width
    y6 = 0.80*height
    display_option2 = "> Back to Present"
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")

    x3 = 0.35*width
    y3 = 0.4*height
    display_title = "Cyberware"
    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")

    # disp.image(editImage("cyborg.png"), rotation)
    delta_sleep(1)

    print("cyborg")
    print("future finished")

def ToFutureTest():
    # print("to past")
    if event_num >= 1:
        FutureCarousel()
    # print("past finished")

def time_travel():
    display_date = strftime("%m/%d")
    display_hour = strftime("%H:%M:%S")
    draw.text((100, 98), str(current_year), font=font, fill="#000000")
    draw.text((45, 114), str(display_date), font=font, fill="#000000")
    draw.text((135, 114), str(display_hour), font=font, fill="#000000")

    image.paste(editImage(pictures[current_year]), (0,0))

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=400)
    x = myJoystick.horizontal
    y = myJoystick.vertical
    b = myJoystick.button
    if current_year <= 1903:
        current_year = 1903
    if current_year >= 2093:
        current_year = 2093
    if x > 575:
         state = 1
         print("L", state)
         timeTravel = False
    elif x < 450:
         state = 1
         print("R", state)
         timeTravel = False
    if y > 575:
         state = 1
         print("U", state)
        #  draw.rectangle((0, 0, width, height), outline=0, fill="#FFFFFF")
         draw.text((100, 70), str(current_year), font=font, fill="#000000")
         print(current_year,"While true")
         current_year -= 10
         print(current_year,"While true")
         timeTravel = False
         val = current_year
         client.publish(topic, val)
         
    elif y < 450:
         state = 1
         print("D", state)
        #  draw.rectangle((0, 0, width, height), outline=0, fill="#000000")
         draw.text((100, 70), str(current_year), font=font, fill="#000000")

         print(current_year,"While true")
         current_year += 10
         print(current_year,"While true")
         timeTravel = False
    if x <= 575 and x >= 450 and y <= 575 and y >= 450:
        print("center",state)
        # draw.text((100, 70), str(current_year), font=font, fill="#000000")
        print(current_year,"While true")
        if state !=0:
            draw.text((100, 70), str(current_year), font=font, fill="#000000")
            draw.text((40, 20), "Press down button", font=font, fill="#000000")
            draw.text((52, 35), "to time travel!", font=font, fill="#000000")
        if timeTravel:
            time_travel()
        if b == 0:
            timeTravel = True
            print("Button")

    if state == 0:
        main_screen()
    # if state == 0:
    #     main_screen()
    #     print("state = 0")
    #     Jiao_run = False
    #     event_num = 0
    #     if buttonB.value and not buttonA.value:
    #         state = 1
    #     if buttonA.value and not buttonB.value:
    #         state = 2
    
    # elif state == 1:
    #     if current_year>1983:
    #         JiaoPast()

    #     ToPastTest()

    #     if buttonB.value and not buttonA.value:
    #         event_num+=1
    #         print("button B")
    #     if buttonA.value and not buttonB.value:
    #         event_num+=1
    #         print("button A")


    # elif state == 2:
    #     # ToFuture()
    #     if current_year<2053:
    #         JiaoFuture()

    #     ToFutureTest()

    #     if buttonB.value and not buttonA.value:
    #         event_num+=1
    #         print("button B")
    #     if buttonA.value and not buttonB.value:
    #         event_num+=1
    #         print("button A")

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.5)
