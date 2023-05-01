import os
import socket
import ipaddress
import subprocess
from icmplib import ping

def get_ip_range():
    ip_range = input("pls enter ip range (x.x.x.x/x)")
    return str(ip_range)
    
def ping_loop():
    ip_range = get_ip_range()
    alive_ip = []
    dead_ip = []
    clear_screen()
    try:
        for ip in ipaddress.IPv4Network(ip_range):
            result = ping(ip.compressed, count=1, interval=1, timeout=2, id=None, source=None, family=None, privileged=True)
            if "Packets received: 1" in str(result):
                alive_ip.append(ip.compressed)
                print(f"{ip.compressed} is alive!")
            else:
                dead_ip.append(ip.compressed)
                print(f"{ip.compressed} is dead!")
    except Exception as e:
        print(f"{e}\nTry Again Pls")
        pass
    return alive_ip, dead_ip

def syn_scanner(ip, port_list):
    open_ports = []
    print(f"\nScanning ip: {ip}...")
    for port in port_list:
        try:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex((ip,port))
                if result == 0:
                    text=f"{ip}:{port} is open"
                    data = s.recv(1024)
                    print(f"{text} -> {data}")
                    open_ports.append(f"{port} -> {data}")
                s.close()
            except TimeoutError:
                s.close()

        except KeyboardInterrupt:
                print(f"\nExiting")
                s.close()
                exit()
        except socket.error as e:
                s.close()
    return open_ports

def scan_ip(ip_list, port_list):
    data = {}
    for ip in ip_list:
        data[ip] = syn_scanner(ip, port_list)
    return data

def backup(name, data):
    with open(f"{name}.txt","w") as file:
        for ip in data:
            file.write(f"Open Ports On Ip: {ip} ( Format: Port -> Banner )\n")
            for x in data[ip]:
                file.write(f"Port {x}")
                file.write("\n")
            file.write("\n")

def clear_screen():
    try:
        os.getuid()
        subprocess.run("clear",shell=True)
    except AttributeError:
        subprocess.run("cls",shell=True)

def goodbye_screen():
    clear_screen()
    print("------------------------------------------------------------")
    print("|             network scan finished succesfuly             |")
    print("|                                                          |")
    print("| results are in found_by_ping.txt, found_by_syn.txt files |")
    print("|                                                          |")
    print("|     pls check my github: https://github.com/arielkl9     |")
    print("|                                                          |")
    print("|                 thanks for using my tool!                |")
    print("|                                                          |")
    print("|                    press enter to exit                   |")
    print("------------------------------------------------------------")
    input()

def main():
    try:    
        port_list = [22,3389,445,139,80,443]
        alive_ip, dead_ip = ping_loop()
        clear_screen()
        print("Initializing Scan...")
        data = scan_ip(alive_ip, port_list)
        backup("found_by_ping.txt", data)
        data = scan_ip(dead_ip, port_list)
        backup("found_by_syn.txt", data)
    except KeyboardInterrupt:
                print(f"\nExiting")
                exit()
    goodbye_screen()

global alive_ip
global dead_ip
main()
    
    

