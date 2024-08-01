#!usr/bin/python

import serial
import subprocess, sys
import rsa

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time

#Giving the HMI a signed message
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def wait_for_usb():
    # Code will break when the new usb device is detected
    new_device = False

    #Loop through and only break when there is a new usb device
    while not new_device:
        
        #Get the usb devices
        result = subprocess.check_output("lsusb", text = True)
        devices = result.split('\n')
        num_devices = len(devices)
        #If the last 'device' is just a '', get rid of it
        if devices[num_devices - 1] == "":
            devices = devices[0 : num_devices - 1]
            num_devices = num_devices - 1
        # print(num_devices, end = "\n")
        # print(devices)
        
        #Determine if there is a new device plugged in
        whitelist = ['1d6b:0003',
                     '046d:c534',
                     '04d9:0006',
                     '05e3:0610',
                     '2109:3431',
                     '1d6b:0002']
        for device in devices:
            if device[23 : 32] not in whitelist:
                new_device = True
                break
    print("New Device Detected")
# ============================================================
def verify_device():
    device_verified = False
    #Wait for encrypted, signed message from the device HMI public key is already on the device
    while True:
        line = ser.readline()
        if len(line) == 0:
            print("Nothing from device")
        else:
            print(line)
            key = RSA.import_key(open('rsa_examples/keys/usb_pub_key.pem').read())
            h = SHA256.new(message)
            try:
                pkcs1_15.new(key).verify(h, signature)
                print("The signature is valid.")
            except (ValueError, TypeError):
                print("The signature is not valid.")

            break
# ============================================================


# ============================================================
#Start the main block
wait_for_usb()
ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 10)
verify_device()
#listen for input like on Google
while True:
    line = ser.readline()
    if len(line) == 0:
        print("Nothing to see here")
    else:
        print(line)
        
#turn this into a while loop
# ser = serial.Serial('/dev/ttyACM0',9600)
# s = [0,1]
# while True:
# 	read_serial=ser.readline()
# 	s[0] = str(int (ser.readline(),16))
# 	print(s[0])
# 	print(read_serial)

