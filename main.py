import yaml
import json
import pandas as pd
from crayons import blue, green, white, black, red, yellow, magenta

import get_token
import get_network_object
import post_network_object
import post_network_groups
import deployment
import get_system_information


def read_ftd_profile(filename="profile_ftd.yml"):
    file = open(filename, "r")
    yaml_raw = file.read()
    ftd_info = yaml.load(yaml_raw, Loader=yaml.FullLoader)
    return ftd_info


if __name__ == '__main__':
    # * Initialization
    print(green("Welcome!"))
    print(green("Reading the FTD Profile file"))

    # * Reading FTD profile(s)
    ftd_information = read_ftd_profile()

    # * Reading complete. Printing information.
    print(f"There are {len(ftd_information['devices'])} devices available:")
    for device in ftd_information["devices"]:
        print(f"- {device['hostname']}")
    print()  # * Adding white space
    selection = input("Which device do you want to work on?  ").strip()

    # * Validate if input was correct
    device_id = None
    for i, device in enumerate(ftd_information["devices"]):
        if ('hostname', selection) in device.items():
            print(green(f"Got it, Working on {selection}", bold=True))
            device_id = i
    if device_id is None:
        print(red("Sorry, there is no such device, please select a correct one."))
        quit(0)

    # * Initializing variables
    base_url = f"https://{ftd_information['devices'][device_id].get('ipaddr')}:{ftd_information['devices'][device_id].get('port')}"
    credentials = {"username": ftd_information['devices'][device_id].get('username'),
                   "password": ftd_information['devices'][device_id].get('password')}
    api_version = f"v{ftd_information['devices'][device_id].get('version')}"

    # * Getting token
    token = get_token.get(base_url, credentials, api_version)
    print(yellow("Token gotten!, Ready to work!"))
    # print(token.get("access_token"))

    # * Working on the device
    # ! Every part of code should be added starting here...
    print(get_system_information.get(base_url,api_version,token.get("access_token")))
    action = input("Do you want to read or write configuration? (r/w)  ").strip()
    if "r" in action:
        # ! Reading configuration code
        # * Collecting network objects and network groups
        print("Collecting objects...")
        objects = {}
        objects['objects'], objects['network_groups'] = get_network_object.get(base_url, api_version,
                                                                               token.get("access_token"))
        print("Done!")

        # * Printing information
        print(green(f"The objects on {selection} are:", bold=True))
        for obj in objects['objects']:
            print(blue("------------------------------"))
            print(f"name: {obj['name']}")
            print(f"value: {obj['value']}")
            print(f"type: {obj['type']}")
        print()
        print(green(f"The network groups on {selection} are:", bold=True))
        for obj in objects['network_groups']:
            print(blue("------------------------------"))
            print(f"name: {obj['name']}")
            print(f"type: {obj['type']}")
            print("Objects:")
            for o in obj['objects']:
                print(magenta("------------------------------"))
                print(f"name: {o['name']}")
                print(f"type: {o['type']}")

        # * Checking if the user wants to write files with the info.
        write = input("Do you want me to save them in a file? (yes/no)  ").strip().lower()
        if "yes" in write:
            print(green("Creating CSV file"))
            toCSV_objects = json.dumps(objects['objects'])
            toCSV_network_groups = json.dumps(objects['network_groups'])
            df = pd.read_json(toCSV_objects)
            df.to_csv(f"output_objects.csv")
            df = pd.read_json(toCSV_network_groups)
            df.to_csv(f"output_network_groups.csv")
            print(f"Done, CSV files have been created")
        else:
            print(green("OK!"))
            # quit(0)

    elif "w" in action:
        # ! Writing configuration code

        # * Code for network objects
        try:
            # * Read information from CSV file
            df = pd.read_csv('objects.csv')
            print(green("Objects found..."))
            print(yellow("Objects read..."))
            # print(df.to_dict("record"))

            # * Writing objects
            for obj in df.to_dict("record"):
                print(blue(f"Writing object {obj['name']}"))
                post_network_object.post(base_url, api_version, token.get("access_token"), obj)
        except:
            print(red("No 'objects' file found"))

        # * Code for network groups
        try:
            # * Read information from CSV file
            df = pd.read_csv('network_groups.csv')
            print(green("Network groups found..."))
            print(yellow("Network groups read..."))

            # * Reading objects for availability
            objects = {'objects': (get_network_object.get(base_url, api_version,
                                                          token.get("access_token")))[0],
                       'network_groups': (get_network_object.get(base_url, api_version,
                                                                 token.get("access_token")))[1]}

            # * Writing network objects
            for obj in df.to_dict("record"):
                print(blue(f"Writing object group {obj['name']}"))
                objects_to_add = []
                _objects = obj['objects'].split(",")
                for _obj in _objects:
                    for row in objects['objects']:
                        if _obj == row['name']:
                            objects_to_add.append(row)
                payload = {
                    "name": obj['name'],
                    "objects": objects_to_add,
                    "type": "networkobjectgroup"
                }
                post_network_groups.post(base_url, api_version, token.get("access_token"), payload)
        except:
            print(red("No 'network_groups' file found"))

        print()
        print(green("Configuration done!"))
        deploy = input("Do you want to deploy the configuration? (y/n): ")
        if "y" in deploy:
            deployment.deploy(base_url, api_version,token.get("access_token"))
        else:
            print("Ok! Please visit FDM to review and deploy the configuration")