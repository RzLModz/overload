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

# --- Fungsi untuk mengekstrak dan memformat proxy dari string teks (diperbaiki lagi) ---
def extract_proxies_from_text(text_content):
    """
    Mengekstrak dan memformat alamat proxy dari string teks menggunakan regular expressions
    dan logika parsing kustom. Output selalu dalam format [user:pass@]ip:port
    atau ip:port jika user/pass tidak ada. Skema (http://, socks5://) tidak akan ditambahkan.
    Hanya akan menyimpan format ip:port dan username:password@ip:port.
    """
    found_proxies = set()

    # Pola dasar IP:Port (misal: 192.168.1.1:8080)
    # Diperketat untuk memastikan IP yang valid dan port yang valid (1-65535)
    ip_pattern = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    port_pattern = r'(?:[1-9]|[1-9][0-9]{1,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])'

    proxy_pattern_ip_port = r'\b' + ip_pattern + r':' + port_pattern + r'\b'

    # Pola untuk proxy dengan otentikasi (misal: user:pass@192.168.1.1:8080 atau user:pass@domain.com:80)
    # username dan password bisa mengandung berbagai karakter yang biasa digunakan
    # Menambahkan dukungan untuk domain/hostname di samping IP
    auth_pattern = r'[a-zA-Z0-9_.-]+:[a-zA-Z0-9_.-]+@'
    domain_or_ip_pattern = r'(?:' + ip_pattern + r'|(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6})' # regex domain sederhana

    proxy_pattern_auth = r'\b' + auth_pattern + domain_or_ip_pattern + r':' + port_pattern + r'\b'

    # Pola untuk URL proxy dengan atau tanpa skema, tapi hanya mengambil ip:port atau user:pass@ip:port
    proxy_pattern_url_capture = r'(?:https?://|socks4://|socks5://)?(' + auth_pattern + domain_or_ip_pattern + r':' + port_pattern + r'|' + ip_pattern + r':' + port_pattern + r')\b'

    # Ekstraksi menggunakan regex untuk menangkap grup yang diinginkan (tanpa skema)
    for match in re.findall(proxy_pattern_url_capture, text_content):
        found_proxies.add(match.strip())

    # Ekstraksi untuk pola otentikasi tanpa skema eksplisit
    for match in re.findall(proxy_pattern_auth, text_content):
        found_proxies.add(match.strip())

    # Ekstraksi untuk pola IP:Port dasar
    for match in re.findall(proxy_pattern_ip_port, text_content):
        found_proxies.add(match.strip())

    # --- Logika parsing kustom untuk ip:port:username:password ---
    for line in text_content.splitlines():
        stripped_line = line.strip()
        if not stripped_line:
            continue

        # Skip lines that are clearly not proxy formats or general text
        if "Bookmark and Share" in stripped_line or "Let Snatcher find FREE PROXY LISTS" in stripped_line or "##" in stripped_line:
            continue

        # If it has a scheme, try to extract the non-scheme part if it's a valid proxy
        if re.match(r'(?:https?://|socks4://|socks5://)', stripped_line):
            match = re.search(proxy_pattern_url_capture, stripped_line)
            if match:
                found_proxies.add(match.group(1).strip())
            continue

        parts = stripped_line.split(':')
        if len(parts) == 4: # Diasumsikan ip:port:username:password
            # Coba validasi ini sebagai username:password@ip:port
            # Ini memerlukan restrukturisasi, asumsikan bagian terakhir adalah IP:Port

            # Jika baris adalah "ip:port:user:pass"
            # Kita perlu mengubahnya menjadi "user:pass@ip:port"
            # Periksa apakah bagian pertama dan kedua adalah IP dan Port
            ip_check = parts[0]
            port_check = parts[1]
            if re.fullmatch(ip_pattern, ip_check) and re.fullmatch(port_pattern, port_check):
                username_part = parts[2]
                password_part = parts[3]
                formatted_proxy = f"{username_part}:{password_part}@{ip_check}:{port_check}"
                found_proxies.add(formatted_proxy)
            # Jika baris adalah "user:pass:ip:port" (kemungkinan kurang tepat, tapi bisa terjadi)
            # Coba interpretasikan 2 bagian terakhir sebagai IP:Port
            elif len(parts) >= 2 and re.fullmatch(ip_pattern, parts[-2]) and re.fullmatch(port_pattern, parts[-1]):
                user_pass_part = ":".join(parts[:-2]) # Gabungkan kembali user dan pass
                formatted_proxy = f"{user_pass_part}@{parts[-2]}:{parts[-1]}"
                found_proxies.add(formatted_proxy)

        elif len(parts) == 2: # Hanya ip:port
            ip_part = parts[0]
            port_part = parts[1]
            # Validasi dasar untuk IP dan Port sebelum menambahkan
            if re.fullmatch(ip_pattern, ip_part) and \
               re.fullmatch(port_pattern, port_part):
                found_proxies.add(stripped_line)
        elif len(parts) >= 3 and '@' in stripped_line: # Kemungkinan user:pass@ip:port
            # Jika ada '@' berarti ini format otentikasi
            match = re.fullmatch(proxy_pattern_auth, stripped_line)
            if match:
                found_proxies.add(stripped_line)


    # Parsing JSON (tetap dipertahankan dengan logika parsing kustom yang ditingkatkan)
    try:
        json_data = json.loads(text_content)
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict):
                    # Handle Webshare.io specific keys: 'proxy_address', 'port', 'username', 'password'
                    if 'proxy_address' in item and 'port' in item:
                        ip_json = item['proxy_address']
                        port_json = item['port']
                        username_json = item.get('username')
                        password_json = item.get('password')

                        # Validate before adding
                        if (re.fullmatch(ip_pattern, str(ip_json)) or re.fullmatch(domain_or_ip_pattern, str(ip_json))) and \
                           re.fullmatch(port_pattern, str(port_json)):
                            if username_json and password_json:
                                found_proxies.add(f"{username_json}:{password_json}@{ip_json}:{port_json}")
                            else:
                                found_proxies.add(f"{ip_json}:{port_json}")
                    # Existing logic for 'ip' and 'port' (if other JSON sources use it)
                    elif 'ip' in item and 'port' in item:
                        ip_json = item['ip']
                        port_json = item['port']
                        username_json = item.get('username') or item.get('user')
                        password_json = item.get('password') or item.get('pass')

                        # Validasi sebelum menambahkan
                        if (re.fullmatch(ip_pattern, str(ip_json)) or re.fullmatch(domain_or_ip_pattern, str(ip_json))) and \
                           re.fullmatch(port_pattern, str(port_json)):
                            if username_json and password_json:
                                found_proxies.add(f"{username_json}:{password_json}@{ip_json}:{port_json}")
                            else:
                                found_proxies.add(f"{ip_json}:{port_json}")
                    elif 'proxy' in item and isinstance(item['proxy'], str):
                        # Ekstrak hanya bagian ip:port atau user:pass@ip:port
                        match = re.search(proxy_pattern_url_capture, item['proxy'])
                        if match:
                            found_proxies.add(match.group(1).strip())
                elif isinstance(item, str):
                    # Ekstrak hanya bagian ip:port atau user:pass@ip:port
                    match = re.search(proxy_pattern_url_capture, item)
                    if match:
                        found_proxies.add(match.group(1).strip())

        elif isinstance(json_data, dict):
            # Special handling for Webshare.io's direct JSON structure (if it's not a list)
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
                                if username_json and password_json:
                                    found_proxies.add(f"{username_json}:{password_json}@{ip_json}:{port_json}")
                                else:
                                    found_proxies.add(f"{ip_json}:{port_json}")
            # Existing logic for other dictionary formats
            for key, value in json_data.items():
                if isinstance(value, str):
                    match = re.search(proxy_pattern_url_capture, value)
                    if match:
                        found_proxies.add(match.group(1).strip())
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            match = re.search(proxy_pattern_url_capture, item)
                            if match:
                                found_proxies.add(match.group(1).strip())
    except json.JSONDecodeError:
        pass

    # Hapus proxy yang jelas-jelas tidak valid (misal: 0.0.0.0:0)
    # Juga pastikan tidak ada skema yang tersisa
    cleaned_proxies = set()
    for p in found_proxies:
        if p != "0.0.0.0:0" and "0.0.0.0:" not in p:
            # Hapus skema jika ada yang lolos dari regex (redundant but safe)
            if "://" in p:
                parts = p.split('://', 1)
                cleaned_proxies.add(parts[1])
            else:
                cleaned_proxies.add(p)
    return [p for p in cleaned_proxies if p] # Pastikan tidak ada string kosong


# Fungsi untuk memuat proxy dari file (tidak diubah, karena fokus pada fetching URL)
def load_proxies_from_file(filename='proxies.txt'):
    proxies = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    proxies.append(proxy)
    return proxies

# Helper function untuk mencetak status dinamis pada satu baris
def print_dynamic_status(message, length=120):
    """
    Mencetak/memperbarui pesan pada satu baris di terminal.
    Menggunakan carriage return (\r) untuk menimpa baris.
    """
    sys.stdout.write(f'\r{message.ljust(length)}')
    sys.stdout.flush()

# --- Fungsi utama untuk mengambil dan menyimpan semua proxy (direvisi untuk dukungan SOCKS5) ---
def fetch_and_save_all_proxies(proxy_urls, output_filename='proxies.txt'):
    all_auth_proxies = set() # Akan menyimpan proxy dengan username:password@ip:port
    all_ip_port_proxies = set() # Akan menyimpan proxy dengan ip:port
    failed_to_fetch_urls = []

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
    spinner_index = 0

    total_urls = len(proxy_urls)

    print_dynamic_status("Memulai pengambilan proxy...")

    for i, url in enumerate(proxy_urls):
        headers['User-Agent'] = user_agents[ua_index % len(user_agents)]
        ua_index += 1

        retries = 2
        initial_wait_time = 5
        current_wait_time = initial_wait_time

        url_short = url.split('//')[-1] # Ambil bagian setelah http(s)://

        url_successful = False

        for attempt in range(retries):
            current_proxy = None

            progress_percent = ((i + (attempt / retries)) / total_urls) * 100
            status_bar_length = 20

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

            current_spinner = SPINNER_CHARS[spinner_index % len(SPINNER_CHARS)]
            spinner_index += 1

            main_status_message = f"[{bar}] {progress_percent:.1f}% {current_spinner} | Mengambil {url_short} (Percobaan {attempt + 1}/{retries})"
            print_dynamic_status(main_status_message)

            try:
                with requests.get(url, timeout=30, headers=headers, proxies=current_proxy) as response:
                    response.raise_for_status()

                    content_type = response.headers.get('Content-Type', '').lower()
                    content = response.text

                    raw_extracted_proxies = []

                    # Panggil fungsi extract_proxies_from_text yang telah diperbaiki
                    raw_extracted_proxies.extend(extract_proxies_from_text(content))

                    # Logika tambahan untuk HTML agar tetap mencoba di elemen spesifik
                    if 'html' in content_type or url.endswith(('.html', '.htm')):
                        soup = BeautifulSoup(content, 'html.parser')
                        # Extract text from relevant tags and then apply extraction
                        # Added more specific filtering for common non-proxy HTML text
                        for tag in soup.find_all(['pre', 'textarea', 'code', 'div', 'p']):
                            text_from_tag = tag.get_text()
                            if "Bookmark and Share" not in text_from_tag and "Let Snatcher find FREE PROXY LISTS" not in text_from_tag and "##" not in text_from_tag:
                                raw_extracted_proxies.extend(extract_proxies_from_text(text_from_tag))
                        for table in soup.find_all('table'):
                            for row in table.find_all('tr'):
                                row_text = row.get_text()
                                if "Bookmark and Share" not in row_text and "Let Snatcher find FREE PROXY LISTS" not in row_text and "##" not in row_text:
                                    raw_extracted_proxies.extend(extract_proxies_from_text(row_text))

                    # Pisahkan proxy ke dalam dua set yang berbeda
                    formatted_proxies_for_this_url_auth = set()
                    formatted_proxies_for_this_url_ip_port = set()

                    for proxy_str in raw_extracted_proxies:
                        # Hapus skema jika ada yang lolos (redundant but safe)
                        if "://" in proxy_str:
                            proxy_str = proxy_str.split('://', 1)[1]

                        # Klasifikasikan berdasarkan format
                        if '@' in proxy_str:
                            formatted_proxies_for_this_url_auth.add(proxy_str)
                        else:
                            formatted_proxies_for_this_url_ip_port.add(proxy_str)

                    total_found_proxies = len(formatted_proxies_for_this_url_auth) + len(formatted_proxies_for_this_url_ip_port)

                    status_msg_end = ""
                    if total_found_proxies > 0:
                        status_msg_end = f"{GREEN}BERHASIL{RESET}: Ditemukan {total_found_proxies} proxy"
                        url_successful = True
                    else:
                        status_msg_end = f"{RED}GAGAL{RESET}: Tidak ditemukan pola proxy"

                    final_main_status = f"[{bar}] {progress_percent:.1f}% | {url_short} - {status_msg_end}"
                    print_dynamic_status(final_main_status)

                    all_auth_proxies.update(formatted_proxies_for_this_url_auth)
                    all_ip_port_proxies.update(formatted_proxies_for_this_url_ip_port)
                    break

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
                        if not url_successful:
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
                    final_status_message = f"[{bar}] {progress_percent:.1f}% | {url_short} - {status_msg_end}"
                    print_dynamic_status(final_status_message)
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

        if not url_successful and url not in failed_to_fetch_urls:
            failed_to_fetch_urls.append(url)

        sleep_duration = 5
        time.sleep(sleep_duration)

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

    # Gabungkan dan urutkan proxy
    final_proxies_list = sorted(list(all_auth_proxies)) + sorted(list(all_ip_port_proxies))

    if final_proxies_list:
        with open(output_filename, 'w') as f:
            for proxy in final_proxies_list:
                f.write(proxy + '\n')
        print(f"Total {len(final_proxies_list)} proxy unik berhasil disimpan ke '{output_filename}'")
    else:
        print("Tidak ada proxy yang ditemukan dan disimpan.")

    if failed_to_fetch_urls:
        print(f"\n{RED}URL yang gagal mengambil proxy setelah {retries} percobaan:{RESET}")
        for failed_url in failed_to_fetch_urls:
            print(f"- {failed_url}")
        with open('failed_proxy_urls.txt', 'w') as f_failed:
            for failed_url in failed_to_fetch_urls:
                f_failed.write(failed_url + '\n')
        print(f"\n{RED}Daftar URL yang gagal juga disimpan ke 'failed_proxy_urls.txt'.{RESET}")


### Daftar URL Sumber Proxy (Dikembalikan seperti semula)
proxy_urls = [
    "https://px.zerobot.network/",
    "https://raw.githubusercontent.com/Patchloop/public-proxies/refs/heads/main/proxies_fast.txt",
    "https://raw.githubusercontent.com/Patchloop/public-proxies/refs/heads/main/proxies_socks5.txt",
    "https://raw.githubusercontent.com/Patchloop/public-proxies/refs/heads/main/proxies_http.txt",
    "https://raw.githubusercontent.com/Patchloop/public-proxies/refs/heads/main/proxies_google.txt",
    "https://raw.githubusercontent.com/Patchloop/public-proxies/refs/heads/main/proxies_cloudflare.txt",
    "https://raw.githubusercontent.com/Patchloop/public-proxies/refs/heads/main/proxies_all.txt",
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
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous",
    "https://proxyspace.pro/http.txt",
    "https://proxy-spider.com/api/proxies.example.txt",
    "http://pubproxy.com/api/proxy",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt",
    "https://proxysnatcher.com/free-proxy-list/",
    "https://proxydb.net/",
    "https://free-proxy-list.net/#",
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://free-proxy-list.net/",
    "https://proxypremium.top/download-proxy-list",
    "https://free-proxy-list.net/",
    "https://proxypremium.top/full-proxy-list",
    "https://www.sslproxies.org/"
]

# Jalankan proses pengambilan dan penyimpanan proxy aktif
if __name__ == "__main__":
    fetch_and_save_all_proxies(proxy_urls)