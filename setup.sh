#!/bin/bash

# Install necessary Python libraries
pip3 install -r requirements.txt

# Run the local API server in the background
python3 local_api.py &

# Function to log a treasure entry
function log_treasure_entry() {
    local keyword="$1"
    local description="$2"
    local solution="$3"
    local tags="$4"

    python3 - <<EOF
import requests
import json
import base64
from cryptography.fernet import Fernet
from datetime import datetime

# Load the key
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

# Load the encrypted credentials
with open("encrypted_credentials.txt", "rb") as cred_file:
    encrypted_credentials = cred_file.read()

# Decrypt the credentials
decrypted_credentials = cipher_suite.decrypt(encrypted_credentials).decode()
username, password = decrypted_credentials.split(":")

# Create the authentication header
credentials = f"{username}:${password}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
headers = {
    "authHeader": f"Basic {encoded_credentials}"
}

# URL of the deployed Google Apps Script web app
url = "https://script.google.com/macros/s/AKfycbw4VOPGcOq2oH0bfmwxz2AMQuKS0XooREBXIjUBYBg3m9Vh6TN2dcLYao0Tdi4mC0o/exec"

# Function to add a treasure entry
def add_treasure_entry(keyword, description, solution, date, tags):
    data = {
        "action": "addTreasureEntry",
        "data": {
            "keyword": keyword,
            "description": description,
            "solution": solution,
            "date": date,
            "tags": tags
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)

# Example usage
add_treasure_entry(
    "${keyword}",
    "${description}",
    "${solution}",
    str(datetime.now()),
    "${tags}"
)
EOF
}

# Log the current bug fix
log_treasure_entry "Fernet Import Error" "NameError: name 'Fernet' is not defined" "Ensure 'from cryptography.fernet import Fernet' is at the beginning of the script." "Python, Flask, Cryptography"
