import whois
import dns.resolver
import requests
import Misc
import os

class Recon:
    def who_is(website, path):
        with open(f"{path}/Whois.txt","w") as whoisfile:
            print("Initializing Whois Scan...\n")
            whoisfile.write("\nWhois Scan Results:\n\n")
            try:
                os.getuid()
                whoisresult = whois.query(website)
                for i in whoisresult.__dict__.keys():
                    whoisfile.writelines(f"{str(i)}:\n")
                    whoisfile.writelines(f"{str(whoisresult.__dict__[i])}\n\n")
                    print(f"{str(i)}:")
                    print(f"{str(whoisresult.__dict__[i])}\n")
                
            except AttributeError:
                whoisresult = whois.whois(website)
                whoisfile.write(str(whoisresult))
                print(f"{whoisresult}\n")

    def dns_enum(website, path):
        with open(f"{path}/DNS_Enum.txt","w") as dnsenumfile:
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

    def subdomains(website, path):
        with open(f"{path}/Subdomains.txt","w") as subdomainsfile:
            with open(f"Recon/subdomains.txt","r") as listfile:
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

    def init_scanner(choise, path):
        website = input("\nEnter A Domain To Scan: ")
        Misc.Misc.clear_screen()
        print("\n")
        if choise == 1:
            Misc.Misc.clear_screen()
            Recon.who_is(website, path)
            Recon.dns_enum(website, path)
        elif choise == 2:
            Misc.Misc.clear_screen()
            Recon.subdomains(website, path)
        else:
            Misc.Misc.clear_screen()
            Recon.who_is(website, path)
            Recon.dns_enum(website, path)  
            Recon.subdomains(website, path)

