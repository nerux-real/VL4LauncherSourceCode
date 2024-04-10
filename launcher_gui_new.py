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


def main():
    clear_screen()
    welcome_screen()
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        fse_status = config.get('OTHER', 'fse')

        if fse_status is None:
            print('ERROR - Failed to fetch fse information.')
            return

        if fse_status == "7":
            #install deps and start VLLauncher.exe
            # at folder /assets/redist/jdk-21_windows-x64_bin.msi
            # and at folder
            current_directory = os.getcwd()
            java_file = os.path.join(current_directory, "assets", "redist", "jdk-21_windows-x64_bin.msi")
            subprocess.call(['msiexec', '/i', java_file, '/passive', '/norestart'])
            print("Successfully installed Java 21!")
            net_file = os.path.join(current_directory, "assets", "redist", "ndp472-kb4054531-web.exe")
            subprocess.call(['msiexec', '/i', net_file, '/passive', '/norestart'])
            print("Successfully installed .NET Framework 4.7.2")

        executable_path = os.path.join(os.getcwd(), "VLLauncher.exe")
        subprocess.Popen([executable_path] + arguments)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()