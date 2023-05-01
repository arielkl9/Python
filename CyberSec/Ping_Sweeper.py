from icmplib import ping
import ipaddress
import subprocess
import os

def get_ip_range():
    ip_range = input("pls enter ip range (x.x.x.x/x)")
    return str(ip_range)
    
def ping_loop():
    ip_range = get_ip_range()
    while True:
        try:
            for i in ipaddress.IPv4Network(ip_range):
                a = ping(str(i), count=1, interval=1, timeout=0.1, id=None, source=None, family=None, privileged=True)
                if "Packets received: 1" in str(a):
                    print(f"{str(i)} is alive!")
                    devices['alive'].append(str(i))
                else:
                    print(f"{str(i)} is dead!")
                    devices['dead'].append(str(i))
            break
        except Exception as e:
            print(f"{e}\nTry Again Pls")
            continue
  
def clear_screen():
    try:
        os.getuid()
        subprocess.run("clear",shell=True)
    except AttributeError:
        subprocess.run("cls",shell=True)

def goodbye_screen():
    clear_screen()
    print("----------------------------------------------------")
    print("|          ping sweep finished succesfuly          |")
    print("|                                                  |")
    print("|         results are in results.txt file          |")
    print("|                                                  |")
    print("| pls check my github: https://github.com/arielkl9 |")
    print("|                                                  |")
    print("|            thanks for using my tool!             |")
    print("|                                                  |")
    print("|               press enter to exit                |")
    print("----------------------------------------------------")
    input()

def backup():
    with open("results.txt","w") as file:
        file.write("Ping Sweep Result:\n\n")
        if devices["alive"]:
            file.write("Alive IPs:\n")
            for i in devices["alive"]:
                file.write(f"{i}\n")
        file.write("\n")
        if devices["dead"]:
            file.write("Dead IPs:\n")
            for i in devices["dead"]:
                file.write(f"{i}\n")
def main():
    global devices
    devices = {
        'alive' : [],
        'dead' : []
    }
    clear_screen()
    ping_loop()
    backup()
    goodbye_screen()

main()