#Copied from bad_script
import time
import board
import digitalio
import adafruit_rsa

#Generating adafruit keys - have to be smaller
print("generating keypair...")
(publickey, privatekey) = adafruit_rsa.newkeys(512)
print("done generating keypair")

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