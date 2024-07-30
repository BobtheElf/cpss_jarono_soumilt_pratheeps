# Cyber Physical Systems Security Final Project Repo
## Overview
A repository to hold all of the files for a secure USB system.
## Files
Files are organized into denoted as universal files or subsystem-specific files. There are universal files and subsystem-specific files.
### Universal Files
These files appear at the root of the repo and include this README.md (denotes structure of the repo), the .gitignore (which files should be tracked and untracked), and the 'enough git to skin a cat.txt' (custom tutorial file made to show and explain the most common functionalities of git) files.
### Subsystem-specific Files
These files are used to create specific parts of a secure USB system, and are partitioned into folders that denote their function. Each subfolder may have a README.md file which describes how to set up this part of the USB system.
## Project Requirements
To emulate a secure USB system, this project requires a USB device, a bad USB device, a computer which runs a USB driver, and another computer which runs a verification on the USB device.
### USB Device
This is the code for a device emulating a PLC (programmable logic controller) or HID (human interface device) which plugs into a usb port. This code is further partitioned into a **Good USB Device** and a **Bad USB Device**.
#### Good USB Device
This device has code with the following requirements:
- Device encrypts all data sent using the HMI computer’s public key
- First thing sent from device upon plugging the device in is authentication key
- Waits for action (keypress, for example) from the user
- If there is a keypress, the pico sends an encrypted message as if it was a keyboard
#### Bad USB Device
This device needs two abilities for testing:
- Device sends random keyboard macro or command to the computer (either with or without keypress - it doesn't matter)
- Device listens to data sent to another USB device
### USB Driver
This is the code emulating how an HMI (human machine interface) should act in the event a USB device is plugged into a USB port. Note that this should also apply to SCADA (supervisory control and data acquisition) computers should also act, but we will refer to the computer that implements this code as the HMI computer.
- Waits for device to send something
- If the device sends valid encryption key
  - Device goes to 'registered' state
  - Sends same key in encrypted message to a different SCADA computer
  - If other SCADA computer authenticates device
    - Device goes to 'validated' state and is allowed to send encrypted information
    - Wait for information, and decrypt it to display
  - Else
    - Device goes to 'flagged' state and is not allowed to send information
    - Sends alert to HMI computer saying that device has been registered on this computer but is not registered on SCADA computer. Either update the keys or remove this device.
    - Device is ignored.
- When the device is ignored, end the driver program.
### Verification
This is the code emulating how a SCADA computer should act in the event a USB device is plugged into an HMI or other SCADA computer's USB port to verify if the device should be able to send information to the computer.
- Waits for other computer to send authentication key
- If authentication key is valid
  - Over an encrypted channel, send signal to HMI computer to put the device into a 'verified' state
- Else
  - Over an encrypted channel, send signal to HMI computer to put the device into a 'flagged' state
  - Display alert saying that there is a device that is registered on the HMI but not the SCADA, and to fix this
