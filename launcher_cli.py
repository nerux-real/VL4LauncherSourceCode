import requests
import configparser
from tqdm import tqdm
import time
import os
import tempfile
import zipfile
from halo import Halo
import platform
import pyfiglet
import tkinter as tk
from tkinter import simpledialog
import json
import uuid
import sys
import subprocess

def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def welcome_screen():
    ascii_art = pyfiglet.figlet_format("VL Launcher")
    print(ascii_art)

def default_choices():
    print("1. Run Game")
    print("2. Change Nickname")
    print("3. Set RAM for a game")
    print("4. Change java runtime path")
    print("5. Check for updates")
    print("6. Exit")
    print('-------------------------------------------------')

def get_current_destination():
    return os.getcwd()

def start_current_game():
    executable_path = os.path.join(os.getcwd(), "assets", "UltimMC", "UltimMC.exe")
    directory_path = os.path.join(os.getcwd(), "assets", "UltimMC")

    arguments = [
        "-d", directory_path,
        "-l", "VL4"
    ]

    subprocess.Popen([executable_path] + arguments)

def default_screen():
    clear_screen()
    welcome_screen()
    print('==================')
    print(f"Version {fetch_local_version()}")
    print('==================')

    print('-------------------------------------------------')
    print(f"Total time played on VL4: {get_time_played()}")
    print('-------------------------------------------------')

    default_choices()

def set_username():
    root = tk.Tk()
    root.withdraw()

    username = simpledialog.askstring("Set", "Enter your username:")

    root.resizable(False, False)

    config_file = "config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)
    config['GAME']['username'] = username
    with open(config_file, 'w') as f:
        config.write(f)

    print("INFO - Username set successfully to:", username)

    set_user_data(username)

def set_user_data(nickname):
    current_directory = os.getcwd()

    id_hex = uuid.uuid4().hex
    client_token_hex = uuid.uuid4().hex
    iat = int(time.time())
    print(nickname)
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
            "name": nickname,
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
                "userName": nickname
            },
            "iat": iat,
            "token": nickname
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

def select_ram():
    while True:
        clear_screen()
        welcome_screen()

        print("INFO - Select RAM to allocate for game.")
        print("1. 3072 (3GB)")
        print("2. 4096 (4GB)")
        print("3. 5120 (5GB) (Recommended)")
        print("4. 6144 (6GB)")
        print("5. 7168 (7GB)")
        user_input = input("ACTION - Enter a number: ")
        if user_input not in ['1', '2', '3', '4', '5', '6', '1.', '2.', '3.', '4.', '5.', '6.']:
            print("ERROR - Invalid Input!")
            time.sleep(2)
            continue
        else:
            current_directory = os.getcwd()
            config_file = os.path.join(current_directory, "assets", "UltimMC", "ultimmc.cfg")
            config_file2 = os.path.join(current_directory, "assets", "UltimMC", "instances", "VL4", "instance.cfg")
            
            with open(config_file, 'r') as f:
                lines = f.readlines()

            if user_input == "1" or user_input == "1.":
                ram_value=3072
            elif user_input == "2" or user_input == "2.":
                ram_value=4096
            elif user_input == "3" or user_input == "3.":
                ram_value=5120
            elif user_input == "4" or user_input == "4.":
                ram_value=6144
            elif user_input == "5" or user_input == "5.":
                ram_value=7168

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
            with open(config_file, 'w') as f:
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

            print(f"INFO - Successfully set RAM to {ram_value}!")
            time.sleep(2)
            return

def get_time_played():
    current_directory = os.getcwd()
    config_file = os.path.join(current_directory, "assets", "UltimMC", "instances", "VL4", "instance.cfg")
    with open(config_file, 'r') as f:
        lines = f.readlines()

    total_time_played_seconds = 0
    for line in lines:
        if line.startswith("totalTimePlayed="):
            total_time_played_seconds = int(line.split("=")[1])
            break

    hours = total_time_played_seconds // 3600
    minutes = (total_time_played_seconds % 3600) // 60
    seconds = total_time_played_seconds % 60

    return f"{hours}h {minutes}min {seconds}sec"

def set_default_java():
    current_directory = os.getcwd()
    java_location = os.path.join(current_directory, "assets", "jdk-21.0.2", "bin", "javaw.exe")
    config_file = os.path.join(current_directory, "assets", "UltimMC", "ultimmc.cfg")
    config_file2 = os.path.join(current_directory, "assets", "UltimMC", "instances", "VL4", "instance.cfg")

    with open(config_file, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("JavaPath="):
            line = f"JavaPath={java_location}\n"
        new_lines.append(line)

    with open(config_file, 'w') as f:
        f.writelines(new_lines)

    with open(config_file2, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("JavaPath="):
            line = f"JavaPath={java_location}\n"
        new_lines.append(line)

    with open(config_file2, 'w') as f:
        f.writelines(new_lines)

    with open('config.ini', 'r+') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("java = "):
                lines[i] = f"java = {java_location}\n"
                break
        f.seek(0)
        f.writelines(lines)
        f.truncate()

    print("INFO - Java path successfully set!")
    time.sleep(2)
    return

def download_file(url, filename):
    try:
        print('INFO - Starting downloading game...')
        response = requests.get(url, stream=True)
        response.raise_for_status()

        temp_dir = tempfile.mkdtemp()
        destination = os.path.join(temp_dir, filename)

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB blocks

        with open(destination, 'wb') as file, tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as progress_bar:
            for data in response.iter_content(block_size):
                file.write(data)
                progress_bar.update(len(data))

        print("INFO - Download complete!")
        return destination
    except requests.exceptions.RequestException as e:
        print('ERROR - ', e)

def extract_zip(zip_file, destination):
    try:
        if zip_file is None:
            print("ERROR - No zip file provided for extraction.")
            return

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            total_size = sum(file.file_size for file in zip_ref.infolist())
            extracted_size = 0
            progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

            for file in zip_ref.infolist():
                zip_ref.extract(file, destination)
                extracted_size += file.file_size
                progress_bar.update(file.file_size)

            progress_bar.close()
            print('INFO - Extraction completed!')
    except zipfile.BadZipFile as e:
        print("ERROR - ", e)

def fetch_local_version():
    config = configparser.ConfigParser()
    config.read('config.ini')
    local_version = config.get('GAME', 'version')
    return local_version

def fetch_version_info():
    spinner = Halo(text='Fetching game version info', spinner='dots')
    spinner.start()
    time.sleep(2)

    url = "https://drive.google.com/uc?export=download&id=1fdKVdwP6O8mHOxR9MS8lwXUj4sivYT0w"
    try:
        response = requests.get(url)
        response.raise_for_status()
        version_number = response.text.strip()
        spinner.succeed("INFO - Version fetched successfully!")
        return version_number
    except requests.exceptions.RequestException as e:
        spinner.fail(f"ERROR - Failed to fetch version: {e}")
        return None

def compare_versions(local_version, online_version):
    return local_version != online_version

def download_launcher():
    game_url = "" #PUT HERE GAME LINK
    destination = download_file(game_url, 'game.zip')
    return destination

def update_local_config(new_version):
    config = configparser.ConfigParser()
    config.read('config.ini')

    config['GAME']['version'] = new_version
    
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def main():
    clear_screen()
    welcome_screen()
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        #online_version = fetch_version_info()
        #local_version = fetch_local_version()
        #temp
        online_version = "0.0.0"
        local_version = "0.0.0"

        if online_version is None:
            print('ERROR - Failed to fetch online version information.')
            return

        if compare_versions(local_version, online_version):
            print(f"INFO - New {online_version} version for game available. Downloading...")
            zip_file = download_launcher()
            extract_zip(zip_file, os.getcwd())
            update_local_config(online_version)
            print("INFO - Game updated successfully to version", online_version)
        else:
            print('INFO - Game is up to date!')
            print('')
            first_start = config.get('OTHER', 'fse')
            if first_start == "7":
                print("INFO - Starting first stratup screen...")
                # username input and generate data
                set_username()
                #RAM
                select_ram()
                #Set Java standart 
                set_default_java()
                print("INFO - First startup process finished.")
                print("INFO - Applying changes...")
                config = configparser.ConfigParser()
                config.read('config.ini')

                config['OTHER']['fse'] = "0"
                
                with open('config.ini', 'w') as config_file:
                    config.write(config_file)

            while True:
                default_screen()

                user_input = input("ACTION - Enter a number: ")
                if user_input not in ['1', '2', '3', '4', '5', '6', '1.', '2.', '3.', '4.', '5.', '6.']:
                    print("ERROR - Invalid Input!")
                    time.sleep(2)
                    continue
                if user_input == "1" or user_input == "1.":
                    start_current_game()
                    sys.exit()
                    return
                elif user_input == "2" or user_input == "2.":
                    #Change Nickname
                    print("ERROR - Not available for this moment.")
                    continue
                elif user_input == "3" or user_input == "3.":
                    select_ram()
                    continue
                elif user_input == "4" or user_input == "4.":
                    #change runtime
                    print("ERROR - Not available for this moment.")
                    continue
                elif user_input == "5" or user_input == "5.":
                    #check for game updates
                    print("ERROR - Not available for this moment.")
                    continue
                elif user_input == "6" or user_input == "6.":
                    sys.exit()
                    return

    except Exception as e:
        print("ERROR - ", e)

if __name__ == "__main__":
    main()