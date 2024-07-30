# How to set up a Raspberry Pi Pico to have the bad_script.py
1. Plug the Raspberry Pi Pico into the computer with the onboard BOOTSEL button pressed (you can let go of the BOOTSEL button once it is plugged into the computer).
2. If the Pico appears as CIRCUITPY, skip to step #5. Else, the Pico will appear as a flashdrive. Add the flash_nuke.uf2 file to eliminate any programs or scripts already on the Pico.
3. Add the adafruit-circuitpython-raspberry_pi_pico_en_US-7.2.3.uf2
4. The Pico will unravel the file, disconnect from the computer, and reconnect to the computer with a bunch of new files and directories. The key folder is lib/, and the key file is code.py. Copy the folder adafruit_hid/ into the lib/ folder.
5. Rename the script you want to send to the pico to code.py, and replace the Pico's code.py with the new code.py.
6. That's it! The Pico will now start running code.py, and you can edit the code.py file inside the Pico to change what it does.
