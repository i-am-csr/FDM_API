import requests
import json
from crayons import red, green

"""
Requires data like:
data = {
        "name": "GroupTest_Python",
        "objects": [
            {
                "type": "networkobject",
                "name": "AD_Server"
            }
        ],
        "type": "networkobjectgroup",
    }
"""

def post(url: str = "cisco.com", api_version: str = "latest", token: str = "xxxx", data=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }

    url = url + f"/api/fdm/{api_version}/object/networkgroups"

    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(data), verify=False)
        if response.status_code == 200:
            print(green("Group created.."))
            print(response.text)
        elif response.status_code == 422:
            print(green("There is something:"))
            print(red(response.text))
    except requests.exceptions.RequestException as e:
        print(red("Oops! Something went wrong.."))
        print(e)