#!/bin/bash

# ===============================================
# Skrip Instalasi Dependencies Proyek (install.sh)
# DIGUNAKAN UNTUK PENGUJIAN KEAMANAN DAN BEBAN TINGGI
# Pastikan Anda menjalankan ini di server virtual yang terisolasi!
# ===============================================

# -----------------------------------------------
# 1. Konfigurasi dan Variabel
# -----------------------------------------------

# Fungsi Logging
log_info() {
    echo -e "\n[\033[34mINFO\033[0m] $1"
}

log_success() {
    echo -e "[\033[32mSUCCESS\033[0m] $1"
}

log_error() {
    echo -e "[\033[31mERROR\033[0m] $1" >&2
}

# Daftar paket NPM (Node.js)
NPM_PACKAGES=(
    "requests" "https-proxy-agent" "crypto-random-string" "events" "fs" "net"
    "cloudscraper" "request" "hcaptcha-solver" "randomstring" "cluster" 
    "cloudflare-bypasser" "socks" "hpack" "axios" "user-agents" "cheerio"
    "gradient-string" "fake-useragent" "header-generator" "math" "p-limit@2.3.0"
    "puppeteer" "puppeteer-extra" "puppeteer-extra-plugin-stealth" "async"
)

# Daftar paket Python (PIP)
PIP_PACKAGES=(
    "colorama" "rich" "tabulate" "termcolor" "bs4" "tqdm" "httpx" "camoufox"
    "httpx[http2]"
)

# -----------------------------------------------
# 2. Fungsi Instalasi (APT, NPM, PIP)
# -----------------------------------------------

install_system_deps() {
    log_info "Memperbarui dan Mengupgrade Sistem Operasi..."
    sudo apt update -y && sudo apt upgrade -y || { log_error "Gagal update/upgrade sistem."; return 1; }
    log_success "Sistem Diperbarui."
    
    log_info "Menginstal Dependencies Chrome dan Sistem Tambahan (APT)..."
    # Dependencies untuk Puppeteer dan Chrome
    sudo apt install -y ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils cpulimit
    
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal dependencies sistem dasar."
        return 1
    fi
    log_success "Dependencies Sistem Dasar Selesai."
}

install_google_chrome() {
    log_info "Mengunduh dan Menginstal Google Chrome Stable..."
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O google-chrome-stable_current_amd64.deb
    sudo apt install ./google-chrome-stable_current_amd64.deb -y
    
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal Google Chrome. Pastikan Anda berada di sistem 64-bit yang kompatibel."
        return 1
    fi
    rm google-chrome-stable_current_amd64.deb
    log_success "Google Chrome Berhasil Diinstal."
}

install_npm_packages() {
    log_info "Menginstal Paket Node.js (NPM)..."
    if ! command -v npm &> /dev/null; then
        log_error "NPM tidak ditemukan. Harap instal Node.js dan NPM terlebih dahulu."
        return 1
    fi

    npm install "${NPM_PACKAGES[@]}"
    
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal beberapa paket NPM. Cek log di atas."
        return 1
    fi
    log_success "Semua Paket NPM Selesai Diinstal."
}

install_pip_packages() {
    log_info "Menginstal Paket Python (PIP)..."
    if ! command -v pip3 &> /dev/null; then
        log_error "PIP3 tidak ditemukan. Harap instal Python3 dan PIP3 terlebih dahulu."
        return 1
    fi

    # Instal paket dari requirements.txt
    if [ -f requirements.txt ]; then
        log_info "Menginstal paket dari requirements.txt..."
        pip3 install -r requirements.txt
    else
        log_info "requirements.txt tidak ditemukan, melewati instalasi file."
    fi  # <-- PERBAIKAN: Menggunakan 'fi' untuk menutup blok 'if'
    
    # Instal paket yang disebutkan dalam daftar
    log_info "Menginstal paket PIP tambahan..."
    pip3 install --upgrade requests urllib3 chardet
    pip3 install "${PIP_PACKAGES[@]}"
    
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal beberapa paket PIP. Cek log di atas."
        return 1
    fi
    log_success "Semua Paket PIP Selesai Diinstal."
}

# -----------------------------------------------
# 3. Fungsi Konfigurasi Pengujian Ekstrem
# -----------------------------------------------

configure_extreme_test_environment() {
    log_info "Mengatur Batasan File Descriptor (ulimit -n 999999)..."
    # Mengatur ulimit -n untuk sesi ini. Ini mungkin memerlukan izin root
    if ulimit -n 999999; then
        log_success "ulimit -n berhasil diatur ke 999999."
    else
        log_error "Gagal mengatur ulimit -n. Mungkin memerlukan izin root atau konfigurasi OS yang berbeda."
    fi

    log_info "Memberikan Izin Penuh (chmod 777 *) di direktori saat ini..."
    # PENTING: Perintah ini memberikan izin R/W/X penuh pada SEMUA file di direktori ini
    if chmod 777 *; then
        log_success "Izin 777 berhasil diterapkan pada semua file/folder di direktori ini."
    else
        log_error "Gagal menerapkan chmod 777. Mungkin ada file yang tidak dapat diakses."
    fi
}

# -----------------------------------------------
# 4. Eksekusi Skrip Utama
# -----------------------------------------------

log_info "Memulai Skrip Instalasi Proyek (Pengujian Ekstrem)..."

install_system_deps && \
install_google_chrome && \
install_npm_packages && \
install_pip_packages && \
configure_extreme_test_environment

if [ $? -eq 0 ]; then
    log_success "-------------------------------------------"
    log_success "Skrip Instalasi Proyek Selesai Dijalankan."
    log_success "Lingkungan pengujian ekstrem telah dikonfigurasi."
    log_success "-------------------------------------------"
else
    log_error "-------------------------------------------"
    log_error "Skrip selesai dengan kesalahan. Harap periksa log."
    log_error "-------------------------------------------"
fi

exit 0