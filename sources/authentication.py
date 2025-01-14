import requests
from sources.config import LOGIN_URL,AUTH_DATA

def authenticate():
    response = requests.post(LOGIN_URL, json=AUTH_DATA, verify=True)

    if response.status_code == 200:
        access_token = response.json()['data']['token']
        print(f"Authenticated! Token: {access_token}")
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
    else:
        print("xxxxxxx - Authentication Failed!!! - xxxxxxx")
        return None
    return headers