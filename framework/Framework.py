import Misc
import Recon
import Scan
import Dirs

class MenusRecon:
    def print_menu_recon():
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

    def menu_recon():
        while True:
            Misc.Misc.clear_screen()
            MenusRecon.print_menu_recon()
            try:
                choice = int(input())
                if 1 <= choice <= 3:
                    Misc.Misc.clear_screen()
                    return choice
                elif choice == 4:
                    Misc.Misc.clear_screen()
                    print("\nThanks For Using My Recon Tool!\n")
                    exit()
                else:
                    print("\nUnvalid Choice Try Again\n")
                    input("Press Enter To Continue...\n")
                    Misc.Misc.clear_screen()
                    pass
            except ValueError:
                print("\nNumbers Only!! Try Again\n")
                input("Press Enter To Continue...\n")
                Misc.Misc.clear_screen()
                pass
            
    def main_recon():
        try:
            choise = MenusRecon.menu_recon()
            path = Misc.Misc.make_dir("Recon")
            Recon.Recon.init_scanner(choise, path)
            input("\npress enter to exit")
        except KeyboardInterrupt:
            Misc.Misc.clear_screen()
            print(f"\nBye See You Never :D\n")

# This class manages the menu
# 
# vars - None
# 
# funcs - main_menu, socket_scan
# 
# input - None
# 
# output - None

class MenusScan:
       
    def main_menu():
        Misc.Misc.clear_screen()
        print("Welcome To My Scan & Enum Framework\n")
        print("1. Scan with ARP & Nmap (Require Nmap installed)\n")
        print("2. Scan with ARP & Socket (No requirements)\n")
        choise = input("Please choose your option: ")
        if choise == '1':
            MenusScan.nmap_scan()
        elif choise == '2':
            MenusScan.socket_scan()
        else:
            Misc.Misc.clear_screen()
            print("Bad Input!!! Exiting")
            exit()

    def nmap_scan():
        Misc.Misc.clear_screen()
        print("Yay!! we going the easy way!!\n")
        Scan.ScanInit.print_res(Scan.ScanInit.arp_nmap())

    def socket_scan():
        Misc.Misc.clear_screen()
        print("why people insist to go the hard way... anyways...\n")
        print("What scan you want to use?\n")
        print("1. Fast scan - scans only common ports\n")
        print("2. Full scan - scans ALL ports (might take some time)\n")
        choise = input("Please choose your option: ")
        if choise == '1':
            Scan.ScanInit.print_res(Scan.ScanInit.arp_socket("fast"))
        elif choise == '2':
            Scan.ScanInit.print_res(Scan.ScanInit.arp_socket("full"))
        else:
            Misc.Misc.clear_screen()
            print("Bad Input!!! Exiting")
            exit()

class BruteForceMenus:
    def dir_buster_menu():
        Misc.Misc.clear_screen()
        print("Example: http://127.0.0.1 , https://google.com\n")
        domain = input("Enter Domain/IP To Scan: ")
        Dirs.MyDirBuster.my_dir_buster(domain)

class main():
    while True:
        Misc.Misc.clear_screen()
        print("Welcome To My Framework!!\n")
        print("This Program Is Still In Development\n")
        print("Please Choose Module:\n")
        print("1. Recon Module\n")
        print("2. Scan Module\n")
        print("3. My Web Dir BF! - New")
        choise = input()
        if choise == '1':
            MenusRecon.main_recon()
            break
        if choise == '2':
            MenusScan.main_menu()
            break
        if choise == '3':
            BruteForceMenus.dir_buster_menu()
            break
            

main()
