import requests
import base64
import time
import json
import csv
import os  # Ensure the os module is imported
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

# Replace with your client ID and client secret
client_id = '23PDS3'
client_secret = '8be183a112c011a53c188db507728577'  # Replace with your actual client secret

# Replace with the access token and refresh token you obtained
access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1BEUzMiLCJzdWIiOiJDNE5XUkIiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3NvYyB3YWN0IHdveHkgd3RlbSB3d2VpIHdzZXQgd2xvYyB3cmVzIiwiZXhwIjoxNzIwMDc3ODgwLCJpYXQiOjE3MjAwNDkwODB9.WDpc53AMTQL0UUD8eRU8tFWpTOmZdU02kRQSlLxuNmw'  # Replace with your actual access token
refresh_token = '2e679cc4e56f7b61a13327c30cb83abd4897098c06655beee5d0d0c97c74c720'  # Replace with your actual refresh token

# Provided activity log ID
log_id = '64505530041'  # Replace with the actual activity log ID

# Paths to save the JSON and CSV files
output_json_path = r'K:\USYD_PhD_OneDrive\OneDrive - The University of Sydney (Students)\PhD_USYD\ResearchDesign01_Physio Prototype\ECG Measurement\Test_Fitbit\Fitbit_Api\HeartBeat_Test_TCX02.json'  # Replace with your actual JSON output path
output_csv_path = r'K:\USYD_PhD_OneDrive\OneDrive - The University of Sydney (Students)\PhD_USYD\ResearchDesign01_Physio Prototype\ECG Measurement\Test_Fitbit\Fitbit_Api\HeartBeat_Test_TCX02.csv'  # Replace with your actual CSV output path

# Set token expiry duration (e.g., 1 hour) and record the last refresh time
token_expiry_duration = timedelta(hours=1)
last_refresh_time = datetime.now()

# Function to refresh the access token
def refresh_access_token():
    global access_token, refresh_token, last_refresh_time
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']
        last_refresh_time = datetime.now()
        print("Access token refreshed successfully.")
        print(f"New access token: {access_token}")
        print(f"New refresh token: {refresh_token}")
    else:
        print(f"Failed to refresh token: {response.status_code}")
        print(response.text)

# Function to fetch the most recent heart rate data
def fetch_heart_rate_data():
    global access_token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    url = f'https://api.fitbit.com/1/user/-/activities/{log_id}.tcx'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.content
    elif response.status_code == 401:
        print("Access token expired, refreshing token.")
        refresh_access_token()
        return fetch_heart_rate_data()
    else:
        print(f"Failed to fetch heart rate data: {response.status_code}")
        print(response.text)
        return None

# Function to parse TCX data
def parse_tcx_data(tcx_data):
    root = ET.fromstring(tcx_data)
    namespace = {"tcx": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    
    heart_rate_data = []

    for trackpoint in root.findall(".//tcx:Trackpoint", namespace):
        time = trackpoint.find("tcx:Time", namespace).text
        heart_rate_element = trackpoint.find(".//tcx:HeartRateBpm/tcx:Value", namespace)
        if heart_rate_element is not None:
            heart_rate = heart_rate_element.text
            heart_rate_data.append({"time": time, "heart_rate": heart_rate})

    return heart_rate_data

# Function to save data to JSON
def save_to_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"JSON file created at {file_path}")

# Function to save data to CSV
def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Time', 'Heart Rate'])
        for record in data:
            csv_writer.writerow([record['time'], record['heart_rate']])
    print(f"CSV file created at {file_path}")

# Ensure directories exist
for path in [output_json_path, output_csv_path]:
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

print(f"Current system time: {datetime.now().strftime('%H:%M:%S')}")

# Check if the token is close to expiry, refresh if needed
if datetime.now() - last_refresh_time > token_expiry_duration - timedelta(minutes=5):
    refresh_access_token()

# Fetch the TCX data using the provided log ID
tcx_data = fetch_heart_rate_data()
if tcx_data:
    # Parse the TCX data to extract heart rate values
    heart_rate_data = parse_tcx_data(tcx_data)
    
    # Save the heart rate data to JSON and CSV files
    save_to_json(heart_rate_data, output_json_path)
    save_to_csv(heart_rate_data, output_csv_path)
else:
    print("No TCX data found.")
