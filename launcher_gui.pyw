import requests
import configparser
from tqdm import tqdm
import time
import os
import tempfile
import zipfile
import platform
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
import psutil
import gdown
from pypresence import Presence
import shutil

def check_discord_process():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'Discord.exe':
            return True
    return False

def start_discord_presence():
    if check_discord_process():
        client_id = '1213446048203276308'
        RPC = Presence(client_id)
        RPC.connect()
        RPC.update(
            state="In a game",
            details="Playing VL SMP",
            large_image="vlll",
            large_text="VL Launcher",
        )

def create_configs_if_not_exist():
    config = configparser.ConfigParser()

    default_config = {
        'MODPACK': {'version': '0.0.0'},
        'SKINS': {'version': '0.0.0'}
    }

    config_file = 'modpack.ini'
    if not os.path.exists(config_file):
        with open(config_file, 'w') as file:
            config.read_dict(default_config)
            config.write(file)

customtkinter.set_appearance_mode("dark")
start_discord_presence()
create_configs_if_not_exist()

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
    send_log('========================')
    send_log(f"Launcher Version: {fetch_launcher_local_version()}")
    send_log('========================')
    send_log(f"Game Version: {fetch_local_version()}")
    send_log('========================')
    send_log(f"Modpack Version: {fetch_local_mod_version()}")
    send_log('========================')
    send_log(f"Skins Version: {fetch_local_skin_version()}")
    send_log('========================')

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
        "-s", "37.230.138.199:25581"
    ]

    subprocess.Popen([executable_path] + arguments)

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

    ram = customtkinter.CTkInputDialog(title="RAM", text="Set your game ram (Choose 1,2,3,4,5 or enter manually in mb):\n1. 3072 (3GB)\n2. 4096 (4GB)\n3. 5120 (5GB) (Recommended)\n4. 6144 (6GB)\n5. 7168 (7GB)")
    ram_value = ram.get_input()

    if not ram_value:
        ram_value = "4096"

    if ram_value == "1" or ram_value == "1.":
        ram_value = "3072"
    elif ram_value == "2" or ram_value == "2.":
        ram_value = "4096"
    elif ram_value == "3" or ram_value == "3.":
        ram_value = "5120"  
    elif ram_value == "4" or ram_value == "4.":
        ram_value = "6144"
    elif ram_value == "5" or ram_value == "5.":
        ram_value = "7168"
    else:
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

        destination = os.path.join(os.getcwd(), filename)

        total_size = int(response.headers.get('content-length', 0))
        block_size = 4096  # 1 KB blocks
        #downloaded_size = 0
        #start_time = time.time()

        try:
            with open(destination, 'wb') as file:
                if file is not None:
                    #progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024)
                    send_log('INFO - Downloading content... Please wait and be patient ;)')
                    #progress_bar.pack(side=tk.BOTTOM, fill=tk.X)
                    #progress_bar.set(0)
                    for data in response.iter_content(block_size):
                        if data:
                            file.write(data)
                            #downloaded_size += len(data)
                            #progress = int((downloaded_size / total_size) * 100)
                            #elapsed_time = time.time() - start_time
                            #download_speed = downloaded_size / (1024 * elapsed_time)  # Speed in KB/s
                            #send_log(f"Downloading game... {progress}% ({downloaded_size}/{total_size} bytes), Speed: {download_speed:.2f} KB/s")
                            #progress_bar['value'] = progress
                            #progress_bar.update()
                        else:
                            send_log("ERROR - Download data not found!")
                            progress_bar.pack_forget()
        except Exception as e:
            send_log(f"ERROR - {e}")
            progress_bar.pack_forget()

        send_log("INFO - Download complete!")
        progress_bar.pack_forget()
        return destination
    except requests.exceptions.RequestException as e:
        send_log(f'ERROR - {e}')
        progress_bar.pack_forget()

def extract_zip(zip_file, destination):
    try:
        if zip_file is None:
            send_log("ERROR - No zip file provided for extraction.")
            return

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            total_size = sum(file.file_size for file in zip_ref.infolist())
            #extracted_size = 0
            #progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

            for file in zip_ref.infolist():
                zip_ref.extract(file, destination)
                #extracted_size += file.file_size
                #progress_bar.update(file.file_size)
                send_log(f"Extracting game... Please be patient ;)")

            #progress_bar.close()
            send_log('INFO - Extraction completed!')
    except zipfile.BadZipFile as e:
        send_log(f"ERROR - {e}")

    try:
        game_zip_path = os.path.join(os.getcwd(), "game.zip")
        if os.path.exists(game_zip_path):
            os.remove(game_zip_path)
            send_log("INFO - Successfully deleted temp files!")
    except Exception as e:
        send_log(f"ERROR - {e}")

def extract_zip_mods(zip_file, destination):
    try:
        if zip_file is None:
            send_log("ERROR - No zip file provided for extraction.")
            return

        mods_folder = os.path.join(destination, "assets", "UltimMC", "instances", "VL4", ".minecraft", "mods")
        extract_dest = os.path.join(destination, "assets", "UltimMC", "instances", "VL4", ".minecraft", "mods")
        if os.path.exists(mods_folder):
            shutil.rmtree(mods_folder)
            send_log("INFO - Existing mods folder deleted.")

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            total_size = sum(file.file_size for file in zip_ref.infolist())

            for file in zip_ref.infolist():
                zip_ref.extract(file, extract_dest)
                send_log(f"Extracting mods... Please be patient ;)")

            send_log('INFO - Modpack extraction completed!')
    except zipfile.BadZipFile as e:
        send_log(f"ERROR - {e}")

    try:
        mods_zip_path = os.path.join(os.getcwd(), "mods.zip")
        if os.path.exists(mods_zip_path):
            os.remove(mods_zip_path)
            send_log("INFO - Successfully deleted temp files!")
    except Exception as e:
        send_log(f"ERROR - {e}")

def extract_zip_skins(zip_file, destination):
    try:
        if zip_file is None:
            send_log("ERROR - No zip file provided for extraction.")
            return

        skins_folder = os.path.join(destination, "assets", "UltimMC", "instances", "VL4", ".minecraft", "cachedImages")
        extract_dest = os.path.join(destination, "assets", "UltimMC", "instances", "VL4", ".minecraft")
        if os.path.exists(skins_folder):
            shutil.rmtree(skins_folder)
            send_log("INFO - Existing skins folder deleted.")

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            total_size = sum(file.file_size for file in zip_ref.infolist())

            for file in zip_ref.infolist():
                zip_ref.extract(file, extract_dest)
                send_log(f"Extracting skins... Please be patient ;)")

            send_log('INFO - Skins extraction completed!')
    except zipfile.BadZipFile as e:
        send_log(f"ERROR - {e}")

    try:
        skins_zip_path = os.path.join(os.getcwd(), "skins.zip")
        if os.path.exists(skins_zip_path):
            os.remove(skins_zip_path)
            send_log("INFO - Successfully deleted temp files!")
    except Exception as e:
        send_log(f"ERROR - {e}")

def download_mods():
    #mariusskrasavcevs2
    mods_url = "https://dl.dropboxusercontent.com/scl/fi/dlmzkk91mar32vpkzvh8z/mods.zip?rlkey=b2bse9kgdbuw2t65l6c7bx60x&dl=0"
    destination = download_file(mods_url, 'mods.zip')
    return destination

def download_launcher():
    #mini13lolix
    game_url = "https://dl.dropboxusercontent.com/scl/fi/uskzkarcc5laq8rorvh7h/game.zip?rlkey=gzdsxkev2uvs54q8agaavb4p3&dl=0"
    destination = download_file(game_url, 'game.zip')
    return destination

def download_skins():
    #google
    skins_url = "https://drive.google.com/uc?export=download&id=1udsB2FIxho0DLZxcjDSHmrJ0OQdIMrzL"
    destination = download_file(skins_url, 'skins.zip')
    return destination

def fetch_local_version():
    config = configparser.ConfigParser()
    config.read('config.ini')
    local_version = config.get('GAME', 'version')
    return local_version

def fetch_local_mod_version():
    config = configparser.ConfigParser()
    config.read('modpack.ini')
    local_mod_version = config.get('MODPACK', 'version')
    return local_mod_version

def fetch_launcher_local_version():
    config = configparser.ConfigParser()
    config.read('config.ini')
    local_version = config.get('LAUNCHER', 'version')
    return local_version

def fetch_version_info():
    send_log("INFO - Fetching game version info")
    time.sleep(2)

    url = "https://drive.google.com/uc?export=download&id=1fdKVdwP6O8mHOxR9MS8lwXUj4sivYT0w"
    try:
        response = requests.get(url)
        response.raise_for_status()
        version_number = response.text.strip()
        send_log("INFO - Version fetched successfully!")
        return version_number
    except requests.exceptions.RequestException as e:
        send_log(f"ERROR - Failed to fetch version: {e}")
        return None

def compare_versions(local_version, online_version):
    return local_version != online_version

def update_local_config(new_version):
    config = configparser.ConfigParser()
    config.read('config.ini')

    config['GAME']['version'] = new_version
    
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def fetch_mod_version_info():
    send_log("INFO - Fetching modpack version info")
    time.sleep(2)

    url = "https://drive.google.com/uc?export=download&id=1NpkzTPb4HoYIwhY8Mii_K9Q2m7zyzvVG"
    try:
        response = requests.get(url)
        response.raise_for_status()
        version_number = response.text.strip()
        send_log("INFO - Modpack version fetched successfully!")
        return version_number
    except requests.exceptions.RequestException as e:
        send_log(f"ERROR - Failed to fetch modpack version: {e}")
        return None

def update_local_mod_config(new_version):
    config = configparser.ConfigParser()
    config.read('modpack.ini')

    config['MODPACK']['version'] = new_version
    
    with open('modpack.ini', 'w') as config_file:
        config.write(config_file)

def fetch_skin_version_info():
    send_log("INFO - Fetching skins version info")
    time.sleep(2)

    url = "https://drive.google.com/uc?export=download&id=1fH3d9UYgQ8_CCreh1NIFb0iKj2Ui3OaR"
    try:
        response = requests.get(url)
        response.raise_for_status()
        version_number = response.text.strip()
        send_log("INFO - Skins version fetched successfully!")
        return version_number
    except requests.exceptions.RequestException as e:
        send_log(f"ERROR - Failed to fetch skins version: {e}")
        return None

def fetch_local_skin_version():
    config = configparser.ConfigParser()
    config.read('modpack.ini')
    local_skin_version = config.get('SKINS', 'version')
    return local_skin_version

def update_local_skin_config(new_version):
    config = configparser.ConfigParser()
    config.read('modpack.ini')

    config['SKINS']['version'] = new_version
    
    with open('modpack.ini', 'w') as config_file:
        config.write(config_file)

def change_username():
    set_username()

def change_runtime():
    set_default_java(False)

def check_updates():
    buttons_busy()
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
            send_log(f"INFO - Game updated successfully to version {online_version}")
            time.sleep(5)
        else:
            send_log('INFO - Game is up to date!')
            time.sleep(1)

        online_mod_version = fetch_mod_version_info()
        local_mod_version = fetch_local_mod_version()

        if online_mod_version is None:
            send_log('ERROR - Failed to fetch modpack online version information.')
            return

        if compare_versions(local_mod_version, online_mod_version):
            send_log(f"INFO - New {online_mod_version} version for modpack available. Downloading...")
            zip_file = download_mods()
            zip_file = os.path.join(os.getcwd(), "mods.zip")
            extract_zip_mods(zip_file, os.getcwd())
            update_local_mod_config(online_mod_version)
            send_log(f"INFO - Modpack updated successfully to version {online_mod_version}")
            time.sleep(5)
        else:
            send_log('INFO - Modpack is up to date!')
            time.sleep(1)

        online_skins_version = fetch_skin_version_info()
        local_skins_version = fetch_local_skin_version()

        if online_skins_version is None:
            send_log('ERROR - Failed to fetch skins online version information.')
            return

        if compare_versions(local_skins_version, online_skins_version):
            send_log(f"INFO - New {online_skins_version} version for skins available. Downloading...")
            zip_file = download_skins()
            zip_file = os.path.join(os.getcwd(), "skins.zip")
            extract_zip_skins(zip_file, os.getcwd())
            update_local_skin_config(online_skins_version)
            send_log(f"INFO - Skins updated successfully to version {online_skins_version}")
            time.sleep(5)
        else:
            send_log('INFO - Skins are up to date!')
            time.sleep(1)

        check_first_startup()
    except Exception as e:
        send_log(f"ERROR - {e}")

def install_redist():
    send_log("Installing Java 21...")
    current_directory = os.getcwd()
    java_file = os.path.join(current_directory, "assets", "redist", "jdk-21_windows-x64_bin.msi")
    #subprocess.call(['msiexec', '/i', java_file, '/quiet', '/norestart'])
    #subprocess.call(['msiexec', '/i', java_file, '/norestart'])
    subprocess.call(['msiexec', '/i', java_file, '/passive', '/norestart'])
    send_log("Successfully installed Java 21!")

def check_first_startup():
    buttons_busy()
    config = configparser.ConfigParser()
    config.read('config.ini')
    first_start = config.get('OTHER', 'fse')
    if first_start == "7":
        send_log("INFO - Starting first stratup screen...")
        #REDIST JAVA
        install_redist()
        #update condfigs
        copy_configs_fse()
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
        buttons_ready()
        send_log("INFO - Game is ready!")
    else:
        send_log("INFO - Game is ready!")
        buttons_ready()

def exit_launcher():
    root.destroy()
    RPC.close()
    subprocess.call(['taskkill', '/F', '/IM', 'launcher_gui.exe'])
    subprocess.call(['taskkill', '/F', '/IM', 'python.exe'])

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

def open_minecraft_folder():
    current_directory = os.getcwd()
    minecraft_folder = os.path.join(current_directory, "assets", "UltimMC", "instances", "VL4", ".minecraft")
    os.startfile(minecraft_folder)

def show_play_count_button():
    send_log('-------------------------------------------------')
    send_log(f"Total time played on VL4: {get_time_played()}")
    send_log('-------------------------------------------------')

def copy_configs_fse():
    current_directory = os.getcwd()
    default_folder = os.path.join(current_directory, "assets", "default", "UltimMC")
    where_copy = os.path.join(current_directory, "assets")
    destination_folder = os.path.join(where_copy, "UltimMC")
    
    shutil.copytree(default_folder, destination_folder, dirs_exist_ok=True)
    send_log(f"INFO - Configs updated!")

def buttons_ready():
    start_button.configure(state=tk.NORMAL)
    change_username_button.configure(state=tk.NORMAL)
    set_ram_button.configure(state=tk.NORMAL)
    #change_runtime_button.configure(state=tk.NORMAL)
    check_updates_button.configure(state=tk.NORMAL)
    open_minecraft_folder_button.configure(state=tk.NORMAL)
    show_play_count_button.configure(state=tk.NORMAL)

def buttons_busy():
    start_button.configure(state=tk.DISABLED)
    change_username_button.configure(state=tk.DISABLED)
    set_ram_button.configure(state=tk.DISABLED)
    #change_runtime_button.configure(state=tk.DISABLED)
    check_updates_button.configure(state=tk.DISABLED)
    open_minecraft_folder_button.configure(state=tk.DISABLED)
    show_play_count_button.configure(state=tk.DISABLED)

def check_update_thread():
    updates_thread = threading.Thread(target=check_updates)
    updates_thread.start()

def get_server_info():
    url = "https://api.mcsrvstat.us/3/37.230.138.199:25581"
    
    try:
        response = requests.get(url)
        data = response.json()

        version = data.get('version', None)
        is_online = data.get('online', False)
        online_player_count = data['players']['online'] if 'players' in data and 'online' in data['players'] else None
        max_player_count = data['players']['max'] if 'players' in data and 'max' in data['players'] else None

        return version, is_online, online_player_count, max_player_count
    except Exception as e:
        send_log(f"ERROR - {e}")
        return None

root = customtkinter.CTk()
root.title("VL4 Launcher")
root.resizable(False, False)
root.geometry("800x340")

log_frame = customtkinter.CTkFrame(root)
log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


log_text = customtkinter.CTkTextbox(log_frame, wrap=tk.WORD, height=10, width=50, state=tk.DISABLED)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


button_frame = customtkinter.CTkFrame(root)
button_frame.pack(side=tk.RIGHT, fill=tk.Y)


start_button = customtkinter.CTkButton(button_frame, text="Start Game", command=start_current_game, state=tk.DISABLED)
start_button.pack(fill=tk.X)

show_play_count_button = customtkinter.CTkButton(button_frame, text="Show Playtime", command=show_play_count_button, state=tk.DISABLED)
show_play_count_button.pack(fill=tk.X)

change_username_button = customtkinter.CTkButton(button_frame, text="Change Username", command=change_username, state=tk.DISABLED)
change_username_button.pack(fill=tk.X)

set_ram_button = customtkinter.CTkButton(button_frame, text="Allocate RAM", command=set_startup_ram, state=tk.DISABLED)
set_ram_button.pack(fill=tk.X)

open_minecraft_folder_button = customtkinter.CTkButton(button_frame, text="Open .minecraft folder", command=open_minecraft_folder, state=tk.DISABLED)
open_minecraft_folder_button.pack(fill=tk.X)

check_updates_button = customtkinter.CTkButton(button_frame, text="Check Updates", command=check_update_thread, state=tk.DISABLED)
check_updates_button.pack(fill=tk.X)

exit_button = customtkinter.CTkButton(button_frame, text="Exit Launcher", command=exit_launcher)
exit_button.pack(fill=tk.X)

progress_bar = customtkinter.CTkProgressBar(button_frame, mode='determinate')
progress_bar.set(0)
progress_bar.pack_forget()


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

def display_server_data():
    data = get_server_info()

    if data is not None:
        version = data[0]
        is_online = data[1]
        online_player_count = data[2]
        max_player_count = data[3]
        bullet_points = ('\u2022') * 30

        send_log(f"INFO - {version}, is_online={is_online}, {online_player_count}/{max_player_count}")
        
        server_status = 'Online: True' if is_online else 'Online: False'
        server_label = customtkinter.CTkLabel(button_frame, text=f"VL4 SERVER STATUS\n{bullet_points}\n{server_status}\nVersion: {version}\nPlayers: {online_player_count}/{max_player_count}\n{bullet_points}", fg_color=("dark green"), corner_radius=8)
    else:
        send_log(f"ERROR - Failed to fetch server information!")
        server_label = customtkinter.CTkLabel(button_frame, text=f"VL4 SERVER STATUS\n{bullet_points}\nFailed to fetch\nserver information\n{bullet_points}", fg_color=("dark red"), corner_radius=8)
        
    server_label.pack(side=tk.BOTTOM, pady=11)

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
    display_server_data_thread = threading.Thread(target=display_server_data)

    welcome_thread.start()
    updates_thread.start()
    display_server_data_thread.start()

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pass
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "Parent process information missing. Try starting launcher from launcher_updater.exe")
        sys.exit(1)

    main()