#!/bin/bash

# ===============================================
# Skrip Instalasi Dependencies - FORCED NODE 14.x
# Versi Lengkap dengan Auto-Environment Refresh
# ===============================================

INSTALL_ERRORS=""
HAS_ERROR=0

log_info() { echo -e "\n[\033[34mINFO\033[0m] $1"; }
log_success() { echo -e "[\033[32mSUCCESS\033[0m] $1"; }
log_error() {
    local error_message="[ERROR] $1 (Fungsi: $2)"
    echo -e "[\033[31mERROR\033[0m] $1" >&2
    INSTALL_ERRORS+="$error_message\n"
    HAS_ERROR=1
}

# Daftar paket NPM yang dikunci untuk Node 14
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
# FUNGSI 1: INSTALASI SYSTEM & GOOGLE CHROME
# -----------------------------------------------
install_system_deps() {
    log_info "Menginstal Dependencies Sistem & Google Chrome..."
    sudo apt update -y
    sudo apt install -y ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils cpulimit curl
    
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O chrome.deb
    sudo apt install ./chrome.deb -y && rm chrome.deb
}

# -----------------------------------------------
# FUNGSI 2: FORCE NODE.JS 14.21.3 (NVM)
# -----------------------------------------------
install_nodejs_with_nvm() {
    log_info "Mengonfigurasi Node.js 14.21.3 melalui NVM..."

    export NVM_DIR="$HOME/.nvm"
    
    # Instal NVM jika belum ada
    if [ ! -d "$NVM_DIR" ]; then
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    fi
    
    # Load NVM secara paksa ke dalam skrip
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

    if ! command -v nvm &> /dev/null; then
        log_error "NVM gagal dimuat." "${FUNCNAME[0]}"
        return 1
    fi

    # Eksekusi Instalasi & Penguncian Versi
    nvm install 14.21.3
    nvm unalias default 2>/dev/null
    nvm alias default 14.21.3
    nvm use 14.21.3

    # Verifikasi Versi
    NODE_VER=$(node -v)
    if [[ $NODE_VER != v14* ]]; then
        log_error "Node masih $NODE_VER. Memaksa PATH manual..." "NodeFix"
        export PATH="$NVM_DIR/versions/node/v14.21.3/bin:$PATH"
    fi
    
    log_success "Node.js yang digunakan: $(node -v)"
}

# -----------------------------------------------
# FUNGSI 3: NPM & PIP PACKAGES
# -----------------------------------------------
install_packages() {
    log_info "Menginstal Paket NPM (Target: Node 14)..."
    for package in "${NPM_PACKAGES[@]}"; do
        npm install "$package" --no-audit --no-fund --quiet
        [ $? -ne 0 ] && log_error "Gagal NPM: $package" "NPM_INSTALL"
    done

    log_info "Menginstal Paket Python (PIP)..."
    for package in "${PIP_PACKAGES[@]}"; do
        pip3 install "$package" --quiet
        [ $? -ne 0 ] && log_error "Gagal PIP: $package" "PIP_INSTALL"
    done
}

# -----------------------------------------------
# EKSEKUSI UTAMA
# -----------------------------------------------
clear
log_info "MEMULAI PROSES INSTALASI..."

install_system_deps
install_nodejs_with_nvm
install_packages

log_info "Konfigurasi Akhir..."
ulimit -n 999999
chmod 777 * 2>/dev/null

# -----------------------------------------------
# LAPORAN AKHIR & SARAN TAMBAHAN
# -----------------------------------------------
echo -e "\n"
if [ $HAS_ERROR -eq 0 ]; then
    log_success "================================================="
    log_success "  INSTALASI BERHASIL!"
    log_success "  Node.js: $(node -v)"
    log_success "  NPM:     $(npm -v)"
    log_success "================================================="
    
    # SARAN TAMBAHAN: Refresh terminal secara otomatis
    log_info "Menjalankan refresh environment (source ~/.bashrc)..."
    [ -s "$HOME/.nvm/nvm.sh" ] && \. "$HOME/.nvm/nvm.sh"
    nvm use 14.21.3
    
    echo -e "[\033[33mTIP\033[0m] Jika terminal masih menunjukkan versi lama, jalankan: \033[1msource ~/.bashrc\033[0m"
    exit 0
else
    log_error "Selesai dengan error. Cek log di atas." "MAIN"
    exit 1
fi