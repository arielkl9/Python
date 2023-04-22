import os
import whois
import dns.resolver
import requests
import subprocess
import datetime

def print_menu():
    print("\n               Welcome To My Recon Tool                 \n")
    print("**********************************************************\n")
    print("|                                                        |\n")
    print("|    Options:                                            |\n")
    print("|    [1] Passive Scan ( Whois Check + DNS Enumeration )  |\n")
    print("|    [2] Active Scan ( Subdomains BF Scan )              |\n")
    print("|    [3] Full Scan ( Passive + Active Option )           |\n")
    print("|    [4] Exit Program                                    |\n")
    print("|                                                        |\n")
    print("**********************************************************\n")

def menu():
    while True:
        clear_screen()
        print_menu()
        try:
            choice = int(input())
            if 1 <= choice <= 3:
                clear_screen()
                return choice
            elif choice == 4:
                clear_screen()
                print("\nThanks For Using My Recon Tool!\n")
                exit()
            else:
                print("\nUnvalid Choice Try Again\n")
                input("Press Enter To Continue...\n")
                clear_screen()
                pass
        except ValueError:
            print("\nNumbers Only!! Try Again\n")
            input("Press Enter To Continue...\n")
            clear_screen()
            pass

def make_dir():
    try:
        time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        path = f"ReconResults/{time}"
        os.makedirs(path,exist_ok=True)
        return time
    except Exception:
        clear_screen()
        print("Error:\n")
        print("Creating Folders Failed!\n")
        print("Press Enter To Exit...\n")
        input()
        exit()

def who_is(website, time):
    with open(f"ReconResults/{time}/Whois.txt","w") as whoisfile:
        print("Initializing Whois Scan...\n")
        whoisfile.write("\nWhois Scan Results:\n\n")
        whoisresult = whois.whois(website)
        whoisfile.write(str(whoisresult))
        print(f"{whoisresult}\n")


def dns_enum(website, time):
    with open(f"ReconResults/{time}/DNS_Enum.txt","w") as dnsenumfile:
        print("Initializing DNS Enumeration...\n")
        dnsenumfile.write("DNS Enumeration Results:\n\n")
        record_types = ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT"]
        resolver = dns.resolver.Resolver()
        for record_type in record_types:
            try:
                answers = resolver.resolve(website, record_type)
            except dns.resolver.NoAnswer:
                continue
            print(f"{record_type} records for {website}:")
            dnsenumfile.write(f"{record_type} records for {website}:\n")
            for record in answers:
                print(f"    {record}")
                dnsenumfile.write(f"    {record}\n")
        print("\n")

def subdomains(website, time):
    with open(f"ReconResults/{time}/Subdomains.txt","w") as subdomainsfile:
        with open("list.txt","r") as listfile:
            print("Initializing Subdomain Bruteforce...\n")
            subdomainsfile.write("Subdomain Bruteforce Results:\n\n")
            content = listfile.read()
            subdomains = content.splitlines()
            discovered_subdomains = []
            for subdomain in subdomains:
                url = f"https://{subdomain}.{website}"
                try:
                    requests.get(url)
                except requests.ConnectionError:
                    pass
                else:
                    print(f"[+] Discovered subdomain: {url}")
                    subdomainsfile.write(f"[+] Discovered subdomain: {url}\n")
                    discovered_subdomains.append(url)

def init_scanner(choise, time):
    website = input("\nEnter A Domain To Scan: ")
    clear_screen()
    print("\n")
    if choise == 1:
        clear_screen()
        who_is(website, time)
        dns_enum(website, time)
    elif choise == 2:
        clear_screen()
        subdomains(website, time)
    else:
        clear_screen()
        who_is(website, time)
        dns_enum(website, time)  
        subdomains(website, time)
        
def clear_screen():
    try:
        os.getuid()
        subprocess.run("clear",shell=True)
    except AttributeError:
        subprocess.run("cls",shell=True)

def main():
    try:
        while True:
            choise = menu()
            time = make_dir()
            init_scanner(choise, time)
            input("\nPress Enter To Reset...\n")
    except KeyboardInterrupt:
        clear_screen()
        print(f"\nBye See You Never :D\n")

main()