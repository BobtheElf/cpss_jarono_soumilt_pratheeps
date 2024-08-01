#!usr/bin/python3
import rsa

#Generate key pair
public_key, private_key = rsa.newkeys(1024)

#Save the key pair into files
with open("spare_pub_key.pem", "wb") as f:
    f.write(public_key.save_pkcs1("PEM"))
with open("spare_prv_key.pem", "wb") as f:
    f.write(private_key.save_pkcs1("PEM"))
    
