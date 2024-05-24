from cryptography.fernet import Fernet
import base64

# Generate a key and save it to a file
key = Fernet.generate_key()
with open("secret.key", "wb") as key_file:
    key_file.write(key)

# Use the key to encrypt your credentials
cipher_suite = Fernet(key)

username = "peanut"
password = "3R@5CL3"
credentials = f"{username}:{password}".encode()
encrypted_credentials = cipher_suite.encrypt(credentials)

# Save the encrypted credentials to a file
with open("encrypted_credentials.txt", "wb") as cred_file:
    cred_file.write(encrypted_credentials)

