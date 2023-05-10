import nmap3
import requests
import subprocess
import os
import time
import re
import ipaddress

def scan(host):
    clear_screen()
    print(f"\nScannning {host}...\n")
    dic = []
    readable_format = []
    data = nmap.nmap_version_detection(host, args="--script vulners --script-args mincvss+5.0")
    if data[f"{host}"]['ports']:
        scan_res.writelines(f"\nScan Result For {host}:\n")
        for port in data[f"{host}"]['ports']:
            try:
                hackable = {}
                text = ""
                scan_res.writelines(f"Protocol -> {port['protocol']} | Port -> {port['portid']} | Service Data -> ")
                text += f"Protocol -> {port['protocol']} | Port -> {port['portid']} | Service Data -> "
                service = port['service'].keys()      
                for item in service:
                    scan_res.writelines(f"{port['service'][item]} ")
                    text += f"{port['service'][item]} "
                    hackable[f'{item}'] = port['service'][item]
                hackable['protocol'] = port['protocol']
                hackable['port'] = port['portid']
                hackable['cpe'] = port['cpe'][0]['cpe']
                scan_res.writelines(f" | CPE -> {port['cpe'][0]['cpe']}")
                text += f" | CPE -> {port['cpe'][0]['cpe']}"
            except IndexError or KeyError:
                scan_res.writelines("\n")
                continue
            scan_res.writelines("\n")
            readable_format.append(text)
            dic.append(hackable)
        return (dic ,readable_format)
    else:
        return (0, "")

def check_cve(dic,readable_format):
    if dic:
        print("Host Alive!\n")
        print("Checking CVE's...\n")
        for i in range(len(dic)):
            cpe = dic[i]['cpe'].strip("cpe:/")
            r = requests.get(f'https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=cpe:2.3:{cpe}')
            cve = re.findall("CVE-\d{4}-\d{4,7}",r.text)
            dic[i]['cve'] = set(cve)
            time.sleep(8)
        return (dic , readable_format)
    else:
        return (0 , "")
            
def log(dic,ip,readable_format):
    cve_file.writelines(f"\nScan Results For Ip - {ip}:\n")
    for i in range(len(dic)):
        cve_file.writelines(f"\nResult {i+1}:\n\n")
        cve_file.writelines(f"{readable_format[i]}\n")
        if dic[i]['cve']:
            cve_file.writelines(f"\nCVE's Found:\n\n")
            for cve in dic[i]['cve']:
                if cve:
                    cve_file.writelines(f'{cve}\n')
        else:
            cve_file.writelines(f"\nNo CVE's Found\n\n")
                

def clear_screen():
    try:
        os.getuid()
        subprocess.run("clear",shell=True)
    except AttributeError:
        subprocess.run("cls",shell=True)

def prints(num):
    if num == 1:
        clear_screen()
        print("Welcome To My Tool\n\nFormat - Enter Ip And Watch The Magic Happend!")
        print("Note: Results Are Saved At The End And Wont Be Printed!\n\n")
    if num == 2:
        clear_screen()
        print("------------------------------------------------------------")
        print("|                CVE Scan Ended successfuly                |")
        print("|                                                          |")
        print("| results are in CVE's_Found.txt and Open_Ports.txt files  |")
        print("|                                                          |")
        print("|     pls check my github: https://github.com/arielkl9     |")
        print("|                                                          |")
        print("|                 thanks for using my tool!                |")
        print("|                                                          |")
        print("|                    press enter to exit                   |")
        print("------------------------------------------------------------")
        input() 
    if num == 3:
        print("\nLeaving So Soon?\n")

def define_globals():
    global nmap
    global cve_file
    global scan_res
    nmap = nmap3.Nmap()
    cve_file = open("CVE's_Found.txt","w")
    scan_res = open("Open_Ports.txt","w")

def close_files():
    cve_file.close()
    scan_res.close()

def scan_managment():
    hosts = ipaddress.IPv4Network(input("Enter Network To Scan (Format CIDR -> X.X.X.X/X): "))
    for ip in hosts:
        dic, readable_format = scan(ip.compressed)
        check_cve(dic, readable_format)
        if dic:
            log(dic,ip.compressed,readable_format)

def main():
    try:
        prints(1)
        define_globals()
        scan_managment()
        prints(2)
        close_files()
    except KeyboardInterrupt:
        clear_screen()
        prints(3)
        close_files()

    
main()
