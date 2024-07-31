from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import socket
import time

# Load the public key of the HMI (ensure you have the public key file 'public_key.pem')
with open('public_key.pem', 'rb') as f:
    public_key = RSA.import_key(f.read())

cipher_rsa = PKCS1_OAEP.new(public_key)

# Function to encrypt data
def encrypt_data(data):
    encrypted_data = cipher_rsa.encrypt(data.encode('utf-8'))
    return encrypted_data

# Function to decrypt data
def decrypt_data(encrypted_data, private_key):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher_rsa.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data

# Function to send data to the HMI computer
def send_data_to_hmi(data):
    # Encrypt the data
    encrypted_message = encrypt_data(data)
   
    # Send the encrypted message to the HMI computer (placeholder code)
    # This should be replaced with actual communication code
    hmi_socket.sendall(encrypted_message)

# Function to receive data from the HMI computer
def receive_data_from_hmi():
    encrypted_message = hmi_socket.recv(1024)
    return encrypted_message

# Function to handle HMI validation
def handle_hmi_validation(encrypted_key):
    try:
        # Decrypt the received encryption key with SCADA's private key
        decrypted_key = decrypt_data(encrypted_key, scada_private_key)
       
        # Check if the decrypted key is valid (replace 'valid_key' with the actual valid key)
        if decrypted_key == 'valid_key':
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

# Initialize connection to HMI computer (placeholder code, replace with actual connection setup)
hmi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hmi_socket.connect(('hmi_computer_ip', hmi_computer_port))

# Load the SCADA private key (ensure you have the private key file 'private_key.pem')
with open('private_key.pem', 'rb') as f:
    scada_private_key = RSA.import_key(f.read())

# Main function to initiate from SCADA and handle HMI signal
def main():
    print("SCADA computer waiting for HMI signal with encryption key...")
    while True:
        encrypted_key = receive_data_from_hmi()
        handle_hmi_validation(encrypted_key)
        time.sleep(1)

if __name__ == "__main__":
    main()
