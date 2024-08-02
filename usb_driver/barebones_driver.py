#!usr/bin/python

import serial
import subprocess, sys

scada_message = "hpbangandolufsen"
device_message = b'SJP587!team'

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
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 10)
    #Wait for encrypted, signed message from the device HMI public key is already on the device
    while True:
        line = ser.readline()
        if len(line) == 0:
            print("Nothing from device")
        else:
            print(line)
            key = RSA.import_key(open('rsa_examples/keys/usb_pub_key.pem').read())
            h = SHA256.new(device_message)
            try:
                pkcs1_15.new(key).verify(h, line)
                print("The signature is valid.")
            except (ValueError, TypeError):
                print("The signature is not valid.")

            break
    print("Verification complete")
# ============================================================


# ============================================================
#Start the main block
wait_for_usb()
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 10)
    print("Connection successful")
except:
    print("Device not connected")
#listen for input like on Google
while True:
    line = ser.readline()
    if len(line) == 0:
        print("Nothing to see here")
    else:
        print(line)

