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
        {"url": "https://freeproxyupdate.com/files/txt/afghanistan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/albania.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/algeria.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/andorra.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/angola.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/argentina.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/armenia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/australia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/austria.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/azerbaijan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/bahrain.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/bangladesh.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/barbados.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/belarus.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/belgium.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/belize.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/benin.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/bermuda.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/bhutan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/bolivia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/bosnia-and-herzegovina.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/botswana.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/brazil.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/british-virgin-islands.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/bulgaria.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/burkina-faso.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/burundi.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/cambodia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/cameroon.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/canada.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/cayman-islands.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/chad.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/chile.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/china.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/colombia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/congo.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/congo-dr.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/costa-rica.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/croatia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/cuba.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/cyprus.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/czech-republic.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/denmark.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/dominican-republic.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/ecuador.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/egypt.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/el-salvador.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/equatorial-guinea.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/estonia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/eswatini.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/ethiopia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/fiji.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/finland.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/france.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/gabon.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/gambia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/georgia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/germany.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/ghana.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/gibraltar.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/greece.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/guadeloupe.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/guam.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/guatemala.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/guinea.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/guyana.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/haiti.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/honduras.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/hong-kong.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/hungary.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/iceland.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/india.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},   
        {"url": "https://freeproxyupdate.com/files/txt/indonesia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/iran.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/iraq.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/ireland.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/israel.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/italy.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/ivory-coast.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/jamaica.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/japan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/jordan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/kazakhstan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/kenya.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/kosovo.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/kuwait.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/kyrgyzstan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/laos.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/latvia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/lebanon.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/lesotho.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/liberia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/libya.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/lithuania.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/luxembourg.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/macao.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/madagascar.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/malawi.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/malaysia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/maldives.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/mali.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/malta.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/martinique.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/mauritania.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/mauritius.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/mayotte.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/mexico.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/moldova.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/mongolia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/montenegro.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/morocco.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/mozambique.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/myanmar.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/namibia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/nepal.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/netherlands.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/new-zealand.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/nicaragua.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/nigeria.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/north-macedonia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/norway.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/oman.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/pakistan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/palestine.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/panama.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/papua-new-guinea.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/paraguay.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/peru.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/philippines.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/poland.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/portugal.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/puerto-rico.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/qatar.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/romania.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/russia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/rwanda.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/saint-kitts-and-nevis.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/saudi-arabia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/senegal.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/serbia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/seychelles.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/sierra-leone.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/singapore.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/slovakia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/slovenia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/somalia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/south-africa.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/south-korea.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/south-sudan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/spain.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/sri-lanka.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/sudan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/suriname.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/sweden.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/switzerland.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/syria.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/taiwan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/tajikistan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/tanzania.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/thailand.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/timor-leste.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/togo.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},  
        {"url": "https://freeproxyupdate.com/files/txt/trinidad-and-tobago.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/tunisia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/turkey.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/turkmenistan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/uganda.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/ukraine.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/united-arab-emirates.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/united-kingdom.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/united-states.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/uruguay.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/uzbekistan.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/vanuatu.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/venezuela.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/vietnam.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/yemen.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/zambia.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},
        {"url": "https://freeproxyupdate.com/files/txt/zimbabwe.txt", "pola": "tbody tr td:nth-child(1), tbody tr td:nth-child(2)"},     
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