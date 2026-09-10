import os
import sys
import RASHFileEditor as FileEd
import codecs
from RASHFileAPI import FileAPI
import inputimeout
import time

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
time.sleep(0.8)
print("\n\033[32m[INFO]     | Looking for boot file...\033[0m")

possible_boots = ["/boot.py", "/boot/boot.py", "/init.py", "/boot/init.py"]
boot_location = []
for possibility in possible_boots:
    if FileAPI.file_exists(possibility):
        boot_location.append(possibility)
        print(f"\033[32m[INFO]     | Boot file found at {possibility}; looking at next location\033[0m")
    else:
        print(f"\033[32m[INFO]     | Boot file not found at {possibility}; looking at next location\033[0m")
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
        vars = {"FileAPI": FileAPI, "FileEd": FileEd}
        exec(FileAPI.get_file(boot_location))
else:
    j = 0
    for boot_file in boot_location:
        print(f"{j}: {boot_file} : {FileAPI.get_file(boot_file).split("\n")[0] if '#' in FileAPI.get_file(boot_file).split("\n")[0] else "NO COMMENT"}")
        j += 1
    response = input(f"\033[34mBoot file found at {boot_location}, booting. Press ENTER to enter mRASH instead, or <number> + ENTER to choose a boot file.\033[0m")
    if response.lower() == "":
        mRASH()
    else:
        clear()
        vars = {"FileAPI": FileAPI, "FileEd": FileEd}
        exec(FileAPI.get_file(boot_location[int(response)]))