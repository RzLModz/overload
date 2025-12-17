#!/bin/bash

# ===============================================
# Skrip Instalasi Dependencies Proyek (install.sh)
# VERSI OPTIMAL UNTUK NODE.JS 14.21.3
# ===============================================

# -----------------------------------------------
# 1. Konfigurasi dan Variabel
# -----------------------------------------------

INSTALL_ERRORS=""
HAS_ERROR=0

log_info() {
    echo -e "\n[\033[34mINFO\033[0m] $1"
}

log_success() {
    echo -e "[\033[32mSUCCESS\033[0m] $1"
}

log_error() {
    local error_message="[ERROR] $1 (Fungsi: $2)"
    echo -e "[\033[31mERROR\033[0m] $1" >&2
    INSTALL_ERRORS+="$error_message\n"
    HAS_ERROR=1
}

# Daftar paket NPM yang dikunci versinya untuk stabilitas di Node 14
NPM_PACKAGES=(
    "https-proxy-agent" "crypto-random-string" "events" "fs" "net"
    "cloudscraper" "request" "hcaptcha-solver" "randomstring" "cluster" 
    "cloudflare-bypasser" "socks" "hpack" "axios" "user-agents" "cheerio"
    "gradient-string" "fake-useragent" "header-generator" "math" "p-limit@2.3.0"
    "puppeteer@19" "puppeteer-extra" "puppeteer-extra-plugin-stealth" "async"
    "node-fetch@2"
)

PIP_PACKAGES=(
    "colorama" "rich" "tabulate" "termcolor" "bs4" "tqdm" "httpx" "camoufox"
    "httpx[http2]"
)

# -----------------------------------------------
# 2. Fungsi Instalasi
# -----------------------------------------------

install_system_deps() {
    log_info "Memulai Instalasi: Dependencies Sistem (APT)"
    sudo apt update -y
    
    # Instalasi dependencies dasar untuk Chrome & Node
    sudo apt install -y ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils cpulimit curl
    
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal dependencies sistem." "${FUNCNAME[0]}"
    fi
}

install_google_chrome() {
    log_info "Memulai Instalasi: Google Chrome"
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O chrome.deb
    sudo apt install ./chrome.deb -y
    if [ $? -ne 0 ]; then
        log_error "Gagal menginstal Google Chrome." "${FUNCNAME[0]}"
    else
        rm -f chrome.deb
        log_success "Google Chrome Berhasil Diinstal."
    fi
}

install_nodejs_with_nvm() {
    log_info "Memulai Instalasi: Node.js 14.21.3 via NVM"

    # Instal NVM jika belum terdeteksi
    if [ ! -d "$HOME/.nvm" ]; then
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    fi
    
    # Memuat NVM ke sesi shell
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

    if ! command -v nvm &> /dev/null; then
        log_error "NVM tidak ditemukan atau gagal dimuat." "${FUNCNAME[0]}"
        return 1
    fi
    
    log_info "Memasang Node.js 14.21.3..."
    nvm install 14.21.3
    nvm use 14.21.3
    nvm alias default 14.21.3
    
    log_success "Versi Node saat ini: $(node -v)"
}

install_npm_packages() {
    log_info "Memulai Instalasi: Paket NPM (Target Node 14)"
    
    # Pastikan berada di versi yang benar
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm use 14.21.3

    for package in "${NPM_PACKAGES[@]}"; do
        log_info "Menginstal: $package"
        npm install "$package" --no-audit --no-fund
        if [ $? -ne 0 ]; then
            log_error "Gagal menginstal paket NPM: $package" "${FUNCNAME[0]}"
        fi
    done
}

install_pip_packages() {
    log_info "Memulai Instalasi: Paket Python (PIP)"
    
    # Update pip terlebih dahulu
    python3 -m pip install --upgrade pip
    
    for package in "${PIP_PACKAGES[@]}"; do
        log_info "Menginstal paket PIP: $package"
        pip3 install "$package"
    done
}

configure_extreme_test_environment() {
    log_info "Konfigurasi Environment Ekstrem"
    ulimit -n 999999 && log_success "Ulimit ditingkatkan." || log_error "Gagal ulimit." "${FUNCNAME[0]}"
    
    # Menghindari error jika ada file yang tidak bisa di-chmod
    chmod 777 * 2>/dev/null
    log_success "Izin file disesuaikan."
}

# -----------------------------------------------
# 3. Eksekusi Utama
# -----------------------------------------------

clear
log_info "=== PROSES INSTALASI DIMULAI (NODE 14.x) ==="

install_system_deps
install_google_chrome
install_nodejs_with_nvm 
install_npm_packages
install_pip_packages
configure_extreme_test_environment

# -----------------------------------------------
# 4. Laporan Akhir
# -----------------------------------------------

echo -e "\n"
if [ $HAS_ERROR -eq 0 ]; then
    log_success "================================================="
    log_success "  INSTALASI SELESAI TANPA ERROR"
    log_success "  Versi Node: $(node -v)"
    log_success "  Versi NPM:  $(npm -v)"
    log_success "================================================="
    exit 0
else
    log_error "=================================================" "LAPORAN_AKHIR"
    log_error "  INSTALASI SELESAI DENGAN BEBERAPA ERROR"
    echo -e "$INSTALL_ERRORS"
    log_error "=================================================" "LAPORAN_AKHIR"
    exit 1
fi