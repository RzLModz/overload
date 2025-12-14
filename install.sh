#!/bin/bash

# ===============================================
# Skrip Instalasi Dependencies Proyek (install.sh)
# DIGUNAKAN UNTUK PENGUJIAN KEAMANAN DAN BEBAN TINGGI
# Pastikan Anda menjalankan ini di server virtual yang terisolasi!
# ===============================================

# -----------------------------------------------
# 1. Konfigurasi dan Variabel
# -----------------------------------------------

# Variabel Global untuk mencatat semua kesalahan
INSTALL_ERRORS=""
HAS_ERROR=0

# Fungsi Logging
log_info() {
    echo -e "\n[\033[34mINFO\033[0m] $1"
}

log_success() {
    echo -e "[\033[32mSUCCESS\033[0m] $1"
}

# Fungsi Logging Error yang juga mencatat error ke variabel global
log_error() {
    local error_message="[ERROR] $1 (Fungsi: $2)"
    echo -e "[\033[31mERROR\033[0m] $1" >&2
    INSTALL_ERRORS+="$error_message\n"
    HAS_ERROR=1
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
    log_info "Memulai Instalasi: Dependencies Sistem Dasar (APT)"
    
    log_info "Memperbarui dan Mengupgrade Sistem Operasi..."
    sudo apt update -y && sudo apt upgrade -y
    if [ $? -ne 0 ]; then
        log_error "Gagal update/upgrade sistem." "${FUNCNAME[0]}"
        # Lanjut eksekusi, karena ini bukan kegagalan kritis yang menghentikan instalasi
    else
        log_success "Sistem Diperbarui."
    fi
    
    log_info "Menginstal Dependencies Chrome dan Sistem Tambahan (APT)..."
    # Dependencies untuk Puppeteer dan Chrome
    sudo apt install -y ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils cpulimit
    
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal dependencies sistem dasar (APT). Harap periksa log di atas." "${FUNCNAME[0]}"
    else
        log_success "Dependencies Sistem Dasar Selesai."
    fi
    
    return 0 # Selalu return 0 untuk melanjutkan skrip utama
}

install_google_chrome() {
    log_info "Memulai Instalasi: Google Chrome Stable"
    
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O google-chrome-stable_current_amd64.deb
    sudo apt install ./google-chrome-stable_current_amd64.deb -y
    
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal Google Chrome. Pastikan Anda berada di sistem 64-bit yang kompatibel dan dependencies sistem sudah terinstal." "${FUNCNAME[0]}"
    else
        rm -f google-chrome-stable_current_amd64.deb
        log_success "Google Chrome Berhasil Diinstal."
    fi
    
    return 0 # Selalu return 0 untuk melanjutkan skrip utama
}

install_npm_packages() {
    log_info "Memulai Instalasi: Paket Node.js (NPM)"
    
    if ! command -v npm &> /dev/null; then
        log_error "NPM tidak ditemukan. Harap instal Node.js dan NPM terlebih dahulu." "${FUNCNAME[0]}"
        return 0 # Lanjut ke langkah berikutnya
    fi

    npm install "${NPM_PACKAGES[@]}"
    
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal beberapa paket NPM. Cek log di atas untuk detail." "${FUNCNAME[0]}"
    else
        log_success "Semua Paket NPM Selesai Diinstal."
    fi
    
    return 0 # Selalu return 0 untuk melanjutkan skrip utama
}

install_pip_packages() {
    log_info "Memulai Instalasi: Paket Python (PIP)"
    
    if ! command -v pip3 &> /dev/null; then
        log_error "PIP3 tidak ditemukan. Harap instal Python3 dan PIP3 terlebih dahulu." "${FUNCNAME[0]}"
        return 0 # Lanjut ke langkah berikutnya
    fi

    # Instal paket dari requirements.txt
    if [ -f requirements.txt ]; then
        log_info "Menginstal paket dari requirements.txt..."
        pip3 install -r requirements.txt
        if [ $? -ne 0 ]; then
            log_error "Gagal menginstal paket dari requirements.txt." "${FUNCNAME[0]}"
        fi
    else
        log_info "requirements.txt tidak ditemukan, melewati instalasi file."
    fi
    
    # Instal paket yang disebutkan dalam daftar
    log_info "Menginstal paket PIP tambahan..."
    pip3 install --upgrade requests urllib3 chardet
    pip3 install "${PIP_PACKAGES[@]}"
    
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal beberapa paket PIP tambahan. Cek log di atas." "${FUNCNAME[0]}"
    else
        log_success "Semua Paket PIP Selesai Diinstal."
    fi
    
    return 0 # Selalu return 0 untuk melanjutkan skrip utama
}

# -----------------------------------------------
# 3. Fungsi Konfigurasi Pengujian Ekstrem
# -----------------------------------------------

configure_extreme_test_environment() {
    log_info "Memulai Konfigurasi: Lingkungan Pengujian Ekstrem"
    
    log_info "Mengatur Batasan File Descriptor (ulimit -n 999999)..."
    if ulimit -n 999999; then
        log_success "ulimit -n berhasil diatur ke 999999 (untuk sesi ini)."
    else
        log_error "Gagal mengatur ulimit -n. Mungkin memerlukan izin root atau konfigurasi OS yang berbeda." "${FUNCNAME[0]}"
    fi

    log_info "Memberikan Izin Penuh (chmod 777 *) di direktori saat ini..."
    # PENTING: Perintah ini memberikan izin R/W/X penuh pada SEMUA file di direktori ini
    chmod 777 *
    if [ $? -ne 0 ]; then
        log_error "Gagal menerapkan chmod 777. Mungkin ada file/direktori yang tidak dapat diakses." "${FUNCNAME[0]}"
    else
        log_success "Izin 777 berhasil diterapkan pada semua file/folder di direktori ini."
    fi
    
    return 0 # Selalu return 0 untuk melanjutkan skrip utama
}

# -----------------------------------------------
# 4. Eksekusi Skrip Utama
# -----------------------------------------------

log_info "Memulai Skrip Instalasi Proyek (Pengujian Ekstrem)..."

# Panggil setiap fungsi secara terpisah tanpa '&&'
install_system_deps
install_google_chrome
install_npm_packages
install_pip_packages
configure_extreme_test_environment

# -----------------------------------------------
# 5. Laporan Akhir
# -----------------------------------------------

if [ $HAS_ERROR -eq 0 ]; then
    log_success "-------------------------------------------"
    log_success "Skrip Instalasi Proyek Selesai Dijalankan."
    log_success "Lingkungan pengujian ekstrem telah dikonfigurasi TANPA KESALAHAN."
    log_success "-------------------------------------------"
    exit 0
else
    log_error "-------------------------------------------"
    log_error "Skrip selesai dengan SATU ATAU LEBIH KESALAHAN." "LAPORAN_AKHIR"
    log_error "-------------------------------------------"
    log_info "Detail Kesalahan yang Terjadi:"
    echo -e "$INSTALL_ERRORS"
    log_error "-------------------------------------------"
    exit 1
fi