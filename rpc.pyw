from pypresence import Presence
import os
import psutil
import time

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
        
def update_rpc():
    RPC.update(
        state="In a game",
        details="Playing VL SMP",
        large_image="vlll",
        large_text="VL Launcher",
    )
    while True:
        time.sleep(10)

start_discord_presence()