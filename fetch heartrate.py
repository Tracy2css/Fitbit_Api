import requests
import base64
import json
import csv
import os
from datetime import datetime

# Replace with your client ID and client secret
client_id = '23PDS3'
client_secret = '8be183a112c011a53c188db507728577'  # Replace with your actual client secret

# Replace with the access token you obtained
access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1BEUzMiLCJzdWIiOiJDNE5XUkIiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3NvYyB3YWN0IHdveHkgd3RlbSB3d2VpIHdzZXQgd2xvYyB3cmVzIiwiZXhwIjoxNzIwMDc3ODgwLCJpYXQiOjE3MjAwNDkwODB9.WDpc53AMTQL0UUD8eRU8tFWpTOmZdU02kRQSlLxuNmw'  # Replace with your actual access token

# Replace with the refresh token you obtained
refresh_token = '2e679cc4e56f7b61a13327c30cb83abd4897098c06655beee5d0d0c97c74c720'  # Replace with your actual refresh token

# Path to save the CSV file
output_csv_path = r'K:\USYD_PhD_OneDrive\OneDrive - The University of Sydney (Students)\PhD_USYD\ResearchDesign01_Physio Prototype\ECG Measurement\Test_Fitbit\Fitbit_Api\HeartBeat_Test.csv'  # Replace with your actual CSV output path

# Path to save the JSON file
output_json_path = r'K:\USYD_PhD_OneDrive\OneDrive - The University of Sydney (Students)\PhD_USYD\ResearchDesign01_Physio Prototype\ECG Measurement\Test_Fitbit\Fitbit_Api\HeartBeat_Test.json'  # Replace with your actual JSON output path

def save_to_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Time', 'Heart Rate'])

        for record in data['activities-heart-intraday']['dataset']:
            csv_writer.writerow([record['time'], record['value']])

def fetch_heart_rate_data():
    global access_token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    # URL for fetching heart rate data on 2024-07-04 with detail level set to 1 second
    url = 'https://api.fitbit.com/1/user/-/activities/heart/date/2024-07-04/1d/1sec.json'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        heart_data = response.json()
        # Debugging: Print the latest timestamp in the fetched data
        if 'activities-heart-intraday' in heart_data and 'dataset' in heart_data['activities-heart-intraday']:
            last_entry = heart_data['activities-heart-intraday']['dataset'][-1]
            print(f"Last entry in the fetched data: Time - {last_entry['time']}, Value - {last_entry['value']}")
            save_to_json(heart_data, output_json_path)
            save_to_csv(heart_data, output_csv_path)
            print("Heart rate data fetched and saved successfully.")
        else:
            print("Error: Data format is not as expected.")
    elif response.status_code == 401:
        print("Access token expired, refreshing token.")
        refresh_access_token()
        fetch_heart_rate_data()
    else:
        print(f"Failed to fetch heart rate data: {response.status_code}")
        print(response.text)

def refresh_access_token():
    global access_token, refresh_token
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
        print("Access token refreshed successfully.")
    else:
        print(f"Failed to refresh token: {response.status_code}")
        print(response.text)

if not os.path.exists(os.path.dirname(output_csv_path)):
    os.makedirs(os.path.dirname(output_csv_path))

if not os.path.exists(os.path.dirname(output_json_path)):
    os.makedirs(os.path.dirname(output_json_path))

print(f"Current system time: {datetime.now().strftime('%H:%M:%S')}")
fetch_heart_rate_data()
