#!/bin/bash

# ===============================================
# Skrip Instalasi Dependencies - FORCED NODE 14.x
# Versi Lengkap: Node 14.21.3 + Browser Assets + Go 1.24.0
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
    "node-fetch@2" "http2-wrapper"
)

PIP_PACKAGES=(
    "colorama" "rich" "tabulate" "termcolor" "bs4" "tqdm" "httpx" "camoufox"
    "httpx[http2]" "browserforge"
)

# -----------------------------------------------
# FUNGSI 1: INSTALASI SYSTEM & GOOGLE CHROME
# -----------------------------------------------
install_system_deps() {
    log_info "Menginstal Dependencies Sistem & Google Chrome..."
    sudo apt update -y
    sudo apt install -y ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils cpulimit curl
    
    if ! command -v google-chrome-stable &> /dev/null; then
        wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O chrome.deb
        sudo apt install ./chrome.deb -y && rm chrome.deb
    else
        log_success "Google Chrome sudah terinstal."
    fi
}

# -----------------------------------------------
# FUNGSI 2: FORCE NODE.JS 14.21.3 (NVM)
# -----------------------------------------------
install_nodejs_with_nvm() {
    log_info "Mengonfigurasi Node.js 14.21.3 melalui NVM..."

    export NVM_DIR="$HOME/.nvm"
    
    if [ ! -d "$NVM_DIR" ]; then
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    fi
    
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

    if ! command -v nvm &> /dev/null; then
        log_error "NVM gagal dimuat." "${FUNCNAME[0]}"
        return 1
    fi

    nvm install 14.21.3
    nvm unalias default 2>/dev/null
    nvm alias default 14.21.3
    nvm use 14.21.3

    NODE_VER=$(node -v)
    if [[ $NODE_VER != v14* ]]; then
        log_error "Node masih $NODE_VER. Memaksa PATH manual..." "NodeFix"
        export PATH="$NVM_DIR/versions/node/v14.21.3/bin:$PATH"
    fi
    
    log_success "Node.js yang digunakan: $(node -v)"
}

# -----------------------------------------------
# FUNGSI 3: NPM, PIP & BROWSER ASSETS
# -----------------------------------------------
install_packages() {
    log_info "Menginstal Paket NPM (Target: Node 14)..."
    for package in "${NPM_PACKAGES[@]}"; do
        log_info "Menginstal modul: $package"
        npm install "$package" --no-audit --no-fund --quiet
        [ $? -ne 0 ] && log_error "Gagal NPM: $package" "NPM_INSTALL"
    done

    log_info "Menginstal Paket Python (PIP)..."
    for package in "${PIP_PACKAGES[@]}"; do
        pip3 install "$package" --quiet
        [ $? -ne 0 ] && log_error "Gagal PIP: $package" "PIP_INSTALL"
    done

    log_info "Mengunduh Data Browser (Browserforge & Camoufox)..."
    python3 -m browserforge update
    [ $? -ne 0 ] && log_error "Gagal mengupdate browserforge" "PYTHON_ASSETS"

    python3 -m camoufox fetch
    [ $? -ne 0 ] && log_error "Gagal memproses camoufox fetch" "PYTHON_ASSETS"
}

# -----------------------------------------------
# FUNGSI 4: GOLANG 1.24.0
# -----------------------------------------------
install_golang() {
    log_info "Menginstal Golang 1.24.0..."
    
    # Menghapus versi lama dan mengunduh versi baru
    sudo rm -rf /usr/local/go && \
    wget https://go.dev/dl/go1.24.0.linux-amd64.tar.gz -O go_dist.tar.gz
    
    if [ $? -eq 0 ]; then
        sudo tar -C /usr/local -xzf go_dist.tar.gz && rm go_dist.tar.gz
        sudo ln -sf /usr/local/go/bin/go /usr/bin/go
        sudo ln -sf /usr/local/go/bin/gofmt /usr/bin/gofmt
        
        # Menjalankan go mod tidy jika file go.mod ditemukan
        if [ -f "go.mod" ]; then
            log_info "Menjalankan go mod tidy..."
            go mod tidy
        fi
        
        log_success "Go berhasil diinstal: $(go version)"
    else
        log_error "Gagal mengunduh atau menginstal Golang" "INSTALL_GOLANG"
    fi
}

# -----------------------------------------------
# EKSEKUSI UTAMA
# -----------------------------------------------
clear
log_info "MEMULAI PROSES INSTALASI..."

install_system_deps
install_nodejs_with_nvm
install_packages
install_golang

log_info "Konfigurasi Akhir..."
ulimit -n 999999
chmod 777 * 2>/dev/null

# -----------------------------------------------
# LAPORAN AKHIR
# -----------------------------------------------
echo -e "\n"
if [ $HAS_ERROR -eq 0 ]; then
    log_success "================================================="
    log_success "  INSTALASI BERHASIL!"
    log_success "  Node.js: $(node -v)"
    log_success "  Go:      $(go version)"
    log_success "  Browser data telah siap digunakan."
    log_success "================================================="
    
    [ -s "$HOME/.nvm/nvm.sh" ] && \. "$HOME/.nvm/nvm.sh"
    nvm use 14.21.3
    
    echo -e "[\033[33mTIP\033[0m] Gunakan perintah: \033[1msource ./install.sh\033[0m agar perubahan langsung aktif."
    exit 0
else
    log_error "Selesai dengan error. Cek laporan di bawah." "MAIN"
    echo -e "$INSTALL_ERRORS"
    exit 1
fi