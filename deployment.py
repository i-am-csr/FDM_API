import requests
import urllib3
from crayons import red, green


urllib3.disable_warnings()


def deploy(url, api_version, token):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    url = url + f"/api/fdm/{api_version}/operational/deploy"

    try:
        response = requests.request("POST", url, headers=headers, data={}, verify=False)
        if response.status_code == 200:
            print(green("Deployment in progress, please check the GUI to see when it finishes"))
            print(response.text)
        elif response.status_code == 422:
            print(green("There is something:"))
            print(red(response.text))
    except requests.exceptions.RequestException as e:
        print(red("Oops! Something went wrong.."))
        print(e)
