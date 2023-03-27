import requests
import json
from crayons import red, green

"""
Requires data like:
data = {
        "name": "Test",
        "subType": "HOST",
        "value": "192.168.100.1",
        "type": "networkobject"
    }
"""

def post(url: str = "cisco.com", api_version: str = "latest", token: str = "xxxx", data=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }

    url = url + f"/api/fdm/{api_version}/object/networks"

    # Validating data
    if "name" in data:
        pass
    else:
        print(red("There is no 'name' in the the entry"))
        quit(0)
    if "subType" in data:
        options = ['HOST', 'NETWORK', 'RANGE', 'FQDN']
        if data['subType'] in options:
            pass
        else:
            print(red(f"The subType {data['subType']} does not exist. It should be HOST, NETWORK, FQDN or RANGE"))
            quit(0)
        pass
    else:
        print(red("There is no 'subType' in the the entry"))
        quit(0)
    if "value" in data:
        pass
    else:
        print(red("There is no 'value' in the the entry"))
        quit(0)
    if "type" in data:
        pass
    else:
        print(red("There is no 'type' in the the entry"))
        quit(0)

    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(data), verify=False)
        if response.status_code == 200:
            print(green("Object created.."))
            print(response.text)
        elif response.status_code == 422:
            print(green("There is something:"))
            print(red(response.text))
    except requests.exceptions.RequestException as e:
        print(red("Oops! Something went wrong.."))
        print(e)
