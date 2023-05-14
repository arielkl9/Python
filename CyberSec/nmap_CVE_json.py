import nmap3
import requests
import subprocess
import os
import time
import re
import ipaddress
import json

def prints(num):
    if num == 1:
        clear_screen()
        print("Welcome To My Tool\n\nFormat - Enter Ip And Watch The Magic Happend!")
        print("Note: Results Are Saved At The End And Wont Be Printed!\n")
    if num == 2:
        clear_screen()
        print("------------------------------------------------------------")
        print("|                CVE Scan Ended successfuly                |")
        print("|                                                          |")
        print("|              results are in results folder               |")
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

def set_globals():
    global nmap 
    global nmap_array

    nmap = nmap3.Nmap()
    nmap_array = []

    global nmap_file
    global json_file
    global cve_file
    global scan_file  
    
    nmap_file = open("results/nmap_scan.json","w")
    json_file = open("results/results.json","w")
    cve_file = open("results/CVE's_found.txt","w")
    scan_file = open("results/readable.txt","w")

def get_hosts():
    while True:
        try:
            prints(1)
            hosts = ipaddress.IPv4Network(input("Enter Network To Scan (Format CIDR -> X.X.X.X/X): "))
            break
        except Exception:
            clear_screen()
            continue
    return hosts

def scan_managment():
    hosts = get_hosts()
    json_data = {}
    for ip in hosts:
        dic, readable_format = scan(ip.compressed)
        if dic:
            dic = check_cve(dic)
            json_data[f'{ip}'] = log(ip.compressed,readable_format, dic)
    json_file.writelines(json.dumps(json_data,indent=2))

def scan(host):
    clear_screen()
    print(f"\nScannning {host}...\n")
    dic = {}
    readable_format = []
    data = nmap.nmap_version_detection(host)
    if data[f"{host}"]['ports']:
        dic = data[f"{host}"]['ports']
        nmap_array.append(data)
        scan_file.writelines(f"\nScan Result For {host}:\n")
        for port in data[f"{host}"]['ports']:
            try:
                text = ""
                text += f"Protocol -> {port['protocol']} | Port -> {port['portid']} | Service Data -> "
                service = port['service'].keys()      
                for item in service:
                    text += f"{port['service'][item]} "
                text += f" | CPE -> {port['cpe'][0]['cpe']}"
            except IndexError or KeyError as e:
                text = ""
                text += f"Protocol -> {port['protocol']} | Port -> {port['portid']} | Service Data -> "
                service = port['service'].keys()      
                for item in service:
                    text += f"{port['service'][item]} "
                pass
            scan_file.writelines(f"{text}\n")
            readable_format.append(text)
        return (dic ,readable_format)
    else:
        return (0, "")

def check_cve(dic):
    if dic:
        print("Host Alive!\n")
        print("Checking CVE's...\n")
        print("Using API May Take Some Time...\n")
        for i in range(len(dic)):
            try:
                for item in dic[i]['cpe']:
                    cve_list = []
                    cpe = item['cpe'].strip("cpe:/")
                    r = requests.get(f'https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=cpe:2.3:{cpe}')
                    cve = re.findall("CVE-\d{4}-\d{4,7}",r.text)
                    if cve:
                        cve = set(cve)
                        for x in cve:
                            cve_list.append(x)
                        dic[i]['cve'] = sorted(cve_list, reverse=True)
                    time.sleep(6)
            except KeyError:
                continue
        return (dic)
    else:
        return (0)

def log(ip,readable_format,dic):
    nmap_file.writelines(json.dumps(nmap_array,indent=2))
    cve_file.writelines(f"\nScan Results For Ip - {ip}:\n")
    for i in range(len(dic)):
        cve_file.writelines("--------------------------------------------------------------------------------------------------------\n")
        cve_file.writelines(f"\n\tResult {i+1}:\n\n")
        cve_file.writelines(f"\t\t{readable_format[i]}\n")
        try:
            if dic[i]['cve']:
                cve_file.writelines(f"\n\t\t\tCVE's Found:\n\n")
                for cve in dic[i]['cve']:
                    if cve:
                        cve_file.writelines(f'\t\t\t\t{cve}\n')   
            else:
                cve_file.writelines(f"\t\t\tNo CVE's Found\n\n")
        except KeyError:
            cve_file.writelines(f"\t\t\tNo CVE's Found\n\n")
    cve_file.writelines("--------------------------------------------------------------------------------------------------------\n")
    return dic

def close_files():
    nmap_file.close()
    json_file.close()
    cve_file.close()
    scan_file.close()

def clear_screen():
    try:
        os.getuid()
        subprocess.run("clear",shell=True)
    except AttributeError:
        subprocess.run("cls",shell=True)

def main():
    try:
        os.makedirs('results', exist_ok=True)
        set_globals()
        scan_managment()
        close_files()
        prints(2)
        
    except KeyboardInterrupt:
        clear_screen()
        close_files()
        prints(3)
        

    
main()
