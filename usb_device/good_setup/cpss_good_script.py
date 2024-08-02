#Copied from bad_script
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
import sys

#Usb_device.py : 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time

#Giving the HMI a signed message
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# Verification message
device_message = b'SJP587!team'

# Function to encrypt data
def encrypt_data(data):
    encrypted_data = cipher_rsa.encrypt(data.encode('utf-8'))
    return encrypted_data

key = RSA.import_key(open('usb_prv_key.pem').read())
h = SHA256.new(device_message)
signature = pkcs1_15.new(key).sign(h)

# Load the public key (ensure you have the public key file 'public_key.pem')
with open('hmi_pub_key.pem', 'rb') as f:
    public_key = RSA.import_key(f.read())

cipher_rsa = PKCS1_OAEP.new(public_key)

encrypted_data = encrypt_data(signature)

print(encrypted_data)

# Set up Consumer Control - Control Codes can be found here: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/consumer_control_code.html#ConsumerControlCode
cc = ConsumerControl(usb_hid.devices)

# Set up a keyboard device. - Keycode can be found here: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html#Keycode
keyboard = Keyboard(usb_hid.devices)

# Set up keyboard to write strings from macro
write_text = KeyboardLayoutUS(keyboard)

buttons = [board.GP0]
key = [digitalio.DigitalInOut(pin_name) for pin_name in buttons]
for x in range(0,len(buttons)):
    key[x].direction = digitalio.Direction.INPUT
    key[x].pull = digitalio.Pull.DOWN

while True:
    if key[0].value:
        print("Hello, World!\n")
        time.sleep(0.3)
    time.sleep(0.1)