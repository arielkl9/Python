from scapy.all import ARP, Ether, srp
import ipaddress
import subprocess
import os

def arp_conf():
    while True:
        try:
            clear_screen()
            get_input = input("pls enter ip range (CIDR Format: x.x.x.x/x): ")
            ip_range = ipaddress.ip_network(get_input)
            arp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_range.compressed)
            return arp_request
        except ValueError or AttributeError:
            continue

def scan():
    arp_request = arp_conf()
    answer, unanswered = srp(arp_request, timeout=2)
    return answer
        
def data_managment():
        answer = scan()
        for snd, rcv in answer:
            host = {
                'ip' : rcv.sprintf('%ARP.psrc%'),
                'mac' : rcv.sprintf('%Ether.src%')
                }
            alive_hosts.append(host)

def log():
    with open("log.txt","w") as file:
        file.write(f"Scan Result: \n\nAlive Hosts: \n")
        for i in range(len(alive_hosts)):
            file.write(f"{alive_hosts[i]['ip']} - {alive_hosts[i]['mac']}\n")

def clear_screen():
    try:
        os.getuid()
        subprocess.run("clear",shell=True)
    except AttributeError:
        subprocess.run("cls",shell=True)

def goodbye_screen():
    clear_screen()
    print("----------------------------------------------------")
    print("|           arp scan finished succesfuly           |")
    print("|                                                  |")
    print("|             log is in log.txt file               |")
    print("|                                                  |")
    print("| pls check my github: https://github.com/arielkl9 |")
    print("|                                                  |")
    print("|            thanks for using my tool!             |")
    print("|                                                  |")
    print("|               press enter to exit                |")
    print("----------------------------------------------------")
    input()

def main():
    global alive_hosts
    alive_hosts = []
    data_managment()
    log()
    goodbye_screen()


main()
