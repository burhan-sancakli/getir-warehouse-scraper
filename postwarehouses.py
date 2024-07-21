import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()

POST_URL = os.getenv('POST_URL')

# Define the URL
url = POST_URL

# Load JSON data from the file
with open('warehouses.json', 'r') as file:
    warehouses = json.load(file)

# Iterate over each item in the JSON data and send a POST request
for warehouse in warehouses:
    response = requests.post(url, json=warehouse)
    if response.ok:
        print(f"Successfully sent warehouse: {warehouse}")
    else:
        print(
            f"Failed to send warehouse: {warehouse}, Status Code: {response.status_code}")
