import os
import subprocess
from typing import Any
import nmap3
import socket
from scapy.all import ARP, Ether, srp

# This class is a template for IP obj
# 
# vars - ip, mac, subnet, services
# 
# funcs - print_res
# 
# input - ip : str, mac : str
# 
# output - None

class IpAddress:
    def __init__(self, ip, mac):
        self.ip = ip
        self.mac = mac
        self.subnet = ""
        self.services = []
    def print_res(self):
        print(f"Results for IP: {self.ip}, MAC: {self.mac}\n")
        print(self.services)

# This class manages the menu
# 
# vars - None
# 
# funcs - main_menu, socket_scan
# 
# input - None
# 
# output - None

class menu:
    def __init__(self):
        self.main_menu()
        
    def main_menu(self):
        Misc.clear_screen()
        print("Welcome To My Scan & Enum Framework\n")
        print("1. Scan with ARP & Nmap (Require Nmap installed)\n")
        print("2. Scan with ARP & Socket (No requirements)\n")
        choise = input("Please choose your option: ")
        if choise == '1':
            self.nmap_scan()
        elif choise == '2':
            self.socket_scan()
        else:
            Misc.clear_screen()
            print("Bad Input!!! Exiting")
            exit()

    def nmap_scan(self):
        Misc.clear_screen()
        print("Yay!! we going the easy way!!\n")
        ScanInit.print_res(ScanInit.arp_nmap())

    def socket_scan(self):
        Misc.clear_screen()
        print("why people insist to go the hard way... anyways...\n")
        print("What scan you want to use?\n")
        print("1. Fast scan - scans only common ports\n")
        print("2. Full scan - scans ALL ports (might take some time)\n")
        choise = input("Please choose your option: ")
        if choise == '1':
            ScanInit.print_res(ScanInit.arp_socket("fast"))
        elif choise == '2':
            ScanInit.print_res(ScanInit.arp_socket("full"))
        else:
            Misc.clear_screen()
            print("Bad Input!!! Exiting")
            exit()

# This class manages and starts all scans
# 
# vars - None
# 
# funcs - arp_nmap, arp_socket, custom_nmap, custom_socket
# 
# input - None
# 
# output - object_list : list

class ScanInit:
    def arp_nmap():
        Misc.clear_screen()
        ip_network = input("Enter network ip (CIDR Format): ")
        ip_subnet = input("Enter prefix (CIDR Format): ")
        arp_scan = ArpScan(ip_network, ip_subnet)
        ip_address_obj = []
        for res in arp_scan.res:
            ip_address_obj.append(IpAddress(res['ip_address'], res['mac_address']))
        for obj in ip_address_obj:
            print(f"scan: {obj.ip}", end="\r")
            for res in NmapScan(obj.ip).res:
                obj.services.append(res)
        return ip_address_obj
    
    def arp_socket(type):
        Misc.clear_screen()
        ip_network = input("Enter network ip (CIDR Format): ")
        ip_subnet = input("Enter prefix (CIDR Format): ")
        arp_scan = ArpScan(ip_network, ip_subnet)
        ip_address_obj = []
        for res in arp_scan.res:
            ip_address_obj.append(IpAddress(res['ip_address'], res['mac_address']))
        for obj in ip_address_obj:
            print(f"scan: {obj.ip}", end="\r")
            for res in TcpScan(obj.ip,type).res:
                obj.services.append(res)
        return ip_address_obj

    def print_res(ip_address_obj):
        Misc.clear_screen()
        for index,i in enumerate(ip_address_obj):
            print(f"\n\nResult {index + 1}:\n")
            print(f"ip: {i.ip}\nmac: {i.mac}\n")
            print(f"services:\n")
            for service in i.services:
                for key in service.keys():
                    print(f"{key} - {service[key]}")
                print("")



# This class gets an IPv4 network and perform 
# a arp scan using scappy 
# 
# vars - ip_network : str, ip_subnet : str, res : list
# 
# funcs - run_arp_scan
# 
# input - IPv4 network, IPv4 subnet (CIDR -> /X)
# 
# output - res = list of alive ip addresses + mac addresses

class ArpScan:
    def __init__(self, ip_network, ip_subnet):
        self.ip_network = ip_network
        self.ip_subnet = ip_subnet
        self.res = self.run_arp_scan()

    def run_arp_scan(self):
        ip_address_list = []
        arp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=f'{self.ip_network}/{self.ip_subnet}')
        answer, unanswered = srp(arp_request, timeout=2)
        for snd, rcv in answer:
            host = {
                'ip_address' : rcv.sprintf('%ARP.psrc%'),
                'mac_address' : rcv.sprintf('%Ether.src%')
                }
            ip_address_list.append(host)
        return ip_address_list

# This class gets an IPv4 address and perform 
# a tcp scan using socket (no need for nmap to be installed) 
# 
# vars - ipv4 : str, scan_type : str, res : list
# 
# funcs - FastScan, AllPortsScan
# 
# input - IPv4 Address, scan type
# 
# output - res = list of dict : [port : '', service : '']

class TcpScan:
    def __init__(self, ip, type):
        self.ip = ip
        if type == "fast":
            self.res = self.fast_scan()
        elif type == "full":
            self.res = self.full_scan()
        else:
            Misc.clear_screen()
            print("IDK HOW THIS CAN HAPPEN")
            exit()

    def fast_scan(self):
        top_ports = [21,22,23,25,53,80,110,143,443,445,3389,5900,8080,8443,3306,5432,6379]
        open_ports = []
        for port in top_ports:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    result = s.connect_ex((self.ip,port))
                    
                    if result == 0:
                        banner = s.recv(1024)
                        open_ports.append({"port":f"{port}","service":f"{banner}"})
                    s.close()
                except TimeoutError:
                    open_ports.append({"port":f"{port}","service":""})
                    s.close()
                except socket.timeout:
                    open_ports.append({"port":f"{port}","service":""})
                    s.close()
        return open_ports
        

    def full_scan(self):
        open_ports = []
        for port in range(1,65535):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    result = s.connect_ex((self.ip,port))
                    if result == 0:
                        banner = s.recv(1024)
                        open_ports.append({"port":f"{port}","service":f"{banner}"})
                    s.close()
                except TimeoutError:
                    open_ports.append({"port":f"{port}","service":""})
                    s.close()
        return open_ports


# This class gets an IPv4 address and perform 
# a Nmap version scan and put answer in self.res
# 
# vars - ip : str, res : list
# 
# funcs - ver_scan
# 
# input - IPv4 Address
# 
# output - res = dictionary : port, name, service
# 

class NmapScan:
    def __init__(self, ip):
        self.ip = ip
        self.res = self.version_scan()

    def version_scan(self):
        nmap = nmap3.Nmap()
        results = nmap.nmap_version_detection(self.ip) #, args="-F")
        detected_services = []
        for open_port in results[self.ip]["ports"]:
            try:
                port_data = {
                    "port" : open_port['portid'],
                    "name" : open_port['service']['name'],
                    "service" : f"{open_port['service']['product']}{open_port['service']['version']}"
                }
                detected_services.append(port_data)
            except KeyError:
                continue
        return detected_services

class ServiceEnum:
    ...

# This class perform misc tasks
# 
# vars - None
# 
# funcs - clear_screen
# 
# input - None
# 
# output - None

class Misc:
    def clear_screen():
        try:
            os.getuid()
            subprocess.run("clear",shell=True)
        except AttributeError:
            subprocess.run("cls",shell=True)

class main:
    menu()

if __name__ == "__main__":
    main()  