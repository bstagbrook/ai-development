import requests
import json
import base64
from cryptography.fernet import Fernet
from datetime import datetime

# Log debug information to Google Sheets
def log_debug_info(location, variable_name, value):
    sheet_url = "https://script.google.com/macros/s/YOUR_SCRIPT_DEPLOYMENT_ID/exec"
    data = {
        "action": "logDebugInfo",
        "data": {
            "location": location,
            "variable_name": variable_name,
            "value": value
        }
    }
    requests.post(sheet_url, data=json.dumps(data))

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

log_debug_info('Python Script', 'encoded_credentials', encoded_credentials)

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
    log_debug_info('Python Script', 'response', response.text)
    print(response.text)

# Example usage
add_treasure_entry(
    "Unauthorized Error",
    "Encountered an 'Unauthorized' error when trying to run the `add_treasure_entry.py` script before updating the `local_api.py` script.",
    "Ensure that the `local_api.py` script is updated with the correct authorization function and logic before running any scripts that interact with it.",
    str(datetime.now()),
    "Python, Authorization, Error, API"
)
