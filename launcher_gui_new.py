import requests
import configparser
import time
import os
import platform
import subprocess
import psutil

def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def welcome_screen():
    print("======VLDEP======")

def read_config_value(filename, section, key):
    with open(filename, 'r') as config_file:
        for line in config_file:
            if line.strip().startswith(f"[{section}]"):
                break
        else:
            return None

        for line in config_file:
            if line.strip().startswith(key):
                _, value = line.split('=', 1)
                return value.strip()

    return None

def main():
    clear_screen()
    welcome_screen()
    try:
        #config = configparser.ConfigParser()
        #config.read('config.ini')
        #fse_status = config.get('OTHER', 'fse')
        fse_status = read_config_value('config.ini', 'OTHER', 'fse')

        if fse_status == "7":
            current_directory = os.getcwd()
            java_file = os.path.join(current_directory, "assets", "redist", "jdk-21_windows-x64_bin.msi")
            subprocess.call(['msiexec', '/i', java_file, '/passive', '/norestart'])
            print("Successfully installed Java 21!")
            net_file = os.path.join(current_directory, "assets", "redist", "ndp472-kb4054531-web.exe")
            subprocess.call(['msiexec', '/i', net_file, '/passive', '/norestart'])
            print("Successfully installed .NET Framework 4.7.2")

        executable_path = os.path.join(os.getcwd(), "VLLauncher.exe")
        subprocess.Popen(executable_path)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()