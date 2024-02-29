import requests
import configparser
from tqdm import tqdm
import time
import os
import tempfile
import zipfile
from halo import Halo
import platform
import subprocess

def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def welcome_screen():
    print("======VL UPDATER======")

def get_current_destination():
    return os.getcwd()

def download_file(url, filename):
    try:
        print('INFO - Starting downloading launcher...')
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
    local_version = config.get('LAUNCHER', 'version')
    return local_version

def fetch_version_info():
    spinner = Halo(text='Fetching version info', spinner='dots')
    spinner.start()
    time.sleep(2)

    url = "https://drive.google.com/uc?export=download&id=1J6wLmEkOQCQq6jzjksPgAnd51X2HL8B5"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        version_number = response.text.strip()
        spinner.succeed("INFO - Version fetched successfully!")
        return version_number
    except requests.exceptions.RequestException as e:
        spinner.fail(f"ERROR - Failed to fetch version: {e}")
        return None

def compare_versions(local_version, online_version):
    return local_version != online_version

def download_launcher():
    launcher_url = "https://dl.dropboxusercontent.com/scl/fi/5jrnlg5yzdgtzzbtfidpf/launcher.zip?rlkey=lxndou25mr1ylsrgfejwnxhxs&dl=0"
    destination = download_file(launcher_url, 'launcher.zip')
    return destination

def update_local_config(new_version):
    config = configparser.ConfigParser()
    config.read('config.ini')

    config['LAUNCHER']['version'] = new_version
    
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def main():
    clear_screen()
    welcome_screen()
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        online_version = fetch_version_info()
        local_version = fetch_local_version()

        if online_version is None:
            print('ERROR - Failed to fetch online version information.')
            return

        if compare_versions(local_version, online_version):
            print(f"INFO - New {online_version} version for launcher available. Downloading...")
            zip_file = download_launcher()
            extract_zip(zip_file, os.getcwd())
            update_local_config(online_version)
            print("INFO - Launcher updated successfully to version", online_version)
            subprocess.run("taskkill /F /T /PID %i" % os.getpid(), shell=True)
            subprocess.Popen(["launcher_gui.exe"], cwd=os.getcwd())
        else:
            print('INFO - Launcher is up to date!')
            subprocess.Popen(["launcher_gui.exe"], cwd=os.getcwd())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()