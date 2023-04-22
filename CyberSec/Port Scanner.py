import socket

get_target=input("enter IP to scan: ")

try:
    with open('ports.txt','w') as textfile:
        textfile.write(f"The Best Port Scanner In Town!\n\nScanned Host: {get_target}\nPort Range 1-65535\nFormat (port -> banner)\n\nPorts Details:\n\n")
        print(f"The Best Port Scanner In Town!\n\nScanned Host: {get_target}\nPort Range 1-65535\nFormat (port -> banner)\n\nPorts Details:\n")
        for port in range(1,65535):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex((get_target,port))
                
                if result == 0:
                    
                    text=f"port {port} is open"
                    data = s.recv(1024)
                    print(f"{text} -> {data}")
                    textfile.write(f"{text} -> {data}\n")

                s.close()
            except TimeoutError:
                print(f"{text}")
                textfile.write(f"{text}\n")
                s.close()
            
except KeyboardInterrupt:

        print(f"\nExiting")
        s.close()

except socket.error as e:
        print(f"\nServer not responding")
        print(e)
        s.close()
