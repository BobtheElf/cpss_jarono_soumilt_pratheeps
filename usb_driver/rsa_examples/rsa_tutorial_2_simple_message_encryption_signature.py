import rsa

#Open the public key and private key files and save them into their respective key variables
with open("hmi_key.pub", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())
with open("hmi_key.prv", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())
    
#Message to encrypt and decrypt
message = "Hello, World!"

#Encrypt the message with the public key
encrypted_message = rsa.encrypt(message.encode(), public_key)
print(encrypted_message, end = "\n")

#Decrypt the message with the private key
clear_message = rsa.decrypt(encrypted_message, private_key)
print(clear_message, end = "\n")

#Sign the message with the private key
signature = rsa.sign(message.encode(), private_key, "SHA-256")

#Verify the message with the public key
try:
    #If the next line is commented, the signature succeeds, else it will fail
    # public_key, _ = rsa.newkeys(1024)
    rsa.verify(message.encode(), signature, public_key)
except:
    print("Signature Invalid", end = "\n")
    exit()
print("Signature Succeeded", end = "\n")