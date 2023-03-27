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
        request = requests.get(f"{url}/api/fdm/{api_version}/operational/systeminfo/default",
                               verify=False, headers=headers)
        return request.json()
    except:
        raise
