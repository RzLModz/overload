#!/bin/bash

# =========================================================
# Skrip Instalasi Dependencies - Node 14 & Go 1.24
# Target: h1-flood, h2-ghost, h2-payload (Single Directory)
# =========================================================

INSTALL_ERRORS=""
HAS_ERROR=0

# Warna untuk Log
log_info() { echo -e "\n[\033[34mINFO\033[0m] $1"; }
log_success() { echo -e "[\033[32mSUCCESS\033[0m] $1"; }
log_error() {
    local error_message="[ERROR] $1 (Fungsi: $2)"
    echo -e "[\033[31mERROR\033[0m] $1" >&2
    INSTALL_ERRORS+="$error_message\n"
    HAS_ERROR=1
}

# -----------------------------------------------
# FUNGSI 1: OPTIMASI KONEKSI (ANTI-DISCONNECT)
# -----------------------------------------------
optimize_connection() {
    log_info "Mengoptimalkan SSH agar VPS tetap Standby (Anti-Idle)..."
    mkdir -p ~/.ssh
    if ! grep -q "ServerAliveInterval" ~/.ssh/config 2>/dev/null; then
        echo -e "Host *\n  ServerAliveInterval 60\n  ServerAliveCountMax 120" >> ~/.ssh/config
        chmod 600 ~/.ssh/config
    fi
    sudo sed -i 's/#ClientAliveInterval 0/ClientAliveInterval 60/g' /etc/ssh/sshd_config
    sudo sed -i 's/#ClientAliveCountMax 3/ClientAliveCountMax 120/g' /etc/ssh/sshd_config
    sudo systemctl restart ssh 2>/dev/null || sudo service ssh restart 2>/dev/null
    sudo apt update -y && sudo apt install -y screen tmux
    log_success "Optimasi koneksi selesai."
}

# -----------------------------------------------
# FUNGSI 2: INSTALASI SYSTEM & GOOGLE CHROME
# -----------------------------------------------
install_system_deps() {
    log_info "Menginstal Dependencies Sistem & Google Chrome..."
    sudo apt install -y ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils cpulimit curl
    
    if ! command -v google-chrome-stable &> /dev/null; then
        wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O chrome.deb
        sudo apt install ./chrome.deb -y && rm chrome.deb
    else
        log_success "Google Chrome sudah terinstal."
    fi
}

# -----------------------------------------------
# FUNGSI 3: FORCE NODE.JS 14.21.3 (NVM)
# -----------------------------------------------
install_nodejs_with_nvm() {
    log_info "Mengonfigurasi Node.js 14.21.3 melalui NVM..."
    export NVM_DIR="$HOME/.nvm"
    if [ ! -d "$NVM_DIR" ]; then
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    fi
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm install 14.21.3
    nvm alias default 14.21.3
    nvm use 14.21.3
    log_success "Node.js Aktif: $(node -v)"
}

# -----------------------------------------------
# FUNGSI 4: NPM, PIP & BROWSER ASSETS
# -----------------------------------------------
install_packages() {
    NPM_PACKAGES=(
        "https-proxy-agent" "crypto-random-string" "events" "fs" "net"
        "cloudscraper" "request" "hcaptcha-solver" "randomstring" "cluster" 
        "cloudflare-bypasser" "socks" "hpack" "axios" "user-agents" "cheerio"
        "gradient-string" "fake-useragent" "header-generator" "math" "p-limit@2.3.0"
        "puppeteer@19" "puppeteer-extra" "puppeteer-extra-plugin-stealth" "async"
        "node-fetch@2" "http2-wrapper"
    )
    PIP_PACKAGES=("colorama" "rich" "tabulate" "termcolor" "bs4" "tqdm" "httpx" "camoufox" "httpx[http2]" "browserforge")

    log_info "Menginstal Paket NPM..."
    for package in "${NPM_PACKAGES[@]}"; do
        npm install "$package" --no-audit --no-fund --quiet || log_error "Gagal NPM: $package" "NPM_INSTALL"
    done

    log_info "Menginstal Paket Python..."
    for package in "${PIP_PACKAGES[@]}"; do
        pip3 install "$package" --quiet || log_error "Gagal PIP: $package" "PIP_INSTALL"
    done

    python3 -m browserforge update
    python3 -m camoufox fetch
}

# -----------------------------------------------
# FUNGSI 5: GOLANG 1.24.0 & MULTI-FILE MODULE
# -----------------------------------------------
install_golang() {
    log_info "Menginstal Golang 1.24.0..."
    sudo rm -rf /usr/local/go
    wget https://go.dev/dl/go1.24.0.linux-amd64.tar.gz -O go1.24.0.tar.gz
    if [ $? -eq 0 ]; then
        sudo tar -C /usr/local -xzf go1.24.0.tar.gz
        rm go1.24.0.tar.gz
        sudo ln -sf /usr/local/go/bin/go /usr/bin/go
        sudo ln -sf /usr/local/go/bin/gofmt /usr/bin/gofmt
        
        # Inisialisasi satu modul untuk semua file .go di folder ini
        if [ ! -f "go.mod" ]; then
            log_info "Inisialisasi modul Go untuk h1-flood, h2-ghost, & h2-payload..."
            go mod init attack-tools || log_error "Gagal go mod init" "GO_INIT"
        fi
        
        log_info "Menjalankan go mod tidy..."
        go mod tidy || log_error "Gagal go mod tidy" "GO_TIDY"
        log_success "Go Siap: $(go version)"
    else
        log_error "Gagal mengunduh Golang" "INSTALL_GO"
    fi
}

# -----------------------------------------------
# EKSEKUSI UTAMA
# -----------------------------------------------
clear
log_info "MEMULAI PROSES INSTALASI LENGKAP..."

optimize_connection
install_system_deps
install_nodejs_with_nvm
install_packages
install_golang

log_info "Konfigurasi Akhir Sistem..."
ulimit -n 999999
chmod +x * 2>/dev/null

echo -e "\n"
if [ $HAS_ERROR -eq 0 ]; then
    log_success "================================================="
    log_success "  INSTALASI SELESAI DENGAN SUKSES!"
    log_success "  Node.js: $(node -v)"
    log_success "  Golang:  $(go version)"
    log_success "================================================="
    exit 0
else
    log_error "Selesai dengan error. Cek log di atas." "MAIN"
    exit 1
fi