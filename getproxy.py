import requests
import re
from bs4 import BeautifulSoup
import time
import json
import os
import sys

# Kode ANSI untuk warna
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m' # Warna kuning
RESET = '\033[0m' # Reset warna ke default terminal

# Karakter untuk animasi spinner gaya 'gasing' (berputar)
SPINNER_CHARS = ['↻'] 

# Karakter untuk bilah progress (dari kosong ke penuh)
BAR_SEGMENTS = [' ', '▂', '▃', '▄', '▅', '▆', '▇', '▉']

# Fungsi untuk mengekstrak proxy (IP:Port) dari string teks menggunakan regular expressions
def extract_proxies_from_text(text_content):
    """
    Mengekstrak alamat proxy (IP:Port) dari string teks menggunakan regular expressions.
    Fungsi ini diperluas untuk menangani berbagai format.
    """
    found_proxies = set() # Menggunakan set sementara untuk menghindari duplikasi internal
    
    # Pola dasar IP:Port
    proxy_pattern_ip_port = r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b'
    
    # Pola untuk URL proxy
    proxy_pattern_url = r'(?:https?://)?(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b'
    
    # Pola untuk proxy dengan otentikasi
    proxy_pattern_auth = r'\b[a-zA-Z0-9_.-]+:[a-zA-Z0-9_.-]+@(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b'

    found_proxies.update(re.findall(proxy_pattern_ip_port, text_content))
    for match in re.findall(proxy_pattern_url, text_content):
        cleaned_match = match.replace("http://", "").replace("https://", "")
        found_proxies.add(cleaned_match)
    for match in re.findall(proxy_pattern_auth, text_content):
        cleaned_match = match.split('@')[-1]
        found_proxies.add(cleaned_match)

    try:
        json_data = json.loads(text_content)
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict):
                    if 'ip' in item and 'port' in item:
                        found_proxies.add(f"{item['ip']}:{item['port']}")
                    elif 'proxy' in item and isinstance(item['proxy'], str):
                        found_proxies.update(re.findall(proxy_pattern_ip_port, item['proxy']))
                elif isinstance(item, str):
                    found_proxies.update(re.findall(proxy_pattern_ip_port, item))
        elif isinstance(json_data, dict):
            for key, value in json_data.items():
                if isinstance(value, str):
                    found_proxies.update(re.findall(proxy_pattern_ip_port, value))
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            found_proxies.update(re.findall(proxy_pattern_ip_port, item))
    except json.JSONDecodeError:
        pass

    return [p.strip() for p in found_proxies if p.strip() != "0.0.0.0:0"]

# Fungsi untuk memuat proxy dari file (tetap ada tapi tidak akan digunakan untuk fetching URL sumber)
def load_proxies_from_file(filename='proxies.txt'):
    proxies = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    if not proxy.startswith(('http://', 'https://')):
                        proxies.append({'http': f'http://{proxy}', 'https': f'https://{proxy}'})
                    else:
                        proxies.append({'http': proxy, 'https': proxy})
    return proxies

# Helper function untuk mencetak status dinamis pada satu baris
def print_dynamic_status(message, length=120):
    """
    Mencetak/memperbarui pesan pada satu baris di terminal.
    Menggunakan carriage return (\r) untuk menimpa baris.
    """
    sys.stdout.write(f'\r{message.ljust(length)}')
    sys.stdout.flush()

def fetch_and_save_all_proxies(proxy_urls, output_filename='proxies.txt'):
    all_extracted_proxies = set()
    failed_to_fetch_urls = [] # List untuk menyimpan URL yang gagal setelah semua percobaan
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/'
    }

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    ]
    ua_index = 0
    spinner_index = 0 # Inisialisasi indeks spinner di sini

    # Tidak akan menggunakan proxy dari proxies.txt untuk fetching URL sumber
    proxy_index = 0
    use_external_proxies = False # SET KE FALSE UNTUK TIDAK MENGGUNAKAN PROXY EKSTERNAL

    total_urls = len(proxy_urls)
    
    # Status awal
    print_dynamic_status("Memulai pengambilan proxy...")

    for i, url in enumerate(proxy_urls):
        headers['User-Agent'] = user_agents[ua_index % len(user_agents)]
        ua_index += 1

        retries = 2 # Jumlah percobaan ulang maksimum. DI SINI ANDA BISA MENGUBAHNYA.
        initial_wait_time = 5 # Waktu tunggu awal (detik)
        current_wait_time = initial_wait_time
        
        url_short = url.split('//')[-1] # Potong URL agar lebih pendek untuk tampilan
        
        url_successful = False # Flag untuk menandakan apakah URL saat ini berhasil mendapatkan proxy

        for attempt in range(retries):
            current_proxy = None # Selalu None karena use_external_proxies adalah False
            proxy_info = "" # Tidak ada info proxy karena tidak digunakan

            # Hitung persentase progres
            progress_percent = ((i + (attempt / retries)) / total_urls) * 100 
            status_bar_length = 20 # Panjang total bilah sinyal (jumlah karakter)
            
            # --- Logika baru untuk bilah progres seperti bar sinyal ▂▃▄▅▆▇▉ ---
            bar_string = ""
            if i == total_urls - 1 and attempt == retries - 1 and url_successful: 
                bar_string = '█' * status_bar_length
            else:
                total_filled_units = (progress_percent / 100) * status_bar_length
                full_blocks = int(total_filled_units)
                partial_block_char = ''
                if full_blocks < status_bar_length:
                    fractional_fill = total_filled_units - full_blocks
                    char_index = int(fractional_fill * (len(BAR_SEGMENTS) - 1)) 
                    partial_block_char = BAR_SEGMENTS[char_index]
                
                bar_string = '█' * full_blocks
                if partial_block_char:
                    bar_string += partial_block_char
                    remaining_len = status_bar_length - full_blocks - 1 
                    bar_string += ' ' * remaining_len
                else:
                    remaining_len = status_bar_length - full_blocks
                    bar_string += ' ' * remaining_len
            
            bar = f"{YELLOW}{bar_string}{RESET}"
            # --- Akhir logika baru bilah progres ---
            
            # Ambil karakter spinner saat ini dan perbarui indeks
            current_spinner = SPINNER_CHARS[spinner_index % len(SPINNER_CHARS)]
            spinner_index += 1

            # Buat pesan status utama yang akan diperbarui
            main_status_message = f"[{bar}] {progress_percent:.1f}% {current_spinner} | Mengambil {url_short} (Percobaan {attempt + 1}/{retries})"
            print_dynamic_status(main_status_message)
            
            try:
                # Lakukan permintaan GET tanpa proxy karena current_proxy selalu None
                with requests.get(url, timeout=30, headers=headers, proxies=current_proxy if use_external_proxies else None) as response:
                    response.raise_for_status()

                    content_type = response.headers.get('Content-Type', '').lower()
                    content = response.text
                    
                    extracted_proxies_from_url = []

                    # Logika ekstraksi konten
                    if 'html' in content_type or url.endswith(('.html', '.htm')):
                        soup = BeautifulSoup(content, 'html.parser')
                        extracted_proxies_from_url.extend(extract_proxies_from_text(soup.get_text()))
                        for tag in soup.find_all(['pre', 'textarea', 'code']):
                            extracted_proxies_from_url.extend(extract_proxies_from_text(tag.get_text()))
                        for table in soup.find_all('table'):
                            for row in table.find_all('tr'):
                                row_text = row.get_text()
                                extracted_proxies_from_url.extend(extract_proxies_from_text(row_text))
                    elif 'json' in content_type or url.endswith('.json'):
                        extracted_proxies_from_url.extend(extract_proxies_from_text(content))
                    elif 'css' in content_type or url.endswith('.css'):
                        extracted_proxies_from_url.extend(extract_proxies_from_text(content))
                    elif 'text/plain' in content_type or url.endswith('.txt'):
                        extracted_proxies_from_url.extend(extract_proxies_from_text(content))
                    else:
                        extracted_proxies_from_url.extend(extract_proxies_from_text(content))

                    extracted_proxies_from_url_unique = list(set(extracted_proxies_from_url))
                    
                    status_msg_end = ""
                    if extracted_proxies_from_url_unique:
                        status_msg_end = f"{GREEN}BERHASIL{RESET}: Ditemukan {len(extracted_proxies_from_url_unique)} proxy"
                        url_successful = True # Set flag to true on success
                    else:
                        status_msg_end = f"{RED}GAGAL{RESET}: Tidak ditemukan pola proxy"
                    
                    final_main_status = f"[{bar}] {progress_percent:.1f}% | {url_short} - {status_msg_end}"
                    print_dynamic_status(final_main_status)
                    
                    all_extracted_proxies.update(extracted_proxies_from_url_unique)
                    break # Keluar dari loop percobaan jika berhasil

            except requests.exceptions.HTTPError as e:
                status_msg_end = ""
                if e.response.status_code == 429:
                    status_msg_end = f"{RED}GAGAL{RESET} (429 Too Many Requests): Coba lagi dalam {current_wait_time} detik..."
                    main_status_message = f"[{bar}] {progress_percent:.1f}% {current_spinner} | {url_short} - {status_msg_end}"
                    print_dynamic_status(main_status_message)
                    time.sleep(current_wait_time)
                    current_wait_time *= 2
                    if attempt == retries - 1:
                        status_msg_end = f"{RED}GAGAL{RESET} setelah {retries} percobaan (429)."
                        final_main_status = f"[{bar}] {progress_percent:.1f}% | {url_short} - {status_msg_end}"
                        print_dynamic_status(final_main_status)
                        # Mark as failed if all retries exhausted for 429
                        if not url_successful: # Only if not already successful in a previous attempt
                            failed_to_fetch_urls.append(url)
                elif e.response.status_code == 403:
                    status_msg_end = f"{RED}GAGAL{RESET} (403 Forbidden - Cloudflare/Blokir): {e}"
                    final_main_status = f"[{bar}] {progress_percent:.1f}% | {url_short} - {status_msg_end}"
                    print_dynamic_status(final_main_status)
                    if not url_successful:
                        failed_to_fetch_urls.append(url)
                    break
                else:
                    status_msg_end = f"{RED}GAGAL{RESET} (HTTP {e.response.status_code}): {e}"
                    final_main_status = f"[{bar}] {progress_percent:.1f}% | {url_short} - {status_msg_end}"
                    print_dynamic_status(final_main_status)
                    if not url_successful:
                        failed_to_fetch_urls.append(url)
                    break
            except requests.exceptions.RequestException as e:
                status_msg_end = f"{RED}GAGAL{RESET} (Kesalahan Permintaan): {e}"
                main_status_message = f"[{bar}] {progress_percent:.1f}% {current_spinner} | {url_short} - {status_msg_end}"
                print_dynamic_status(main_status_message)
                time.sleep(current_wait_time)
                current_wait_time *= 2
                if attempt == retries - 1:
                    status_msg_end = f"{RED}GAGAL{RESET} setelah {retries} percobaan (Masalah Koneksi)."
                    final_main_status = f"[{bar}] {progress_percent:.1f}% | {url_short} - {status_msg_end}"
                    print_dynamic_status(final_main_status)
                    if not url_successful:
                        failed_to_fetch_urls.append(url)
            except Exception as e:
                status_msg_end = f"{RED}GAGAL{RESET} (Tak Terduga): {e}"
                final_main_status = f"[{bar}] {progress_percent:.1f}% | {url_short} - {status_msg_end}"
                print_dynamic_status(final_main_status)
                if not url_successful:
                    failed_to_fetch_urls.append(url)
                break
        
        # Jika URL tidak berhasil setelah semua percobaan, tambahkan ke daftar gagal
        # Pastikan hanya ditambahkan sekali
        if not url_successful and url not in failed_to_fetch_urls:
            failed_to_fetch_urls.append(url)

        # Jeda waktu tetap antar URL (setelah semua percobaan untuk URL saat ini)
        sleep_duration = 5 
        time.sleep(sleep_duration)

    # Perbarui bilah progres akhir menjadi 100% dan tambahkan baris baru (tanpa spinner)
    final_progress_percent = 100.0
    status_bar_length = 20
    final_bar_string = '█' * status_bar_length
    bar = f"{YELLOW}{final_bar_string}{RESET}"

    final_status_message = f"[{bar}] {final_progress_percent:.1f}% | Semua URL telah diproses. Menyimpan proxy..."
    print_dynamic_status(final_status_message)
    sys.stdout.write('\n')
    sys.stdout.flush()
    sys.stdout.write('\n')
    sys.stdout.flush()

    # Logika penyimpanan proxy
    if all_extracted_proxies:
        with open(output_filename, 'w') as f:
            for proxy in sorted(list(all_extracted_proxies)):
                f.write(proxy + '\n')
        print(f"Total {len(all_extracted_proxies)} proxy unik berhasil disimpan ke '{output_filename}'")
    else:
        print("Tidak ada proxy yang ditemukan dan disimpan.")

    if failed_to_fetch_urls:
        print(f"\n{RED}URL yang gagal mengambil proxy setelah {retries} percobaan:{RESET}")
        for failed_url in failed_to_fetch_urls:
            print(f"- {failed_url}")
        # Secara opsional, simpan URL yang gagal ke file terpisah untuk ditinjau
        with open('failed_proxy_urls.txt', 'w') as f_failed:
            for failed_url in failed_to_fetch_urls:
                f_failed.write(failed_url + '\n')
        print(f"\n{RED}Daftar URL yang gagal juga disimpan ke 'failed_proxy_urls.txt'.{RESET}")


### Daftar URL Sumber Proxy
proxy_urls = [
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/AZ/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/AT/any/sourceip/ip/-/",    
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/AU/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/AM/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/AO/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/DZ/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/AL/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/AF/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/IT/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/ES/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/TH/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/KH/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/CN/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/VN/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/BD/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/RU/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/GB/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/FR/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/DE/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/MX/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/PH/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/IN/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/US/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/ID/any/sourceip/ip/-/",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/-/any/sourceip/ip/-/",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
    "https://api.openproxylist.xyz/http.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies",
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxydocker.com/en/proxylist/download?email=noshare&country=all&city=all&port=all&type=all&anonymity=all&state=all&need=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous",
    "http://worm.rip/http.txt",
    "https://proxyspace.pro/http.txt",
    "https://multiproxy.org/txt_all/proxy.txt",
    "https://proxy-spider.com/api/proxies.example.txt",
    "https://raw.githubusercontent.com/jetkai/free-proxies/main/proxies/http.txt",
    "http://pubproxy.com/api/proxy",
    "https://gimmeproxy.com/api/getProxy",
    "https://www.proxyscan.io/download?type=http",
    "http://theproxybay.me/api/proxy",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt",
    "https://openproxylist.com/v2ray/",
    "https://proxysnatcher.com/free-proxy-list/",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&format=txt",
    "https://iproyal.com/free-proxy-list/",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://proxydb.net/",
    "https://www.proxynova.com/proxy-server-list/",
    "https://fineproxy.org/free-proxies/asia/indonesia/",
    "https://smallseotools.com/free-proxy-list/",
    "https://proxy-tools.com/proxy/id",
    "https://free.proxy-sale.com/en/",
    "https://free-proxy-list.net/#",
    "https://proxybros.com/free-proxy-list/",
    "https://proxiware.com/free-proxy-list",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://freeproxyupdate.com/files/txt/http.txt",
    "https://proxyscrape.com/free-proxy-list",
    "https://proxyelite.info/free-proxy-list/",
    "https://free-proxy-list.net/",
    "https://proxypremium.top/download-proxy-list",
    "https://advanced.name/freeproxy",
    "https://spys.me/proxy.txt",
    "https://freeproxyupdate.com/files/txt/https-ssl.txt",
    "https://freeproxyupdate.com/files/txt/socks4.txt",
    "https://freeproxyupdate.com/files/txt/socks5.txt",
    "https://freeproxyupdate.com/files/txt/elite.txt",
    "https://freeproxyupdate.com/files/txt/anonymous.txt",
    "https://freeproxyupdate.com/files/txt/afghanistan.txt",
    "https://freeproxyupdate.com/files/txt/albania.txt",
    "https://freeproxyupdate.com/files/txt/algeria.txt",
    "https://freeproxyupdate.com/files/txt/andorra.txt",
    "https://freeproxyupdate.com/files/txt/angola.txt",
    "https://freeproxyupdate.com/files/txt/argentina.txt",
    "https://freeproxyupdate.com/files/txt/armenia.txt",
    "https://freeproxyupdate.com/files/txt/australia.txt",
    "https://freeproxyupdate.com/files/txt/austria.txt",
    "https://freeproxyupdate.com/files/txt/azerbaijan.txt",
    "https://freeproxyupdate.com/files/txt/bahrain.txt",
    "https://freeproxyupdate.com/files/txt/bangladesh.txt",
    "https://freeproxyupdate.com/files/txt/barbados.txt",
    "https://freeproxyupdate.com/files/txt/belarus.txt",
    "https://freeproxyupdate.com/files/txt/belgium.txt",
    "https://freeproxyupdate.com/files/txt/belize.txt",
    "https://freeproxyupdate.com/files/txt/benin.txt",
    "https://freeproxyupdate.com/files/txt/bermuda.txt",
    "https://freeproxyupdate.com/files/txt/bhutan.txt",
    "https://freeproxyupdate.com/files/txt/bolivia.txt",
    "https://freeproxyupdate.com/files/txt/bosnia-and-herzegovina.txt",
    "https://freeproxyupdate.com/files/txt/botswana.txt",
    "https://freeproxyupdate.com/files/txt/brazil.txt",
    "https://freeproxyupdate.com/files/txt/british-virgin-islands.txt",
    "https://freeproxyupdate.com/files/txt/bulgaria.txt",
    "https://freeproxyupdate.com/files/txt/burkina-faso.txt",
    "https://freeproxyupdate.com/files/txt/burundi.txt",
    "https://freeproxyupdate.com/files/txt/cambodia.txt",
    "https://freeproxyupdate.com/files/txt/cameroon.txt",
    "https://freeproxyupdate.com/files/txt/canada.txt",
    "https://freeproxyupdate.com/files/txt/cayman-islands.txt",
    "https://freeproxyupdate.com/files/txt/chad.txt",
    "https://freeproxyupdate.com/files/txt/chile.txt",
    "https://freeproxyupdate.com/files/txt/china.txt",
    "https://freeproxyupdate.com/files/txt/colombia.txt",
    "https://freeproxyupdate.com/files/txt/congo.txt",
    "https://freeproxyupdate.com/files/txt/congo-dr.txt",
    "https://freeproxyupdate.com/files/txt/costa-rica.txt",
    "https://freeproxyupdate.com/files/txt/croatia.txt",
    "https://freeproxyupdate.com/files/txt/cuba.txt",
    "https://freeproxyupdate.com/files/txt/cyprus.txt",
    "https://freeproxyupdate.com/files/txt/czech-republic.txt",
    "https://freeproxyupdate.com/files/txt/denmark.txt",
    "https://freeproxyupdate.com/files/txt/dominican-republic.txt",
    "https://freeproxyupdate.com/files/txt/ecuador.txt",
    "https://freeproxyupdate.com/files/txt/egypt.txt",
    "https://freeproxyupdate.com/files/txt/el-salvador.txt",
    "https://freeproxyupdate.com/files/txt/equatorial-guinea.txt",
    "https://freeproxyupdate.com/files/txt/estonia.txt",
    "https://freeproxyupdate.com/files/txt/eswatini.txt",
    "https://freeproxyupdate.com/files/txt/ethiopia.txt",
    "https://freeproxyupdate.com/files/txt/fiji.txt",
    "https://freeproxyupdate.com/files/txt/finland.txt",
    "https://freeproxyupdate.com/files/txt/france.txt",
    "https://freeproxyupdate.com/files/txt/gabon.txt",
    "https://freeproxyupdate.com/files/txt/gambia.txt",
    "https://freeproxyupdate.com/files/txt/georgia.txt",
    "https://freeproxyupdate.com/files/txt/germany.txt",
    "https://freeproxyupdate.com/files/txt/ghana.txt",
    "https://freeproxyupdate.com/files/txt/gibraltar.txt",
    "https://freeproxyupdate.com/files/txt/greece.txt",
    "https://freeproxyupdate.com/files/txt/guadeloupe.txt",
    "https://freeproxyupdate.com/files/txt/guam.txt",
    "https://freeproxyupdate.com/files/txt/guatemala.txt",
    "https://freeproxyupdate.com/files/txt/guinea.txt",
    "https://freeproxyupdate.com/files/txt/guyana.txt",
    "https://freeproxyupdate.com/files/txt/haiti.txt",
    "https://freeproxyupdate.com/files/txt/honduras.txt",
    "https://freeproxyupdate.com/files/txt/hong-kong.txt",
    "https://freeproxyupdate.com/files/txt/hungary.txt",
    "https://freeproxyupdate.com/files/txt/iceland.txt",
    "https://freeproxyupdate.com/files/txt/india.txt",   
    "https://freeproxyupdate.com/files/txt/indonesia.txt",
    "https://freeproxyupdate.com/files/txt/iran.txt",
    "https://freeproxyupdate.com/files/txt/iraq.txt",
    "https://freeproxyupdate.com/files/txt/ireland.txt",
    "https://freeproxyupdate.com/files/txt/israel.txt",
    "https://freeproxyupdate.com/files/txt/italy.txt",
    "https://freeproxyupdate.com/files/txt/ivory-coast.txt",
    "https://freeproxyupdate.com/files/txt/jamaica.txt",
    "https://freeproxyupdate.com/files/txt/japan.txt",
    "https://freeproxyupdate.com/files/txt/jordan.txt",
    "https://freeproxyupdate.com/files/txt/kazakhstan.txt",
    "https://freeproxyupdate.com/files/txt/kenya.txt",
    "https://freeproxyupdate.com/files/txt/kosovo.txt",
    "https://freeproxyupdate.com/files/txt/kuwait.txt",
    "https://freeproxyupdate.com/files/txt/kyrgyzstan.txt",
    "https://freeproxyupdate.com/files/txt/laos.txt",
    "https://freeproxyupdate.com/files/txt/latvia.txt",
    "https://freeproxyupdate.com/files/txt/lebanon.txt",
    "https://freeproxyupdate.com/files/txt/lesotho.txt",
    "https://freeproxyupdate.com/files/txt/liberia.txt",
    "https://freeproxyupdate.com/files/txt/libya.txt",
    "https://freeproxyupdate.com/files/txt/lithuania.txt",
    "https://freeproxyupdate.com/files/txt/luxembourg.txt",
    "https://freeproxyupdate.com/files/txt/macao.txt",
    "https://freeproxyupdate.com/files/txt/madagascar.txt",
    "https://freeproxyupdate.com/files/txt/malawi.txt",
    "https://freeproxyupdate.com/files/txt/malaysia.txt",
    "https://freeproxyupdate.com/files/txt/maldives.txt",
    "https://freeproxyupdate.com/files/txt/mali.txt",
    "https://freeproxyupdate.com/files/txt/malta.txt",
    "https://freeproxyupdate.com/files/txt/martinique.txt",
    "https://freeproxyupdate.com/files/txt/mauritania.txt",
    "https://freeproxyupdate.com/files/txt/mauritius.txt",
    "https://freeproxyupdate.com/files/txt/mayotte.txt",
    "https://freeproxyupdate.com/files/txt/mexico.txt",
    "https://freeproxyupdate.com/files/txt/moldova.txt",
    "https://freeproxyupdate.com/files/txt/mongolia.txt",
    "https://freeproxyupdate.com/files/txt/montenegro.txt",
    "https://freeproxyupdate.com/files/txt/morocco.txt",
    "https://freeproxyupdate.com/files/txt/mozambique.txt",
    "https://freeproxyupdate.com/files/txt/myanmar.txt",
    "https://freeproxyupdate.com/files/txt/namibia.txt",
    "https://freeproxyupdate.com/files/txt/nepal.txt",
    "https://freeproxyupdate.com/files/txt/netherlands.txt",
    "https://freeproxyupdate.com/files/txt/new-zealand.txt",
    "https://freeproxyupdate.com/files/txt/nicaragua.txt",
    "https://freeproxyupdate.com/files/txt/nigeria.txt",
    "https://freeproxyupdate.com/files/txt/north-macedonia.txt",
    "https://freeproxyupdate.com/files/txt/norway.txt",
    "https://freeproxyupdate.com/files/txt/oman.txt",
    "https://freeproxyupdate.com/files/txt/pakistan.txt",
    "https://freeproxyupdate.com/files/txt/palestine.txt",
    "https://freeproxyupdate.com/files/txt/panama.txt",
    "https://freeproxyupdate.com/files/txt/papua-new-guinea.txt",
    "https://freeproxyupdate.com/files/txt/paraguay.txt",
    "https://freeproxyupdate.com/files/txt/peru.txt",
    "https://freeproxyupdate.com/files/txt/philippines.txt",
    "https://freeproxyupdate.com/files/txt/poland.txt",
    "https://freeproxyupdate.com/files/txt/portugal.txt",
    "https://freeproxyupdate.com/files/txt/puerto-rico.txt",
    "https://freeproxyupdate.com/files/txt/qatar.txt",
    "https://freeproxyupdate.com/files/txt/romania.txt",
    "https://freeproxyupdate.com/files/txt/russia.txt",
    "https://freeproxyupdate.com/files/txt/rwanda.txt",
    "https://freeproxyupdate.com/files/txt/saint-kitts-and-nevis.txt",
    "https://freeproxyupdate.com/files/txt/saudi-arabia.txt",
    "https://freeproxyupdate.com/files/txt/senegal.txt",
    "https://freeproxyupdate.com/files/txt/serbia.txt",
    "https://freeproxyupdate.com/files/txt/seychelles.txt",
    "https://freeproxyupdate.com/files/txt/sierra-leone.txt",
    "https://freeproxyupdate.com/files/txt/singapore.txt",
    "https://freeproxyupdate.com/files/txt/slovakia.txt",
    "https://freeproxyupdate.com/files/txt/slovenia.txt",
    "https://freeproxyupdate.com/files/txt/somalia.txt",
    "https://freeproxyupdate.com/files/txt/south-africa.txt",
    "https://freeproxyupdate.com/files/txt/south-korea.txt",
    "https://freeproxyupdate.com/files/txt/south-sudan.txt",
    "https://freeproxyupdate.com/files/txt/spain.txt",
    "https://freeproxyupdate.com/files/txt/sri-lanka.txt",
    "https://freeproxyupdate.com/files/txt/sudan.txt",
    "https://freeproxyupdate.com/files/txt/suriname.txt",
    "https://freeproxyupdate.com/files/txt/sweden.txt",
    "https://freeproxyupdate.com/files/txt/switzerland.txt",
    "https://freeproxyupdate.com/files/txt/syria.txt",
    "https://freeproxyupdate.com/files/txt/taiwan.txt",
    "https://freeproxyupdate.com/files/txt/tajikistan.txt",
    "https://freeproxyupdate.com/files/txt/tanzania.txt",
    "https://freeproxyupdate.com/files/txt/thailand.txt",
    "https://freeproxyupdate.com/files/txt/timor-leste.txt",
    "https://freeproxyupdate.com/files/txt/togo.txt",
    "https://freeproxyupdate.com/files/txt/trinidad-and-tobago.txt",
    "https://freeproxyupdate.com/files/txt/turkey.txt",
    "https://freeproxyupdate.com/files/txt/turkmenistan.txt",
    "https://freeproxyupdate.com/files/txt/uganda.txt",
    "https://freeproxyupdate.com/files/txt/ukraine.txt",
    "https://freeproxyupdate.com/files/txt/united-arab-emirates.txt",
    "https://freeproxyupdate.com/files/txt/united-kingdom.txt",
    "https://freeproxyupdate.com/files/txt/united-states.txt",
    "https://freeproxyupdate.com/files/txt/uruguay.txt",
    "https://freeproxyupdate.com/files/txt/uzbekistan.txt",
    "https://freeproxyupdate.com/files/txt/vanuatu.txt",
    "https://freeproxyupdate.com/files/txt/venezuela.txt",
    "https://freeproxyupdate.com/files/txt/vietnam.txt",
    "https://freeproxyupdate.com/files/txt/yemen.txt",
    "https://freeproxyupdate.com/files/txt/zambia.txt",
    "https://freeproxyupdate.com/files/txt/zimbabwe.txt",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://proxyscrape.com/free-proxy-list",
    "https://proxyelite.info/free-proxy-list/",
    "https://free-proxy-list.net/",
    "https://proxypremium.top/download-proxy-list",
    "https://advanced.name/freeproxy",
    "https://spys.me/proxy.txt",
    "https://www.sslproxies.org/"
]

# Jalankan proses pengambilan dan penyimpanan proxy aktif
if __name__ == "__main__":
    fetch_and_save_all_proxies(proxy_urls)