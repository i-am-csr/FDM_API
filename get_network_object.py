import requests
import urllib3

urllib3.disable_warnings()


def get(url, api_version, token):
    # Initializing variables
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(token)
    }

    # List network objects first
    limit = 1000
    offset = 0
    api_path = url + f"/api/fdm/{api_version}/object/networks?offset={offset}&limit={limit}"

    response = requests.request("GET", api_path, headers=headers, verify=False)
    _list_of_objects = [response.json()['items']]
    while len(response.json()['items']) >= limit:  # This means there are still objects
        offset += limit
        api_path = url + f"/api/fdm/{api_version}/object/networks?offset={offset}&limit={limit}"
        response = requests.request("GET", api_path, headers=headers, verify=False)
        _list_of_objects.append(response.json()['items'])

    list_of_objects = []
    for part in _list_of_objects:
        for obj in part:
            list_of_objects.append(obj)

    # List network groups now
    limit = 1000
    offset = 0
    api_path = url + f"/api/fdm/{api_version}/object/networkgroups?offset={offset}&limit={limit}"

    response = requests.request("GET", api_path, headers=headers, verify=False)
    _list_of_network_groups = [response.json()['items']]
    while len(response.json()['items']) >= limit:  # This means there are still objects
        offset += limit
        api_path = url + f"/api/fdm/{api_version}/object/networkgroups?offset={offset}&limit={limit}"
        response = requests.request("GET", api_path, headers=headers, verify=False)
        _list_of_network_groups.append(response.json()['items'])

    list_of_network_groups = []
    for part in _list_of_network_groups:
        for obj in part:
            list_of_network_groups.append(obj)

    return list_of_objects, list_of_network_groups
