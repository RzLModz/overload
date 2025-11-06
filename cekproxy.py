import concurrent.futures
import requests
import time
from requests.exceptions import RequestException
from tqdm import tqdm
# === Impor tambahan untuk waktu real-time ===
import datetime
import pytz
# ============================================

# === Konstanta Warna ANSI ===
# ANSI Escape Codes untuk warna hijau (Green) dan reset warna
COLOR_GREEN = '\033[92m'
COLOR_RESET = '\033[0m'
# ============================

# ==================== KONFIGURASI KECEPATAN TINGGI ====================
# BARU: Mengubah menjadi file input dan menambahkan file output
INPUT_FILE = 'proxyunchek.txt' # File yang berisi daftar proxy mentah
OUTPUT_FILE = 'proxies.txt'    # File untuk menyimpan proxy yang hidup/valid
CHECK_URL = 'http://httpbin.org/ip'
TIMEOUT = 5 
MAX_THREADS = 1000 
# ======================================================================

def check_proxy(proxy):
    # ... (Fungsi check_proxy tetap sama) ...
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    try:
        response = requests.get(CHECK_URL, proxies=proxies, timeout=TIMEOUT)
        
        if response.status_code == 200:
            return proxy
        else:
            return None
            
    except (RequestException, Exception):
        return None

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
        d = super(TqdmRealTime, self).format_dict
        
        # Hitung waktu saat ini dalam zona waktu WIB
        now_wib = datetime.datetime.now(self.WIB)
        
        # 1. Format Waktu ke HH:MM:SS
        time_raw = now_wib.strftime('%H:%M:%S')
        # Tambahkan kode warna HIJAU sebelum waktu dan RESET setelahnya
        wib_time_str = f"{COLOR_GREEN}{time_raw}{COLOR_RESET}"
        
        # 2. Format Tanggal ke D-M-YYYY (Contoh: 4-11-2025)
        # Menggunakan %#d untuk Windows dan %-d untuk Linux/macOS. 
        # Di sini menggunakan format yang lebih umum tanpa '#' atau '-' 
        # untuk portabilitas atau menggunakan %d (dengan nol di depan).
        date_raw = now_wib.strftime('%d-%m-%Y') 
        # Tambahkan kode warna HIJAU sebelum tanggal dan RESET setelahnya
        wib_date_str = f"{COLOR_GREEN}{date_raw}{COLOR_RESET}"
        
        # Tambahkan ke dictionary format
        d.update(wib_time=wib_time_str, wib_date=wib_date_str)
        return d
# ======================================================================


def main_turbo_with_progress():
    """
    Fungsi utama dengan threading dan progress bar tqdm.
    """
    live_proxies = []

    try:
        # 1. Baca daftar proxy dari file INPUT_FILE (proxyunchek.txt)
        with open(INPUT_FILE, 'r') as f:
            all_proxies = [line.strip() for line in f if line.strip()]
            
    except FileNotFoundError:
        print(f"❌ ERROR: File '{INPUT_FILE}' tidak ditemukan.")
        return

    total_proxies = len(all_proxies)
    print(f"Memulai pengecekan {total_proxies} proxy menggunakan {MAX_THREADS} thread.")
    start_time = time.time()

    # 2. Pengecekan Paralel menggunakan ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        
        # Menggunakan format "TIME {wib_time} DATE {wib_date}".
        custom_bar_format = (
            "{l_bar}{bar}| {n_fmt}/{total_fmt} [TIME {wib_time} DATE {wib_date}]"
        )
        
        results = TqdmRealTime(executor.map(check_proxy, all_proxies), 
                       total=total_proxies, 
                       desc="Progres Pengecekan", 
                       unit="", 
                       bar_format=custom_bar_format
                       )
        
        # Mengumpulkan hasil yang valid (proxy yang hidup)
        for result in results:
            if result:
                live_proxies.append(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Menampilkan ringkasan
    print("\n" + "=" * 50)
    print(f"INFORMATION")
    print(f"Total Proxy Dicek: {total_proxies}")
    print(f"Proxy Hidup Ditemukan: {len(live_proxies)}")
    print(f"Total Waktu Pengecekan: {elapsed_time:.2f} detik.")
    if elapsed_time > 0:
        # Kecepatan tetap ditampilkan di ringkasan karena merupakan metrik penting
        print(f"Kecepatan: {total_proxies / elapsed_time:.2f} proxy/detik.")
    print("=" * 50)
    
    # 3. Menulis file OUTPUT_FILE (proxies.txt)
    if live_proxies:
        try:
            # Gunakan OUTPUT_FILE di sini
            with open(OUTPUT_FILE, 'w') as f:
                f.write('\n'.join(live_proxies) + '\n')
            
            print(f"\nBERHASIL {len(live_proxies)} proxy hidup telah disimpan ke '{OUTPUT_FILE}'.")
            
        except Exception as e:
            print(f"❌ ERROR saat menulis ke file: {e}")
            
    else:
        try:
            # Gunakan OUTPUT_FILE di sini
            with open(OUTPUT_FILE, 'w') as f:
                f.write('')
            print(f"\n⚠️ Perhatian: Tidak ada proxy yang hidup. File '{OUTPUT_FILE}' telah dikosongkan.")
        except Exception as e:
            print(f"❌ ERROR saat mengosongkan file: {e}")


if __name__ == "__main__":
    main_turbo_with_progress()