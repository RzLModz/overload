import concurrent.futures
import requests
from requests.adapters import HTTPAdapter
import time
from tqdm import tqdm
import datetime
import pytz
import json

# === KONSTANTA WARNA ===
COLOR_GREEN = '\033[92m'
COLOR_CYAN = '\033[96m'
COLOR_YELLOW = '\033[93m'
COLOR_RED = '\033[91m'
COLOR_RESET = '\033[0m'

# ==================== KONFIGURASI ULTRA PRO ====================
INPUT_FILE = 'proxyunchek.txt'
OUTPUT_FILE = 'proxies.txt'

# Strategi Multi-Domain: Menghindari False Negative
CHECK_URLS = [
    'http://httpbin.org/ip',               # Target 1: Validasi Identitas (Anti-Honeypot)
    'http://www.google.com/generate_204',  # Target 2: Uji Kecepatan (Paling Ringan)
    'http://1.1.1.1/cdn-cgi/trace',        # Target 3: Infrastruktur Cloudflare
    'http://www.msftconnecttest.com/connecttest.txt' # Target 4: Akses Global Microsoft
]

TIMEOUT = 10        # 10 detik per percobaan
MAX_THREADS = 1000   # Dioptimalkan untuk 8 CPU / 16GB RAM
# ===============================================================

def check_proxy(proxy):
    """
    Logika: Multi-Target Failover + Anti-Honeypot + Latency Measure.
    """
    proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    proxy_ip = proxy.split(':')[0]
    
    start_time = time.perf_counter()
    
    with requests.Session() as session:
        # Optimasi adapter untuk manajemen thread yang efisien
        adapter = HTTPAdapter(pool_connections=1, pool_maxsize=1)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        for url in CHECK_URLS:
            try:
                response = session.get(url, proxies=proxies, timeout=TIMEOUT, headers=headers)
                
                if response.status_code in [200, 204]:
                    # --- FITUR ANTI HONEYPOT (Validasi Identitas) ---
                    if 'httpbin' in url:
                        try:
                            # Memeriksa apakah IP yang dideteksi server sesuai dengan IP proxy
                            detected_ip = response.json().get('origin', '')
                            if proxy_ip not in detected_ip:
                                continue # Jika IP tidak cocok, coba domain lain atau abaikan
                        except:
                            continue
                    
                    # Jika lolos salah satu verifikasi
                    latency = (time.perf_counter() - start_time) * 1000
                    return (proxy, latency)
            except:
                continue # Failover ke domain berikutnya jika terjadi error
                
    return None

class TqdmRealTime(tqdm):
    WIB = pytz.timezone('Asia/Jakarta')
    @property
    def format_dict(self):
        d = super(TqdmRealTime, self).format_dict
        now_wib = datetime.datetime.now(self.WIB)
        wib_info = f"{COLOR_GREEN}{now_wib.strftime('%H:%M:%S')}{COLOR_RESET}"
        d.update(wib_time=wib_info)
        return d

def main():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            # Membersihkan spasi, karakter aneh, dan hapus duplikat
            all_proxies = list(dict.fromkeys([line.strip() for line in f if line.strip()]))
    except FileNotFoundError:
        print(f"{COLOR_RED}❌ ERROR: File '{INPUT_FILE}' tidak ditemukan!{COLOR_RESET}")
        return

    total = len(all_proxies)
    print(f"\n{COLOR_CYAN}🛡️  PROXY CHECKER ULTRA PRO v2.0{COLOR_RESET}")
    print(f"{'='*55}")
    print(f"Target Check : {total} Proxy")
    print(f"Threads      : {MAX_THREADS}")
    print(f"Strategy     : Multi-Domain Failover + Anti-Honeypot")
    print(f"{'='*55}\n")
    
    live_results = []

    # Eksekusi Pararel dengan 1000 Threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        custom_format = "{l_bar}{bar}| {n_fmt}/{total_fmt} [{wib_time}]"
        
        # Submit semua tugas
        futures = {executor.submit(check_proxy, p): p for p in all_proxies}
        
        with TqdmRealTime(total=total, desc="Checking", bar_format=custom_format) as pbar:
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res:
                    live_results.append(res)
                pbar.update(1)

    # === FITUR AUTO-SORT (Urutkan dari yang tercepat) ===
    print(f"\n{COLOR_YELLOW}Sorting {len(live_results)} proxy berdasarkan latensi terbaik...{COLOR_RESET}")
    live_results.sort(key=lambda x: x[1])

    # Menulis hasil akhir ke proxies.txt
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for p, lat in live_results:
            f.write(f"{p}\n")

    print(f"\n{'='*55}")
    print(f"✅ {COLOR_GREEN}PROSES SELESAI!{COLOR_RESET}")
    print(f"Proxy Hidup & Valid : {len(live_results)}")
    if live_results:
        print(f"Proxy Tercepat      : {live_results[0][0]} ({live_results[0][1]:.0f}ms)")
        print(f"Proxy Terlambat     : {live_results[-1][0]} ({live_results[-1][1]:.0f}ms)")
    print(f"Hasil disimpan di   : {OUTPUT_FILE}")
    print(f"{'='*55}")

if __name__ == "__main__":
    main()