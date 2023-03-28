import socket

HOST = '192.168.2.27'
open_ports = []

for port in range(20,30):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        socket.setdefaulttimeout(1)
        print(f"{HOST}:{port}", end="\r")
        status_code = client_socket.connect_ex((HOST, port))
        if status_code == 0:
            open_ports.append(port)
            data = client_socket.recv(1024)
            print(data.decode("utf-8"))
        client_socket.close()
        
for port in open_ports:
    print(f"\n{port}")