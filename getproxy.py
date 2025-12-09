import requests
import re
from bs4 import BeautifulSoup
import time 
import json
import os
import sys
from tqdm import tqdm
import random 
# === Impor tambahan untuk waktu real-time ===
import datetime
import pytz
# ============================================

# Kode ANSI untuk warna
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m' 
RESET = '\033[0m' 

# === Kelas TQDM Custom untuk Waktu Real-Time (Waktu & Tanggal) ===
class TqdmRealTime(tqdm):
    """
    Kelas tqdm kustom untuk menambahkan waktu dan tanggal real-time WIB 
    dengan pewarnaan hijau (Green) ke dalam format progress bar.
    """
    # Menetapkan zona waktu ke WIB (Asia/Jakarta)
    WIB = pytz.timezone('Asia/Jakarta')
    
    @property
    def format_dict(self):
        """
        Override format_dict untuk menambahkan variabel kustom {wib_time} dan {wib_date}
        yang sudah diwarnai.
        """
        # Panggil format_dict default
        d = super(TqdmRealTime, self).format_dict
        
        # Hitung waktu saat ini dalam zona waktu WIB
        now_wib = datetime.datetime.now(self.WIB)
        
        # 1. Format Waktu ke HH:MM:SS
        time_raw = now_wib.strftime('%H:%M:%S')
        # Tambahkan kode warna HIJAU sebelum waktu dan RESET setelahnya
        wib_time_str = f"{GREEN}{time_raw}{RESET}"
        
        # 2. Format Tanggal ke D-M-YYYY (menghilangkan nol di depan hari/bulan)
        date_raw = now_wib.strftime('%d-%m-%Y').lstrip('0').replace('-0', '-')
        # Tambahkan kode warna HIJAU sebelum tanggal dan RESET setelahnya
        wib_date_str = f"{GREEN}{date_raw}{RESET}"
        
        # Tambahkan ke dictionary format
        d.update(wib_time=wib_time_str, wib_date=wib_date_str)
        return d
# ======================================================================


# --- Fungsi untuk mengekstrak dan memformat proxy dari string teks (Fixed) ---
def extract_proxies_from_text(text_content):
    """
    Mengekstrak dan memformat alamat proxy dari string teks menggunakan regular expressions
    dan logika parsing kustom. Output selalu dalam format [user:pass@]ip:port
    atau ip:port jika user/pass tidak ada.
    """
    found_proxies = set()

    # Pola dasar IP:Port 
    ip_pattern = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    port_pattern = r'(?:[1-9]|[1-9][0-9]{1,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])'

    # Pola 1: ip:port saja
    proxy_pattern_ip_port = r'\b' + ip_pattern + r':' + port_pattern + r'\b'
    
    # Komponen untuk otentikasi (user:pass@)
    auth_pattern = r'[a-zA-Z0-9_.-]+:[a-zA-Z0-9_.-]+@'
    domain_or_ip_pattern = r'(?:' + ip_pattern + r'|(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6})' 
    
    # Pola 2: Menangkap [user:pass@]ip:port dengan atau tanpa skema (http://, dll.)
    # Pola ini mencakup kedua format proxy: [auth@ip:port] dan [ip:port]
    proxy_pattern_url_capture = r'(?:https?://|socks4://|socks5://)?(' + auth_pattern + domain_or_ip_pattern + r':' + port_pattern + r'|' + ip_pattern + r':' + port_pattern + r')\b'

    # Menangkap semua yang sesuai dengan pola proxy:
    for match in re.findall(proxy_pattern_url_capture, text_content):
        # re.findall dengan group penangkap ( ) akan mengembalikan isi group
        found_proxies.add(match.strip())
    
    # Menangkap pola ip:port standar tanpa skema atau auth:
    for match in re.findall(proxy_pattern_ip_port, text_content):
        found_proxies.add(match.strip())

    # Logika Parsing Kustom (untuk format yang tidak teratur, seperti JSON atau line breaks)
    for line in text_content.splitlines():
        stripped_line = line.strip()
        if not stripped_line: continue
        if "Bookmark and Share" in stripped_line or "Let Snatcher find FREE PROXY LISTS" in stripped_line or "##" in stripped_line: continue

        parts = stripped_line.split(':')
        
        # Penanganan format 'ip:port:user:pass' yang tidak standar
        if len(parts) == 4:
            ip_check = parts[0]
            port_check = parts[1]
            if re.fullmatch(ip_pattern, ip_check) and re.fullmatch(port_pattern, port_check):
                username_part = parts[2]
                password_part = parts[3]
                formatted_proxy = f"{username_part}:{password_part}@{ip_check}:{port_check}"
                found_proxies.add(formatted_proxy)
            elif len(parts) >= 2 and re.fullmatch(ip_pattern, parts[-2]) and re.fullmatch(port_pattern, parts[-1]):
                user_pass_part = ":".join(parts[:-2]) 
                formatted_proxy = f"{user_pass_part}@{parts[-2]}:{parts[-1]}"
                found_proxies.add(formatted_proxy)
        elif len(parts) == 2:
            ip_part = parts[0]
            port_part = parts[1]
            if re.fullmatch(ip_pattern, ip_part) and re.fullmatch(port_pattern, port_part):
                found_proxies.add(stripped_line)
        # Penanganan format user:pass@ip:port yang mungkin terlewat oleh Regex utama
        elif len(parts) >= 3 and '@' in stripped_line:
            match = re.search(proxy_pattern_url_capture, stripped_line)
            if match: found_proxies.add(match.group(1).strip())
        
    # Penanganan data JSON
    try:
        json_data = json.loads(text_content)
        # Logika parsing JSON tetap dipertahankan
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict):
                    # Mencari pola 'proxy_address' dan 'port'
                    if 'proxy_address' in item and 'port' in item:
                        ip_json = item['proxy_address']
                        port_json = item['port']
                        username_json = item.get('username')
                        password_json = item.get('password')
                        if (re.fullmatch(ip_pattern, str(ip_json)) or re.fullmatch(domain_or_ip_pattern, str(ip_json))) and \
                           re.fullmatch(port_pattern, str(port_json)):
                            if username_json and password_json: found_proxies.add(f"{username_json}:{password_json}@{ip_json}:{port_json}")
                            else: found_proxies.add(f"{ip_json}:{port_json}")
                    # Mencari pola 'ip' dan 'port'
                    elif 'ip' in item and 'port' in item:
                        ip_json = item['ip']
                        port_json = item['port']
                        username_json = item.get('username') or item.get('user')
                        password_json = item.get('password') or item.get('pass')
                        if (re.fullmatch(ip_pattern, str(ip_json)) or re.fullmatch(domain_or_ip_pattern, str(ip_json))) and \
                           re.fullmatch(port_pattern, str(port_json)):
                            if username_json and password_json: found_proxies.add(f"{username_json}:{password_json}@{ip_json}:{port_json}")
                            else: found_proxies.add(f"{ip_json}:{port_json}")
                    # Mencari string proxy di dalam key 'proxy'
                    elif 'proxy' in item and isinstance(item['proxy'], str):
                        match = re.search(proxy_pattern_url_capture, item['proxy'])
                        if match: found_proxies.add(match.group(1).strip())
                elif isinstance(item, str):
                    match = re.search(proxy_pattern_url_capture, item)
                    if match: found_proxies.add(match.group(1).strip())
        elif isinstance(json_data, dict):
            if 'results' in json_data and isinstance(json_data['results'], list):
                for item in json_data['results']:
                    if isinstance(item, dict):
                        if 'proxy_address' in item and 'port' in item:
                            ip_json = item['proxy_address']
                            port_json = item['port']
                            username_json = item.get('username')
                            password_json = item.get('password')
                            if (re.fullmatch(ip_pattern, str(ip_json)) or re.fullmatch(domain_or_ip_pattern, str(ip_json))) and \
                               re.fullmatch(port_pattern, str(port_json)):
                                if username_json and password_json: found_proxies.add(f"{username_json}:{password_json}@{ip_json}:{port_json}")
                                else: found_proxies.add(f"{ip_json}:{port_json}")
            for key, value in json_data.items():
                if isinstance(value, str):
                    match = re.search(proxy_pattern_url_capture, value)
                    if match: found_proxies.add(match.group(1).strip())
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            match = re.search(proxy_pattern_url_capture, item)
                            if match: found_proxies.add(match.group(1).strip())
    except json.JSONDecodeError: pass

    cleaned_proxies = set()
    for p in found_proxies:
        if p != "0.0.0.0:0" and "0.0.0.0:" not in p:
            if "://" in p:
                parts = p.split('://', 1)
                cleaned_proxies.add(parts[1])
            else:
                cleaned_proxies.add(p)
    return [p for p in cleaned_proxies if p]


# --- Fungsi utama untuk mengambil dan menyimpan semua proxy ---
def fetch_and_save_all_proxies(proxy_urls, output_filename='proxyunchek.txt', delay_min=1, delay_max=5): 
    # Acak Urutan URL
    random.shuffle(proxy_urls) 
    
    all_proxies_in_order = [] 
    failed_to_fetch_urls = []

    # Inisialisasi Header dan User-Agents
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

    total_urls = len(proxy_urls)
    
    # Menggunakan TqdmRealTime untuk progress bar dan menyesuaikan format
    custom_bar_format = (
        # Format untuk menempatkan TIME/DATE di ujung output bar
        "{l_bar}{bar}| {n_fmt}/{total_fmt} [TIME {wib_time} DATE {wib_date}]"
    )

    url_pbar = TqdmRealTime(enumerate(proxy_urls), 
                            total=total_urls, 
                            desc="Scraper Proxy", # Menggunakan "Scraper Proxy"
                            unit="", # Menghilangkan unit " URL"
                            bar_format=custom_bar_format)

    for i, url in url_pbar:
        headers['User-Agent'] = user_agents[ua_index % len(user_agents)]
        ua_index += 1

        retries = 2
        initial_wait_time = 5
        current_wait_time = initial_wait_time

        url_short = url.split('//')[-1].split('/')[0]

        url_successful = False
        zero_proxies_found = False # Tambahkan flag untuk 0 proxy

        for attempt in range(retries):
            current_proxy = None
            
            status_message = f"Mengambil: {url_short} (Percobaan {attempt + 1}/{retries})"
            # Menggunakan "Scraper Proxy" sebagai deskripsi berwarna kuning
            url_pbar.set_description(f"{YELLOW}Scraper Proxy{RESET}: {status_message}")

            try:
                with requests.get(url, timeout=30, headers=headers, proxies=current_proxy) as response:
                    response.raise_for_status()

                    content_type = response.headers.get('Content-Type', '').lower()
                    content = response.text

                    raw_extracted_proxies = []

                    raw_extracted_proxies.extend(extract_proxies_from_text(content))

                    if 'html' in content_type or url.endswith(('.html', '.htm')):
                        soup = BeautifulSoup(content, 'html.parser')
                        for tag in soup.find_all(['pre', 'textarea', 'code', 'div', 'p', 'table', 'tr']):
                            text_from_tag = tag.get_text()
                            if "Bookmark and Share" not in text_from_tag and "Let Snatcher find FREE PROXY LISTS" not in text_from_tag and "##" not in text_from_tag:
                                raw_extracted_proxies.extend(extract_proxies_from_text(text_from_tag))

                    total_found_proxies = len(raw_extracted_proxies)
                    
                    # --- FITUR BARU: Menangani kasus 0 proxy yang ditemukan ---
                    if total_found_proxies == 0:
                        zero_proxies_found = True
                        url_pbar.set_description(f"{RED}PROXY 0{RESET}: {url_short} - Tidak ada proxy ditemukan")
                        break # Keluar dari loop percobaan untuk URL ini
                    # --------------------------------------------------------

                    all_proxies_in_order.extend(raw_extracted_proxies)

                    # Mengubah format BERHASIL tanpa URL yang diminta user
                    url_pbar.set_description(f"{GREEN}BERHASIL{RESET} -> Ditemukan {total_found_proxies} proxy")
                    url_successful = True
                    
                    break 

            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code
                if status_code == 429: # Rate limit terdeteksi
                    # Tunda lebih lama dan secara progresif
                    url_pbar.set_description(f"{RED}429{RESET}: {url_short} - Tunggu {current_wait_time}s")
                    time.sleep(current_wait_time)
                    current_wait_time *= 2 # Gandakan waktu tunggu
                elif status_code == 403:
                    url_pbar.set_description(f"{RED}403{RESET}: {url_short} - Blokir (Gagal permanen)")
                    break
                else:
                    url_pbar.set_description(f"{RED}HTTP {status_code}{RESET}: {url_short} - Gagal")
                    break
            except requests.exceptions.RequestException:
                url_pbar.set_description(f"{RED}Koneksi Error{RESET}: {url_short} - Coba lagi")
                time.sleep(current_wait_time)
                current_wait_time *= 2
            except Exception as e:
                url_pbar.set_description(f"{RED}Error Tdk Tdga{RESET}: {url_short} - {type(e).__name__}")
                break

        # --- Modifikasi Blok 'if not url_successful:' untuk menyertakan kasus 0 proxy ---
        if not url_successful:
            if zero_proxies_found: # Kasus proxy 0
                url_pbar.set_description(f"{RED}GAGAL TOTAL{RESET}: {url_short} - Proxy 0 Ditemukan")
                failed_to_fetch_urls.append(url)
            elif 'Koneksi Error' in url_pbar.desc:
                url_pbar.set_description(f"{RED}GAGAL TOTAL{RESET}: {url_short} - Koneksi/Timeout")
                failed_to_fetch_urls.append(url)
            # Jika gagal karena 403/404/dll, URL sudah ditambahkan oleh `break` di loop `for attempt`
            # Cek jika URL belum ditambahkan (misalnya karena 403/404 gagal pada percobaan pertama)
            elif url not in failed_to_fetch_urls:
                 # Hanya tambahkan jika gagal dan bukan karena 0 proxy (sudah ditangani di atas) atau koneksi error
                 # Untuk mencakup kegagalan seperti 403, 404, dll. 
                 # Cek desc untuk memastikan ini adalah kegagalan yang belum ditambahkan
                 if any(status_code in url_pbar.desc for status_code in ['403', 'HTTP']) and "BERHASIL" not in url_pbar.desc:
                    failed_to_fetch_urls.append(url)
            
        # *** Jeda acak yang tangguh melawan rate limit (1-5 detik) ***
        random_delay = random.uniform(delay_min, delay_max)
        url_pbar.set_description(f"Menunggu {random_delay:.2f}s...")
        time.sleep(random_delay)


    # Proses deduplikasi yang mempertahankan urutan penemuan.
    final_proxies_set = set()
    final_proxies_list = []
    for proxy in all_proxies_in_order:
        if proxy not in final_proxies_set:
            final_proxies_set.add(proxy)
            final_proxies_list.append(proxy)
            
    # Finalisasi tqdm dan mencetak hasil
    url_pbar.close() 
    sys.stdout.write('\n')
    sys.stdout.flush()

    # --- MODIFIKASI: Menggunakan 'proxyunchek.txt' sebagai output file utama ---
    if final_proxies_list:
        # Nama file yang digunakan adalah output_filename (default-nya 'proxyunchek.txt')
        with open(output_filename, 'w') as f:
            for proxy in final_proxies_list:
                f.write(proxy + '\n')
        print(f"Total {len(final_proxies_list)} proxy unik berhasil disimpan ke '{output_filename}'")
    else:
        print("Tidak ada proxy yang ditemukan dan disimpan.")
    # -----------------------------------------------------------------------

    if failed_to_fetch_urls:
        print(f"\n{RED}URL yang gagal mengambil proxy setelah {retries} percobaan:{RESET}")
        for failed_url in failed_to_fetch_urls:
            print(f"- {failed_url}")
        with open('failed_proxy_urls.txt', 'w') as f_failed:
            for failed_url in failed_to_fetch_urls:
                f_failed.write(failed_url + '\n')
        print(f"\n{RED}Daftar URL yang gagal juga disimpan ke 'failed_proxy_urls.txt'.{RESET}")


# --- Daftar URL Sumber Proxy ---
proxy_urls = [
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=http&geo=VN",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=socks5&geo=VN",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=socks4&geo=VN",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=http&geo=ALL",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=socks5&geo=ALL",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=tcp&geo=ALL",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=socks4&geo=ALL",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=ldap&geo=ALL",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=ntp&geo=ALL",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=wsd&geo=ALL",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=coap&geo=ALL",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=stun&geo=ALL",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=ssdp&geo=ALL",
    "https://tools.elitestress.st/api/proxy?license=81caff769fb7adf481b088a530a3e658&type=dvr&geo=ALL",
    "https://raw.githubusercontent.com/berkay-digital/Proxy-Scraper/main/proxies.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/http.txt",
    "https://raw.githubusercontent.com/iplocate/free-proxy-list/refs/heads/main/all-proxies.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/refs/heads/main/proxies/http.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/socks5_proxies.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/socks4_proxies.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/http_proxies.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/allive.txt",
    "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/socks5.txt",
    "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/https.txt",
    "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/http.txt",
    "https://raw.githubusercontent.com/zloi-user/hideip.me/refs/heads/master/connect.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/https.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks4.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks5.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/proxylist.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/http.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/all/data.txt",
    "https://proxyfreeonly.com/api/free-proxy-list?limit=50000&page=1&country=VN&sortBy=lastChecked&sortType=desc",
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/-/any/username/ip/-/",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://px.zerobot.network/",
    "https://api.openproxylist.xyz/http.txt",
    "https://api.openproxylist.xyz/https.txt",
    "https://api.openproxylist.xyz/socks4.txt",
    "https://api.openproxylist.xyz/socks5.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies",
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous",
    "https://proxyspace.pro/http.txt",
    "https://proxy-spider.com/api/proxies.example.txt",
    "http://pubproxy.com/api/proxy",
    "https://proxysnatcher.com/free-proxy-list/",
    "https://proxydb.net/",
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
    "https://free-proxy-list.net/",
    "https://proxypremium.top/download-proxy-list",
    "https://proxypremium.top/full-proxy-list",
    "https://www.sslproxies.org/"
]

# Jalankan proses pengambilan dan penyimpanan proxy aktif dengan jeda acak 1 hingga 5 detik
if __name__ == "__main__":
    # Mengubah nama file output utama menjadi 'proxyunchek.txt'
    fetch_and_save_all_proxies(proxy_urls, output_filename='proxyunchek.txt', delay_min=1, delay_max=5)