# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import

from time import strftime, sleep

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
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
# pylint: enable=line-too-long

# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

state = 0

# First define some constants to allow easy resizing of shapes.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
rotation = 90
padding = -2
top = padding
bottom = height - padding

# # Create blank image for drawing.
# # Make sure to create image with mode 'RGB' for full color.
# if disp.rotation % 180 == 90:
#     height = disp.width  # we swap height/width to rotate it to landscape!
#     width = disp.height
# else:
#     width = disp.width  # we swap height/width to rotate it to landscape!
#     height = disp.height
image = Image.new("RGB", (width, height))

# # Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# # Draw a black filled box to clear the image.
# draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
# disp.image(image)

# image = Image.open("red.jpg")

# # jamie
# image2 = Image.open("spider.jpeg")

# backlight = digitalio.DigitalInOut(board.D22)
# backlight.switch_to_output()
# backlight.value = True


# # Scale the image to the smaller screen dimension
# image_ratio = image.width / image.height
# screen_ratio = width / height
# if screen_ratio < image_ratio:
#     scaled_width = image.width * height // image.height
#     scaled_height = height
# else:
#     scaled_width = width
#     scaled_height = image.height * width // image.width
# image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

# # Scale jamie image to the smaller screen dimension
# image_ratio2 = image2.width / image2.height
# screen_ratio = width / height
# if screen_ratio < image_ratio2:
#     scaled_width = image2.width * height // image2.height
#     scaled_height = height
# else:
#     scaled_width = width
#     scaled_height = image2.height * width // image2.width
# image2 = image2.resize((scaled_width, scaled_height), Image.BICUBIC)

# # Crop and center the image
# x = scaled_width // 2 - width // 2
# y = scaled_height // 2 - height // 2
# image = image.crop((x, y, x + width, y + height))

# # Crop and center jamie image
# x = scaled_width // 2 - width // 2
# y = scaled_height // 2 - height // 2
# image2 = image2.crop((x, y, x + width, y + height))

# Display image.
# disp.image(image)
# /////////////////////////////////////
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

# /////////////////////////////////////

def scale_and_crop_and_center(image):
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))
    return image

def to_past():
    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)


    x3 = 0.1*width
    y3 = 0.33*height
    x4 = 0.4*width
    y4 = 0.46*height

    x5 = 0.1*width
    y5 = 0.65*height
    x6 = 0.1*width
    y6 = 0.80*height

    display_title = "ARE YOU READY"
    display_title2 = "FOR TIME TRAVEL?"
    display_option1 = "> Forward to the back"
    display_option2 = "> Back to the future"

    draw.text((x3, y3), display_title, font=text_font, fill="#20E200")
    draw.text((x4, y4), display_title2, font=text_font, fill="#20E200")
    draw.text((x5, y5), display_option1, font=text_font, fill="#FFFFFF")
    draw.text((x6, y6), display_option2, font=text_font, fill="#FFFFFF")

# def to_future():
#     image = Image.open("red.jpg")
#     image_ratio = image.width / image.height
#     screen_ratio = width / height
#     if screen_ratio < image_ratio:
#         scaled_width = image.width * height // image.height
#         scaled_height = height
#     else:
#         scaled_width = width
#         scaled_height = image.height * width // image.width
#     image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
#     x = scaled_width // 2 - width // 2
#     y = scaled_height // 2 - height // 2
#     image = image.crop((x, y, x + width, y + height))
#     disp.image(image, rotation)
    


# Main loop:
while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Main screen
    if state == 0:
        main_screen()
        # Top: state 1: go to past
        if buttonB.value and not buttonA.value:
            state = 1

        # Bottom: state 2: go to future
        elif not buttonB.value and buttonA.value:
            state = 2

    elif state == 1:
        to_past()

    # traveling to the past
    # elif state == 1:
    #     to_past()
    # elif state == 2:
    #     to_future()
        
        # # Top: randomize
        # if buttonB.value and not buttonA.value:
        #     selected_quote = randrange(10)
        #     selected_color = randrange(10)
        # # Bottom: return to main
        # elif not buttonB.value and buttonA.value:
        #     state = 0

    # # traveling to the future
    # elif state == 2:
    #     to_future()
        
    #     # Top: start mental minute and return to main when complete
    #     if buttonB.value and not buttonA.value:
    #         mental_minute()
    #         state = 0
    #     # Bottom: return to main
    #     elif not buttonB.value and buttonA.value:
    #         state = 0
    # Display image.
    disp.image(image, rotation)
    time.sleep(1)