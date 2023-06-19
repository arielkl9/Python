import urllib.request
import os
import Misc

class MyDirBuster:
    def my_dir_buster(domain): 
        path = Misc.Misc.make_dir("Dirs")
        with open(f"{os.getcwd()}/Lists/dirs.txt","r") as file:
            with open(f"{path}/dirs.txt","w") as res:
                print("Running Dir Brute Force Abuse...\n")
                res.writelines("Running Dir Brute Force Abuse...\n\n")
                print(f"Using List: {os.getcwd()}/Lists/dirs.txt\n")
                res.writelines(f"Using List: {os.getcwd()}/Lists/dirs.txt\n")
                for line in file:
                    try:
                        line = line.strip("\n")
                        code = urllib.request.urlopen(f'{domain}/{line}').getcode()
                        print(f"[+] {domain}/{line} CODE: {code}")
                        res.writelines(f"[+] {domain}/{line} CODE: {code}\n")
                    except Exception:
                        pass

