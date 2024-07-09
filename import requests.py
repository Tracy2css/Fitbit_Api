import requests
import base64

# Replace with your client ID and client secret
client_id = '23PDS3'
client_secret = '8be183a112c011a53c188db507728577'  # Replace with your actual client secret

# Authorization code received from Fitbit
authorization_code = 'bf1801d6a095e32388a7d137e0f963e70727d512'

# Base64 encode the client ID and client secret
credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

# Headers for the token request
headers = {
    'Authorization': f'Basic {credentials}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Data for the token request
data = {
    'client_id': client_id,
    'grant_type': 'authorization_code',
    'redirect_uri': 'http://127.0.0.1:8080/',  # Replace with your actual redirect URI
    'code': authorization_code,
    'code_verifier': '2s1x3y6m474i1x2v6j5u4f0i1e295m300e502v4a335s0m301r6s3c15494b580r5u2j6o6o4d141l0s1e37083i5s2j306x3r304w5h5i593e6g2n1s3x5y35702a0f'  # Replace with your actual code verifier
}

# Send POST request to Fitbit token endpoint
response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data)

# Process the response
if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access_token']
    refresh_token = token_data['refresh_token']
    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")
else:
    print(f"Failed to obtain token: {response.status_code}")
    print(response.text)
