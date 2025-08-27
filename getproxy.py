import requests
import re
from bs4 import BeautifulSoup
import time 

# Fungsi untuk mengekstrak proxy (IP:Port) dari string teks menggunakan regular expressions
def extract_proxies_from_text(text_content):
    """
    Mengekstrak alamat proxy (IP:Port) dari string teks menggunakan regular expressions.
    """
    proxy_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b'
    found_proxies = re.findall(proxy_pattern, text_content)
    # Filter out common invalid IP:Port patterns like 0.0.0.0:0
    return [p.strip() for p in found_proxies if p.strip() != "0.0.0.0:0"]

# Fungsi utama untuk mengambil dan menyimpan semua proxy yang ditemukan
def fetch_and_save_all_proxies(proxy_urls, output_filename='proxies.txt'): # Nama file output diubah menjadi 'proxies.txt'
    """
    Mengambil proxy dari daftar URL yang diberikan dan menyimpan semua proxy yang ditemukan
    dan unik ke dalam file tanpa verifikasi keaktifan.
    """
    all_extracted_proxies = set() # Menggunakan set untuk menyimpan proxy yang diekstrak dan unik
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    for url in proxy_urls:
        print(f"Mengambil dari: {url}")
        try:
            with requests.get(url, timeout=30, headers=headers) as response: 
                response.raise_for_status() # Akan memunculkan HTTPError untuk respons yang buruk

                content_type = response.headers.get('Content-Type', '').lower()
                content = response.text
                
                extracted_proxies_from_url = [] # Proxy yang diekstrak dari URL saat ini

                # Logika deteksi tipe konten dan ekstraksi
                if 'html' in content_type or url.endswith(('.html', '.htm')):
                    print("  -> Terdeteksi HTML, memproses...")
                    soup = BeautifulSoup(content, 'html.parser')
                    extracted_proxies_from_url.extend(extract_proxies_from_text(soup.get_text()))
                    # Cari juga di dalam tag 'pre' atau 'textarea'
                    for pre_tag in soup.find_all(['pre', 'textarea']):
                        extracted_proxies_from_url.extend(extract_proxies_from_text(pre_tag.get_text()))
                elif 'css' in content_type or url.endswith('.css'):
                    print("  -> Terdeteksi CSS, mencari pola proxy...")
                    extracted_proxies_from_url.extend(extract_proxies_from_text(content))
                elif 'text/plain' in content_type or url.endswith('.txt'):
                    print("  -> Terdeteksi TXT, mencari pola proxy...")
                    extracted_proxies_from_url.extend(extract_proxies_from_text(content))
                else:
                    print(f"  -> Tipe konten tidak spesifik ('{content_type}'), mencoba ekstrak umum...")
                    extracted_proxies_from_url.extend(extract_proxies_from_text(content))

                # Hapus duplikasi dari proxy yang baru diekstrak dari URL ini
                extracted_proxies_from_url_unique = list(set(extracted_proxies_from_url)) 

                if extracted_proxies_from_url_unique:
                    print(f"  Ditemukan {len(extracted_proxies_from_url_unique)} proxy dari {url}. Menambahkan ke daftar.")
                    all_extracted_proxies.update(extracted_proxies_from_url_unique) # Tambahkan ke set utama
                else:
                    print(f"  Tidak ada pola proxy yang ditemukan dari {url}.")
                
                # Tambahkan sedikit jeda antar URL untuk menghindari blokir
                time.sleep(1) 

        except requests.exceptions.RequestException as e:
            print(f"  Gagal mengambil atau memproses {url}: {e}")
        except Exception as e:
            print(f"  Kesalahan tak terduga saat memproses {url}: {e}")
        print("-" * 50) # Garis pemisah untuk keterbacaan

    # Simpan semua proxy yang diekstrak dan unik ke file
    if all_extracted_proxies:
        with open(output_filename, 'w') as f:
            for proxy in sorted(list(all_extracted_proxies)): # Urutkan untuk konsistensi
                f.write(proxy + '\n')
        print(f"\nTotal {len(all_extracted_proxies)} proxy unik berhasil disimpan ke '{output_filename}'")
    else:
        print("\nTidak ada proxy yang ditemukan dan disimpan.")

### Daftar URL Sumber Proxy (Diposisikan di Sini)
# --- Daftar URL Sumber Proxy Anda ---
# Anda dapat dengan mudah menambahkan atau menghapus URL di sini
proxy_urls = [
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
    "https://www.proxydocker.com/en/proxylist/download?email=noshare&country=all&city=all&port=all&type=all&anonymity=all&state=all&need=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous",
    "http://worm.rip/http.txt",
    "https://proxyspace.pro/http.txt",
    "https://multiproxy.org/txt_all/proxy.txt",
    "https://proxy-spider.com/api/proxies.example.txt",
    "https://am-shape-fp-laptops.trycloudflare.com",
    "https://px.zerobot.network",
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
    "https://proxydb.net/"
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
    "https://freeproxyupdate.com/",
    "https://proxyscrape.com/free-proxy-list",
    "https://proxyelite.info/free-proxy-list/",
    "https://free-proxy-list.net/",
    "https://proxypremium.top/download-proxy-list",
    "https://advanced.name/freeproxy",
    "https://spys.me/proxy.txt",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://proxyscrape.com/free-proxy-list",
    "https://proxyelite.info/free-proxy-list/",
    "https://free-proxy-list.net/",
    "https://proxypremium.top/download-proxy-list",
    "https://advanced.name/freeproxy",
    "https://spys.me/proxy.txt",
    "https://hide.mn/en/proxy-list/",
    "https://free.geonix.com/en/",
    "https://proxytitan.com/free-proxy-list",
    "https://databay.com/free-proxy-list",
    "https://proxy-tools.com/proxy",
    "https://www.freeproxy.world/",
    "https://www.freeproxy.world/?country=ID",
    "https://proxydb.net/",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://proxypremium.top/full-proxy-list",
    "https://www.sslproxies.org/"
]
# --- Akhir Daftar URL Sumber Proxy Anda ---

# Jalankan proses pengambilan dan penyimpanan proxy aktif
fetch_and_save_all_proxies(proxy_urls)