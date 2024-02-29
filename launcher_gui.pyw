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
import tkinter as tk
from tkinter import messagebox, Text, Scrollbar
import customtkinter
import threading
import random

customtkinter.set_appearance_mode("dark")

def send_log(message):
    if threading.current_thread() is threading.main_thread():
        log_text.configure(state=tk.NORMAL)
        log_text.insert(tk.END, f"{message}\n")
        log_text.configure(state=tk.DISABLED)
        log_text.see(tk.END)
    else:
        root.after(0, send_log, message)

def welcome_screen():
    send_log("Welcome to VL Launcher GUI!")
    send_log("==================")
    send_log(f"Version: {fetch_local_version()}")
    send_log("==================")
    send_log("---------------------------------------------------------")
    send_log(f"Total time played on VL4: {get_time_played()}")
    send_log("---------------------------------------------------------")

def get_current_destination():
    return os.getcwd()

def start_current_game():
    executable_path = os.path.join(os.getcwd(), "assets", "UltimMC", "UltimMC.exe")
    directory_path = os.path.join(os.getcwd(), "assets", "UltimMC")

    arguments = [
        "-d", directory_path,
        "-l", "VL4",
        "-s", "87.98.151.230:25584"
    ]

    subprocess.Popen([executable_path] + arguments)

def default_screen():
    clear_screen()
    welcome_screen()
    send_log('==================')
    send_log(f"Version {fetch_local_version()}")
    send_log('==================')

    send_log('-------------------------------------------------')
    send_log(f"Total time played on VL4: {get_time_played()}")
    send_log('-------------------------------------------------')

    default_choices()

def set_username():
    dialog = customtkinter.CTk()
    dialog.withdraw()
    dialog.resizable(False, False)

    username = customtkinter.CTkInputDialog(title="Set", text="Enter your username:")
    username_entry = username.get_input()

    if username_entry is not None:
        username_entry = username_entry
    else:
        username_entry = f"VLUser_{random.randint(1, 9999999)}"

    config = configparser.ConfigParser()
    config.read('config.ini')
    config['GAME']['username'] = username_entry   
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

    send_log(f"INFO - Username set successfully to: {username_entry}")

    set_user_data(username_entry)

def set_user_data(nickname):
    current_directory = os.getcwd()

    id_hex = uuid.uuid4().hex
    client_token_hex = uuid.uuid4().hex
    iat = int(time.time())
    send_log(nickname)
    send_log(id_hex)
    send_log(client_token_hex)
    send_log(iat)

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

    send_log("INFO - Account data set successfully.")
    time.sleep(2)
    return

def set_startup_ram():
    dialog = customtkinter.CTk()
    dialog.withdraw()
    dialog.resizable(False, False)

    ram = customtkinter.CTkInputDialog(title="RAM", text="Set your game ram:\n1. 3072 (3GB)\n2. 4096 (4GB)\n3. 5120 (5GB) (Recommended)\n4. 6144 (6GB)\n5. 7168 (7GB)")
    ram_value = ram.get_input()

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

    send_log(f"INFO - Successfully set RAM to {ram_value}!")

#not working
def update_ram_config(event):
    selected_option = selected_ram.get()
    ram_value = int(selected_option.split()[0])
    print(ram_value)

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

    send_log(f"INFO - Successfully set RAM to {ram_value}!")

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

def set_default_java(autoSet):
    if autoSet:
        current_directory = os.getcwd()
        java_location = os.path.join(current_directory, "assets", "jdk-21.0.2", "bin", "javaw.exe")
        java_location = java_location.replace('/', '\\')
        java_location = java_location.replace('\\', '\\\\')
        config_file = os.path.join(current_directory, "assets", "UltimMC", "ultimmc.cfg")
        config_file2 = os.path.join(current_directory, "assets", "UltimMC", "instances", "VL4", "instance.cfg")
    else:
        selected_java_path = customtkinter.askopenfilename(
            title="Select javaw.exe file",
            filetypes=[("Executable files", "*.exe")],
            initialdir=os.getcwd()
        )
        if selected_java_path:
            if os.path.basename(selected_java_path).lower() == 'javaw.exe':
                java_location = selected_java_path
                java_location = java_location.replace('/', '\\')
                java_location = java_location.replace('\\', '\\\\')
            else:
                customtkinter.messagebox.showerror("Invalid File", "Please select a valid javaw.exe file.")
                return
        else:
            return

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

    send_log(f"INFO - Java path successfully set to {java_location}!")
    time.sleep(2)
    return

def download_file(url, filename):
    try:
        send_log('INFO - Starting downloading game...')
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

        send_log("INFO - Download complete!")
        return destination
    except requests.exceptions.RequestException as e:
        send_log('ERROR - ', e)

def extract_zip(zip_file, destination):
    try:
        if zip_file is None:
            send_log("ERROR - No zip file provided for extraction.")
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
            send_log('INFO - Extraction completed!')
    except zipfile.BadZipFile as e:
        send_log("ERROR - ", e)

def fetch_local_version():
    config = configparser.ConfigParser()
    config.read('config.ini')
    local_version = config.get('GAME', 'version')
    return local_version

def fetch_version_info():
    #spinner = Halo(text='Fetching game version info', spinner='dots')
    #spinner.start()
    send_log("INFO - Fetching game version info")
    time.sleep(2)

    url = "https://drive.google.com/uc?export=download&id=1fdKVdwP6O8mHOxR9MS8lwXUj4sivYT0w"
    try:
        response = requests.get(url)
        response.raise_for_status()
        version_number = response.text.strip()
        #spinner.succeed("INFO - Version fetched successfully!")
        send_log("INFO - Version fetched successfully!")
        return version_number
    except requests.exceptions.RequestException as e:
        #spinner.fail(f"ERROR - Failed to fetch version: {e}")
        send_log(f"ERROR - Failed to fetch version: {e}")
        return None

def compare_versions(local_version, online_version):
    return local_version != online_version

def download_launcher():
    game_url = "https://drive.google.com/uc?export=download&id=1MUIhk9jZIQK8-Fcl2v1QuLl9n1Sp7236" #PUT HERE GAME LINK
    destination = download_file(game_url, 'game.zip')
    return destination

def update_local_config(new_version):
    config = configparser.ConfigParser()
    config.read('config.ini')

    config['GAME']['version'] = new_version
    
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def change_username():
    set_username()

def change_runtime():
    set_default_java(False)

def check_updates():
    send_log("INFO - Checking for updates...")
    time.sleep(2)
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        online_version = fetch_version_info()
        local_version = fetch_local_version()

        if online_version is None:
            send_log('ERROR - Failed to fetch online version information.')
            return

        if compare_versions(local_version, online_version):
            send_log(f"INFO - New {online_version} version for game available. Downloading...")
            zip_file = download_launcher()
            extract_zip(zip_file, os.getcwd())
            update_local_config(online_version)
            send_log("INFO - Game updated successfully to version", online_version)
            time.sleep(5)
            check_first_startup()
        else:
            send_log('INFO - Game is up to date!')
            time.sleep(1)
            set_default_java(True)
            check_first_startup()
    except Exception as e:
        send_log(f"ERROR - {e}")

def check_first_startup():
    config = configparser.ConfigParser()
    config.read('config.ini')
    first_start = config.get('OTHER', 'fse')
    if first_start == "7":
        send_log("INFO - Starting first stratup screen...")
        # username input and generate data
        set_username()
        #RAM
        set_startup_ram()
        #Set Java standart 
        #set_default_java()
        send_log("INFO - First startup process finished.")
        send_log("INFO - Applying changes...")
        config = configparser.ConfigParser()
        config.read('config.ini')

        config['OTHER']['fse'] = "0"
                
        with open('config.ini', 'w') as config_file:
            config.write(config_file)

        send_log("INFO - Changes applied!")
        send_log("INFO - Game is ready!")

def exit_launcher():
    root.destroy()

def set_default_ram():
    current_directory = os.getcwd()
    config_file = os.path.join(current_directory, "config.ini")

    with open(config_file, 'r') as f:
        lines = f.readlines()

    ram_value = None
    for line in lines:
        if line.startswith("ram = "):
            ram_value = line.split('=')[1].strip()

    if ram_value:
        selected_ram.set(ram_value)

root = customtkinter.CTk()
root.title("VL4 Launcher")
root.resizable(False, False)
root.geometry("700x320")

log_frame = customtkinter.CTkFrame(root)
log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


log_text = customtkinter.CTkTextbox(log_frame, wrap=tk.WORD, height=10, width=50, state=tk.DISABLED)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


button_frame = customtkinter.CTkFrame(root)
button_frame.pack(side=tk.RIGHT, fill=tk.Y)


start_button = customtkinter.CTkButton(button_frame, text="Start Game", command=start_current_game)
start_button.pack(fill=tk.X)

change_username_button = customtkinter.CTkButton(button_frame, text="Change Username", command=change_username)
change_username_button.pack(fill=tk.X)

set_ram_button = customtkinter.CTkButton(button_frame, text="Allocate RAM", command=set_startup_ram)
set_ram_button.pack(fill=tk.X)

change_runtime_button = customtkinter.CTkButton(button_frame, text="Change Runtime", command=change_runtime)
change_runtime_button.pack(fill=tk.X)

check_updates_button = customtkinter.CTkButton(button_frame, text="Check Updates", command=check_updates)
check_updates_button.pack(fill=tk.X)

exit_button = customtkinter.CTkButton(button_frame, text="Exit Launcher", command=exit_launcher)
exit_button.pack(fill=tk.X)

#ram_options = [
#    "3072 (3GB)",
#    "4096 (4GB)",
#    "5120 (5GB) (Recommended)",
#    "6144 (6GB)",
#    "7168 (7GB)"
#]

#selected_ram = tk.StringVar(root)
#ram_combo_menu = customtkinter.CTkComboBox(root, values=ram_options, textvariable=selected_ram)
#ram_combo_menu.pack(side=tk.BOTTOM)

#ram_combo_menu.bind("<<ComboboxSelected>>", update_ram_config)

#ram_label = customtkinter.CTkLabel(button_frame, text="Select RAM for game:")
#ram_label.pack(side=tk.BOTTOM, pady=11)

def fetch_launcher_version():
    config = configparser.ConfigParser()
    config.read('config.ini')
    version = config.get('LAUNCHER', 'version')
    return version

def main():
    send_log("Initializing VL4 Launcher")
    send_log(get_current_destination())

    welcome_thread = threading.Thread(target=welcome_screen)
    updates_thread = threading.Thread(target=check_updates)

    welcome_thread.start()
    updates_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()