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
credentials = f"{username}:{password}"
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
    "Task Focus and Script Update",
    "Updated the `contentservice.gs` script to include authorization checks and new functionality, provided a diff for clarity, and ensured the Python script was run successfully to add entries. Implemented a focus mode to keep tasks on track while parking lotting additional ideas.",
    "Detailed the steps taken to update the script, provided a diff for tracking changes, and ensured successful execution of the Python script. Implemented a system to maintain focus and handle additional ideas efficiently.",
    str(datetime.now()),
    "Script Update, Authorization, Focus Mode, Task Management, Python Script, Google Apps Script"
)
