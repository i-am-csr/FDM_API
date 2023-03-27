import requests
import urllib3

urllib3.disable_warnings()


def get(url, api_version, token):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    try:
        # * Request code
        # request = requests.get(f"{url}/api/fdm/{api_version}/URI",
        #                        verify=False, headers=headers)
        # return request.json()
        # ? Once this code is added, we need to delete the 'pass' statement below 👇🏽
        pass
    except:
        raise
