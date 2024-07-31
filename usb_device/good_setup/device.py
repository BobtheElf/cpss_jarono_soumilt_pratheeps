#Usb_device.py : 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from pynput import keyboard
import time

# Load the public key (ensure you have the public key file 'public_key.pem')
with open('public_key.pem', 'rb') as f:
    public_key = RSA.import_key(f.read())

cipher_rsa = PKCS1_OAEP.new(public_key)

# Function to encrypt data
def encrypt_data(data):
    encrypted_data = cipher_rsa.encrypt(data.encode('utf-8'))
    return encrypted_data

# Function to send data to the computer
def send_data(data):
    encrypted_message = encrypt_data(data)
    # Here you would send the encrypted_message to the computer
    # This is a placeholder print statement
    print("Sending encrypted message:", encrypted_message)

# Initial authentication key sending
auth_key = "your_authentication_key"
send_data(auth_key)

# Function to handle keypress events
def on_press(key):
    try:
        key_char = key.char
        print(f"Key {key_char} pressed, sending encrypted message...")
        send_data(key_char)
    except AttributeError:
        pass

# Main function to wait for keypress
def main():
    print("Device is waiting for keypress...")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()