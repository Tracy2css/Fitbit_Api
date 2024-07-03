import requests
import base64

# Replace with your client ID and client secret
client_id = '23PDS3'
client_secret = '8be183a112c011a53c188db507728577'  # Replace with your actual client secret

# Authorization code received from Fitbit
authorization_code = '6827d53372b21b9a4e5fa0920e36d048cbc3b329'

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
    'code_verifier': '4l5j0b5e15361h120u5g400y020u532o3p621q2l6a191i2l162r160s6y0y2i324g0x4l2o62602s0d4u0b1s6n713c4s1b166e0l3t5y4h4m0i3i6l6x1j6x1s176z'  # Replace with your actual code verifier
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
