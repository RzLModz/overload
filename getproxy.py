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
    "https://proxy.webshare.io/api/v2/proxy/list/download/joagployahcfvuhpmnngjyhfihzdvuckbmxfafhn/-/any/username/direct/-/",
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
    "https://freeproxyupdate.com/files/txt/tunisia.txt",
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
# --- Akhir Daftar URL Sumber Proxy Anda ---

# Jalankan proses pengambilan dan penyimpanan proxy aktif
fetch_and_save_all_proxies(proxy_urls)