import concurrent.futures
import requests
import time
from requests.exceptions import RequestException
from tqdm import tqdm # Import pustaka tqdm untuk progress bar

# ==================== KONFIGURASI KECEPATAN TINGGI ====================
FILE_PROXY = 'proxies.txt'
CHECK_URL = 'http://httpbin.org/ip'
TIMEOUT = 5 
MAX_THREADS = 1000 
# ======================================================================

def check_proxy(proxy):
    """
    Mengecek liveness proxy. Akan mengembalikan proxy jika hidup, atau None jika mati.
    """
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    try:
        # Melakukan GET request, dengan timeout yang singkat
        response = requests.get(CHECK_URL, proxies=proxies, timeout=TIMEOUT)
        
        # Hanya mengembalikan proxy jika status 200 (HIDUP)
        if response.status_code == 200:
            return proxy
        else:
            return None
            
    # Tangani semua exception yang berarti proxy MATI
    except (RequestException, Exception):
        return None


def main_turbo_with_progress():
    """
    Fungsi utama dengan threading dan progress bar tqdm.
    """
    live_proxies = []

    try:
        # 1. Baca daftar proxy dari file
        with open(FILE_PROXY, 'r') as f:
            all_proxies = [line.strip() for line in f if line.strip()]
            
    except FileNotFoundError:
        print(f"❌ ERROR: File '{FILE_PROXY}' tidak ditemukan.")
        return

    total_proxies = len(all_proxies)
    print(f"Memulai pengecekan {total_proxies} proxy menggunakan {MAX_THREADS} thread.")
    start_time = time.time()

    # 2. Pengecekan Paralel menggunakan ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # executor.map menjalankan fungsi check_proxy untuk semua proxy secara paralel.
        # tqdm() membungkus results untuk menampilkan progress bar.
        results = tqdm(executor.map(check_proxy, all_proxies), 
                       total=total_proxies, 
                       desc="Progres Pengecekan", 
                       unit=" proxy")
        
        # Mengumpulkan hasil yang valid (proxy yang hidup)
        for result in results:
            if result:
                live_proxies.append(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Menampilkan ringkasan
    print("\n" + "=" * 50)
    print(f"📊 RINGKASAN HASIL")
    print(f"Total Proxy Dicek: {total_proxies}")
    print(f"Proxy Hidup Ditemukan: {len(live_proxies)}")
    print(f"Total Waktu Pengecekan: {elapsed_time:.2f} detik.")
    if elapsed_time > 0:
        print(f"Kecepatan: {total_proxies / elapsed_time:.2f} proxy/detik.")
    print("=" * 50)
    
    # 3. Menulis ulang file proxies.txt
    if live_proxies:
        try:
            with open(FILE_PROXY, 'w') as f:
                f.write('\n'.join(live_proxies) + '\n')
            
            print(f"\n🎉 Sukses! {len(live_proxies)} proxy hidup telah disimpan kembali ke '{FILE_PROXY}'.")
            
        except Exception as e:
            print(f"❌ ERROR saat menulis ke file: {e}")
            
    else:
        try:
            with open(FILE_PROXY, 'w') as f:
                f.write('')
            print(f"\n⚠️ Perhatian: Tidak ada proxy yang hidup. File '{FILE_PROXY}' telah dikosongkan.")
        except Exception as e:
            print(f"❌ ERROR saat mengosongkan file: {e}")


if __name__ == "__main__":
    main_turbo_with_progress()