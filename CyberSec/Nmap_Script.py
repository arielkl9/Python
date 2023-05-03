import nmap3
import requests
import subprocess
import os
import time
import re

def scan(host):
    with open("Scan_Results.txt","w") as file:
        dic = []
        data = nmap.nmap_version_detection(host, args="--script vulners --script-args mincvss+5.0")
        for port in data[f"{host}"]['ports']:
            try:
                hackable = {}
                file.writelines(f"{port['protocol']}:{port['portid']} -> ")
                service = port['service'].keys()      
                for item in service:
                    file.writelines(f"{port['service'][item]} ")
                    hackable[f'{item}'] = port['service'][item]
                hackable['protocol'] = port['protocol']
                hackable['port'] = port['portid']
                hackable['cpe'] = port['cpe'][0]['cpe']
                file.writelines(f"-> {port['cpe'][0]['cpe']}")
            except IndexError or KeyError:
                continue
            file.writelines("\n")
            dic.append(hackable)
    return dic

def check_cve(dic):
    for i in range(len(dic)):
        cpe = dic[i]['cpe'].strip("cpe:/")
        r = requests.get(f'https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=cpe:2.3:{cpe}')
        cve = re.findall("CVE-\d{4}-\d{4,7}",r.text)
        dic[i]['cve'] = cve
        time.sleep(3)
    return dic
            
def log(dic):
    with open("CVE's_Found.txt","w") as file:
        file.writelines("Scan Results:")
        for i in range(len(dic)):
            file.writelines(f"\n\nresult {i+1}:\n")
            keys = dic[i].keys()
            for key in keys:
                if key != 'cve':
                    file.writelines(f"{dic[i][key]} ")
                elif len(dic[i]['cve']) != 0 :
                    file.writelines(f"\n\nCVE's Found For Scan {i+1}:\n\n")
                    for cve in dic[i]['cve']:
                        file.writelines(f'{cve}\n')

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
        print("| results are in CVE's_Found.txt and Scan_Result.txt files |")
        print("|                                                          |")
        print("|     pls check my github: https://github.com/arielkl9     |")
        print("|                                                          |")
        print("|                 thanks for using my tool!                |")
        print("|                                                          |")
        print("|                    press enter to exit                   |")
        print("------------------------------------------------------------")
        input() 

def main():
    global nmap
    global host
    nmap = nmap3.Nmap()
    prints(1)
    host = input("Enter Ip To Scan: ")
    dic = check_cve(scan(host))
    log(dic)
    prints(2)
    
main()