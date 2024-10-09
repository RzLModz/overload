import os
import threading
import requests
import cloudscraper
from urllib.parse import urlparse
import datetime
import time
import socket
import socks
import ssl
import random

def get_target(url):
    url = url.rstrip()
    target = {}
    target['uri'] = urlparse(url).path
    if target['uri'] == "":
        target['uri'] = "/"
    target['host'] = urlparse(url).netloc
    target['scheme'] = urlparse(url).scheme
    if ":" in urlparse(url).netloc:
        target['port'] = urlparse(url).netloc.split(":")[1]
    else:
        target['port'] = "443" if urlparse(url).scheme == "https" else "80"
    return target

def bypass_cloudflare(url):
    try:
        target = get_target(url)
        proxies = load_proxies('proxies.txt')
        user_agents = load_user_agents()
        
        # Menggunakan cloudscraper untuk mengatasi Cloudflare
        scraper = cloudscraper.create_scraper()
        headers = {
            'User-Agent': random.choice(user_agents)
        }
        
        response = scraper.get(url, headers=headers, proxies=random.choice(proxies))
        response.raise_for_status()  # Memicu pengecualian jika status tidak OK
        print(f"Berhasil mengakses {url} dengan status {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan saat mengakses {url}: {e}")
    except Exception as e:
        print(f"Kesalahan umum: {e}")

def load_proxies(file_path):
    proxies = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                proxies.append({'http': line.strip(), 'https': line.strip()})
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan.")
    except Exception as e:
        print(f"Kesalahan saat memuat proxy: {e}")
    return proxies

def load_user_agents():
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36"
    ]

if __name__ == "__main__":
    url = input("Masukkan URL yang ingin diakses: ")
    bypass_cloudflare(url)
