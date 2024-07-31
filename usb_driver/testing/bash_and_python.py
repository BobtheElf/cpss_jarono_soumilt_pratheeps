#!/usr/bin/python

import subprocess, sys

#Get the result of nabbing the usb list to do something with later
result = subprocess.check_output("lsusb", text = True)

print(result)