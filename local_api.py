from flask import Flask, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

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

# Function to run shell commands
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {"stdout": result.stdout.decode('utf-8'), "stderr": result.stderr.decode('utf-8')}
    except subprocess.CalledProcessError as e:
        return {"stdout": e.stdout.decode('utf-8'), "stderr": e.stderr.decode('utf-8')}

# Basic authentication function
def is_authorized(auth_header):
    if not auth_header:
        return False
    encoded_credentials = auth_header.split(" ")[1]
    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    username_, password_ = decoded_credentials.split(":")
    return username_ == username and password_ == password

@app.route('/execute', methods=['POST'])
def execute():
    auth_header = request.headers.get('Authorization')
    if not is_authorized(auth_header):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    command = data.get('command')
    if not command:
        return jsonify({"error": "No command provided"}), 400
    
    result = run_command(command)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
