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

    print("INFO - Account data set successfully.")
    return

def set_startup_ram(ram_value):

    if not ram_value:
        ram_value = "4096"

    current_directory = os.getcwd()
    config_file = os.path.join(current_directory, "assets", "UltimMC", "ultimmc.cfg")
    config_file2 = os.path.join(current_directory, "assets", "UltimMC", "instances", "VL4", "instance.cfg")

    with open(config_file, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("MaxMemAlloc="):
            line = f"MaxMemAlloc={ram_value}\n"
        elif line.startswith("MinMemAlloc="):
            line = f"MinMemAlloc={ram_value}\n"
        new_lines.append(line)

    with open(config_file, 'w') as f:
        f.writelines(new_lines)

    with open(config_file2, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("MaxMemAlloc="):
            line = f"MaxMemAlloc={ram_value}\n"
        elif line.startswith("MinMemAlloc="):
            line = f"MinMemAlloc={ram_value}\n"
        new_lines.append(line)

    with open(config_file2, 'w') as f:
        f.writelines(new_lines)

    with open('config.ini', 'r+') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("ram = "):
                lines[i] = f"ram = {ram_value}\n"
                break
        f.seek(0)
        f.writelines(lines)
        f.truncate()
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set user data for fcc.exe args')
    parser.add_argument('-u', '--username', type=str, help='Username to set')
    parser.add_argument('-r', '--ram', type=str, help='RAM to allocate')
    args = parser.parse_args()

    if args.username:
        set_user_data(args.username)
    else:
        print("ERROR - fcc.exe invalid username.")

    if args.ram:
        set_startup_ram(args.ram)
    else:
        print("ERROR - fcc.exe invalid RAM.")
