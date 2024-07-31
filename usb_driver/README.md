# USB Driver
This is the code that determines how the USB driver acts on a Linux system
## Requirements
The end goal is to securely monitor and translate between a USB device/PLC and an HMI computer. In order to do this, the script needs to have these attributes
- Find all of the current usb devices (have a whitelist for this computer's keyboard and mouse for now)
- Wait until there is a new usb device
- Send the usb device the HMI public key
- Wait for a response with a signed, predetermined secret message (if verification fails, turn off the port)
- Send the signed, predetermined secret message to another computer (ignore any data coming from the device)
- Wait for the other computer to verify the key
- If the other computer verifies the key
  - Stop ignoring the device
- Else
  - Turn off the port
## Setup
Make sure you have a terminal command that can run python scripts and bash scripts (Ubuntu, Debian, etc. with python3 command, earlier versions like python command fail due to bash-python interfacing)
Run command:
```
python3 script.py
```
