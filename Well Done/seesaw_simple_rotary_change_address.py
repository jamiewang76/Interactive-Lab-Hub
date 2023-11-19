from __future__ import print_function
import board
from adafruit_seesaw import seesaw, rotaryio, digitalio
import time
import sys

old_address = 0x36 # default
new_address = 0x37 # must be within 0x07 to 0x78, DEFAULT: 0x72

def runExample():

	i2c = board.I2C()  # uses board.SCL and board.SDA
	print("Connected!")
	qt_enc1 = seesaw.Seesaw(i2c, addr=0x36)
	qt_enc1.setI2CAddr(0x37)
	while True:
		time.sleep(1) # do nothing

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 17")
		sys.exit(0)