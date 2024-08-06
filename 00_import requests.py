import requests
import base64

# Replace with your client ID and client secret
client_id = '23PDS3'
client_secret = '8be183a112c011a53c188db507728577'  # Replace with your actual client secret

# Authorization code received from Fitbit
authorization_code = '376ee9f215640c212768d90522767ec932427d8f'

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
    'code_verifier': '052p6s3o3t5g68663h1x6e0k372h111a38605d2h5y601m6o0a076j4f2g5u2u0x2c0h104x6m300u2f3k2p5a005h582g0q011p63533d5q2p5g566e0o160a5k5e5i'  # Replace with your actual code verifier
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
