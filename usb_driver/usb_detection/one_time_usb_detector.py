#!/usr/bin/python

import subprocess, sys

#Get the usb devices
result = subprocess.check_output("lsusb", text = True)
devices = result.split('\n')
num_devices = len(devices)
if devices[num_devices - 1] == "":
    devices = devices[0 : num_devices - 1]
    num_devices = num_devices - 1
# print(num_devices, end = "\n")
# print(devices)
# Determine if there is a new device plugged in
whitelist = ['Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub',
             'Bus 001 Device 005: ID 046d:c534 Logitech, Inc. Unifying Receiver',
             'Bus 001 Device 004: ID 04d9:0006 Holtek Semiconductor, Inc. ',
             'Bus 001 Device 003: ID 05e3:0610 Genesys Logic, Inc. 4-port hub',
             'Bus 001 Device 002: ID 2109:3431 VIA Labs, Inc. Hub',
             'Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub']
new_device = False
for device in devices:
    if device not in whitelist:
        new_device = True
        break
if new_device:
    print("New Device Detected")
else:
    print("No New Devices")
        
