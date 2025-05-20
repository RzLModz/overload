import requests
from bs4 import BeautifulSoup

def ekstrak_proxy(url, pola):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        proxy_list = soup.select(pola)
        proxies = [proxy.text.strip() for proxy in proxy_list]
        return proxies
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengambil data dari {url}: {e}")
        return []
    except Exception as e:
        print(f"Terjadi kesalahan saat memproses {url}: {e}")
        return []

def simpan_ke_file(proxies, nama_file="proxies.txt"):
    try:
        with open(nama_file, "w") as f:
            for proxy in proxies:
                f.write(proxy + "\n")
        print(f"Berhasil menyimpan {len(proxies)} proxy ke dalam {nama_file}")
    except Exception as e:
        print(f"Gagal menyimpan ke file {nama_file}: {e}")

if __name__ == "__main__":
    daftar_website = [
        {"url": "https://freeproxyupdate.com/files/txt/http.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://proxyscrape.com/free-proxy-list", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://proxyelite.info/free-proxy-list/", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://free-proxy-list.net/", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://proxypremium.top/download-proxy-list", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://advanced.name/freeproxy", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://spys.me/proxy.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/https-ssl.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/socks4.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/socks5.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/elite.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/anonymous.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        # Tambahkan lebih banyak website dan pola CSS selector di sini
    ]

    semua_proxy = []

    for website in daftar_website:
        print(f"Mengambil proxy dari: {website['url']}")
        url = website['url']
        pola_ip = website['pola'].split(', ')[0]
        pola_port = website['pola'].split(', ')[1]

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            ips = [ip.text.strip() for ip in soup.select(pola_ip)]
            ports = [port.text.strip() for port in soup.select(pola_port)]

            if len(ips) == len(ports):
                for i in range(len(ips)):
                    semua_proxy.append(f"{ips[i]}:{ports[i]}")
            else:
                print(f"Jumlah IP dan Port tidak sesuai di {url}")

        except requests.exceptions.RequestException as e:
            print(f"Gagal mengambil data dari {url}: {e}")
        except Exception as e:
            print(f"Terjadi kesalahan saat memproses {url}: {e}")

    # Hapus duplikat proxy
    semua_proxy_unik = sorted(list(set(semua_proxy)))

    if semua_proxy_unik:
        simpan_ke_file(semua_proxy_unik)
    else:
        print("Tidak ada proxy yang berhasil ditemukan.")