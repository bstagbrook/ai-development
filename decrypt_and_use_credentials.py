import requests
import json
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

# Function to add a conversation log
def add_conversation_log(date, summary, details):
    data = {
        "action": "addConversationLog",
        "data": {
            "date": date,
            "summary": summary,
            "details": details
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)

# Function to add a task or parking lot item
def add_task_or_parking_lot_item(sheet_name, id, description, status, notes, date):
    data = {
        "action": "addTaskOrParkingLotItem",
        "data": {
            "sheetName": sheet_name,
            "id": id,
            "description": description,
            "status": status,
            "notes": notes,
            "date": date
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)

# Function to add or update project state
def add_or_update_project_state(project_name, description, architecture, designs, roadmap, links):
    data = {
        "action": "addOrUpdateProjectState",
        "data": {
            "projectName": project_name,
            "description": description,
            "architecture": architecture,
            "designs": designs,
            "roadmap": roadmap,
            "links": links
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)

# Example usage
add_conversation_log(str(datetime.now()), "Discussed AI Infrastructure Plan", "Detailed plan for AI infrastructure and memoization system.")
add_task_or_parking_lot_item("Tasks", "task-001", "Implement API key authentication", "Pending", "Enhance security", str(datetime.now()))
add_task_or_parking_lot_item("Parking Lot", "idea-005", "Obscure IP while divvying out tasks to bots", "Pending", "", str(datetime.now()))
add_or_update_project_state("AI Infrastructure", "Developing AI collaborative infrastructure", "Microservices", "Initial designs", "Phase 1: Setup, Phase 2: Integration", "Link to Treasures")
