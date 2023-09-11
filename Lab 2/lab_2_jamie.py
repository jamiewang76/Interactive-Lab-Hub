import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
import tkinter as tk


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

event_num = 0

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
year_bk_1 = 1983

initial_time = int(time.time()) #frame of reference in seconds

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
    display_option1 = "> Forward to the back"
    display_option2 = "> Back to the future"

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")
    draw.text((x2, y2), display_hour, font=time_font, fill="#FFFFFF")
    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")
    draw.text((x4, y4), display_title2, font=text_font, fill="#20E200")
    draw.text((x5, y5), display_option1, font=text_font, fill="#FFFFFF")
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")

def ToPast():
    Jiao()
    PastCarousel()


def Jiao():
    time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

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
    display_option1 = "> Forward to the back"
    display_option2 = "> Back to the future"

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")
    draw.text((x2, y2), display_hour, font=time_font, fill="#FFFFFF")
    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")
    draw.text((x4, y4), display_title2, font=text_font, fill="#20E200")
    draw.text((x5, y5), display_option1, font=text_font, fill="#FFFFFF")
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")

    time.sleep(5)

def PastCarousel():
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


def Internet():
    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

    x3 = 0.1*width
    y3 = 0.33*height
    x4 = 0.4*width
    y4 = 0.46*height

    display_title = "ARE YOU READY"
    display_title2 = "FOR TIME TRAVEL?"

    draw.text((x3, y3), display_title, font=text_font, fill="#E20000")
    draw.text((x4, y4), display_title2, font=text_font, fill="#E20000")

def Moon():
    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

    x3 = 0.1*width
    y3 = 0.33*height
    x4 = 0.4*width
    y4 = 0.46*height

    display_title = "ARE YOU READY"
    display_title2 = "FOR TIME TRAVEL?"

    draw.text((x3, y3), display_title, font=text_font, fill="#E2B100")
    draw.text((x4, y4), display_title2, font=text_font, fill="#E2B100")

def WWII():
    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

    x3 = 0.1*width
    y3 = 0.33*height
    x4 = 0.4*width
    y4 = 0.46*height

    display_title = "ARE YOU READY"
    display_title2 = "FOR TIME TRAVEL?"

    draw.text((x3, y3), display_title, font=text_font, fill="#00BAE2")
    draw.text((x4, y4), display_title2, font=text_font, fill="#00BAE2")

def Wright():
    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

    time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

    x1 = 0.3*width
    y1 = 0.05*height
    x2 = 0.35*width
    y2 = 0.17*height

    display_date = strftime("%m/%d/%Y")
    display_hour = strftime("%H:%M:%S")

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")
    draw.text((x2, y2), display_hour, font=time_font, fill="#FFFFFF")

    x3 = 0.1*width
    y3 = 0.33*height
    x4 = 0.4*width
    y4 = 0.46*height

    display_title = "ARE YOU READY"
    display_title2 = "FOR TIME TRAVEL?"

    draw.text((x3, y3), display_title, font=text_font, fill="#9A00E2")
    draw.text((x4, y4), display_title2, font=text_font, fill="#9A00E2")


def ToFuture():
    time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

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
    display_option1 = "> Forward to the back"
    display_option2 = "> Back to the future"

    draw.text((x1, y1), display_date, font=time_font, fill="#FFFFFF")
    draw.text((x2, y2), display_hour, font=time_font, fill="#FFFFFF")
    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")
    draw.text((x4, y4), display_title2, font=text_font, fill="#20E200")
    draw.text((x5, y5), display_option1, font=text_font, fill="#FFFFFF")
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")


while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=400)

    if state == 0:
        main_screen()
        if buttonA.value and not buttonB.value:
            state = 1
        if buttonB.value and not buttonA.value:
            state = 2
    
    if state == 1:
        ToPast()
        if buttonA.value and not buttonB.value:
            event_num+=1
        if buttonB.value and not buttonA.value:
            event_num+=1

    if state == 2:
        ToFuture()

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.5)