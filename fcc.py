#fcc.exe args
import argparse
import configparser
import json
import os
import time
import uuid

def set_user_data(username):
    current_directory = os.getcwd()

    id_hex = uuid.uuid4().hex
    client_token_hex = uuid.uuid4().hex
    iat = int(time.time())
    print(username)
    print(id_hex)
    print(client_token_hex)
    print(iat)

    account_data = {
        "active": True,
        "entitlement": {
            "canPlayMinecraft": True,
            "ownsMinecraft": True
        },
        "profile": {
            "capes": [],
            "id": id_hex,
            "name": username,
            "skin": {
                "id": "",
                "url": "",
                "variant": ""
            }
        },
        "type": "dummy",
        "ygg": {
            "extra": {
                "clientToken": client_token_hex,
                "userName": username
            },
            "iat": iat,
            "token": username
        }
    }

    file_path = "./assets/UltimMC/accounts.json"
    with open(file_path, 'r') as f:
        data = json.load(f)

    data['accounts'].append(account_data)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    config = configparser.ConfigParser()
    config.read('config.ini')
    config['GAME']['id'] = id_hex
    config['GAME']['token'] = client_token_hex
    with open('config.ini', 'w') as f:
        config.write(f)

    print("INFO - Account data set successfully.")
    time.sleep(2)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set user data for fcc.exe args')
    parser.add_argument('-u', '--username', type=str, help='Username to set')
    args = parser.parse_args()

    if args.username:
        set_user_data(args.username)
    else:
        print("ERROR - fcc.exe invalid username.")