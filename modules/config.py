from modules.variables import Checker
from modules.functions import *
from os import makedirs
from json import load, dump

default = {"proxy_type":"http","proxy_timeout":5,"threads":200,"retries":1,"print_mode":"cui",'solver_service':'2captcha','api_key':''}

def load_config():
    """Load the config values"""
    while 1:
        try:
            with open("Data/config.json","r") as file: data = load(file)
            Checker.proxy_type = str(data["proxy_type"]).lower()
            Checker.retries = int(data["retries"])
            Checker.timeout = int(data["proxy_timeout"])
            Checker.threads = int(data["threads"])
            Checker.solver_serice = str(data["solver_service"]).lower()
            Checker.api_key = str(data["api_key"])
            cui = str(data["print_mode"]).lower()
            if Checker.threads <= 0: Checker.threads = 1
            if Checker.proxy_type not in ("http","socks4","socks5","none"): raise
            if Checker.solver_serice not in ('2captcha','anycaptcha','anticaptcha'): raise
            if cui not in ("log","cui"): raise
            Checker.cui = False if cui == "log" else True
            break
        except:
            makedirs("Data",exist_ok=True)
            with open("Data/config.json","w") as file: dump(default,file,indent=4)

def update_config(values:dict):
    """Update the config values"""
    makedirs("Data",exist_ok=True)
    with open("Data/config.json","w") as file: dump(values,file,indent=4)

def change(option:str):
    """
    Change a value in the config file
    change("threads")
    """
    values = {"proxy_type":Checker.proxy_type,"proxy_timeout":Checker.timeout,"threads":Checker.threads,"retries":Checker.retries,"print_mode":"cui" if Checker.cui else "log",'solver_service':Checker.solver_serice,'api_key':Checker.api_key}
    clear()
    ascii()
    print("\n\n")
    match option:
        case "proxy_type":
            match Checker.proxy_type:
                case "socks4": Checker.proxy_type = "socks5"
                case "socks5": Checker.proxy_type = "http"
                case "http": Checker.proxy_type = "none"
                case _: Checker.proxy_type = "socks4"
            values["proxy_type"] = Checker.proxy_type
            update_config(values)
        case "proxy_timeout":
            print(f"    [{cyan}>{reset}] Pick proxy timeout")
            print("\n")
            timeout = input(f"    [{cyan}>{reset}] ")
            if not timeout.isdigit(): return
            if int(timeout) <= 0: timeout = 1
            Checker.timeout = int(timeout)
            values["proxy_timeout"] = Checker.timeout
            update_config(values)
        case "retries":
            print(f"    [{cyan}>{reset}] Pick max request retries")
            print("\n")
            retries = input(f"    [{cyan}>{reset}] ")
            if not retries.isdigit(): return
            if int(retries) <= 0: retries = 1
            Checker.retries = int(retries)
            values["retries"] = Checker.retries
            update_config(values)
        case "print":
            match Checker.cui:
                case False: Checker.cui = True
                case _: Checker.cui = False
            values["print_mode"] = "cui" if Checker.cui else "log"
            update_config(values)
        case "threads":
            print(f"    [{cyan}>{reset}] Pick ammount of threads")
            print("\n")
            threads = input(f"    [{cyan}>{reset}] ")
            if not threads.isdigit(): return
            if int(threads) <= 0: threads = 0
            Checker.threads = threads
            values["threads"] = threads
            update_config(values)
        case 'solver_service':
            match Checker.solver_serice:
                case '2captcha': Checker.solver_serice = 'anticaptcha'
                case 'anticaptcha': Checker.solver_serice = 'anycaptcha'
                case _: Checker.solver_serice = '2captcha'
            values['solver_service'] = Checker.solver_serice
            update_config(values)
        case 'api_key':
            print(f"    [{cyan}>{reset}] Input API key")
            print(f"    [{cyan}>{reset}] Enter nothing to disable")
            print("\n")
            api_key = input(f"    [{cyan}>{reset}] ")
            values["api_key"] = api_key
            update_config(values)