#In common with bad_script
import board
import digitalio

#Usb_device.py : 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time

#Giving the HMI a signed message
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import usb_serial

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