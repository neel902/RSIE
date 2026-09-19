from RashUSBAPI import USBAPI
import configparser
import os
import sys
import RASHFileEditor as FileEd
import codecs
from RASHFileAPI import FileAPI
import inputimeout
import time

RSIEPATH = "/rsei.rsei"

def evaluate_escape_sequences(text):
    raw_bytes = text.encode('utf-8')
    decoded_bytes, _ = codecs.escape_decode(raw_bytes)
    return decoded_bytes.decode('utf-8')

def mRASH():
    print("Mini RASH Terminal (mRASH v0.1.0)\n")
    RUNNING = True
    while RUNNING:
        cmd = input("> ")
        if cmd == "reboot":
            print("Rebooting... ")
            time.sleep(0.5)
            os.execl(sys.executable, sys.executable, *sys.argv)
        if cmd == "exit": RUNNING = False
        cmd = cmd.split(" ")
        if cmd[0].lower() == "del":
            FileAPI.delete_file(cmd[1])
        if cmd[0].lower() == "read":
            print(FileAPI.get_file(cmd[1]))
        if cmd[0].lower() == "create":
            FileAPI.set_file(cmd[1], "")
        if cmd[0].lower() == "list":
            print("  ,  ".join(FileAPI.list_file_regex(' '.join(cmd[1:]))))
        if cmd[0].lower() == "set":
            FileAPI.set_file(cmd[1], evaluate_escape_sequences(" ".join(cmd[2:])))


clear = lambda : print("\033[2J\033[3J\033[H")
clear()

time.sleep(0.1)
print("Rash Sandboxing Interface Extended Edition (v0.1.0)")

config = configparser.ConfigParser()

if FileAPI.file_exists(RSIEPATH):
    print("\n\033[32m[INFO]     | Found RFEI BIOS settings...\033[0m")
    rseifirmware = FileAPI.get_file(RSIEPATH)
else:
    print("\n\033[32m[INFO]     | Could not find RSIE Firmware settings, making file...\033[0m")
    rseifirmware = """
[BootLocations]
possible_boots = /boot/boot.py, /boot.py, /init.py, /boot/init.py
"""
    FileAPI.set_file(RSIEPATH, rseifirmware)
    print("\033[32m[INFO]     | Done\033[0m")
config.read_string(rseifirmware)
time.sleep(0.8)
print("\033[32m[INFO]     | Read RSIE Firmware settings\033[0m")
print("\033[32m[INFO]     | Looking for boot file...\033[0m")

possible_boots = [p.strip() for p in config.get("BootLocations", "possible_boots").split(",")]

boot_location = []
for possibility in possible_boots:
    if FileAPI.file_exists(possibility):
        boot_location.append(possibility)
        print(f"\033[32m[INFO]     | Boot file found at {possibility}; looking at next location\033[0m")
    else:
        print(f"\033[32m[INFO]     | Boot file not found at {possibility}; looking at next location\033[0m")

print(f"\033[32m[INFO]     | Searching for bootable mounts...\033[0m")
usbs = USBAPI.search()
bootableexist = len(usbs) > 0
bootableusb = ""
for usb in usbs:
    usbapi = USBAPI.FileAPI(usb)
    if usbapi.file_exists("/boot.py"):
        print(f"\033[32m[INFO]     | Found '{usb}' as bootable.\033[0m")
        bootableusb = usb
        break
bootusb = False
if bootableexist:
    if input(f"\033[34mType 'y' to boot from mount '{bootableusb}' \033[0m") == "y":
        bootusb = True
if bootusb:
    usbapi = USBAPI.FileAPI(bootableusb)
    clear()
    vars = {"FileAPI": FileAPI, "FileEd": FileEd, "USBAPI": USBAPI}
    exec(usbapi.get_file("/boot.py"))
else:
    print(f"\033[32m[INFO]     | Booting from drive...\033[0m" if bootableexist else f"\033[32m[INFO]     | No bootable mount found; continuing.\033[0m")
    if len(boot_location) == 0:
        print("\033[1;31m[CRITICAL] | No boot file found. Entering mRASH...\033[0m")
        mRASH()
    elif len(boot_location) == 1:
        boot_location = boot_location[0]
        try:
            response = inputimeout.inputimeout(f"\033[34mBoot file found at {boot_location}, booting. Press ENTER to enter mRASH instead, or S + ENTER to skip this wait.\033[0m", 3)
            if response.lower() == "s": raise inputimeout.TimeoutOccurred
            mRASH()
        except inputimeout.TimeoutOccurred:
            clear()
            vars = {"FileAPI": FileAPI, "FileEd": FileEd, "USBAPI": USBAPI}
            exec(FileAPI.get_file(boot_location))
    else:
        j = 0
        for boot_file in boot_location:
            print(f"{j}: {boot_file} : {FileAPI.get_file(boot_file).split("\n")[0] if '#' in FileAPI.get_file(boot_file).split("\n")[0] else "NO COMMENT"}")
            j += 1
        response = input(f"\033[34mBoot files found, booting. Press ENTER to enter mRASH instead, or <number> + ENTER to choose a boot file.\033[0m")
        if response.lower() == "":
            mRASH()
        else:
            clear()
            vars = {"FileAPI": FileAPI, "FileEd": FileEd, "USBAPI": USBAPI}
            exec(FileAPI.get_file(boot_location[int(response)]))