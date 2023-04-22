import subprocess
import os
import socket
import ctypes
import logging

def clear_screen(your_os : str):
    if your_os == "Linux":
        subprocess.run("clear",shell=True)
    else:
        subprocess.run("cls",shell=True)

def get_sys_info():
    try:
        is_admin = os.getuid() == 0
        your_os="Linux"
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        your_os="Windows"
    if is_admin:
        tag="#"
    else:
        tag="$"
    return (your_os, tag)

def main():
    clear_screen(get_sys_info())
    while True:
        try:
            path=os.getcwd()
            hostname=socket.gethostname()
            username=os.getlogin()
            your_os, tag = get_sys_info()
            command=input(f"{your_os} Terminal At - {path} [{username}@{hostname}]{tag} ")
            if "cd" in command:
                try:
                    chdir = command.replace("cd ","")
                    os.chdir(chdir)
                except FileNotFoundError:
                    print("Path Not Found")
                    continue
            else:
               subprocess.run(command,stdout=subprocess.PIPE, shell=True)

        except KeyboardInterrupt:
            clear_screen(your_os)
            print("Thank You For Using My Terminal\n")
            exit()
main()
