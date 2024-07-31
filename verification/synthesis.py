from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from pynput import keyboard
import socket

# Load the public key of the HMI (ensure you have the public key file 'hmi_public_key.pem')
with open('hmi_public_key.pem', 'rb') as f:
    hmi_public_key = RSA.import_key(f.read())

# Load the SCADA private key (ensure you have the private key file 'scada_private_key.pem')
with open('scada_private_key.pem', 'rb') as f:
    scada_private_key = RSA.import_key(f.read())

hmi_cipher_rsa = PKCS1_OAEP.new(hmi_public_key)
scada_cipher_rsa = PKCS1_OAEP.new(scada_private_key)

# Function to encrypt data
def encrypt_data(data):
    encrypted_data = hmi_cipher_rsa.encrypt(data.encode('utf-8'))
    return encrypted_data

# Function to decrypt data
def decrypt_data(encrypted_data):
    decrypted_data = scada_cipher_rsa.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data

# Function to send data to the HMI computer
def send_data_to_hmi(data):
    encrypted_message = encrypt_data(data)
    hmi_socket.sendall(encrypted_message)

# Function to receive data from the HMI computer
def receive_data_from_hmi():
    encrypted_message = hmi_socket.recv(1024)
    return encrypted_message

# Function to handle HMI validation
def handle_hmi_validation(encrypted_key):
    try:
        # Decrypt the received encryption key
        decrypted_key = decrypt_data(encrypted_key)
       
        # Check if the decrypted key is valid
        valid_key = "valid_key"  # Replace with the actual valid key
        if decrypted_key == valid_key:
            send_data_to_hmi("valid")
            print("HMI put in valid state")
        else:
            send_data_to_hmi("flagged")
            print("HMI put in flagged state")
            print("Alert: Device is registered on the HMI but not the SCADA. Please fix this.")
    except Exception as e:
        print("Decryption failed or invalid key:", str(e))
        send_data_to_hmi("flagged")
        print("HMI put in flagged state")

# Initial authentication key sending to HMI
auth_key = "your_authentication_key"
send_data_to_hmi(auth_key)

# Initialize connection to HMI computer
hmi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hmi_socket.connect(('hmi_computer_ip', 12345))  # Replace with actual HMI computer IP and port

# Function to handle keypress events
def on_press(key):
    try:
        key_char = key.char
        print(f"Key {key_char} pressed, sending encrypted message...")
        send_data_to_hmi(key_char)
    except AttributeError:
        pass

# Main function to initiate from SCADA and handle HMI signal
def main():
    print("SCADA computer waiting for HMI signal with encryption key...")
    # Start keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while True:
        encrypted_key = receive_data_from_hmi()
        handle_hmi_validation(encrypted_key)

if __name__ == "__main__":
    main()