import requests
import base64
import time
import json
import csv
import os
from datetime import datetime, timedelta

# Replace with your client ID and client secret
client_id = '23PDS3'
client_secret = '8be183a112c011a53c188db507728577'  # Replace with your actual client secret

# Replace with the access token and refresh token you obtained
access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1BEUzMiLCJzdWIiOiJDNE5XUkIiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd3NvYyB3YWN0IHdveHkgd3RlbSB3d2VpIHdzZXQgd2xvYyB3cmVzIiwiZXhwIjoxNzIwNTkzNzkyLCJpYXQiOjE3MjA1NjQ5OTJ9._e944mGBzPr3v35kAve5gYNrBk4Q-60NDK3yLSAK_gU'  # Replace with your actual access token
refresh_token = 'c9de870211346f25478054efafbc7837333fb8ce42cb3af7b9e1f7282a5f1922'  # Replace with your actual refresh token

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

# Function to fetch the activity log list
def fetch_activity_log_list(date):
    global access_token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    url = f'https://api.fitbit.com/1/user/-/activities/list.json?beforeDate={date}&sort=desc&limit=10&offset=0'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("Access token expired, refreshing token.")
        refresh_access_token()
        return fetch_activity_log_list(date)
    else:
        print(f"Failed to fetch activity log list: {response.status_code}")
        print(response.text)
        return None

# Function to save data to JSON
def save_to_json(data, file_path):
    print(f"Attempting to save JSON to: {file_path}")
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"JSON file created at {file_path}")

# Function to save data to CSV
def save_to_csv(data, file_path):
    print(f"Attempting to save CSV to: {file_path}")
    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['logId', 'Time', 'Name', 'Duration', 'Heart_Rate_Zones'])
        for record in data['activities']:
            csv_writer.writerow([record['logId'], record['startTime'], record['activityName'], record['duration'], record['heartRateZones']])
    print(f"CSV file created at {file_path}")

# Provided date for fetching activity log list
date = '2024-07-05'  # Replace with the actual date

# Paths to save the JSON and CSV files
output_json_path = r'K:\USYD_PhD_OneDrive\OneDrive - The University of Sydney (Students)\PhD_USYD\ResearchDesign01_Physio Prototype\ECG Measurement\Test_Fitbit\Fitbit_Api\Activity_Log_List_0704.json'  # Replace with your actual JSON output path
output_csv_path = r'K:\USYD_PhD_OneDrive\OneDrive - The University of Sydney (Students)\PhD_USYD\ResearchDesign01_Physio Prototype\ECG Measurement\Test_Fitbit\Fitbit_Api\Activity_Log_List_0704.csv'  # Replace with your actual CSV output path

# Ensure directories exist
for path in [output_json_path, output_csv_path]:
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

print(f"Current system time: {datetime.now().strftime('%H:%M:%S')}")

# Check if the token is close to expiry, refresh if needed
if datetime.now() - last_refresh_time > token_expiry_duration - timedelta(minutes=5):
    refresh_access_token()

# Fetch the activity log list using the provided date
activity_log_list = fetch_activity_log_list(date)
if activity_log_list:
    # Save the activity log list to JSON and CSV files
    save_to_json(activity_log_list, output_json_path)
    save_to_csv(activity_log_list, output_csv_path)
else:
    print("No activity log data found.")
