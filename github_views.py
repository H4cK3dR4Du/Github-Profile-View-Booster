import json
import time
import os
import random
import string
import ctypes

try:
    import pystyle
    import colored
    import requests
    import tls_client
    import threading
    import httpx
    import datetime
except ModuleNotFoundError:
    os.system('pip install pystyle')
    os.system('pip install colored')
    os.system('pip install requests')
    os.system('pip install tls_client')
    os.system('pip install threading')
    os.system('pip install httpx')
    os.system('pip install datetime')

from colored import fg
from pystyle import Write, System, Colors, Colorate
from tls_client import Session
from string import digits

lock = threading.Lock()
proxy_count = len(open('proxies.txt').readlines())
blue = fg(6)
reset = fg(7)
red = fg(1)
green = fg(2)
purple = fg(5)
pink = fg(216)
yellow = fg(226)
gray = fg(250)
views_sent = 0

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def save_proxies(proxies):
    with open("proxies.txt", "w") as file:
        file.write("\n".join(proxies))

def get_proxies():
    with open('proxies.txt', 'r', encoding='utf-8') as f:
        proxies = f.read().splitlines()
    if not proxies:
        proxy_log = {}
    else:
        proxy = random.choice(proxies)
        proxy_log = {
            "http://": f"http://{proxy}", "https://": f"http://{proxy}"
        }
    try:
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
        time_rn = get_time_rn()
        response = httpx.get(url, proxies=proxy_log, timeout=60)

        if response.status_code == 200:
            proxies = response.text.splitlines()
            save_proxies(proxies)
            print(f"{reset}{time_rn} {pink}| {reset}[ {pink}Proxy-Worker{reset} ] Success {purple}>{green} Scrapped Proxies {reset}[{pink} Total : {len(proxies)} {reset}]")
        else:
            print(f"{reset}{time_rn} {pink}| {reset}[ {pink}Proxy-Worker{reset} ] Error {purple}>{red} Failed Getting Proxies...")
            time.sleep(3)
            get_proxies()
    except httpx.ProxyError:
        pass
    except httpx.ReadError:
        pass
    except httpx.ConnectTimeout:
        pass
    except httpx.ReadTimeout:
        pass
    except httpx.ConnectError:
        pass
    except httpx.ProtocolError:
        pass

def check_proxy_count():
    with open("proxies.txt", "r") as file:
        lines = file.readlines()
        proxy_count = len(lines)
        time_rn = get_time_rn()
        if proxy_count < 105:
            print(f"{reset}{time_rn} {pink}| {reset}[ {pink}Proxy-Worker{reset} ] Warning {purple}>{yellow} You're close to running out of proxies.")
            print(f"{reset}{time_rn} {pink}| {reset}[ {pink}Proxy-Worker{reset} ] Re-Fill {purple}>{yellow} Filling proxies.txt with fresh and new proxies...")
            time.sleep(1.5)
            get_proxies()
        else:
            pass

def view_booster():
    check_proxy_count()
    thread_name = threading.currentThread().getName()
    with open("config.json") as f:
        data = json.load(f)
        github_link = data.get('github_link')
    global views_sent
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW(f'Github Profile View Booster | By H4cK3dR4Du#0001 | Views Sent : {views_sent}')
        date = datetime.datetime.now()
        hour = date.hour
        minute = date.minute
        second = date.second
        time_rn = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
        with open('proxies.txt', 'r', encoding='utf-8') as f:
            proxies = f.read().splitlines()
        if not proxies:
            print(f"{reset}{time_rn} {pink}| {reset}[ {pink}{thread_name}{reset} ] Error {purple}>{red} No Proxy Found!")
            proxy_log = {}
        else:
            proxy = random.choice(proxies)
            proxy_log = {
                "http://": f"http://{proxy}", "https://": f"http://{proxy}"
            }
            print(f"{reset}{time_rn} {pink}| {reset}[ {pink}{thread_name}{reset} ] Loaded Proxy {purple}>{reset} {proxy}")
        try:
            response = httpx.get(github_link, proxies=proxy_log, timeout=20)
            if response.status_code == 200:
                date = datetime.datetime.now()
                hour = date.hour
                minute = date.minute
                second = date.second
                time_rn = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
                views_sent += 1
                print(f"{reset}{time_rn} {pink}| {reset}[ {pink}{thread_name}{reset} ] Success {purple}>{green} Sent View {reset}[{pink} Total : {views_sent} {reset}]")
            else:
                print(f"{reset}{time_rn} {pink}| {reset}[ {pink}{thread_name}{reset} ] Error {purple}>{red} Bad Gateaway 502")
        except httpx.ProxyError:
            print(f"{reset}{time_rn} {pink}| {reset}[ {pink}{thread_name}{reset} ] Bad Proxy {purple}> {red}{proxy} {reset}| [{pink}REMOVED{reset}]")
            with open('proxies.txt', 'r') as f:
                lines = f.readlines()
            with open('proxies.txt', 'w') as f:
                for line in lines:
                    if proxy not in line:
                        f.write(line)
        except httpx.ReadError:
            continue
        except httpx.ConnectTimeout:
            continue
        except httpx.ReadTimeout:
            continue
        except httpx.ConnectError:
            continue
        except httpx.ProtocolError:
            continue
        except ValueError:
            print(f"{reset}{time_rn} {pink}| {reset}[ {pink}{thread_name}{reset} ] Error {purple}> {red}Invalid Github Camo Link...")

def run():
    while True:
        view_booster()

with open("config.json") as f:
    data = json.load(f)

num_threads = data.get('threads', 250)
threads = []
for i in range(int(num_threads)):
    thread = threading.Thread(target=run, name=f"VIEW_BOOSTER-{i+1}")
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
