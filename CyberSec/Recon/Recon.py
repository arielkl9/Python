import os
import whois
import dns.resolver
import requests

def makedir():
    try:
        os.mkdir("ReconResults")
    except Exception:
        pass

def usewhois(website):
    with open("ReconResults/Whois.txt","w") as whoisfile:
        print("Initializing Whois Scan...\n")
        whoisfile.write("Whois Scan Results:\n\n")
        whoisresult = whois.whois(website)
        whoisfile.write(str(whoisresult))
        print(f"{whoisresult}\n")


def dnsenum(website):
    with open("ReconResults/DNS_Enum.txt","w") as dnsenumfile:
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

def subdomains(website):
    with open("ReconResults/Subdomains.txt","w") as subdomainsfile:
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

def main():
    try:
        website = input("enter a domain to recon ")
        makedir()
        usewhois(website)
        dnsenum(website)
        subdomains(website)
        print(f"\nThanks For Using My Recon Tool!\n")
    except KeyboardInterrupt:
        print(f"\nWhy Leave So Soon? :c\n")

main()