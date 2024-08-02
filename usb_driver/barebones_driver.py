#!usr/bin/python

import serial
import subprocess, sys
import adafruit_rsa
from adafruit_rsa import PublicKey, PrivateKey
import json

scada_message = "hpbangandolufsen"
device_message = "SJP587!team"

with open("adafruit_rsa_keys/device_small_prv.json", "r") as f:
    device_priv_key_obj = json.loads(f.read())
device_small_prv_key = PrivateKey(*device_priv_key_obj["private_key_arguments"])

with open("adafruit_rsa_keys/hmi_small_prv.json", "r") as f:
    hmi_priv_key_obj = json.loads(f.read())
hmi_small_prv_key = PrivateKey(*hmi_priv_key_obj["private_key_arguments"])


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
        line = ser.readline().decode("utf-8")
        if len(line) == 0:
            print("Nothing from device in verify_device")
        else:
            try:
                decrypted_message = adafruit_rsa.decrypt(line, device_small_prv_key)
                print("Decrypted Message: ", decrypted_message.decode("utf-8"))
            except:
                print(line, " failed to decrypt")
                print("Length from driver: ", len(line))
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
verify_device()
while True:
    line = ser.readline()
    if len(line) == 0:
        print("Nothing to see here")
    else:
        print(line)

