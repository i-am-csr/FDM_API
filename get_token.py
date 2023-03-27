import requests
import json
import urllib3

urllib3.disable_warnings()


def get(url: str = "cisco.com", credentials=None, api_version: str = "latest") -> dict:
    if credentials is None:
        credentials = {"username": "admin", "password": "Admin123"}
    url = url + f"/api/fdm/{api_version}/fdm/token"
    payload = json.dumps({
        "grant_type": "password",
        "username": credentials.get("username"),
        "password": credentials.get("password")
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        return response.json()
    except requests.exceptions.RequestException as e:
        print("Ooops! Something went wrong.")
        print(e)
        quit(0)
    # Returns a json with the following keys:
    # {
    #     "access_token": "-----",
    #     "expires_in": 1800,
    #     "token_type": "Bearer",
    #     "refresh_token": "-----",
    #     "refresh_expires_in": 2400
    # }
