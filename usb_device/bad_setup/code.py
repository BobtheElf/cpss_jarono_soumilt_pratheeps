
'''

This is a pico macro keyboard based on CircuitPython adafruit_hid library
The PCB is currently in version one and thus the key layout is all crazy
like this:

    ****This will be fixed in Final version***

         key[0]    Key[3]   Key[6]

         key[1]    Key[4]   Key[7]

         key[2]    Key[5]   Key[8]

         key[9]    Key[10]   Key[11]

'''
#Import all the relevant Libraries

import time
import board
import digitalio
import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import random

# Set up Consumer Control - Control Codes can be found here: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/consumer_control_code.html#ConsumerControlCode
cc = ConsumerControl(usb_hid.devices)

# Set up a keyboard device. - Keycode can be found here: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html#Keycode
keyboard = Keyboard(usb_hid.devices)

# Set up keyboard to write strings from macro
write_text = KeyboardLayoutUS(keyboard)

# These are the corresponding GPIOs on the Pi Pico that is used for the Keys on the PCB
buttons = [board.GP0]
key = [digitalio.DigitalInOut(pin_name) for pin_name in buttons]
for x in range(0,len(buttons)):
    key[x].direction = digitalio.Direction.INPUT
    key[x].pull = digitalio.Pull.DOWN


time.sleep(5.0)
write_text.write("Hello, World! Press the button to write \"Hello, World\"")
while True:
    #Fix this key for each coach
    if key[0].value:
        write_text.write("Hello, World!\n")
        time.sleep(0.3)
    time.sleep(0.1)
