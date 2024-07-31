import rsa

#Generate key pair
public_key, private_key = rsa.newkeys(1024)

#Save the key pair into files
with open("hmi_key.pub", "wb") as f:
    f.write(public_key.save_pkcs1("PEM"))
with open("hmi_key.prv", "wb") as f:
    f.write(private_key.save_pkcs1("PEM"))
    
