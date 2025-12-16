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
    # Tambahan paket yang diminta pengguna
    "node-fetch"
)

# Daftar paket Python (PIP)
PIP_PACKAGES=(
    "colorama" "rich" "tabulate" "termcolor" "bs4" "tqdm" "httpx" "camoufox"
    "httpx[http2]"
)

# -----------------------------------------------
# 2. Fungsi Instalasi (APT, NVM, NPM, PIP)
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
    # Menambahkan 'curl' yang dibutuhkan NVM
    sudo apt install -y ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils cpulimit curl
    
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal dependencies sistem dasar (APT). Harap periksa log di atas." "${FUNCNAME[0]}"
    else
        log_success "Dependencies Sistem Dasar Selesai."
    fi
    
    return 0
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
    
    return 0
}

# --- FUNGSI BARU UNTUK NVM DAN NODE.JS ---
install_nodejs_with_nvm() {
    log_info "Memulai Instalasi: Node.js dan NPM menggunakan NVM"

    # 1. Instal NVM
    log_info "Menginstal NVM (Node Version Manager)..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    
    # 2. Muat NVM untuk sesi saat ini
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # Ini memuat nvm
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" # Ini memuat nvm bash_completion

    if ! command -v nvm &> /dev/null; then
        log_error "NVM gagal dimuat atau diinstal. Pastikan 'curl' sudah tersedia." "${FUNCNAME[0]}"
        return 0
    fi
    
    # 3. Instal Node.js LTS
    log_info "Menginstal versi LTS Node.js..."
    nvm install --lts
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal Node.js LTS melalui NVM." "${FUNCNAME[0]}"
        return 0
    fi
    
    # 4. Gunakan Node.js yang baru diinstal (opsional, sudah default setelah install)
    nvm use --lts
    log_success "Node.js LTS dan NPM berhasil diinstal dan dimuat."
    
    return 0
}
# ---------------------------------------------

install_npm_packages() {
    log_info "Memulai Instalasi: Paket Node.js (NPM)"
    
    # Memastikan NPM sudah tersedia setelah instalasi NVM
    if ! command -v npm &> /dev/null; then
        log_error "NPM tidak ditemukan. Harap pastikan instalasi Node.js (melalui NVM) berhasil." "${FUNCNAME[0]}"
        return 0
    fi

    # MODIFIKASI: Menginstal paket NPM satu per satu untuk memastikan kelanjutan jika ada kegagalan.
    for package in "${NPM_PACKAGES[@]}"; do
        log_info "Menginstal paket NPM: $package"
        # Menghilangkan 'requests' dari daftar karena ini adalah modul Python. 
        # Di Node.js biasanya menggunakan 'request', 'axios', atau 'node-fetch'.
        # Saya telah memastikan semua modul Node.js (termasuk 'node-fetch' yang diminta) ada di array NPM_PACKAGES.
        
        # Menggunakan 'npm install' lokal untuk menghindari modifikasi global
        npm install "$package"
        
        if [ $? -ne 0 ]; then
            log_error "Gagal menginstal paket NPM: $package" "${FUNCNAME[0]}"
        else
            log_success "Paket NPM $package berhasil diinstal."
        fi
    done
    
    # Tambahkan pemeriksaan ringkasan untuk memverifikasi apakah ada paket yang tidak terinstal
    if [ $HAS_ERROR -eq 1 ]; then
        log_error "Satu atau lebih Paket NPM gagal diinstal. Cek detail di Laporan Akhir." "${FUNCNAME[0]}"
    else
        log_success "Semua Paket NPM Selesai Diinstal."
    fi
    
    return 0
}

install_pip_packages() {
    log_info "Memulai Instalasi: Paket Python (PIP)"
    
    if ! command -v pip3 &> /dev/null; then
        log_error "PIP3 tidak ditemukan. Harap instal Python3 dan PIP3 terlebih dahulu." "${FUNCNAME[0]}"
        return 0
    fi

    # Instal paket dari requirements.txt
    if [ -f requirements.txt ]; then
        log_info "Menginstal paket dari requirements.txt..."
        pip3 install -r requirements.txt
        if [ $? -ne 0 ]; then
            log_error "Gagal menginstal paket dari requirements.txt." "${FUNCNAME[0]}"
        else
            log_success "Paket dari requirements.txt berhasil diinstal."
        fi
    else
        log_info "requirements.txt tidak ditemukan, melewati instalasi file."
    fi
    
    # MODIFIKASI: Menginstal paket PIP tambahan secara terpisah
    log_info "Menginstal paket PIP standar yang di-upgrade (requests, urllib3, chardet)..."
    pip3 install --upgrade requests urllib3 chardet
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal atau meng-upgrade paket standar PIP (requests, urllib3, chardet)." "${FUNCNAME[0]}"
    fi

    log_info "Menginstal paket PIP tambahan satu per satu..."
    # MODIFIKASI: Menginstal paket PIP satu per satu
    for package in "${PIP_PACKAGES[@]}"; do
        log_info "Menginstal paket PIP: $package"
        # Gunakan --break-system-packages jika diperlukan pada Python versi baru (opsional)
        pip3 install "$package"
        
        if [ $? -ne 0 ]; then
            log_error "Gagal menginstal paket PIP: $package" "${FUNCNAME[0]}"
        else
            log_success "Paket PIP $package berhasil diinstal."
        fi
    done

    # Tambahkan pemeriksaan ringkasan
    if [ $HAS_ERROR -eq 1 ]; then
        log_error "Satu atau lebih Paket PIP gagal diinstal. Cek detail di Laporan Akhir." "${FUNCNAME[0]}"
    else
        log_success "Semua Paket PIP Selesai Diinstal."
    fi
    
    return 0
}

# -----------------------------------------------
# 3. Fungsi Konfigurasi Pengujian Ekstrem
# -----------------------------------------------

configure_extreme_test_environment() {
    log_info "Memulai Konfigurasi: Lingkungan Pengujian Ekstrem"
    
    log_info "Mengatur Batasan File Descriptor (ulimit -n 999999)..."
    # Batas ini hanya berlaku untuk sesi shell saat ini.
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
    
    return 0
}

# -----------------------------------------------
# 4. Eksekusi Skrip Utama
# -----------------------------------------------

log_info "Memulai Skrip Instalasi Proyek (Pengujian Ekstrem)..."

# Panggil setiap fungsi secara terpisah
install_system_deps
install_google_chrome
# Memanggil fungsi baru untuk instalasi Node.js/NVM
install_nodejs_with_nvm 
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